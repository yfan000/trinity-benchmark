#!/usr/bin/env python3
"""Derive requirements from what the real runs actually did.

The catalog says what a file set *should* contain. The runs show what a working job *did*
contain, and the difference is where the interesting requirements live — `-l filesystems=`
and `place=scatter` were hand-written into skills/trinity_site.py from documentation; this is
how they would have been discovered instead.

Three kinds of output, and the third is the one that cannot be obtained any other way:

  ALWAYS   present in every run of an app -> candidate `must_have`
  USUALLY  present in most               -> candidate, needs a human to judge
  VARIES   differs across runs that all worked -> candidate `free_choice`

That last one matters because `free_choice` is otherwise guesswork. If five successful QE runs
each pick a different `ecutwfc`, then `ecutwfc` is not something a judge may deduct for. The
current Resource-selection grading note asserts "there is no single correct allocation" as
prose; mining turns that kind of claim into evidence with a support count behind it.

Nothing here is authoritative on its own. Every mined requirement carries its support count
and needs sign-off before entering the library: a convention in one team's runs is not
automatically a correctness rule.

Usage:
    python skills/runs_mine.py
    python skills/runs_mine.py --app qe
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

RUNS = ROOT.parent / "trinity_jobs" / "polaris"
IDX = ROOT / "results" / "skills" / "trinity" / "runs" / "index.jsonl"
OUT = ROOT / "results" / "skills" / "trinity" / "runs" / "mined.json"

# Directive families, normalised so `-l select=4:system=polaris` and `-l select=1:...` count
# as the same requirement ("a select statement is present") while their VALUES are mined
# separately as a range.
DIRECTIVE = re.compile(r"^\s*#PBS\s+(-\w+)\s+(.*?)\s*$", re.M)
RESOURCE = re.compile(r"(\w+)=([\w:.@+-]+)")


def facts(script_path: Path) -> dict:
    """Everything mineable from one job script."""
    txt = script_path.read_text(errors="replace")
    d = defaultdict(list)
    for flag, val in DIRECTIVE.findall(txt):
        if flag == "-l":
            for k, v in RESOURCE.findall(val):
                d[f"-l {k}"].append(v)
        else:
            d[flag].append(val)
    mods = re.findall(r"^\s*module\s+(?:load|swap)\s+([\w/.@+-]+)", txt, re.M)
    launch = re.findall(r"^\s*((?:mpiexec|srun|torchrun)\s.*)$", txt, re.M)
    flags = set()
    for l in launch:
        flags |= set(re.findall(r"(--?[\w-]+)", l))
    return {"directives": dict(d), "modules": mods, "launch_flags": sorted(flags),
            "n_launch": len(launch),
            "module_purge": bool(re.search(r"^\s*module\s+purge", txt, re.M)),
            "cd_workdir": bool(re.search(r"cd\s+\$\{?PBS_O_WORKDIR", txt)),
            "self_resolve_workdir": bool(re.search(r"dirname\s+\$0", txt)),
            "mkdir": bool(re.search(r"^\s*mkdir\s+-p", txt, re.M)),
            "set_e": bool(re.search(r"^\s*set\s+-\w*e", txt, re.M))}


def mine(app: str, recs: list[dict]) -> dict:
    n = len(recs)
    allf = [facts(RUNS / r["script"]) for r in recs]

    # directive presence
    pres = Counter()
    for f in allf:
        pres.update(f["directives"].keys())
    always = sorted(k for k, c in pres.items() if c == n)
    usually = sorted(k for k, c in pres.items() if n > c >= max(2, n * 0.6))
    sometimes = sorted(k for k, c in pres.items() if c < max(2, n * 0.6))

    # directive VALUES — what varies is what a judge must not deduct for
    vals = defaultdict(Counter)
    for f in allf:
        for k, vv in f["directives"].items():
            for v in vv:
                vals[k][v] += 1
    varies = {k: dict(c) for k, c in vals.items() if len(c) > 1}
    fixed = {k: next(iter(c)) for k, c in vals.items() if len(c) == 1 and pres[k] == n}

    # shell habits
    habits = {k: sum(f[k] for f in allf) for k in
              ("module_purge", "cd_workdir", "self_resolve_workdir", "mkdir", "set_e")}

    mods = Counter()
    for f in allf:
        mods.update(set(f["modules"]))
    lflags = Counter()
    for f in allf:
        lflags.update(f["launch_flags"])

    return {
        "app": app, "n_runs": n,
        "directives_always": always,
        "directives_usually": usually,
        "directives_sometimes": sometimes,
        "values_fixed": fixed,
        "values_vary": varies,
        "modules_always": sorted(m for m, c in mods.items() if c == n),
        "modules_sometimes": sorted(m for m, c in mods.items() if c < n),
        "launch_flags_always": sorted(f for f, c in lflags.items() if c == n),
        "launch_flags_sometimes": sorted(f for f, c in lflags.items() if c < n),
        "habits": habits,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--app")
    ap.add_argument("--min-runs", type=int, default=2)
    a = ap.parse_args()
    idx = [json.loads(l) for l in IDX.open()]
    # PBS-bearing scripts only: a script with no directives says nothing about what a job
    # submission requires, and half the archive is run inside an existing allocation.
    idx = [r for r in idx if r["app"] and r["has_pbs"]]
    by = defaultdict(list)
    for r in idx:
        by[r["app"]].append(r)

    out = {}
    for app, recs in sorted(by.items(), key=lambda kv: -len(kv[1])):
        if len(recs) < a.min_runs or (a.app and app != a.app):
            continue
        out[app] = mine(app, recs)

    OUT.write_text(json.dumps(out, indent=1))
    print(f"mined {len(out)} apps -> {OUT}\n")

    for app, m in out.items():
        print(f"=== {app}  ({m['n_runs']} PBS scripts) ===")
        print(f"  ALWAYS present : {', '.join(m['directives_always']) or '(none)'}")
        if m["directives_usually"]:
            print(f"  USUALLY        : {', '.join(m['directives_usually'])}")
        if m["values_fixed"]:
            print(f"  FIXED values   : " +
                  ", ".join(f"{k}={v}" for k, v in sorted(m["values_fixed"].items())))
        if m["values_vary"]:
            print("  VARIES (candidate free_choice):")
            for k, c in sorted(m["values_vary"].items()):
                top = ", ".join(f"{v}x{n}" for v, n in
                                sorted(c.items(), key=lambda kv: -kv[1])[:5])
                print(f"      {k:<20} {len(c)} distinct: {top}")
        if m["modules_always"]:
            print(f"  modules ALWAYS : {', '.join(m['modules_always'])}")
        if m["launch_flags_always"]:
            print(f"  launch flags   : {', '.join(m['launch_flags_always'])}")
        h = m["habits"]
        print(f"  habits         : " +
              ", ".join(f"{k} {v}/{m['n_runs']}" for k, v in h.items() if v))
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
