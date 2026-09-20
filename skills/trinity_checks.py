#!/usr/bin/env python3
"""Evaluate the deterministic requirements in Python, before the judge is called.

This is the load-bearing change. Re-judging the same frozen answers three times under an
unchanged config flipped 12 of 141 verdicts, and 21% of Resource-selection rows — the judge
disagrees with itself. Every requirement decided here is removed from that variance
permanently, and the judge is handed the result as a settled fact rather than asked to
re-derive it.

35 of the library's 50 requirements are `decided_by: deterministic`. Of those, the ones that
matter most are the three failure modes named in review: a missing input file, a syntax error,
and a walltime over the queue maximum. None of them needs an opinion.

Verdicts:
    satisfied       the check passed
    violated        the check failed; `evidence` says how
    not_applicable  the requirement's `applies_if` guard excluded it
    not_evaluated   this check kind is not implemented yet — falls through to the judge

`not_evaluated` is deliberate and visible. A check that silently passed when it could not run
would inflate every score, which is the failure mode this whole exercise exists to remove.

Usage:
    python skills/trinity_checks.py --corpus v6 --limit 5
    python skills/trinity_checks.py --corpus v6 --subtask "Resource selection"
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from skills.judging.loader import load as load_skill  # noqa: E402
from skills.trinity_generate import CATALOG, app_yaml, scheduler  # noqa: E402
from skills import catalog  # noqa: E402

TRIN = ROOT / "results" / "skills" / "trinity"

# A reservation is a legitimate queue. 24 real scripts use `-q R7143698` and another uses
# R7156017; a check that consulted only the catalog's queue table would fail all of them.
RESERVATION = re.compile(r"^R\d{4,}$")

HMS = re.compile(r"^(\d+):(\d{2})(?::(\d{2}))?$")


def secs(t: str) -> int | None:
    m = HMS.match(t.strip())
    if not m:
        return None
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3) or 0)


def queues(system: str) -> dict:
    """The raw queue table, keyed by name.

    Shape is deliberately the untouched catalog mapping — `_queue_limit` and `_queue_exists`
    index it with `.get("max_walltime")` / `.get("min_nodes")` — but it is sourced through
    skills.catalog so there is one loader, one cache and one repair path.
    """
    return {k: q.raw for k, q in catalog.queues(system).items()}


def join_continuations(t: str) -> str:
    """Fold `\\`-continued lines into one before any pattern matching.

    Real scripts wrap their launch lines:
        mpiexec -n 4 --ppn 4 --depth=8 --cpu-bind=depth \\
            ${PW_X} -in v2o3.scf.in
    Matching line-by-line sees only the `mpiexec` fragment, so the binary that identifies the
    job is invisible — which made invokes_application flag a production QE script that plainly
    launches pw.x. The same bug bit app inference in runs_ingest.py; fixed in both places.
    """
    return re.sub(r"\\\s*\n\s*", " ", t)


def fenced_blocks(answer: str) -> str:
    """The file/script text a model produced, stripped of its prose.

    Requirements about syntax apply to what was written, not to the sentences around it —
    otherwise a model that *discusses* `#PBS -l filesystems` scores the same as one that
    emits it.
    """
    blocks = re.findall(r"```[^\n]*\n(.*?)```", answer, re.S)
    return join_continuations("\n".join(blocks) if blocks else answer)


# ---------------------------------------------------------------------------------------
# check kinds
# ---------------------------------------------------------------------------------------
def _regex(req, ctx) -> tuple[str, str]:
    pat = req["check"]["pattern"]
    m = re.search(pat, ctx["code"], re.M)
    return ("satisfied", f"matched at offset {m.start()}") if m else \
           ("violated", f"no match for /{pat[:48]}/")


def _regex_absent(req, ctx) -> tuple[str, str]:
    pat = req["check"]["pattern"]
    m = re.search(pat, ctx["code"], re.M)
    if not m:
        return "satisfied", "pattern absent"
    line = ctx["code"][:m.start()].count("\n") + 1
    return "violated", f"line {line}: {m.group(0)[:70]!r}"


_CONTRACTS = ROOT / "skills" / "format_contracts.yaml"


@lru_cache(maxsize=1)
def _contracts() -> dict:
    return (yaml.safe_load(_CONTRACTS.read_text()) or {}).get("contracts") or {}


def format_contract_for(app: str) -> dict:
    """The curated mandatory/expected sections for one application's input format."""
    return _contracts().get(app) or {}


RUBRIC_FIELD = "__rubric."      # sentinel: read from the requirement file, not the catalog


def catalog_get(req, ctx, default_path: str, default=None):
    """Resolve `check.field`, falling back to the kind's historical default path.

    Four of the six `field:` declarations in the requirement library were DEAD — the path was
    hardcoded in the implementing function, so retargeting a check by editing YAML silently did
    nothing. This makes the declaration mean what it says, and lets a requirement name any
    catalog path, including ones no check read before (`input_detection.filenames`,
    `output_patterns`, `defaults.constraint`).

    Each default is the exact path that kind used before, alternations included.
    `required_inputs|input_files` is load-bearing: 97 entries carry one and 96 the other, so
    collapsing it to a single path would quietly change behaviour on dozens of files.
    """
    path = (req.get("check") or {}).get("field") or default_path
    if path.startswith(RUBRIC_FIELD):
        return ctx.get(path[len(RUBRIC_FIELD):]) or default
    return catalog.get(ctx["system"], ctx["app"], path, default)


def _markers_present(req, ctx) -> tuple[str, str]:
    """All of the named strings must appear. Semantics matter here — see the warning.

    WARNING, and it cost this subtask most of its score. When `values:` is absent this falls
    back to `input_detection.content_markers`, which is a file-TYPE DETECTION list — "does this
    look like an NWChem deck?", any-of semantics — and applying it as all-of completeness made
    it the single largest violation source in Input preparation, 19 of 38 rows, wrong in nearly
    every instance: it demanded `echo` and `memory stack` (optional NWChem directives), `dump`
    (optional LAMMPS output), `vdwtype` (GROMACS default) and the literal amino-acid alphabet
    `ACDEFGHIKLMNPQRSTVWY` inside every FASTA.

    Mandatory sections belong in `values:`, curated per format — see
    skills/format_contracts.yaml and the `sections_present` kind, which reads it. Use
    `file_identifiable` for the any-of question this catalog field is actually good for.
    """
    vals = req["check"].get("values")
    if not vals:
        vals = catalog_get(req, ctx, "input_detection.content_markers") or []
    if not vals:
        # catalog silence, not an evaluation failure — see _numeric_match
        return "not_applicable", "catalog records no content markers for this application"
    missing = [v for v in vals if v.lower() not in ctx["code"].lower()]
    return ("satisfied", f"all {len(vals)} markers present") if not missing else \
           ("violated", f"missing: {', '.join(map(str, missing[:6]))}")


def _sections_present(req, ctx) -> tuple[str, str]:
    """The curated mandatory sections for this format, from skills/format_contracts.yaml.

    The honest replacement for content_markers_present: only what the application refuses to
    run without. Anything conditional or defaulted lives in `expected` there and is never
    required here.
    """
    c = format_contract_for(ctx["app"])
    vals = (req["check"].get("values") or (c.get("mandatory") if c else None)) or []
    if not vals:
        return "not_applicable", (f"no curated mandatory sections on file for {ctx['app']}"
                                  f" (see skills/format_contracts.yaml)")
    missing = [v for v in vals if v.lower() not in ctx["code"].lower()]
    return ("satisfied", f"all {len(vals)} mandatory sections present") if not missing else \
           ("violated", f"missing mandatory: {', '.join(map(str, missing[:6]))}")


def _file_identifiable(req, ctx) -> tuple[str, str]:
    """ANY-OF: does what the answer wrote read as this application's input format?

    This is `input_detection`'s honest use — the question it was written to answer. It catches
    the real failure (a model that emits a confident, well-formatted file of the WRONG format)
    without demanding every optional marker, which is what the all-of misreading did.
    """
    vals = catalog_get(req, ctx, "input_detection.content_markers") or []
    if not vals:
        return "not_applicable", "catalog records no detection markers for this application"
    code = ctx["code"].lower()
    hit = [v for v in vals if str(v).lower() in code]
    return ("satisfied", f"recognisable as {ctx['app']} input ({', '.join(map(str, hit[:4]))})") \
        if hit else ("violated", f"nothing written matches any known {ctx['app']} input marker "
                                 f"({', '.join(map(str, vals[:5]))})")


def _filenames_present(req, ctx) -> tuple[str, str]:
    """Exact filenames the application opens by name, e.g. HPL.dat, INCAR, namelist.input.

    Only meaningful where the name itself is load-bearing — `xhpl` opens `HPL.dat` and nothing
    else — so extension-bearing entries are kept only when the extension is actually an input
    extension. `input_detection.filenames` sometimes names the driver script instead:
    alphafold@perlmutter lists `run_alphafold.py` while its inputs are .fasta/.fa.
    """
    # Only formats that genuinely open a file BY NAME. GROMACS takes every filename as a CLI
    # argument — `gmx grompp -c lysozyme.gro -f md.mdp` is ordinary practice — so the catalog's
    # conf.gro/md.mdp/topol.top are conventions, and requiring them failed a correct answer that
    # had simply named its structure file after the protein. Opt in per format.
    if not format_contract_for(ctx["app"]).get("fixed_filenames"):
        return "not_applicable", (f"{ctx['app']} filenames are passed as arguments, not opened "
                                  f"by a fixed name")
    names = catalog_get(req, ctx, "input_detection.filenames") or []
    i = catalog.inputs(ctx["system"], ctx["app"])
    exts = {f.ext for f in (*i.required, *i.optional) if f.ext} | set(i.extensions)
    names = [n for n in names
             if "." not in n or not exts or f".{n.rsplit('.', 1)[1]}" in exts]
    if not names:
        return "not_applicable", "no exact input filenames recorded for this application"
    missing = [n for n in names if n.lower() not in ctx["answer"].lower()]
    return ("satisfied", f"names {', '.join(names)}") if not missing else \
           ("violated", f"never names {', '.join(missing[:4])}, which this application opens "
                        f"by that exact name")


def _outputs_not_authored(req, ctx) -> tuple[str, str]:
    """The answer must not write contents for files the RUN produces.

    Catalog-driven from `output_patterns` (101 entries) rather than the hand-written
    `binary_files:` lists that exist in only three rubric files. The derivation subtracts
    anything that is also an input — gromacs@sirius lists `md.gro` as an output while `.gro` is
    a legitimately authored input — and the rubric's hand lists are UNIONED in rather than
    replaced, because they encode format knowledge the catalog lacks (`.tpr` sits in
    required_inputs yet is compiled by grompp, never written).
    """
    i = catalog.inputs(ctx["system"], ctx["app"])
    pats = {f.ext or f.raw for f in i.authorable_outputs} | set(ctx.get("binary_files") or [])
    pats = {p for p in pats if p}
    if not pats:
        return "satisfied", "this application produces no files the answer could fabricate"
    return _no_contents_for({"check": {"values": sorted(pats)}}, ctx)


def _file_present(req, ctx) -> tuple[str, str]:
    """Is each required input actually PRODUCED, not merely mentioned?

    30% agreement before this: the check asked whether the extension string appeared anywhere
    in the answer, so a model that wrote "the .h5 is generated by pw2qmcpack" scored the same
    as one that emitted the file. The human found 5 violations it passed.

    A file counts as produced when a filename bearing that extension appears as a code-block
    heading or label — the shape every answer uses when it writes a file out — rather than
    anywhere in the prose.
    """
    req_in = catalog_get(req, ctx, "required_inputs|input_files") or []
    # A binary required input is COMPILED or produced at runtime, so "was it written out?" is
    # the wrong question and answering yes rewards exactly the defect no_binary_contents
    # forbids. GROMACS lists `.tpr` as required; this check was reporting "all of ['.tpr']
    # produced" for an answer that authored a .tpr as text — a fatal error under the
    # gromacs rule two lines down. Measured: 4 of the 47 misses.
    binaries = {b.lower() for b in (ctx.get("binary_files") or [])}
    req_in = [e for e in req_in if str(e).lower() not in binaries]
    if not req_in:
        return "not_applicable", "every required input for this app is binary or runtime-built"
    ans = ctx["answer"]
    produced, mentioned = [], []
    for e in req_in:
        ext = re.escape(str(e).lstrip("*"))
        # a filename carrying the extension, on a heading/label line or a fence info string
        as_file = re.search(rf"(?m)^[^\n]{{0,80}}?[\w./-]+{ext}\b[^\n]{{0,40}}$", ans)
        fenced = re.search(rf"```[^\n]*{ext}", ans)
        near_fence = re.search(rf"[\w./-]+{ext}\b[^\n]{{0,60}}\n+```", ans)
        (produced if (fenced or near_fence or as_file) else mentioned).append(str(e))
    # Where the catalog lists alternative extensions for one artifact (LAMMPS accepts
    # .lammps, .in or .lmp for the same input script), producing any ONE of them satisfies
    # the requirement. Demanding all three failed answers that were correct.
    ALT = {"lammps", "qe", "cp2k", "namd", "alphafold"}
    if ctx["app"] in ALT and produced:
        return "satisfied", f"produced {produced[0]} (alternatives: {', '.join(req_in)})"
    if not mentioned:
        return "satisfied", f"all of {req_in} produced"
    return "violated", (f"required input(s) {', '.join(mentioned)} not produced as a file"
                        + (f" (produced: {', '.join(produced)})" if produced else ""))


def _no_contents_for(req, ctx) -> tuple[str, str]:
    """A binary file must be referenced, never authored with contents."""
    vals = req["check"].get("values") or catalog_get(req, ctx, "__rubric.binary_files") or []
    if not vals:
        # Worst-agreeing rule in the library at 20%: it returned not_applicable for every app
        # without a declared binary list, while the human correctly read "did not fabricate
        # binary contents" as trivially SATISFIED. An app with no binary inputs cannot fail
        # this, so say so rather than standing down.
        return "satisfied", "this application has no binary or runtime-generated inputs"
    bad = []
    for ext in vals:
        # a fenced block whose header or preceding line names the binary file
        for m in re.finditer(rf"([^\n]*{re.escape(ext)}[^\n]*)\n+```[^\n]*\n(.{{0,400}})",
                             ctx["answer"], re.S | re.I):
            if len(m.group(2).strip()) > 40:
                bad.append(f"{ext}: contents written under {m.group(1).strip()[:48]!r}")
                break
    return ("satisfied", f"{', '.join(vals)} referenced, not authored") if not bad else \
           ("violated", "; ".join(bad))


def _hpl_lines(code: str) -> list[str]:
    """The HPL.dat block from an answer, as a list of non-empty lines."""
    m = re.search(r"```[^\n]*\n(.*?)```", code, re.S)
    body = m.group(1) if m else code
    return [ln.rstrip() for ln in body.splitlines() if ln.strip()]


def _hpl_counts(code: str) -> list[tuple[str, int, int]]:
    """Every (label, declared count, values on the next line) triple in an HPL.dat.

    HPL.dat is strictly positional and its count lines come in pairs: a line reading
    `4            # of problem sizes (N)` followed by a line holding exactly that many values.
    A mismatch is the single most common HPL error and PBS cannot catch it — xhpl reads past
    the end and either misreads the grid or segfaults.
    """
    lines = _hpl_lines(code)
    out = []
    for i, ln in enumerate(lines[:-1]):
        m = re.match(r"^\s*(\d+)\s+(?:#\s*)?of\s+(.+?)\s*$", ln, re.I)
        if not m:
            continue
        label = re.sub(r"\s+", " ", m.group(2))[:40]
        nxt = re.split(r"\s{2,}(?=[A-Za-z#])|#", lines[i + 1].strip())[0]
        vals = [v for v in re.split(r"[\s,]+", nxt.strip()) if re.fullmatch(r"-?\d+(\.\d+)?", v)]
        out.append((label, int(m.group(1)), len(vals)))
    return out


def _grid_matches_ranks(req, ctx) -> tuple[str, str]:
    """P x Q from the HPL.dat the answer WROTE, against the rank count it states.

    Must never read ctx["extracted"]: that cache was keyed without a subtask, so this rule was
    reading nodes x ranks_per_node out of the model's RESOURCE-SELECTION answer and reporting
    `deterministic / satisfied` on all four HPL rows. Its evidence, "64 x 128 = 8192", never
    came near an HPL.dat.
    """
    lines = _hpl_lines(ctx["code"])
    def after(label):
        for i, ln in enumerate(lines[:-1]):
            if re.search(rf"of\s+{label}", ln, re.I):
                nxt = re.split(r"\s{2,}(?=[A-Za-z#])|#", lines[i + 1].strip())[0]
                return [int(v) for v in re.split(r"[\s,]+", nxt.strip()) if v.isdigit()]
        return []
    ps, qs = after(r"process grids?\s*\(\s*P"), after(r"process grids?\s*\(\s*Q")
    if not ps:
        ps = [int(v) for v in re.findall(r"(?m)^\s*(\d+)\s*$", "")] or []
    if not (ps and qs):
        return "not_evaluated", "no P/Q grid lines found in the HPL.dat written"
    grid = ps[0] * qs[0]
    m = re.search(r"(\d+)\s*(?:total\s+)?(?:MPI\s+)?(?:ranks|processes|tasks)", ctx["answer"], re.I)
    if not m:
        return "not_evaluated", f"P x Q = {grid} but the answer states no rank count"
    ranks = int(m.group(1))
    return ("satisfied", f"P x Q = {ps[0]} x {qs[0]} = {grid} matches {ranks} ranks") \
        if grid == ranks else \
        ("violated", f"P x Q = {ps[0]} x {qs[0]} = {grid} but the answer states {ranks} ranks; "
                     f"xhpl requires P*Q to equal the rank count exactly")


def _count_match(req, ctx) -> tuple[str, str]:
    c = req["check"]
    if c.get("style") == "hpl":
        rows = _hpl_counts(ctx["code"])
        if not rows:
            return "not_evaluated", "no `N of ...` count lines found in the HPL.dat written"
        bad = [f"{lab}: declares {n}, {k} value(s) on the next line"
               for lab, n, k in rows if n != k]
        return ("satisfied", f"all {len(rows)} count lines match their value lines") if not bad \
            else ("violated", "; ".join(bad[:3]))
    dec, card = c.get("declares"), c.get("counts_card") or c.get("counts")
    if not dec or not card:
        return "not_evaluated", "check under-specified"
    m = re.search(dec, ctx["code"], re.I)
    if not m:
        return "not_applicable", f"no declaration matching /{dec}/"
    declared = int(m.group(1))
    # count non-blank, non-comment lines after the card until a blank line or next card
    seg = re.split(rf"{re.escape(card)}[^\n]*\n", ctx["code"], maxsplit=1, flags=re.I)
    if len(seg) < 2:
        return "violated", f"{declared} declared but no {card} card found"
    lines = []
    for ln in seg[1].splitlines():
        s = ln.strip()
        if not s or s.startswith(("!", "#", "/")):
            break
        if re.match(r"^[A-Z_]{3,}", s) and not re.match(r"^[A-Z][a-z]?\s", s):
            break
        lines.append(s)
    return ("satisfied", f"{declared} declared, {len(lines)} written") if len(lines) == declared \
        else ("violated", f"{declared} declared, {len(lines)} written under {card}")


def _queue_exists(req, ctx) -> tuple[str, str]:
    q = ctx["extracted"].get("queue")
    if not q:
        # A batch script names its queue directly in `#PBS -q` / `--qos=`, so it needs no
        # LLM extraction step. Reading it here is what lets this requirement apply to Batch
        # job creation as well as Resource selection.
        m = re.search(r"(?m)^\s*#PBS\s+-q\s+(\S+)", ctx["code"]) or \
            re.search(r"(?m)^\s*#SBATCH\s+(?:-q|--qos=|-p|--partition=)\s*(\S+)", ctx["code"])
        q = m.group(1) if m else None
    if not q:
        return "not_evaluated", "no queue named in the answer"
    qs = queues(ctx["system"])
    if RESERVATION.match(q):
        return "satisfied", f"{q} is a reservation ID"
    return ("satisfied", f"{q} exists on {ctx['system']}") if q in qs else \
           ("violated", f"{q} is not a queue on {ctx['system']} "
                        f"(has: {', '.join(sorted(qs)[:6])})")


def _no_reservation(req, ctx) -> tuple[str, str]:
    """A reservation is legal but is not a defensible choice for a freshly written script.

    `R7143698` is a temporary allocation tied to one project and one window. 24 real archived
    scripts use one — correctly, for their moment — which is exactly why those scripts are
    imperfect positive controls for queue choice, and why judge_calibrate exempts this rule.
    """
    q = ctx["extracted"].get("queue")
    if not q:
        return "not_evaluated", "no queue extracted from the answer"
    return ("violated", f"{q} is a reservation; a generated script should target a standard "
                        f"queue") if RESERVATION.match(q) else \
           ("satisfied", f"{q} is a standard queue")


def _queue_limit(req, ctx) -> tuple[str, str]:
    field = req["check"]["field"]
    q = ctx["extracted"].get("queue")
    qs = queues(ctx["system"])
    if not q or q not in qs:
        return "not_evaluated", "queue unknown or not in the catalog table"
    lim = qs[q]
    if field == "walltime":
        w = ctx["extracted"].get("walltime_seconds")
        cap = lim.get("max_walltime")
        if not isinstance(w, int) or not cap:
            return "not_evaluated", "walltime or cap unavailable"
        return ("satisfied", f"{w//3600}h{(w%3600)//60:02d} <= cap {cap//3600}h") if w <= cap \
            else ("violated", f"walltime {w//3600}h{(w%3600)//60:02d} exceeds {q} maximum "
                              f"{cap//3600}h")
    n = ctx["extracted"].get("nodes")
    if not isinstance(n, int):
        return "not_evaluated", "node count unavailable"
    lo, hi = lim.get("min_nodes"), lim.get("max_nodes")
    if hi and n > hi:
        return "violated", f"{n} nodes exceeds {q} maximum {hi}"
    if lo and n < lo:
        return "violated", f"{n} nodes is below {q} minimum {lo}"
    return "satisfied", f"{n} nodes within {q} [{lo}, {hi}]"


def _arithmetic(req, ctx) -> tuple[str, str]:
    e = ctx["extracted"]
    n, ppn, tot = e.get("nodes"), e.get("ranks_per_node"), e.get("total_ranks")
    if not all(isinstance(v, int) for v in (n, ppn, tot)):
        return "not_evaluated", "nodes/ranks not all extracted"
    return ("satisfied", f"{n} x {ppn} = {tot}") if n * ppn == tot else \
           ("violated", f"{n} nodes x {ppn} ranks/node = {n*ppn}, but {tot} stated")


def _numeric_match(req, ctx) -> tuple[str, str]:
    """Compare against the catalog's build default — but only where one is recorded.

    The distinction between the two non-verdicts is load-bearing and was wrong here:
        not_applicable  the rule does not apply; NOBODY rules on it
        not_evaluated   code could not decide; the judge rules instead

    A missing catalog field is the first. Returning the second meant that on the 57 of 144
    catalog entries (40%) with no `defaults.ppn` — 12 of 40 Resource-selection answers — the
    judge was handed "ranks must follow the build defaults" with no defaults in existence. It
    duly invented them: one answer asserted "one MPI rank per GPU" as standard GROMACS build
    behaviour, when the recorded default for that system is 8.
    """
    want = catalog_get(req, ctx, "defaults.ppn")
    if want is None:
        # r10 turned this into not_applicable so the judge would stop inventing defaults.
        # That over-corrected: the question disappeared entirely, and 6 of the 47 missed
        # violations are here. There is no default to compare against, but the HARDWARE is in
        # the prompt, so a rank layout can still be implausible (16 ranks per node on a 4-GPU
        # node). Hand it back to the judge to check against the hardware, not against a
        # default that does not exist.
        return "not_evaluated", ("catalog records no defaults.ppn — judge against the "
                                 "hardware in the prompt, not against a build default")
    got = ctx["extracted"].get("ranks_per_node")
    if not isinstance(got, int):
        return "not_evaluated", "no ranks-per-node extracted from the answer"
    return ("satisfied", f"{got} ranks/node matches the build default") if got == want else \
           ("violated", f"{got} ranks/node; the build default is {want}")


def _invokes_app(req, ctx) -> tuple[str, str]:
    """Does the script launch this application at all? Deliberately tolerant.

    Accepts any of: the catalog binary's basename, the app name, or a common alias, appearing
    on or after a launcher line. Does NOT compare flags, paths or argument order — real
    launchers carry affinity and depth settings the catalog's example omits, and demanding a
    match there failed 3 of 7 production scripts.
    """
    # Resolve simple shell assignments before matching. Scripts routinely do
    #     PW_X=/soft/applications/quantum_espresso/7.5/bin/pw.x
    #     mpiexec -n 4 ... "$PW_X" -in v2o3.scf.in
    # so the launcher line names a VARIABLE, not the binary. Pattern-matching around the
    # variable was brittle — the first attempt required whitespace after it and the script
    # used `"$PW_X"`, a quote. Substituting the value is what actually works.
    def resolve(text: str) -> str:
        env = dict(re.findall(r"(?m)^\s*(\w+)=([^\s;#]+)", text))
        for _ in range(2):                    # two passes: values may reference other vars
            for k, v in env.items():
                text = text.replace(f"${{{k}}}", v).replace(f"${k}", v)
        return text

    names = {ctx["app"].lower()}
    b = str(ctx["app_cfg"].get("binary") or "")
    if b:
        names.add(Path(b).name.lower())
    names |= {str(a).lower() for a in (ctx["app_cfg"].get("aliases") or [])}
    names |= {"pw.x", "bands.x"} if ctx["app"] == "qe" else set()
    names |= {"torchrun"} if ctx["app"] == "pytorch" else set()
    code = resolve(ctx["code"]).lower()
    launchers = [l for l in code.splitlines()
                 if re.match(r"\s*(mpiexec|srun|aprun|torchrun|python)\b", l)]
    if not launchers:
        return "violated", "no launcher line (mpiexec/srun/torchrun) in the script"
    blob = "\n".join(launchers)
    hit = [n for n in names if n and len(n) > 2 and n in blob]
    if hit:
        return "satisfied", f"launches {sorted(hit)[0]}"
    # A Python framework is invoked through a SCRIPT, never by its own name. Real PyTorch
    # jobs in the archive run `torchrun ... train_cifar10_ddp.py` or
    # `mpiexec ... python train.py` — neither contains the string "pytorch", so demanding it
    # failed every correct answer. Same shape as the nekRS `--setup` case: the check encoded
    # one mechanism instead of the outcome.
    if ctx["app"] in {"pytorch", "deepspeed", "vllm", "alphafold", "openfold", "chai_lab"}:
        m = re.search(r"[\w./${}-]+\.py\b|(?:^|\s)python[0-9.]*\s+[\w./${}-]+", blob)
        if m:
            return "satisfied", f"launches the python program {m.group(0).strip()[:44]}"
    # the binary may be held in a variable assigned earlier
    if re.search(r"\$\{?\w+\}?\s", blob) and any(n in code for n in names if len(n) > 2):
        return "satisfied", "launches the application through a shell variable"
    return "violated", f"no launcher references {ctx['app']} or its binary"


GPU_CLAIM = re.compile(r"\b(gpu[- ]?(accel|offload|enabled|support)|cuda|sycl|rocm|hip|xpu|"
                       r"offload(ed|ing)? to (the )?gpu|gpu[- ]resident)\b", re.I)


def _claims_match_catalog(req, ctx) -> tuple[str, str]:
    """Narrow, machine-checkable contradiction of a recorded catalog field.

    Only `gpu_support` is checked, and only when the catalog actually records it. This rule
    previously had no implementation at all, so it fell through to the judge, which read its
    title and applied it to anything the catalog did not mention — flagging a correct claim
    that CP2K supports B3LYP, and vLLM claims where `gpu_support` is absent entirely. Five of
    its eight firings were that.

    The three that were real all had the same shape: `qe@aurora` has `gpu_support: False`, and
    three different models claimed SYCL/XPU offload for it. That is worth catching and is
    pure comparison, so it belongs in code. Silence is never contradiction.
    """
    # This check only compares ONE field — gpu_support — while the requirement covers module
    # names, install paths, dependencies and how the code is loaded as well. So it may only
    # report "satisfied" for the slice it actually examined, and must hand the rest to the
    # judge. Saying satisfied on the strength of an unexamined claim is how all 5 of this
    # rule's missed violations happened: the human found contradictions about modules and
    # paths while the code passed the answer because gpu_support happened to agree.
    gs = ctx["app_cfg"].get("gpu_support")
    if gs is None:
        return "not_evaluated", ("catalog records no gpu_support; other facility claims "
                                 "(modules, paths, dependencies) still need checking")
    if gs:
        return "not_evaluated", ("gpu_support is true so no GPU contradiction is possible; "
                                 "other facility claims still need checking")
    m = GPU_CLAIM.search(ctx["answer"])
    if not m:
        return "not_evaluated", ("CPU-only build and no GPU claim made; other facility "
                                 "claims still need checking")
    line = ctx["answer"][max(0, m.start() - 70):m.end() + 40].replace("\n", " ")
    return "violated", (f"catalog records gpu_support: false, but the answer claims "
                        f"{m.group(0)!r} — ...{line.strip()[:90]}")


def _dialect_match(req, ctx) -> tuple[str, str]:
    want = scheduler(ctx["system"])
    has_pbs, has_slurm = "#PBS" in ctx["code"], "#SBATCH" in ctx["code"]
    if has_pbs and has_slurm:
        return "violated", "both #PBS and #SBATCH directives present"
    if want == "PBS Pro" and has_slurm:
        return "violated", f"#SBATCH used, but {ctx['system']} runs PBS Pro"
    if want == "Slurm" and has_pbs:
        return "violated", f"#PBS used, but {ctx['system']} runs Slurm"
    if not (has_pbs or has_slurm):
        return "violated", "no scheduler directives at all"
    return "satisfied", f"{want} directives, correct for {ctx['system']}"


KINDS = {"no_reservation": _no_reservation, "invokes_app": _invokes_app,
         "sections_present": _sections_present, "file_identifiable": _file_identifiable,
         "filenames_present": _filenames_present,
         "outputs_not_authored": _outputs_not_authored,
         "grid_matches_ranks": _grid_matches_ranks,
         "claims_match_catalog": _claims_match_catalog, "regex": _regex, "regex_absent": _regex_absent, "markers_present": _markers_present,
         "file_present": _file_present, "no_contents_for": _no_contents_for,
         "count_match": _count_match, "queue_exists": _queue_exists,
         "queue_limit": _queue_limit, "arithmetic": _arithmetic,
         "numeric_match": _numeric_match, "dialect_match": _dialect_match}


def guard_blocks(req: dict, app: str, system: str) -> str | None:
    """Why this requirement does not apply here, or None if it does.

    `applies_if` previously understood only `scheduler`, and only for deterministic checks —
    a JUDGED requirement was handed to the LLM unconditionally. So vLLM, whose catalog records
    no required inputs at all and whose prompt says "(none required)", was asked whether it
    passed its input filenames, and the judge reported the absence of something never needed.
    """
    g = req.get("applies_if") or {}
    if g.get("scheduler") and g["scheduler"] != scheduler(system):
        return f"guard: {g['scheduler']} only"
    if g.get("has_required_inputs"):
        d = app_yaml(system, app)
        if not (d.get("required_inputs") or d.get("input_files")):
            return "this application has no required input files"
    return None


def evaluate(subtask: str, app: str, system: str, answer: str,
             extracted: dict | None = None) -> dict:
    skill = load_skill(subtask, app, system)
    ctx = {"answer": answer, "code": fenced_blocks(answer), "app": app, "system": system,
           "app_cfg": app_yaml(system, app), "extracted": extracted or {},
           "binary_files": skill.binary_files}
    out = {}
    for r in skill.deterministic:
        why = guard_blocks(r, app, system)
        if why:
            out[r["id"]] = {"verdict": "not_applicable", "evidence": why}
            continue
        fn = KINDS.get((r.get("check") or {}).get("kind"))
        if not fn:
            out[r["id"]] = {"verdict": "not_evaluated",
                            "evidence": f"kind {(r.get('check') or {}).get('kind')!r} "
                                        f"not implemented"}
            continue
        try:
            v, ev = fn(r, ctx)
        except Exception as e:
            v, ev = "not_evaluated", f"{type(e).__name__}: {e}"
        out[r["id"]] = {"verdict": v, "evidence": ev, "severity": r.get("severity", "major"),
                        "dimension": r.get("dimension")}
    return out


# Resource-selection answers are prose, so the nodes/queue/walltime have to be READ out
# before they can be checked. That read is a far lower-variance task than judging — it is
# extraction, not evaluation — and the DECISION stays arithmetic. Cached to disk so the
# checks themselves are reproducible without re-calling anything.
EXTRACT = """Read this HPC resource-sizing answer and extract what it finally requests.
If it offers several options, take the one it recommends. Use null for anything absent.

Return ONLY JSON:
{"queue": "<name or null>", "nodes": <int|null>, "walltime_seconds": <int|null>,
 "ranks_per_node": <int|null>, "total_ranks": <int|null>}

Answer:
{answer}"""


def extraction_cache(corpus: str) -> Path:
    return TRIN / f"extracted_{corpus}.json"


# The extraction cache holds nodes/ranks/walltime READ OUT of a Resource-selection answer.
# It was keyed "{model}::{app}::{system}" — no subtask — while `run_cell` handed it to every
# subtask, so an Input-preparation check could read a DIFFERENT subtask's answer and rule on it.
# Measured on v7: INP.hpl.grid_matches_ranks returned deterministic/satisfied for all four
# models, its evidence ("64 x 128 = 8192") being nodes x ranks_per_node lifted straight from the
# model's Resource-selection answer. It never looked at the HPL.dat at all.
EXTRACT_SUBTASK = "Resource selection"


def cache_key(subtask: str, model: str, app: str, system: str) -> str:
    return f"{subtask}::{model}::{app}::{system}"


def cache_get(cache: dict, subtask: str, model: str, app: str, system: str) -> dict | None:
    """Look up extracted values for THIS subtask, never another's.

    Legacy caches (v6, v7) hold unkeyed 3-part entries. Those were all written from
    Resource-selection answers, so they resolve only for that subtask; every other subtask
    correctly misses and its arithmetic checks return not_evaluated.
    """
    hit = cache.get(cache_key(subtask, model, app, system))
    if hit is None and subtask == EXTRACT_SUBTASK:
        hit = cache.get(f"{model}::{app}::{system}")
    return hit


def extract_all(corpus: str, workers: int = 5) -> dict:
    """Fill the extraction cache for every Resource-selection answer."""
    import judge
    from concurrent.futures import ThreadPoolExecutor, as_completed
    cache_p = extraction_cache(corpus)
    cache = json.loads(cache_p.read_text()) if cache_p.exists() else {}
    rows = [json.loads(l) for l in (TRIN / f"answers_{corpus}.jsonl").open()]
    todo = [r for r in rows if r["subtask"] == EXTRACT_SUBTASK and r.get("answer")
            and cache_get(cache, r["subtask"], r["model"], r["app"], r["system"]) is None]
    print(f"extracting {len(todo)} Resource-selection answers")

    def one(r):
        k = cache_key(r["subtask"], r["model"], r["app"], r["system"])
        try:
            msg = judge._get_client().with_options(timeout=300).messages.create(
                model=judge.TRINITY_JUDGE_MODEL, max_tokens=2500,
                messages=[{"role": "user",
                           "content": EXTRACT.replace("{answer}", r["answer"][:9000])}])
            m = re.search(r"\{.*\}", judge._text_of(msg), re.S)
            return k, (json.loads(m.group()) if m else None)
        except Exception:
            return k, None

    with ThreadPoolExecutor(max_workers=workers) as pool:
        for fut in as_completed([pool.submit(one, r) for r in todo]):
            k, v = fut.result()
            if v:
                cache[k] = v
    cache_p.write_text(json.dumps(cache, indent=1))
    print(f"extraction cache: {len(cache)} entries -> {cache_p.name}")
    return cache


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--extract", action="store_true",
                    help="fill the extraction cache (one LLM read per answer)")
    ap.add_argument("--corpus", default="v6")
    ap.add_argument("--subtask")
    ap.add_argument("--limit", type=int)
    a = ap.parse_args()

    if a.extract:
        extract_all(a.corpus)
    cp = extraction_cache(a.corpus)
    cache = json.loads(cp.read_text()) if cp.exists() else {}

    answers = [json.loads(l) for l in (TRIN / f"answers_{a.corpus}.jsonl").open()
               if json.loads(l).get("answer")]
    if a.subtask:
        answers = [r for r in answers if r["subtask"] == a.subtask]
    if a.limit:
        answers = answers[:a.limit]

    tally, by_req = Counter(), {}
    viol = []
    for r in answers:
        res = evaluate(r["subtask"], r["app"], r["system"], r["answer"],
                       cache_get(cache, r["subtask"], r["model"], r["app"], r["system"]))
        for rid, v in res.items():
            tally[v["verdict"]] += 1
            by_req.setdefault(rid, Counter())[v["verdict"]] += 1
            if v["verdict"] == "violated":
                viol.append((r["model"], r["subtask"], r["app"], rid, v["evidence"]))

    n = sum(tally.values())
    print(f"{len(answers)} answers, {n} deterministic checks evaluated\n")
    for k in ("satisfied", "violated", "not_applicable", "not_evaluated"):
        print(f"  {k:<16}{tally[k]:>5}{tally[k]/max(n,1):>7.0%}")

    print(f"\n{'requirement':<44}{'sat':>5}{'viol':>6}{'n/a':>5}{'n/e':>5}")
    for rid, c in sorted(by_req.items(), key=lambda kv: -kv[1]["violated"]):
        print(f"{rid:<44}{c['satisfied']:>5}{c['violated']:>6}"
              f"{c['not_applicable']:>5}{c['not_evaluated']:>5}")

    print(f"\nsample violations:")
    for m, st, app, rid, ev in viol[:12]:
        print(f"  [{st[:14]:<14}] {app:<10} {rid:<38} {ev[:60]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
