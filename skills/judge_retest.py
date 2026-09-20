#!/usr/bin/env python3
"""Measure the judge's own test-retest noise on a frozen corpus.

This gates every later phase, and it has never been run. The v2/v4/v6 grade rows for unchanged
subtasks were carried forward deliberately (to hold one variable at a time while prompts
changed), which means the judge has never been asked the same question twice. `judge_trinity`
sets no temperature — Opus 5 rejects it as deprecated — so it samples at a provider default.

If the judge's own spread is comparable to the effects we are trying to measure, then every
rubric comparison needs replicates and per-dimension medians, and every downstream phase costs
three times as much. Cheaper to find out now.

Decision rule, fixed BEFORE running so the result cannot be rationalised:

    pass-rate spread <= 1 point   k=1 is fine; judge once and move on
    spread 2-4 points            k=3 replicates + per-dimension median everywhere
    spread > 4 points            the judge is noisier than the effects under study;
                                 fix determinism before any rubric work

Usage:
    python skills/judge_retest.py --corpus v6 --runs 3
    python skills/judge_retest.py --report
"""
from __future__ import annotations
import argparse
import json
import statistics
import sys
import threading
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import judge  # noqa: E402
from skills.trinity_generate import grading_key, physical_system  # noqa: E402
from skills.trinity_task_spec import SUBTASKS  # noqa: E402

TRIN = ROOT / "results" / "skills" / "trinity"


def load(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.open()] if p.exists() else []


def key(r: dict) -> tuple:
    return (r["model"], r["subtask"], r["app"], r["system"])


def is_pass(g: dict) -> bool:
    return (g.get("correctness") == 2 and g.get("completeness") == 2
            and g.get("usability") == 2 and not g.get("fatal_error"))


def out_path(corpus: str, run: int) -> Path:
    return TRIN / f"retest_{corpus}__{judge.TRINITY_JUDGE_MODEL}__r0__run{run}.jsonl"


def run_once(corpus: str, run: int, workers: int) -> None:
    """One full pass over the frozen corpus with the CURRENT judge config, unchanged."""
    samples = {(s["subtask"], s["app"], s["system"]): s
               for s in load(TRIN / f"samples_{corpus}.jsonl")}
    answers = [a for a in load(TRIN / f"answers_{corpus}.jsonl")
               if a.get("answer") and not a.get("error")]
    dest = out_path(corpus, run)
    have = {key(r) for r in load(dest)}
    todo = [a for a in answers if key(a) not in have]
    if not todo:
        print(f"  run {run}: complete ({len(have)} rows)")
        return
    print(f"  run {run}: {len(todo)} to judge -> {dest.name}", flush=True)

    lock, buf, done = threading.Lock(), [], [0]

    def one(a):
        s = samples[(a["subtask"], a["app"], a["system"])]
        spec = SUBTASKS[a["subtask"]]
        gk = {**grading_key(a["system"], a["app"], spec["key_fields"]),
              "physical_system": physical_system(a["app"]),
              "reference": s.get("reference", "")}
        v = judge.judge_trinity(a["subtask"], spec["goal"], a["system"],
                                gk.get("scheduler", ""), s["prompt"], a["answer"], gk,
                                grading_note=spec.get("grading_note", ""))
        return a, v

    with ThreadPoolExecutor(max_workers=workers) as pool:
        for fut in as_completed([pool.submit(one, a) for a in todo]):
            a, v = fut.result()
            with lock:
                done[0] += 1
                if not v.get("judge_failed"):
                    buf.append({**{k: a[k] for k in ("model", "subtask", "app", "system")},
                                "judge_run": run, **v})
                if len(buf) >= 5:
                    with dest.open("a") as f:
                        for r in buf:
                            f.write(json.dumps(r) + "\n")
                    buf.clear()
                if done[0] % 25 == 0:
                    print(f"     {done[0]}/{len(todo)}", flush=True)
    with dest.open("a") as f:
        for r in buf:
            f.write(json.dumps(r) + "\n")


def report(corpus: str) -> int:
    runs = sorted(TRIN.glob(f"retest_{corpus}__*__run*.jsonl"))
    if len(runs) < 2:
        print("need at least 2 completed runs")
        return 1
    by_run = {}
    for p in runs:
        n = int(p.stem.split("run")[-1])
        by_run[n] = {key(r): r for r in load(p)}
    common = set.intersection(*(set(d) for d in by_run.values()))
    print(f"corpus {corpus}: {len(runs)} runs, {len(common)} rows judged in all of them\n")

    # pass rate per run — the headline number the decision rule is written against
    rates = []
    for n in sorted(by_run):
        k = sum(1 for key_ in common if is_pass(by_run[n][key_]))
        rates.append(100 * k / len(common))
        print(f"  run {n}: {k}/{len(common)} pass = {rates[-1]:.1f}%")
    spread = max(rates) - min(rates)
    print(f"\n  pass-rate spread: {spread:.1f} points "
          f"(sd {statistics.pstdev(rates):.2f})")

    # how often the full verdict is identical across every run
    exact = sum(1 for key_ in common
                if len({(by_run[n][key_]["correctness"], by_run[n][key_]["completeness"],
                         by_run[n][key_]["usability"], bool(by_run[n][key_]["fatal_error"]))
                        for n in by_run}) == 1)
    print(f"  identical 4-tuple in every run: {exact}/{len(common)} "
          f"({100 * exact / len(common):.0f}%)")

    print(f"\n  {'dimension':<14}{'unstable rows':>15}{'max spread':>12}")
    for dim in ("correctness", "completeness", "usability"):
        vals = [[by_run[n][key_][dim] for n in by_run] for key_ in common]
        unstable = sum(1 for v in vals if len(set(v)) > 1)
        print(f"  {dim:<14}{f'{unstable}/{len(common)}':>15}"
              f"{max(max(v) - min(v) for v in vals):>12}")
    flips = sum(1 for key_ in common if len({is_pass(by_run[n][key_]) for n in by_run}) > 1)
    print(f"  {'is_pass':<14}{f'{flips}/{len(common)}':>15}")

    by_sub = defaultdict(lambda: [0, 0])
    for key_ in common:
        s = key_[1]
        by_sub[s][1] += 1
        if len({is_pass(by_run[n][key_]) for n in by_run}) > 1:
            by_sub[s][0] += 1
    print(f"\n  pass/fail flips by subtask:")
    for s, (f_, n_) in sorted(by_sub.items(), key=lambda kv: -kv[1][0]):
        print(f"    {s:<22}{f_:>3}/{n_}")

    verdict = ("k=1 is fine — judge once" if spread <= 1 else
               "k=3 replicates + per-dimension median needed everywhere" if spread <= 4 else
               "STOP — the judge is noisier than the effects under study; fix determinism")
    print(f"\n  DECISION (rule fixed before running): {verdict}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="v6")
    ap.add_argument("--runs", type=int, default=0)
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    if a.runs:
        print(f"judge test-retest: {judge.TRINITY_JUDGE_MODEL}, corpus {a.corpus}, "
              f"{a.runs} runs, config UNCHANGED")
        for r in range(1, a.runs + 1):
            run_once(a.corpus, r, a.workers)
    if a.report or not a.runs:
        return report(a.corpus)
    return report(a.corpus)


if __name__ == "__main__":
    sys.exit(main())
