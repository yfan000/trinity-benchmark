#!/usr/bin/env python3
"""Blind re-categorization of every HPC instance, as a check on the task axis.

Each instance carries an hpc_task label only because the generator was asked for that
category — it is an input, not a measurement. If the generator drifted, the mapping's rows
are contaminated and nothing downstream would notice.

This shows each instance's text alone, with no category attached, and asks which of the 8
tasks it belongs to. Agreement with the asked-for label is the check. Disagreement is not
automatically an error: real HPC tickets belong to several categories at once ("my job won't
run" is submission *and* diagnosis), so a soft axis is expected — the point is to measure how
soft, and to let hpc_build_mapping.py recompute on the agreed subset as a robustness test.

Usage:
    python skills/hpc_recheck_tasks.py
"""
from __future__ import annotations
import json
import sys
import threading
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import judge  # noqa: E402
from skills.hpc_task_spec import SEED_TASKS  # noqa: E402

HPC = ROOT / "results" / "skills" / "hpc"
SOURCES = {"advisory": HPC / "labels.jsonl", "execution": HPC / "labels_execution.jsonl"}
OUT = HPC / "task_recheck.jsonl"
TASKS = sorted(SEED_TASKS)

PROMPT = """Here is a request handled by an HPC facility's user-support team at Argonne.

Which ONE of these categories best describes it?
{cats}

Request:
{q}

Answer with ONLY the category name, exactly as written above."""


def classify(text: str) -> str:
    try:
        m = judge._get_client().messages.create(
            model=judge.JUDGE_MODEL, max_tokens=40, temperature=0,
            messages=[{"role": "user", "content": PROMPT.format(
                cats="\n".join(f"- {t}" for t in TASKS), q=text[:2500])}])
        pred = m.content[0].text.strip().strip('."')
        return next((t for t in TASKS if t.lower() == pred.lower()), f"?{pred[:30]}")
    except Exception as e:
        return f"!{type(e).__name__}"


def main() -> int:
    rows = []
    for framing, path in SOURCES.items():
        if path.exists():
            rows += [{**json.loads(l), "framing": framing} for l in path.open()]

    done = {}
    if OUT.exists():
        done = {json.loads(l)["sample_id"]: json.loads(l) for l in OUT.open()}
    todo = [r for r in rows if r["sample_id"] not in done]
    print(f"{len(rows)} instances, {len(todo)} to re-check against {len(TASKS)} categories")

    lock, t0, n = threading.Lock(), time.perf_counter(), 0
    with OUT.open("a") as f, ThreadPoolExecutor(max_workers=8) as pool:
        futs = {pool.submit(classify, r["question"]): r for r in todo}
        for fut in as_completed(futs):
            r = futs[fut]
            rec = {"sample_id": r["sample_id"], "framing": r["framing"],
                   "asked_for": r["hpc_task"], "blind": fut.result()}
            with lock:
                f.write(json.dumps(rec) + "\n"); f.flush(); n += 1
                if n % 60 == 0:
                    print(f"  {n}/{len(todo)}", flush=True)
    if todo:
        print(f"  done in {(time.perf_counter() - t0) / 60:.1f} min")

    recs = [json.loads(l) for l in OUT.open()]
    per = defaultdict(lambda: [0, 0])
    flow = Counter()
    for r in recs:
        per[r["asked_for"]][1] += 1
        if r["asked_for"] == r["blind"]:
            per[r["asked_for"]][0] += 1
        else:
            flow[(r["asked_for"], r["blind"])] += 1
    agree = sum(v[0] for v in per.values())
    print(f"\nblind agreement: {agree}/{len(recs)} = {agree / len(recs):.0%}\n")
    print(f"{'asked-for task':<28}{'agree':>10}")
    for t in TASKS:
        ok, tot = per[t]
        if tot:
            flag = "   <-- soft" if ok / tot < 0.6 else ""
            print(f"  {t:<26}{ok:>4}/{tot:<4} {ok/tot:>4.0%}{flag}")
    print("\nmost common re-assignments:")
    for (a, b), c in flow.most_common(8):
        print(f"  {c:>3}  {a}  ->  {b}")
    print(f"\n-> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
