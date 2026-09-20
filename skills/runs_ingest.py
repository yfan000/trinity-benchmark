#!/usr/bin/env python3
"""Index the real Polaris runs so requirements can be mined from execution, not inference.

A run that executed is ground truth in a way an LLM-written reference answer is not. These
directories hold the artifacts of all four pipeline stages at once — the job script (Batch job
creation), the input decks (Input preparation), the resources actually requested (Resource
selection) and the application actually used (Software selection).

The unit of indexing is the **job script**, not the directory, because the directory is not a
reliable unit: `water_qmc_v2/` holds four scripts over three cases, while
`dft_mp-18937.archive_*/` is one script at the top level. Inputs and logs are associated by
proximity and by what the launcher lines actually reference.

Nothing here trusts a filename. The application is inferred from the binary paths and module
lines in the script and cross-checked against the catalog's own `binary`/`aliases`/`keywords`;
success is inferred from log content, not from a file existing.

Usage:
    python skills/runs_ingest.py                     # index and report coverage
    python skills/runs_ingest.py --show water_qmc_v2 # dump one directory's parse
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from skills.trinity_task_spec import ANCHORS, SUBSET  # noqa: E402
from skills import catalog  # noqa: E402
from skills.trinity_generate import CATALOG  # noqa: E402

RUNS = ROOT.parent / "trinity_jobs" / "polaris"
OUT = ROOT / "results" / "skills" / "trinity" / "runs"

# A job script is anything that drives work on a compute node. Some carry #PBS directives;
# the IRI-style ones do not, because they are launched inside an existing allocation.
LAUNCHER = re.compile(r"^\s*(mpiexec|srun|aprun|torchrun|python\s+-m\s+torch\.distributed)\b",
                      re.M)
PBS_LINE = re.compile(r"^\s*#PBS\s+(-\w+)\s+(.*?)\s*$", re.M)


def catalog_index() -> list[dict]:
    """Every catalog app on Polaris, with the strings that identify it in a script."""
    out = []
    for f in sorted((CATALOG / "software" / "polaris").glob("*.yaml")):
        d = catalog.merged("polaris", f.stem)   # repaired + multi-document
        binary = str(d.get("binary") or "")
        # IDENTIFIERS ONLY. `keywords` is a descriptive/search field and contains generic
        # words — alphafold.yaml lists "python", hpl.yaml lists "benchmark" — so using it to
        # identify an application made any script mentioning python an AlphaFold job. That
        # mislabelled 2 of 8 calibration samples and inflated alphafold to 74 scripts.
        marks = {f.stem.lower()}
        marks |= {str(a).lower() for a in (d.get("aliases") or [])}
        if binary:
            marks.add(Path(binary).name.lower())
        marks = {m for m in marks if len(m) > 2 and m not in GENERIC}
        out.append({"app": f.stem, "name": d.get("name") or f.stem,
                    "binary": binary, "marks": marks,
                    "required_inputs": d.get("required_inputs") or d.get("input_files") or []})
    return out


# Binaries that identify an application but are not its catalog name. pw.x and pw2qmcpack.x
# both appear in QMCPACK workflows, so ordering matters: the more specific wins.
BINARY_HINTS = [("qmcpack", "qmcpack"), ("pw2qmcpack", "qmcpack"), ("nekrs", "nekrs"),
                ("lmp", "lammps"), ("gmx", "gromacs"), ("nwchem", "nwchem"),
                ("cp2k", "cp2k"), ("namd", "namd"), ("xhpl", "hpl"),
                ("pw.x", "qe"), ("bands.x", "qe"), ("ph.x", "qe"), ("cp.x", "qe"),
                # torchrun is the giveaway for a PyTorch job. Without it these matched
                # `conda.yaml` in the catalog, because every one of them does
                # `module load conda` — an environment, not the application under test.
                ("torchrun", "pytorch"), ("torch.distributed", "pytorch"),
                ("deepspeed", "deepspeed"),
                ("vllm", "vllm"), ("alphafold", "alphafold"), ("colabfold", "alphafold")]

# Catalog entries that describe an environment or toolchain rather than a scientific
# application. Matching one of these tells us nothing about what the job actually ran.
NOT_APPS = {"conda", "python", "frameworks", "spack"}

# Words that identify nothing. Any of these matching would label a script by coincidence.
GENERIC = {"python", "benchmark", "bench", "run", "test", "job", "gpu", "cpu", "mpi", "omp",
           "parallel", "simulation", "compute", "science", "data", "train", "serve", "build",
           "demo", "smoke", "app", "code", "tool", "library", "framework"}

# A script that COMPILES software is not a script that RUNS it. Build scripts legitimately
# have no launcher and pass no input files, so grading one against "did it launch the
# application correctly?" asks the wrong question — which is what made build_gromacs/run.sh
# look like a judge false positive when the judge was right.
BUILD = re.compile(r"(?m)^\s*(make\b|cmake\b|\./configure|python\s+setup\.py|"
                   r"pip\s+install|spack\s+install|cargo\s+build|meson\b|ninja\b)")

# The archive lives under a directory called "polaris", but that is only where results were
# saved — some jobs ran on other machines. The target system has to come from the script.
# Ordered most-specific first: an explicit `system=` in the select statement beats a
# filesystem hint, which beats a module or path convention.
SYSTEM_HINTS = [
    (re.compile(r"select=[^\s]*system=(\w+)", re.I), None),        # capture group wins
    (re.compile(r"filesystems=[\w:]*\bflare\b", re.I), "aurora"),
    (re.compile(r"filesystems=[\w:]*\beagle\b", re.I), "polaris"),
    (re.compile(r"/lus/flare/", re.I), "aurora"),
    (re.compile(r"\bmodule\s+load\s+frameworks\b", re.I), "aurora"),
    (re.compile(r"\bsunspot\b", re.I), "sunspot"),
    (re.compile(r"\bperlmutter\b|#SBATCH\s+-C\s+gpu", re.I), "perlmutter"),
    (re.compile(r"\bfrontier\b|\brocm\b", re.I), "frontier"),
    (re.compile(r"\bsophia\b", re.I), "sophia"),
    (re.compile(r"\bcrux\b", re.I), "crux"),
    (re.compile(r"/soft/applications/|PrgEnv-nvhpc|cudatoolkit-standalone", re.I), "polaris"),
]


def infer_system(txt: str) -> tuple[str | None, str]:
    for pat, fixed in SYSTEM_HINTS:
        m = pat.search(txt)
        if not m:
            continue
        if fixed is None:
            return m.group(1).lower(), f"select system={m.group(1)}"
        return fixed, f"matched /{pat.pattern[:34]}/"
    return None, ""


SUCCESS = re.compile(r"JOB DONE|Job completed|=== .*DONE|finished successfully|"
                     r"convergence has been achieved|Final energy|Total wall time|"
                     r"exit status: 0", re.I)
FAILURE = re.compile(r"Traceback \(most recent|command not found|No such file or directory|"
                     r"error while loading shared|CUDA out of memory|"
                     r"=>> PBS: job killed|Segmentation fault|srun: error|MPI_ABORT|"
                     r"%%%%%%%%%%%%%%%%|Error in routine", re.I)


def join_continuations(t: str) -> str:
    """Fold `\\`-continued lines into one.

    Real scripts wrap their launchers: `mpiexec -n 8 --ppn 4 \\` with `torchrun ... train.py`
    on the next line. Reading line-by-line saw only the `mpiexec` fragment, so the binary that
    identifies the job was invisible — which is why 14 ddp_scaling scripts came back
    unidentified despite plainly being PyTorch.
    """
    return re.sub(r"\\\s*\n\s*", " ", t)


def parse_script(p: Path, cat: list[dict]) -> dict:
    txt = join_continuations(p.read_text(errors="replace"))
    pbs = {k: v for k, v in PBS_LINE.findall(txt)}
    sel = pbs.get("-l", "")
    resources = {}
    for k, v in re.findall(r"(\w+)=([\w:.]+)", " ".join(
            m[1] for m in PBS_LINE.findall(txt) if m[0] == "-l")):
        resources[k] = v
    launchers = [l.strip() for l in txt.splitlines() if LAUNCHER.match(l)]
    modules = re.findall(r"^\s*module\s+(load|swap|purge)\s*(.*)$", txt, re.M)
    binaries = re.findall(r"(/[\w./-]+/bin/[\w.-]+|\b[\w.-]+\.x\b)", txt)

    # Where a name appears decides whether it identifies the job. A binary path or a launcher
    # line is evidence; a mention in a comment is not.
    exec_ctx = "\n".join(
        [l for l in txt.splitlines()
         if LAUNCHER.match(l) or re.search(r"/bin/|\.x\b|^\s*module\s+load|=\s*/", l)]).lower()
    app, why = None, ""
    blob = txt.lower()
    for hint, a in BINARY_HINTS:
        if hint in exec_ctx:
            app, why = a, f"binary/launcher '{hint}'"
            break
    if not app:
        for hint, a in BINARY_HINTS:
            if re.search(rf"\b{re.escape(hint)}\b", blob):
                app, why = a, f"mentioned '{hint}' (weak)"
                break
    if not app:
        for c in cat:
            if c["app"] in NOT_APPS:
                continue
            hit = [m for m in c["marks"] if re.search(rf"\b{re.escape(m)}\b", blob)]
            if hit:
                app, why = c["app"], f"catalog marks {sorted(hit)[:3]}"
                break

    ranks = re.search(r"-n\s+\$?\{?(\w+)\}?", " ".join(launchers))
    ppn = re.search(r"--ppn\s+\$?\{?(\w+)\}?", " ".join(launchers))
    system, sys_why = infer_system(txt)
    return {
        "script": str(p.relative_to(RUNS)),
        "system": system,
        "system_evidence": sys_why,
        "scheduler": "Slurm" if "#SBATCH" in txt else "PBS Pro" if pbs else None,
        "has_pbs": bool(pbs),
        "account": pbs.get("-A"),
        "queue": pbs.get("-q"),
        "job_name": pbs.get("-N"),
        "select": resources.get("select"),
        "walltime": resources.get("walltime"),
        "filesystems": resources.get("filesystems"),
        "place": resources.get("place"),
        "modules": [f"{k} {v}".strip() for k, v in modules],
        "launchers": launchers[:6],
        "ranks_expr": ranks.group(1) if ranks else None,
        "ppn_expr": ppn.group(1) if ppn else None,
        "binaries": sorted({b for b in binaries if "/" in b or b.endswith(".x")})[:6],
        "app": app,
        "app_evidence": why,
        # "strong" = named in a launcher or binary path; "weak" = merely mentioned somewhere.
        # Inferring the application from an arbitrary shell script is genuinely unreliable
        # (a PyTorch job may invoke train_x.py inside a `bash -c` block with no torchrun), so
        # consumers that need a trustworthy label must filter on this rather than assume.
        "app_confidence": ("strong" if why.startswith("binary/launcher")
                           else "weak" if why else "none"),
        "kind": "build" if BUILD.search(txt) and not LAUNCHER.search(txt) else "run",
    }


def classify_dir(d: Path, cat: list[dict]) -> dict:
    """Inputs, logs and an outcome for the directory a script lives in."""
    files = [f for f in d.rglob("*") if f.is_file()]
    logs = [f for f in files if f.suffix in {".out", ".err", ".log"}
            or re.search(r"\.[oe]\d+$", f.name)]
    inputs = [f for f in files if f not in logs and f.suffix not in {".sh", ".py"}]
    ok = bad = 0
    for f in logs:
        t = f.read_text(errors="replace")[:200_000]
        ok += bool(SUCCESS.search(t))
        bad += bool(FAILURE.search(t))
    return {"n_files": len(files),
            "inputs": sorted(str(f.relative_to(d)) for f in inputs)[:20],
            "logs": sorted(str(f.relative_to(d)) for f in logs)[:20],
            "logs_with_success": ok, "logs_with_failure": bad,
            # A run counts as ground truth only on positive evidence of completion.
            "status": "success" if ok and not bad else
                      "mixed" if ok and bad else
                      "failed" if bad else "unknown"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--show")
    a = ap.parse_args()
    if not RUNS.exists():
        print(f"no runs at {RUNS} — rsync them first")
        return 1
    cat = catalog_index()

    scripts = []
    for p in sorted(RUNS.rglob("*")):
        if not p.is_file() or p.suffix not in {".sh", ".pbs", ".sbatch"}:
            continue
        txt = p.read_text(errors="replace")
        if not (PBS_LINE.search(txt) or LAUNCHER.search(txt)):
            continue
        rec = parse_script(p, cat)
        rec.update(classify_dir(p.parent, cat))
        rec["top"] = rec["script"].split("/")[0]
        scripts.append(rec)

    if a.show:
        for r in [r for r in scripts if r["top"] == a.show]:
            print(json.dumps(r, indent=1))
        return 0

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.jsonl").write_text("".join(json.dumps(r) + "\n" for r in scripts))
    print(f"{len(scripts)} job scripts indexed -> {OUT / 'index.jsonl'}\n")

    print(f"{'status':<10}{'n':>5}")
    for s, n in Counter(r["status"] for r in scripts).most_common():
        print(f"{s:<10}{n:>5}")

    print(f"\n{'app':<12}{'scripts':>9}{'successful':>12}{'with #PBS':>11}")
    by = defaultdict(lambda: [0, 0, 0])
    for r in scripts:
        k = r["app"] or "(unidentified)"
        by[k][0] += 1
        by[k][1] += r["status"] == "success"
        by[k][2] += r["has_pbs"]
    for k, (n, ok, pbs) in sorted(by.items(), key=lambda kv: -kv[1][1]):
        print(f"{k:<12}{n:>9}{ok:>12}{pbs:>11}")

    print(f"\n{'target system':<16}{'scripts':>9}{'successful':>12}")
    bysys = defaultdict(lambda: [0, 0])
    for r in scripts:
        k = r["system"] or "(unknown)"
        bysys[k][0] += 1
        bysys[k][1] += r["status"] == "success"
    for k, (n, ok) in sorted(bysys.items(), key=lambda kv: -kv[1][0]):
        print(f"{k:<16}{n:>9}{ok:>12}")

    # The number the plan turns on. Keyed on (app, system) as the benchmark is.
    # These are the project's own archived runs and their inputs are taken as correct, so a
    # run counts as ground truth on presence rather than on log evidence. `status` is still
    # recorded per run, for the cases where knowing it later turns out to matter.
    print("\n=== COVERAGE OF THE BENCHMARK ANCHORS (inputs assumed correct) ===")
    succ = {(r["app"], r["system"]) for r in scripts if r["app"] and r["system"]}
    anyrun = succ
    for label, anchors in (("SUBSET (the 10 graded)", SUBSET), ("all 39 ANCHORS", ANCHORS)):
        pairs = [(app, s) for _, app, s in anchors]
        hit = [p for p in pairs if p in succ]
        part = [p for p in pairs if p in anyrun and p not in succ]
        print(f"\n  {label}: {len(hit)}/{len(pairs)} have a successful run")
        if hit:
            print(f"      grounded: {sorted(f'{a}@{s}' for a, s in hit)}")
        if part:
            print(f"      run present, success unconfirmed: "
                  f"{sorted(f'{a}@{s}' for a, s in part)}")
    # App-level match ignores the machine: input-format requirements largely transfer between
    # systems even when queue and module requirements do not.
    succ_apps = {a for a, _ in succ}
    print(f"\n  App-level (ignoring system), successful runs exist for: {sorted(succ_apps)}")
    for label, anchors in (("SUBSET", SUBSET), ("all ANCHORS", ANCHORS)):
        pairs = {app for _, app, _ in anchors}
        print(f"      {label}: {len(pairs & succ_apps)}/{len(pairs)} apps covered "
              f"{sorted(pairs & succ_apps)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
