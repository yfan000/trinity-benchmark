#!/usr/bin/env python3
"""Generate the Trinity agent benchmark: 4 pre-submission subtasks x 15 catalog anchors.

    Software selection -> Input preparation -> Resource selection -> PBS job creation

Every sample is anchored to a real (system, application) pair from the cached
application_catalog, so the workload can cite true hardware and queue limits and the grading
key is drawn from the catalog's own YAML rather than invented.

Two mechanisms keep the samples honest:

  Leak enforcement — the prompt is scanned for terms that would give away this subtask's
  answer, and a leaking sample is regenerated with those terms quoted back as forbidden.
  Without it the rule does not hold: an early trial wrote "a LAMMPS-format data file" into a
  Software-selection prompt, which is realistic and completely useless as a test.

  Pipeline carry-forward — later subtasks are told what earlier ones decided. Naming the
  application in a Resource-selection prompt is correct, because selecting it was the
  previous subtask's job; withholding it there would test the wrong capability.

Usage:
    python skills/trinity_generate.py
    python skills/trinity_generate.py --show 4
    python skills/trinity_generate.py --subtask "Resource selection"
"""
from __future__ import annotations
import argparse
import json
import random
import re
import sys
import textwrap
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import judge  # noqa: E402
from skills.trinity_task_spec import (ANCHORS, LEAK_PATTERNS,  # noqa: E402
                                      PHYSICAL_SYSTEMS, SUBSET, SUBTASKS,
                                      VARIATIONS)
from skills import trinity_site  # noqa: E402
from skills import catalog  # noqa: E402

TRIN = ROOT / "results" / "skills" / "trinity"
CATALOG = TRIN / "catalog"
OUT = TRIN / "samples.jsonl"
SECTIONS = ("Task", "Workload", "Instructions", "Output")


def has_section(prompt: str, name: str) -> bool:
    """Accept "Name:", "**Name:**" and "## Name" heading styles."""
    import re as _re
    return bool(_re.search(rf"(?:^|\n)\s*(?:#+\s*|\*\*)?{name}\b\s*:?\s*(?:\*\*)?\s*(?:\n|$|[A-Z])",
                           prompt, _re.I))
MAX_RETRIES = 3


def app_yaml(system: str, app: str) -> dict:
    """Parse one catalog entry. Delegates to skills.catalog, which is the only reader now.

    This used to `yaml.safe_load` and return `{}` on any YAMLError. That silence is how
    software/polaris/qe.yaml — one of the richest entries in the catalog — contributed nothing
    to any prompt or check for months, and why the Software-selection list rendered it as
    "qe — " with an empty description. skills.catalog repairs the two one-character syntax
    errors from an overlay, reads multi-document files (frontier/gromacs.yaml carries a whole
    second GPU build), and warns rather than going quiet.

    Kept as a shim so the thirteen call sites do not have to move at once.
    """
    return catalog.merged(system, app)


# Per-system scratch roots, taken from the catalog's storage mounts. Working directories are
# randomized under these rather than reusing the catalog owner's real path — every sample
# previously sat under /lus/flare/projects/datascience/hzheng/, which is both unrealistic and
# a hint, since that is the account the software was built under.
_SCRATCH = {
    "polaris":    "/eagle/{proj}/{user}",
    "crux":       "/eagle/{proj}/{user}",
    "sophia":     "/eagle/{proj}/{user}",
    "aurora":     "/lus/flare/projects/{proj}/{user}",
    "sirius":     "/lus/tegu/projects/{proj}/{user}",
    "frontier":   "/lustre/orion/{proj}/scratch/{user}",
    "perlmutter": "/pscratch/sd/{initial}/{user}",
}
_USERS = ["jmartinez", "kwong", "aschmidt", "rpatel", "lchen", "dokafor", "mrossi",
          "tnakamura", "gpetrov", "shaddad", "efaraday", "bkowalski", "yamamoto", "nsvensson"]
_PROJECTS = ["CombustionSim", "MatGenome", "AstroLENS", "BioFoldX", "PlasmaEdge", "TurbFlowDNS",
             "QuantumMatX", "ClimateRegional", "NuclearMPX", "CatalysisDFT", "ProteinDesign",
             "FusionPIC", "CosmoSurvey", "AlloyDesign"]


# Neutral directory names for Software selection, where ".../nekrs_run" would name the
# answer outright — the judge caught models being marked down for "ignoring the strong hint
# in the working directory path".
_NEUTRAL_DIRS = ["run01", "prod_run", "campaign_a", "sim_run", "case01", "job_dir",
                 "run_current", "study_1", "baseline_run", "expt_02"]


def workdir(system: str, app: str, subtask: str, neutral: bool = False) -> str:
    """A plausible but arbitrary working directory, stable per (system, app, subtask)."""
    import hashlib
    h = int(hashlib.md5(f"{system}{app}{subtask}".encode()).hexdigest(), 16)
    user = _USERS[h % len(_USERS)]
    proj = _PROJECTS[(h // 7) % len(_PROJECTS)]
    root = _SCRATCH.get(system, "/scratch/{proj}/{user}")
    leaf = _NEUTRAL_DIRS[h % len(_NEUTRAL_DIRS)] if neutral else f"{app}_run"
    return root.format(proj=proj, user=user, initial=user[0]) + f"/{leaf}"


def scheduler(system: str) -> str:
    """PBS Pro or Slurm, from the catalog. ALCF entries omit `type`; Slurm sites set it."""
    return catalog.scheduler_kind(system)


def installed(system: str) -> str:
    """The software catalog an agent would consult on that system."""
    names = []
    for f in sorted((CATALOG / "software" / system).glob("*.yaml")):
        if f.stem.startswith("_"):
            continue
        d = app_yaml(system, f.stem)
        names.append(f"{d.get('name', f.stem)} — {(d.get('description') or '')[:72]}")
    return "\n".join(names)


def perf(system: str, app: str) -> dict:
    """A filled-in benchmark record, if one exists. 8 of 114 are populated; the rest are
    stubs. Where present it is the strongest ground truth available for sizing a run."""
    d = catalog.performance(system, app)
    b = d.get("benchmark") or {}
    return b if (b.get("name") or b.get("throughput") or b.get("walltime_s")) else {}


def grading_key(system: str, app: str, fields: list[str]) -> dict:
    """Objective facts from the catalog that a correct answer must match."""
    d = app_yaml(system, app)
    # some entries use "app" instead of "name" (e.g. frontier/hacc.yaml)
    key = {"app": d.get("name") or d.get("app") or app, "system": system,
           "scheduler": scheduler(system)}
    for f in fields:
        if f in d:
            key[f] = d[f]
    p = perf(system, app)
    if p:
        key["measured_benchmark"] = p
    return key


def _legal_queue(system: str, want: str | None, nodes: int, walltime_s: int | None) -> str:
    """A queue that actually exists on this machine and admits the request.

    THE CARRY-FORWARD MUST NOT HAND OVER AN ILLEGAL DECISION. `defaults.queue` is a software
    field and is not validated against the machine's queue table: 26 catalog entries name a
    queue their own system does not have, including EVERY Crux entry, which says `workq` while
    Crux runs debug / demand / preemptable / workq-route.

    Measured cost before this guard: all four models, in both A/B arms, were told
    "queue workq" for hpl@crux, wrote `#PBS -q workq` exactly as instructed, and were failed
    FATALLY by BATCH.common.queue_exists — eight failures, none of them the model's doing.

    Falls back to the system's own job_defaults queue, then to any queue whose node and
    walltime limits admit the request, then to the first queue on the machine.
    """
    qs = catalog.queues(system)
    if not qs:
        return want or "debug"
    def admits(name: str) -> bool:
        q = qs[name]
        if q.min_nodes is not None and nodes < q.min_nodes:
            return False
        if q.max_nodes is not None and nodes > q.max_nodes:
            return False
        if walltime_s and q.max_walltime and walltime_s > q.max_walltime:
            return False
        return True
    # Existence is not enough: Polaris `prod` exists but rejects anything under 10 nodes, so a
    # carry-forward of "1 node, queue prod" is as unusable as a queue that does not exist.
    if want in qs and admits(want):
        return want
    jd = catalog.job_defaults(system).queue
    if jd in qs and admits(jd):
        return jd
    for name in qs:
        if admits(name):
            return name
    return next(iter(qs))


def prior_block(subtask: str, system: str, app: str, name: str) -> str:
    """What the earlier pipeline stages correctly produced, taken from the catalog.

    The four subtasks are answered independently, not chained, so a later one has to be told
    the earlier decisions rather than left to re-derive them — and the values come from the
    catalog, not from another model's output, so one stage's mistake cannot contaminate the
    measurement of the next. Supplying this took Input preparation 6% -> 25% and Batch job
    creation 11% -> 17% fully correct on the preview set before any other change.
    """
    order = SUBTASKS[subtask]["order"]
    if order < 2:
        return ""
    d = app_yaml(system, app)
    lines = [f"Software selection chose: {name}"]
    if order >= 3:
        req = d.get("required_inputs") or d.get("input_files") or []
        stem = {"nwchem": "run", "qe": "scf", "cp2k": "run", "lammps": "in",
                "nekrs": "case", "qmcpack": "qmc"}.get(app, "run")
        # The catalog does not distinguish "all of these" from "any one of these", and
        # treating every entry as a separate required file produced nonsense: LAMMPS lists
        # .lammps/.in/.lmp — three names for ONE input script — and the prompt claimed all
        # three had been produced. nekRS's .par/.re2/.udf really are three distinct files.
        # The tell is whether an application accepts several extensions for one artifact.
        ALTERNATIVES = {"lammps": True, "qe": True, "cp2k": True, "namd": True,
                        "alphafold": True, "nekrs": False, "qmcpack": False,
                        "gromacs": False, "nwchem": False}
        # A catalog entry may be an EXTENSION (".par") or already a full FILENAME
        # ("HPL.dat"). Prepending the stem to both turned HPL.dat into "runHPL.dat" — a name
        # xhpl can never read, since it requires exactly HPL.dat in the working directory.
        # The prompt then described an input the application cannot open.
        def name(e: str) -> str:
            return f"{stem}{e}" if str(e).startswith(".") else str(e)

        if req and ALTERNATIVES.get(app, False):
            files = f"{name(req[0])} (any of {', '.join(req)} is equivalent)"
        else:
            files = ", ".join(name(e) for e in req) if req else "(none required)"
        lines.append(f"Input preparation produced: {files} in the working directory")
    if order >= 4:
        df = catalog.defaults(system, app)
        wt = df.walltime_s
        hh = f"{wt // 3600:02d}:{(wt % 3600) // 60:02d}:00" if isinstance(wt, int) else "01:00:00"
        nodes = df.nodes or 1
        q = _legal_queue(system, df.queue, nodes, wt)
        lines.append(f"Resource selection determined: {nodes} node(s), "
                     f"{df.ppn or 4} ranks per node, walltime {hh}, queue {q}")
    return ("\nDecisions already made by earlier pipeline stages — state these in the Workload "
            "as given facts, since this subtask is answered independently and must not have "
            "to re-derive them:\n  " + "\n  ".join(lines) + "\n")


def machine_spec(system: str) -> str:
    """Hardware and queue limits for the target machine, from the catalog.

    Supplied to the agent rather than withheld: in deployment the orchestrator knows which
    machine it is targeting and can inject these from this same catalog, so requiring the
    model to recall Aurora's node count tests trivia, not capability. What stays withheld is
    the answer — how much of the machine to request.
    """
    d = catalog.system_doc(system)
    if not d:
        return ""
    # `.raw`, not the normalized dataclass: this format string relies on `.get(k, default)`
    # firing only when the key is ABSENT. Crux records `gpus_per_node: 0` and `gpu_type: ""`,
    # so a truthiness-based default would print "? x GPU per node" for a CPU-only machine.
    # Memory per node is deliberately NOT added here — that is a prompt change and belongs in
    # the arm work, where both arms receive it together.
    hw = catalog.hardware(system).raw
    parts = [f"{d.get('name', system)} ({d.get('facility','')}): "
             f"{hw.get('nodes','?')} nodes, {hw.get('gpus_per_node','?')} x "
             f"{hw.get('gpu_type','GPU')} per node, {hw.get('cpus_per_node','?')} CPU cores per node"]
    for q, v in catalog.queues(system).items():
        bits = []
        if v.min_nodes is not None and v.max_nodes is not None:
            bits.append(f"{v.min_nodes}-{v.max_nodes} nodes")
        if v.max_walltime:
            bits.append(f"max {v.max_walltime // 3600}h" if v.max_walltime >= 3600
                        else f"max {v.max_walltime // 60}min")
        if bits:
            parts.append(f"  queue {q}: " + ", ".join(bits))
    return "\n".join(parts)


def build_defaults(system: str, app: str) -> str:
    """The build's own rank/GPU layout, which Resource selection is told to follow.

    `defaults` is a one-node functional smoke test, so the NODE COUNT and WALLTIME in it are
    deliberately NOT surfaced — those are the agent's to choose and supplying them would hand
    over the answer. Only the layout ratios are given, which is what the rule actually asks
    for. 57 of 144 catalog entries record no ppn at all; those produce an empty block and the
    requirement correctly stands down.
    """
    d = app_yaml(system, app)
    df = d.get("defaults") or {}
    out = []
    if df.get("ppn"):
        out.append(f"ranks per node (build default): {df['ppn']}")
    if d.get("gpu_notes"):
        out.append(f"GPU notes: {' '.join(str(d['gpu_notes']).split())[:220]}")
    if d.get("scaling_notes"):
        out.append(f"scaling notes: {' '.join(str(d['scaling_notes']).split())[:220]}")
    return "\n".join(out)


def _file_plan(system: str, app: str):
    """(write, compiled, optional, sources, contract) — the one place that decides which files
    a human authors and which the toolchain builds.

    Shared by the inventory block (both arms) and the format block (rich arm) so the two can
    never disagree, which they did: the rich prompt carried "Required input files" AND "Input
    format contract", each listing the same files in different words.
    """
    i = catalog.inputs(system, app)
    c = _contracts()["contracts"].get(app) or {}
    binaries = {b.lower() for b in _binary_files(system, app)}
    write = [f for f in i.required if str(f).lower() not in binaries]
    compiled = [f for f in i.required if str(f).lower() in binaries]
    optional = list(i.optional)
    srcs = list(c.get("sources") or [])
    # When every required input is compiled, the sources ARE the deliverable — GROMACS's only
    # required_input is .tpr, so without this nothing told the model what to write.
    if srcs and not write:
        write = [catalog.filespec(x) for x in srcs]
        optional = [f for f in optional if str(f) not in set(srcs)]
    return write, compiled, optional, srcs, c, i


def _input_spec(system: str, app: str) -> str:
    """WHICH FILES to produce, and which not to. Supplied to both arms.

    `required_inputs` records what the application CONSUMES, which is not what a human WRITES:
    GROMACS consumes a .tpr that grompp compiles, nekRS a binary .re2 mesh, QMCPACK an HDF5
    .h5. Listing those as "required" told the model to author files the rubric fails fatally.
    """
    write, compiled, optional, srcs, c, i = _file_plan(system, app)
    out = []
    if write:
        if c.get("alternatives") and len(write) > 1:
            # `required_inputs` does not distinguish "all of" from "any of". QE lists four
            # names for ONE deck; LAMMPS and AlphaFold do the same.
            # The naming note goes on its OWN line. Trailing it after the file list made a
            # run-on line, and any consumer parsing "WRITE ...: <files>" then read the prose as
            # filenames — which is exactly what the example-coverage gate did.
            out.append("WRITE ONE file, in a fenced code block. The catalog records these "
                       "forms: " + " / ".join(str(f) for f in write))
            if c.get("naming"):
                out.append("  " + " ".join(str(c["naming"]).split()))
        elif c.get("fixed_filenames") and i.filenames:
            out.append("WRITE this file, in a fenced code block, under exactly this name "
                       "(the application opens no other): " + ", ".join(i.filenames))
        else:
            out.append(("WRITE this file, in a fenced code block, filename is yours to choose: "
                        if len(write) == 1 else
                        f"WRITE these {len(write)} files, one fenced code block each, "
                        f"filenames are yours to choose: ")
                       + ", ".join(str(f) for f in write))
    dont = []
    if compiled:
        src = " from the files above" if (srcs and write) else ""
        dont += [f"{f} — built by the toolchain, not written by hand; give the command that "
                 f"builds it{src}" for f in compiled]
    if i.authorable_outputs:
        dont.append(", ".join(str(f) for f in i.authorable_outputs)
                    + " — the run produces these")
    if dont:
        out.append("DO NOT write contents for:")
        out += ["  " + d for d in dont]
    if optional:
        out.append("Optional, only if this workload needs them: "
                   + ", ".join(str(f) for f in optional))
    return "\n".join(out)


def _app_setup(system: str, app: str) -> str:
    """The site's module lines and launcher for this application.

    The module lines are site fact and are handed over verbatim: the agent has no shell and
    cannot discover them, so withholding them would test recall rather than the ability to
    assemble a working script.

    `run_command` is NOT site fact in the same way, and presenting it as though it were set a
    trap. The catalog's launch lines carry placeholder filenames and the build's own smoke-test
    rank counts, which contradict the workload on five of the ten evaluation anchors:

        lammps   workload says in.lammps   launch says `lmp -in input.lammps`
        nwchem   workload says run.nw      launch says `nwchem input.nw`
        qmcpack  workload says qmc.xml     launch says `qmcpack input.xml`
        gromacs  workload says run.tpr     launch says `mdrun -deffnm md`  (reads md.tpr)
        qe       workload says scf.scf.in  launch says `pw.x -in input.scf.in`

    A model that copies the line — the reasonable reading of a block labelled "Software
    Environment" — passes the wrong filename and fails BATCH.common.inputs_passed. The worked
    example carries a "do not copy its launch command" warning; this block carried none. Saying
    plainly that the line is a FORM keeps the substitution as the test instead of a trap.
    """
    d = app_yaml(system, app)
    out = []
    if d.get("setup"):
        out += list(d["setup"])
    if d.get("modules"):
        out.append("modules: " + ", ".join(d["modules"]))
    if d.get("run_command"):
        out.append("launch command FORM (the filenames and rank counts in it are the catalog's "
                   "own placeholders from a smoke test — substitute the input file named in the "
                   "Workload and the resources decided above):")
        out.append("  " + " ".join(str(d["run_command"]).split()))
    if d.get("binary"):
        out.append("binary: " + str(d["binary"]))
    return "\n".join(out)


def physical_system(app: str) -> str:
    """The concrete system a sample must describe, so its output can be checked."""
    return PHYSICAL_SYSTEMS.get(app, "")


# ---------------------------------------------------------------- enriched blocks (RICH arm)

_CONTRACTS_PATH = Path(__file__).resolve().parent / "format_contracts.yaml"


@lru_cache(maxsize=1)
def _contracts() -> dict:
    d = yaml.safe_load(_CONTRACTS_PATH.read_text()) or {}
    return {"contracts": d.get("contracts") or {}, "no_contract": set(d.get("no_contract") or [])}


_MEM_CLAIM = re.compile(r"(\d+)\s*(?:GB|GiB)\s*/?\s*(?:per\s+)?node", re.I)
_GPU_CLAIM = re.compile(r"(\d+)\s*GPUs?\s*(?:per\s+node|/\s*node)", re.I)


def _binary_files(system: str, app: str) -> list[str]:
    """Compiled/binary inputs: the rubric's list UNION the format contract's.

    Only three applications have a rubric file carrying `binary_files`, so relying on it alone
    left nekRS's `.re2` mesh and QMCPACK's `.h5` wavefunction rendering as "files to produce" —
    the same defect as GROMACS's `.tpr`, with nothing to catch it.
    """
    out = list((_contracts()["contracts"].get(app) or {}).get("binary") or [])
    try:
        from skills.judging.loader import load as _load
        out += _load("Input preparation", app, system).binary_files or []
    except Exception:
        pass
    return out


def _drop_memory_contradictions(text: str, system: str) -> tuple[str, list[str]]:
    """Remove sentences whose per-node memory figure contradicts systems/<system>.yaml.

    The catalog disagrees with itself in one measured place: `systems/crux.yaml` records
    `memory_per_node_gb: 256` while `software/crux/hpl.yaml` scaling_notes says "Tune N, NB, P,
    Q parameters in HPL.dat for Crux node memory (512 GB/node)". Shipping both to a model that
    must size N from memory is worse than shipping neither, and HPL is precisely the anchor
    where the figure decides the answer.

    The system file wins: it is the system-level authority, and the app note is prose. Little
    is lost — the surviving contract already tells the model HPL.dat must carry Ns/NBs/Ps/Qs.
    Every drop is returned so it can be reported rather than happening silently.
    """
    hw = catalog.hardware(system).memory_per_node_gb
    if not (hw or catalog.hardware(system).gpus_per_node):
        return text, []
    hw = hw or -1e9
    gp = catalog.hardware(system).gpus_per_node
    kept, dropped = [], []
    for s in re.split(r"(?<=[.!?])\s+", text or ""):
        claims = [float(m.group(1)) for m in _MEM_CLAIM.finditer(s)]
        gclaims = [int(m.group(1)) for m in _GPU_CLAIM.finditer(s)]
        if (gp and any(g != gp for g in gclaims)) or any(abs(c - hw) > 1 for c in claims):
            dropped.append(s.strip())
        elif s.strip():
            kept.append(s.strip())
    return " ".join(kept), dropped


def _redact(text: str, terms: list[str]) -> str:
    """Drop whole sentences that would leak, keep the rest.

    Required, not defensive: copying `scaling_notes` verbatim leaks on 3 of 39 anchors —
    qmcpack@perlmutter says "use all 256 cores", gromacs@polaris "1 rank per GPU", and
    lammps@sirius names `--ppn`. Those are Resource-selection answers sitting inside a field
    Input preparation wants for its sizing guidance.
    """
    keep = [s for s in re.split(r"(?<=[.!?])\s+|\n", text or "")
            if s.strip() and not leaks(s, terms, True)]
    return " ".join(x.strip() for x in keep).strip()


def format_contract(system: str, app: str) -> str:
    """WHAT MUST BE INSIDE each file. The RICH arm's addition, and only that.

    It deliberately does not repeat the file inventory — that lives in `_input_spec` and both
    arms get it. Carrying both produced a prompt with "Required input files" and "Input format
    contract" listing the same files in different words, which is the duplication this split
    removes. What is genuinely new here is the per-format content requirement.

    It equally does not use `input_detection.content_markers`: that field is a file-TYPE
    heuristic (any-of), and as a contract it would instruct the model to write the literal
    amino-acid alphabet into a FASTA. The lists come from skills/format_contracts.yaml, which
    records only what the application refuses to run without.
    """
    _, _, _, _, c, _ = _file_plan(system, app)
    if not (c.get("mandatory") or c.get("expected")):
        return ("(the facility catalog records no format requirements for this application — "
                "determine the file contents yourself)")
    out = []
    if c.get("mandatory"):
        out.append(f"Every {c.get('file', 'input file')} you write must contain: "
                   + ", ".join(c["mandatory"]))
    if c.get("expected"):
        out.append("Usually present, not required: " + ", ".join(c["expected"]))
    return "\n".join(out)


def system_context(system: str) -> str:
    """Hardware and scratch mounts, for sizing a deck.

    NEVER renders `job_defaults`. That map carries nodes, walltime and queue — the three
    values `build_defaults()` deliberately withholds (see its docstring). Excluding it here is
    belt-and-braces: this block is Input-prep-gated, but a future flag flip must not be able to
    hand Resource selection its own answer.
    """
    hw = catalog.hardware(system)
    bits = []
    if hw.cpus_per_node:
        bits.append(f"{hw.cpus_per_node} CPU cores per node")
    if hw.gpus_per_node:
        bits.append(f"{hw.gpus_per_node} x {hw.gpu_type or 'GPU'} per node")
    # Memory is what makes HPL answerable at all: its own scaling note is
    # "N ~ sqrt(total_memory * 0.8 / 8)", and the memory figure was unread on all 9 systems.
    if hw.memory_per_node_gb:
        bits.append(f"{hw.memory_per_node_gb:g} GB memory per node")
    out = []
    if bits:
        out.append("per node: " + ", ".join(bits))
    mounts = [m.mount_path for m in catalog.storage(system)]
    if mounts:
        out.append("filesystems available: " + ", ".join(mounts))
    return "\n".join(out)


def input_scaling(system: str, app: str, terms: list[str]) -> str:
    """The application's own sizing guidance, filtered down to what bears on an INPUT FILE.

    `scaling_notes` is mostly about how to LAUNCH the job — `-ntmpi 8`, `-gpu_id 01234567`,
    `-pme cpu -npme 1`, `--ppn`. That is Resource-selection and Batch material, and in an
    Input-preparation prompt it is at best noise and at worst wrong: GROMACS on Sirius says
    "-gpu_id 01234567 maps ranks 0-7" on a node the catalog records as having four GPUs.

    What IS worth carrying is the minority of sentences that talk about the file being written:
    HPL's "Tune N, NB, P, Q parameters in HPL.dat", NWChem's "Set memory stack/heap/global in
    input file". Keep a sentence only when it names an input artifact or an input keyword.
    """
    raw = " ".join(str(catalog.merged(system, app).get("scaling_notes") or "").split())
    raw, _ = _drop_memory_contradictions(raw, system)
    raw = _redact(raw, terms)

    i = catalog.inputs(system, app)
    cues = {"input file", "input deck", "input"} | {str(f).lstrip(".").lower()
                                                    for f in (*i.required, *i.optional)}
    cues |= {n.lower() for n in i.filenames}
    cues |= {m.lower() for m in ((_contracts()["contracts"].get(app) or {}).get("mandatory") or [])}
    cues = {c for c in cues if len(c) > 2}
    keep = [s for s in re.split(r"(?<=[.!?])\s+", raw)
            if s.strip() and any(c in s.lower() for c in cues)]
    return " ".join(s.strip() for s in keep).strip()


# A MECHANICAL TRAP LIVES HERE. `strip_catalog` skips from a SUPPLIED_HEADINGS match until it
# hits a line whose head is in _SECTION_HEADS. Input preparation already supplies "required
# input files" and "worked example", so any NEW heading placed after one of those would be
# swallowed by the ongoing skip and silently exempted from leak checking. "input format
# contract" therefore goes in _SECTION_HEADS (it TERMINATES a skip, and is itself checked) and
# deliberately NOT in SUPPLIED_HEADINGS. That is the conservative direction, and it is
# affordable because the contract measures clean against Input prep's leak terms on every
# anchor — see `--leak-audit`.
_SECTION_HEADS = ("instructions", "output", "task", "workload", "target system",
                  "physical system", "your task", "deliverable",
                  "input file format", "system context")
SUPPLIED_HEADINGS = ("installed software", "available software", "software catalog",
                     "installed applications", "available applications",
                     "required input files", "input files required", "file inventory",
                     "software environment", "environment setup", "module environment",
                     "supplied environment",
                     # Batch job creation hands over the site rules and one complete script
                     # for a different application. Both necessarily contain #PBS/#SBATCH
                     # lines and a real account, which is the whole point of supplying them.
                     "scheduler conventions", "site conventions", "worked example",
                     "example script", "reference script", "example input", "example deck")


def strip_catalog(prompt: str) -> str:
    """Drop any SUPPLIED context section before leak-checking.

    Sections the prompt deliberately hands the agent — the software catalog, the input-file
    inventory, the module lines — necessarily contain terms that would otherwise read as
    leaks. Naming those things anywhere ELSE in the prompt is still a leak, so only the
    supplied blocks are exempt.

    Software selection now lists every installed application, so the correct answer's name
    is necessarily present — that is the point, since the task is to pick it from ~19
    options rather than recall it. Naming it anywhere ELSE in the prompt is still a leak,
    so only the catalog block is exempt.
    """
    out, skipping, fenced = [], False, False
    for ln in prompt.split("\n"):
        if ln.lstrip().startswith("```"):
            fenced = not fenced
            if skipping:
                continue
        # Headings arrive as "## Installed Software", "**Installed software:**" or bare
        # text, so normalise markdown emphasis before matching. A supplied block's own
        # heading often carries a parenthetical caveat ("**Worked example** (for a
        # DIFFERENT application...)"), so match on the leading words, not the whole line.
        head = ln.strip().lstrip("#").strip().strip("*").strip().lower().rstrip(":")
        if any(head.startswith(h) for h in SUPPLIED_HEADINGS):
            skipping = True
            continue
        # Only a real section heading ends a supplied block. Shell comments inside an
        # example script start with "#" too, and treating those as headings used to end the
        # skip early and re-expose the rest of the script to the leak check.
        if skipping and not fenced and head in _SECTION_HEADS:
            skipping = False
        if not skipping:
            out.append(ln)
    return "\n".join(out)


def leaks(prompt: str, terms: list[str], patterns: bool = False) -> list[str]:
    """Terms or prescriptive phrases that would give away this subtask's answer.

    Word-boundary matching, not substring: plain `in` flagged the application "Chai" inside
    the word "chain", and a false positive here is not harmless — it burns a retry and can
    push the generator into stripping context the agent legitimately needs.
    """
    def bounded(t: str) -> str:
        # A \b only asserts a word/non-word transition, so it can never match against a term
        # that begins or ends with punctuation: "\b--ppn\b" failed on " --ppn" because space
        # and hyphen are both non-word characters, which silently disabled every flag-shaped
        # term in the list. Anchor each end only where the term actually starts or ends with
        # a word character.
        t = t.strip()
        return ((r"\b" if t[:1].isalnum() or t[:1] == "_" else "") + re.escape(t)
                + (r"\b" if t[-1:].isalnum() or t[-1:] == "_" else ""))

    found = {t for t in terms if re.search(bounded(t), prompt, re.I)}
    if patterns:
        for pat in LEAK_PATTERNS:
            for m in re.finditer(pat, prompt, re.I):
                found.add(m.group().strip())
    return sorted(found)


def show(n: int) -> int:
    rows = [json.loads(l) for l in OUT.open()]
    for r in random.Random(0).sample(rows, min(n, len(rows))):
        print(f"\n\033[1m{r['sample_id']}\033[0m  {r['subtask']} · {r['domain']} · "
              f"{r['system']}  \033[2m({r['variation']})\033[0m")
        print("─" * 94)
        for ln in r["prompt"].split("\n"):
            print(textwrap.fill(ln, 92, initial_indent="  ", subsequent_indent="     ")
                  if ln.strip() else "")
        print(f"  \033[2m── grading key from catalog ──\033[0m")
        print(textwrap.fill(json.dumps(r["grading_key"])[:400], 92,
                            initial_indent="    ", subsequent_indent="    "))
    print(f"\n{len(rows)} samples")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--show", type=int)
    ap.add_argument("--subtask")
    ap.add_argument("--subset", action="store_true",
                    help="the 10 stratified anchors only (40 samples)")
    ap.add_argument("--out", help="write elsewhere than samples.jsonl")
    args = ap.parse_args()
    global OUT
    if args.out:
        OUT = Path(args.out)
    anchors = SUBSET if args.subset else ANCHORS
    if args.show:
        return show(args.show)

    subs = {args.subtask: SUBTASKS[args.subtask]} if args.subtask else SUBTASKS
    jobs = []
    for st, spec in subs.items():
        pool = [v for v in VARIATIONS if v not in spec.get("skip_variations", [])]
        for i, (dom, app, sysn) in enumerate(anchors):
            # offset per subtask so the same anchor gets a different situation at each stage
            jobs.append((st, spec, dom, app, sysn,
                         pool[(i + 3 * spec["order"]) % len(pool)]))
    print(f"{len(jobs)} samples ({len(subs)} subtasks x {len(anchors)} anchors), "
          f"{args.workers} workers, up to {MAX_RETRIES} retries on leakage")

    done = {}
    if OUT.exists():
        for line in OUT.open():
            r = json.loads(line)
            if (r["prompt"] and not r["leaked"]
                    and all(has_section(r["prompt"], k) for k in SECTIONS)):
                done[(r["subtask"], r["app"], r["system"])] = r
    jobs = [j for j in jobs if (j[0], j[3], j[4]) not in done]
    if not jobs:
        print("all samples present — delete the file to regenerate")
        return show(3)

    lock, t0 = threading.Lock(), time.perf_counter()
    results, retried, failed = [], 0, []

    def work(job):
        st, spec, dom, app, sysn, var = job
        # Rendered in labelled, individually-budgeted sections rather than handed over raw and
        # clipped at judge.py:616. The old clip was inverted: Globus UUIDs and ClearML hashes
        # sit at the top of every system file and survived, while `hardware` and `job_defaults`
        # sit at the bottom and were cut on 6 of 9 systems. vllm@frontier lost 71% of its entry
        # including run_command and defaults, so its reference answer was written without them.
        cfg = catalog.render_system(sysn)
        acfg = catalog.render_app(sysn, app)
        wd = workdir(sysn, app, st, neutral=spec.get("needs_software_list", False))
        phys = physical_system(app) if spec.get("needs_physical_system") else ""
        mach = machine_spec(sysn) if spec.get("needs_machine_spec") else ""
        p = perf(sysn, app)
        if p:
            acfg += f"\n\n# MEASURED BENCHMARK on this system:\n{yaml.safe_dump(p)}"
        _d = app_yaml(sysn, app)
        name = _d.get("name") or _d.get("app") or app
        prior = prior_block(st, sysn, app, name)
        bad: list[str] = []
        r = {"prompt": "", "reference": ""}
        for _ in range(MAX_RETRIES):
            r = judge.generate_trinity_sample(
                st, spec["goal"], dom, sysn.capitalize(), var, spec["instructions"],
                spec["output"], spec["withhold"], cfg, installed(sysn), acfg,
                prior=prior, retry_terms=bad or None, sched=scheduler(sysn), workdir=wd,
                phys=phys, mach=mach, gives_sched=spec.get("gives_scheduler", False),
                show_catalog=spec.get("needs_software_list", False),
                input_spec=(_input_spec(sysn, app) if spec.get("needs_input_spec") else ""),
                app_setup=(_app_setup(sysn, app) if spec.get("needs_app_setup") else ""),
                build_defaults=(build_defaults(sysn, app)
                                if spec.get("needs_machine_spec") else ""),
                conventions=(trinity_site.CONVENTIONS.get(scheduler(sysn), "")
                             if spec.get("needs_conventions") else ""),
                example=(trinity_site.worked_script(scheduler(sysn))
                         if spec.get("needs_conventions") else
                         trinity_site.worked_deck(app)
                         if spec.get("needs_deck_example") else ""),
                example_kind=("script" if spec.get("needs_conventions") else "input deck"),
                account=(trinity_site.account(sysn) if spec.get("gives_account") else ""))
            if not r["prompt"]:
                continue
            # An application named by a prior stage is not a leak for that stage.
            terms = [t for t in spec["leak_terms"]
                     if not (prior and t.lower() in name.lower())]
            # prose leak patterns apply everywhere; they are about concluding the
            # answer in narrative, which is not specific to numeric subtasks
            supplies = any(spec.get(f) for f in ("needs_software_list", "needs_input_spec",
                                                 "needs_app_setup"))
            checked = strip_catalog(r["prompt"]) if supplies else r["prompt"]
            bad = leaks(checked, terms, True)
            # The account pattern was written when the account was WITHHELD. It is now
            # supplied on purpose (gives_account), because withholding it forced a correct
            # answer to use a placeholder and the judge then called the script unsubmittable.
            # Flagging our own supplied block as a leak is a false positive.
            if spec.get("gives_account"):
                bad = [b for b in bad
                       if not re.match(r"(?i)\s*(project\s+)?(account|allocation)\s*[:=]", b)]
            bad += [f"missing section {k}" for k in SECTIONS if not has_section(r["prompt"], k)]
            if not bad:
                break
        return job, r, bad

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futs = [pool.submit(work, j) for j in jobs]
        for i, fut in enumerate(as_completed(futs), 1):
            (st, spec, dom, app, sysn, var), r, bad = fut.result()
            if not r["prompt"]:
                bad = ["<empty>"]
            with lock:
                if bad:
                    failed.append((st, dom, bad))
                results.append({"subtask": st, "domain": dom, "system": sysn, "app": app,
                                "variation": var, "order": spec["order"],
                                "prompt": r["prompt"], "reference": r["reference"],
                                "grading_key": {**grading_key(sysn, app, spec["key_fields"]),
                                                **({"physical_system": physical_system(app)}
                                                   if spec.get("needs_physical_system") else {})},
                                "leaked": bad})
                print(f"  [{i}/{len(jobs)}] {'ok  ' if not bad else 'LEAK'} {st:<20}"
                      f"{dom:<30}{sysn}", flush=True)

    seen = {(r["subtask"], r["app"], r["system"]) for r in results}
    results += [v for k, v in done.items() if k not in seen]
    results.sort(key=lambda r: (r["order"], r["domain"]))
    with OUT.open("w") as f:
        for i, r in enumerate(results):
            # id last: a merged row carries its old sample_id and would otherwise win.
            f.write(json.dumps({**r, "sample_id": f"trin::{i:03d}"}, ensure_ascii=False) + "\n")

    print(f"\n{len(results)} samples in {(time.perf_counter()-t0)/60:.1f} min -> {OUT}")
    print(f"  {len(failed)} still flagged")
    for st, dom, bad in failed:
        print(f"    {st} / {dom}: {bad}")
    print(f"  by subtask: {dict(Counter(r['subtask'] for r in results))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
