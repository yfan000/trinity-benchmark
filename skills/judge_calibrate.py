#!/usr/bin/env python3
"""Calibrate the judge against runs that actually executed. Free, objective, no human time.

Everything measured so far is PRECISION — the same answer getting the same verdict. r2 cut
replicate instability from 33/159 to 22/159, but the pass rate did not move and McNemar said
p=1.0, so nothing yet shows the new pipeline is more ACCURATE. Precision without accuracy is a
thermometer that reliably reads the wrong temperature.

Real runs settle that, because a script that ran IS a correct answer:

  POSITIVE CONTROLS  feed a real job script to the judge as if a model wrote it. It must come
                     back clean. Anything it marks down is a false positive — the judge (or a
                     requirement) is wrong, not the script.

  NEGATIVE CONTROLS  mutate that same script in a way a human can verify is broken — a queue
                     whose limits the request violates, a deleted mandatory directive, the
                     wrong scheduler's dialect. The judge must catch it, and should cite the
                     matching requirement id.

Together those give precision AND recall against ground truth, with no labelling. That is why
this gates the human review: 40 reviewer decisions are too scarce to spend confirming that
correct answers are correct.

A caveat this script cannot fix: the archive is Polaris-only and PBS-only, so the Slurm half
of the dialect rule gets no positive control here.

Usage:
    python skills/judge_calibrate.py --judge gpt56terra --rubric r2 --limit 12
"""
from __future__ import annotations
import argparse
import json
import random
import re
import sys
import threading
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from skills.judge_client import JudgeError  # noqa: E402
from skills.trinity_judge import judge_one  # noqa: E402

RUNS = ROOT.parent / "trinity_jobs" / "polaris"
TRIN = ROOT / "results" / "skills" / "trinity"
IDX = TRIN / "runs" / "index.jsonl"
OUT = TRIN / "calibration.json"


# ---------------------------------------------------------------------------------------
# Mutations. Each must be obviously wrong to a human, and each names the requirement that
# SHOULD catch it — so a miss is attributable to a specific rule rather than to the judge
# in general.
# ---------------------------------------------------------------------------------------
def mut_drop_filesystems(t: str) -> str | None:
    out = re.sub(r"(?m)^\s*#PBS\s+-l\s+filesystems=.*\n", "", t)
    return out if out != t else None


def mut_drop_walltime(t: str) -> str | None:
    out = re.sub(r"(?m)^\s*#PBS\s+-l\s+walltime=.*\n", "", t)
    return out if out != t else None


def mut_drop_queue(t: str) -> str | None:
    out = re.sub(r"(?m)^\s*#PBS\s+-q\s+.*\n", "", t)
    return out if out != t else None


def mut_wrong_dialect(t: str) -> str | None:
    if "#PBS" not in t:
        return None
    # swap the whole directive block to Slurm on a PBS system
    out = re.sub(r"(?m)^\s*#PBS\s+-N\s+", "#SBATCH --job-name=", t)
    out = re.sub(r"(?m)^\s*#PBS\s+-q\s+", "#SBATCH --qos=", out)
    out = re.sub(r"(?m)^\s*#PBS\s+-A\s+", "#SBATCH --account=", out)
    return out if "#SBATCH" in out else None


def mut_nonexistent_queue(t: str) -> str | None:
    out = re.sub(r"(?m)^(\s*#PBS\s+-q\s+)\S+", r"\1turbo-fast", t)
    return out if out != t else None


def mut_directive_comment(t: str) -> str | None:
    m = re.search(r"(?m)^(\s*#PBS\s+-l\s+walltime=\S+)\s*$", t)
    return t[:m.end()] + "   # 40 minutes" + t[m.end():] if m else None


def mut_shell_var_in_directive(t: str) -> str | None:
    m = re.search(r"(?m)^(\s*#PBS\s+-N\s+)(\S+)\s*$", t)
    if not m:
        return None
    return t[:m.start()] + f"#PBS -o ${{WORK}}/out.log\n" + t[m.start():]


MUTATIONS = [
    ("drop_filesystems", mut_drop_filesystems, "BATCH.common.filesystems_declared"),
    ("drop_walltime", mut_drop_walltime, "BATCH.common.walltime_declared"),
    ("drop_queue", mut_drop_queue, "BATCH.common.queue_declared"),
    ("wrong_dialect", mut_wrong_dialect, "BATCH.common.correct_dialect"),
    ("nonexistent_queue", mut_nonexistent_queue, "RES.common.queue_exists"),
    ("directive_comment", mut_directive_comment, "BATCH.common.no_directive_comments"),
    ("shell_var_in_directive", mut_shell_var_in_directive,
     "BATCH.common.no_shell_vars_in_directives"),
]


def as_answer(script: str) -> str:
    """Present a real script the way a model would have — fenced, with a line of prose."""
    return ("Here is the batch script for this job.\n\n```bash\n" + script.strip() + "\n```\n")


def valid_control(r: dict) -> tuple[bool, str]:
    """Is this script usable as a positive control?

    A control only tests the JUDGE if the question put to the judge is the right one. Two
    classes of sample broke that in the first run, and both looked like judge false positives:

      - a MISLABELLED script. csci394_gpu_p1/pbs_run.sh was labelled alphafold because
        alphafold.yaml lists "python" among its keywords. The judge correctly reported that a
        CUDA course assignment does not invoke AlphaFold; the sample was wrong, not the judge.
      - a BUILD script. build_gromacs/run.sh compiles GROMACS. It legitimately has no launcher
        and passes no input files, so "did it launch the application correctly?" has no right
        answer.

    So require a strong label, a run rather than a build, and the app name actually present in
    the script text.
    """
    if r.get("kind") == "build":
        return False, "build script, not a run"
    if r.get("app_confidence") != "strong":
        return False, f"app label is {r.get('app_confidence')}"
    txt = (RUNS / r["script"]).read_text(errors="replace").lower()
    if r["app"].lower() not in txt:
        return False, f"{r['app']} does not appear in the script"
    return True, "ok"


CONTROL_SET = ROOT / "skills" / "judging" / "control_set.yaml"


def pick_scripts(limit: int, seed: int = 7) -> list[dict]:
    """Hand-picked controls, read individually. See control_set.yaml for why each qualifies.

    Heuristic selection was tried twice and admitted invalid samples both times — a
    mislabelled course assignment, then a verification wrapper — each of which I misreported
    as a judge false positive. The set is explicit now.
    """
    import yaml
    if CONTROL_SET.exists():
        doc = yaml.safe_load(CONTROL_SET.read_text()) or {}
        picked = []
        for c in (doc.get("controls") or [])[:limit]:
            if not (RUNS / c["script"]).exists():
                print(f"   ! missing {c['script']}")
                continue
            picked.append({"script": c["script"], "app": c["app"], "system": c["system"],
                           "kind": "run", "app_confidence": "hand",
                           "expected": set(c.get("expected_violations") or [])})
        print(f"{len(picked)} hand-picked controls from {CONTROL_SET.name}")
        return picked
    idx = [json.loads(l) for l in IDX.open()]
    cand = [r for r in idx if r.get("app") and r.get("has_pbs") and r.get("system")]
    ok, rejected = [], Counter()
    for r in cand:
        good, why = valid_control(r)
        (ok.append(r) if good else rejected.update([why.split(" ")[0]]))
    print(f"{len(cand)} candidates -> {len(ok)} usable as controls; "
          f"rejected: {dict(rejected)}")
    random.Random(seed).shuffle(ok)
    seen, out = set(), []
    for r in ok:                       # spread across applications
        if r["app"] in seen and len(seen) < 6:
            continue
        seen.add(r["app"])
        out.append(r)
        if len(out) >= limit:
            break
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--judge", default="gpt56terra")
    ap.add_argument("--rubric", default="r2")
    ap.add_argument("--limit", type=int, default=12)
    ap.add_argument("--workers", type=int, default=5)
    a = ap.parse_args()

    scripts = pick_scripts(a.limit)
    print(f"{len(scripts)} real scripts: "
          f"{dict(Counter(s['app'] for s in scripts))}\n")

    jobs = []
    for r in scripts:
        txt = (RUNS / r["script"]).read_text(errors="replace")
        jobs.append(("positive", r, None, txt, None))
        for name, fn, expect in MUTATIONS:
            m = fn(txt)
            if m:
                jobs.append(("negative", r, name, m, expect))
    print(f"{sum(1 for j in jobs if j[0]=='positive')} positive controls, "
          f"{sum(1 for j in jobs if j[0]=='negative')} negative controls\n")

    lock, done, res = threading.Lock(), [0], []

    def one(job):
        kind, r, name, text, expect = job
        sample = {"subtask": "Batch job creation", "app": r["app"], "system": r["system"],
                  "prompt": f"Write the batch script to run {r['app']} on {r['system']}.\n"
                            f"Output: the complete batch script.",
                  "reference": ""}
        try:
            v = judge_one(sample, as_answer(text), a.judge, a.rubric)
        except JudgeError as e:
            return {"kind": kind, "app": r["app"], "mutation": name, "error": str(e)}
        # Real archived scripts legitimately target reservations; a generated script should
        # not. That makes them imperfect controls for this one rule, so it is exempted here
        # rather than counted as a judge error.
        # Reservations: real runs use them correctly, generated scripts must not.
        # `expected`: firings a human reviewed and confirmed correct for this script.
        EXEMPT = {"RES.common.no_reservation_queue"} | set(r.get("expected") or ())
        viol = [k for k, x in v["requirements"].items()
                if x.get("verdict") == "violated" and k not in EXEMPT]
        with lock:
            done[0] += 1
            if done[0] % 10 == 0:
                print(f"   {done[0]}/{len(jobs)}", flush=True)
        return {"kind": kind, "app": r["app"], "script": r["script"], "mutation": name,
                "expect": expect, "violated": viol, "caught": expect in viol if expect else None,
                "clean": not viol, "scores": {k: v[k] for k in
                                              ("correctness", "completeness", "usability",
                                               "fatal_error")}}

    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        for fut in as_completed([pool.submit(one, j) for j in jobs]):
            res.append(fut.result())
    OUT.write_text(json.dumps(res, indent=1))

    pos = [r for r in res if r["kind"] == "positive" and "error" not in r]
    neg = [r for r in res if r["kind"] == "negative" and "error" not in r]
    print(f"\n=== POSITIVE CONTROLS — a real script must come back clean ===")
    clean = sum(1 for r in pos if r["clean"])
    print(f"  {clean}/{len(pos)} clean   "
          f"({'PASS' if clean == len(pos) else 'FALSE POSITIVES — see below'})")
    fp = Counter()
    for r in pos:
        for v in r["violated"]:
            fp[v] += 1
    for rid, n in fp.most_common():
        print(f"     {n:>3}  falsely flagged: {rid}")

    print(f"\n=== NEGATIVE CONTROLS — each break must be caught ===")
    by = defaultdict(lambda: [0, 0])
    for r in neg:
        by[r["mutation"]][1] += 1
        by[r["mutation"]][0] += bool(r["caught"])
    print(f"  {'mutation':<26}{'caught':>8}{'of':>5}  expected requirement")
    for m, (c, n) in sorted(by.items(), key=lambda kv: kv[1][0] / max(kv[1][1], 1)):
        exp = next(e for nm, _, e in MUTATIONS if nm == m)
        print(f"  {m:<26}{c:>8}{n:>5}  {exp}")
    tot_c = sum(v[0] for v in by.values())
    tot_n = sum(v[1] for v in by.values())
    print(f"\n  recall {tot_c}/{tot_n} = {tot_c/max(tot_n,1):.0%}")
    errs = [r for r in res if "error" in r]
    if errs:
        print(f"\n  {len(errs)} judge failures (not counted)")
    print(f"\n-> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
