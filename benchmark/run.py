#!/usr/bin/env python3
"""Answer + grade the 40-sample v2 Trinity benchmark on the four on-prem models.

v2 is the same four subtasks, regenerated with every prompting fix that was validated on a
10-sample preview first:

    Software selection  installed-software catalog supplied            22% -> 85%
    Input preparation   prior-step context, verified upstream deck,
                        no-fabrication and form-only rules              2% -> 33%
    Resource selection  legality check, ranks-from-defaults, no
                        invented timings, closing restatement,
                        plus a grading key that stops treating the
                        one-node smoke-test defaults as the answer      5% -> 23%
    Batch job creation  site conventions, a real worked script per
                        scheduler family, and the account               0% -> 53%

Answers and grades are written incrementally so an interrupted run resumes rather than
restarts, and a failed call is never persisted as an answer — an errored row scoring zero
was what made an earlier run's scoreboard wrong.

Usage:
    python skills/trinity_run_v2.py --answer
    python skills/trinity_run_v2.py --grade
    python skills/trinity_run_v2.py --report
"""
from __future__ import annotations
import argparse, json, os, sys, threading, time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from benchmark import prompt as judge
from benchmark._run_base import ask, MODELS  # noqa: E402
from benchmark.generate import grading_key, physical_system  # noqa: E402
from benchmark.task_spec import SUBTASKS  # noqa: E402

TRIN = ROOT / "data" / "corpus" / "v8"
VER = os.environ.get("TRINITY_VER", "v2")
SAMPLES = TRIN / f"samples_{VER}.jsonl"
ANSWERS = TRIN / f"answers_{VER}.jsonl"
GRADES = TRIN / f"grades_{VER}.jsonl"
# Minerva 504s under load; three earlier runs degraded from 25/min to 3/min on it.
WORKERS = {"nemotron-3-ultra": 2}
DEFAULT_WORKERS = 5
TARGETS = ["gpt-oss-120b", "gemma-4-31b", "llama-3.1-8b", "nemotron-3-ultra"]


def load(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.open()] if path.exists() else []


def append(path: Path, rows: list[dict]) -> None:
    with path.open("a") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


def key(r: dict) -> tuple:
    return (r["model"], r["subtask"], r["app"], r["system"])


def phase_answer(models: list[str]) -> None:
    samples = load(SAMPLES)
    have = {key(r) for r in load(ANSWERS) if r.get("answer") and not r.get("error")}
    lock, t0 = threading.Lock(), time.perf_counter()

    for m in models:
        jobs = [s for s in samples
                if (m, s["subtask"], s["app"], s["system"]) not in have]
        if not jobs:
            print(f"{m:18} complete")
            continue
        w = WORKERS.get(m, DEFAULT_WORKERS)
        print(f"{m:18} {len(jobs)} to answer, {w} workers", flush=True)
        done, buf = 0, []

        def one(s):
            a, e = ask(m, s["prompt"])
            return {"model": m, "subtask": s["subtask"], "app": s["app"],
                    "system": s["system"], "domain": s["domain"],
                    "answer": a, "error": e}

        with ThreadPoolExecutor(max_workers=w) as pool:
            for fut in as_completed([pool.submit(one, s) for s in jobs]):
                r = fut.result()
                with lock:
                    done += 1
                    # Only a real answer is persisted: an errored row written as "done"
                    # silently enters the scoreboard as a zero.
                    if r["answer"] and not r["error"]:
                        buf.append(r)
                    else:
                        print(f"   ! {r['subtask'][:14]:14} {r['app']:10} "
                              f"{str(r['error'])[:60]}", flush=True)
                    if len(buf) >= 5:
                        append(ANSWERS, buf); buf = []
                    if done % 10 == 0:
                        print(f"   {done}/{len(jobs)}  {time.perf_counter()-t0:.0f}s", flush=True)
        append(ANSWERS, buf)
    n = len([r for r in load(ANSWERS) if r.get("answer")])
    print(f"\n{n} answers on file -> {ANSWERS}")


def phase_grade(workers: int) -> None:
    samples = {(s["subtask"], s["app"], s["system"]): s for s in load(SAMPLES)}
    answers = [r for r in load(ANSWERS) if r.get("answer") and not r.get("error")]
    have = {key(r) for r in load(GRADES)}
    todo = [r for r in answers if key(r) not in have]
    print(f"{len(todo)} to grade with {judge.TRINITY_JUDGE_MODEL}, {workers} workers")
    lock, buf, done = threading.Lock(), [], 0

    def one(r):
        s = samples[(r["subtask"], r["app"], r["system"])]
        spec = SUBTASKS[r["subtask"]]
        gk = {**grading_key(r["system"], r["app"], spec["key_fields"]),
              "physical_system": physical_system(r["app"]),
              "reference": s.get("reference", "")}
        v = judge.judge_trinity(r["subtask"], spec["goal"], r["system"],
                                gk.get("scheduler", ""), s["prompt"], r["answer"], gk,
                                grading_note=spec.get("grading_note", ""))
        return r, v

    with ThreadPoolExecutor(max_workers=workers) as pool:
        for fut in as_completed([pool.submit(one, r) for r in todo]):
            r, v = fut.result()
            with lock:
                done += 1
                # A judge failure is not a model failure; leave it unwritten and retry.
                if not v.get("judge_failed"):
                    buf.append({**r, **v})
                if len(buf) >= 5:
                    append(GRADES, buf); buf = []
                if done % 20 == 0:
                    print(f"   {done}/{len(todo)}", flush=True)
    append(GRADES, buf)
    print(f"{len(load(GRADES))} grades on file -> {GRADES}")


def is_core(g: dict) -> bool:
    """The substance is right, whatever else is wrong."""
    return g.get("correctness") == 2


def is_pass(g: dict) -> bool:
    """Every dimension perfect and nothing fatal."""
    return (g.get("correctness") == 2 and g.get("completeness") == 2
            and g.get("usability") == 2 and not g.get("fatal_error"))


def phase_report() -> None:
    grades = load(GRADES)
    subs = list(SUBTASKS)
    for label, fn in (("ANSWER CORRECT (correctness == 2)", is_core),
                      ("FULLY CORRECT (all three == 2, no fatal error)", is_pass)):
        print(f"\n{label}")
        print(f"{'model':<18}" + "".join(f"{s[:13]:>15}" for s in subs) + f"{'overall':>11}")
        for m in TARGETS:
            rows = [g for g in grades if g["model"] == m]
            if not rows:
                continue
            cells = ""
            for s in subs:
                r = [g for g in rows if g["subtask"] == s]
                cells += f"{(f'{sum(map(fn,r))}/{len(r)}' if r else '-'):>15}"
            print(f"{m:<18}{cells}{f'{sum(map(fn,rows))}/{len(rows)}':>11}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--answer", action="store_true")
    ap.add_argument("--grade", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--models", default=",".join(TARGETS))
    ap.add_argument("--workers", type=int, default=5)
    a = ap.parse_args()
    if a.answer:
        phase_answer([m for m in a.models.split(",") if m in MODELS])
    if a.grade:
        phase_grade(a.workers)
    if a.report or not (a.answer or a.grade):
        phase_report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
