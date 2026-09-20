#!/usr/bin/env python3
"""Generate realistic ALCF task instances, grounded in the cached documentation.

One generation call per (category, variation) pair, each seeded with a different ALCF doc
page. Output shape deliberately matches results/skills/samples.jsonl so the existing
classifier and labeling scripts consume it with no special-casing.

Everything downstream inherits the quality of these instances, so read some before trusting
any of it:  python skills/hpc_generate_tasks.py --show 12

Usage:
    python skills/hpc_generate_tasks.py --per-variation 5
    python skills/hpc_generate_tasks.py --show 12       # hand-inspect what was generated
"""
from __future__ import annotations
import argparse
import json
import random
import sys
import textwrap
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import judge  # noqa: E402
from skills.hpc_task_spec import SEED_TASKS  # noqa: E402

DOCS = ROOT / "results" / "skills" / "hpc" / "docs"
HPC_DIR = ROOT / "results" / "skills" / "hpc"


def load_doc(name: str) -> str:
    p = DOCS / f"{name}.md"
    return p.read_text() if p.exists() else ""


def out_path(framing: str) -> Path:
    return HPC_DIR / ("instances.jsonl" if framing == "advisory"
                      else f"instances_{framing}.jsonl")


def show(n: int, framing: str) -> int:
    rows = [json.loads(l) for l in out_path(framing).open()]
    rng = random.Random(0)
    for r in rng.sample(rows, min(n, len(rows))):
        print(f"\n\033[1m{r['sample_id']}\033[0m  {r['hpc_task']} — {r['variation']}")
        print(f"  \033[36msource:\033[0m {r['source_doc']}")
        for label, body in (("Q", r["question"]), ("A", r["answer"])):
            wrapped = textwrap.fill(body, width=96, initial_indent=f"  {label}: ",
                                    subsequent_indent="     ")
            print(wrapped)
    print(f"\n{len(rows)} instances total")
    print(f"by task: {dict(Counter(r['hpc_task'] for r in rows))}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-variation", type=int, default=5)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--show", type=int, help="print N generated instances and exit")
    ap.add_argument("--framing", choices=["advisory", "execution"], default="advisory",
                    help="advisory = user asks the help desk; execution = agent must act")
    args = ap.parse_args()

    OUT = out_path(args.framing)
    if args.show:
        return show(args.show, args.framing)

    jobs = []
    for task, spec in SEED_TASKS.items():
        for i, variation in enumerate(spec["variations"]):
            # Rotate through the task's doc pages so variations aren't all grounded in the
            # same text — otherwise the whole category inherits one page's vocabulary.
            doc_name = spec["docs"][i % len(spec["docs"])]
            jobs.append((task, variation, doc_name))

    print(f"[{args.framing}] {len(jobs)} (task, variation) pairs x {args.per_variation} "
          f"= {len(jobs) * args.per_variation} target, {args.workers} workers")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()
    results: list[dict] = []

    def work(job):
        task, variation, doc_name = job
        doc = load_doc(doc_name)
        if not doc:
            return task, variation, doc_name, []
        items = judge.generate_hpc_tasks(task, doc, variation, args.per_variation,
                                         framing=args.framing)
        return task, variation, doc_name, items

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(work, j) for j in jobs]
        for done, fut in enumerate(as_completed(futures), 1):
            task, variation, doc_name, items = fut.result()
            for it in items:
                results.append({"hpc_task": task, "variation": variation,
                                "source_doc": doc_name, **it})
            status = "ok " if items else "EMPTY"
            print(f"  [{done}/{len(jobs)}] {status} {task} — {variation[:52]} ({len(items)})",
                  flush=True)

    # Stable ids assigned after collection, ordered by task so the file reads coherently.
    results.sort(key=lambda r: (r["hpc_task"], r["variation"]))
    with OUT.open("w") as f:
        for i, r in enumerate(results):
            f.write(json.dumps({
                "sample_id": f"hpc{'x' if args.framing == 'execution' else ''}::{i:04d}",
                "benchmark": f"hpc_{args.framing}",
                "framing": args.framing,
                "question": r["question"],
                "answer": r["answer"],
                "original_category": r["hpc_task"],
                "original_difficulty": None,
                "hpc_task": r["hpc_task"],
                "variation": r["variation"],
                "source_doc": r["source_doc"],
                "fundamental_skills": [],
                "human_validated": False,
                "label_confidence": None,
            }, ensure_ascii=False) + "\n")

    per_task = Counter(r["hpc_task"] for r in results)
    print(f"\n{len(results)} instances in {(time.perf_counter() - t0) / 60:.1f} min -> {OUT}")
    for task, n in sorted(per_task.items()):
        print(f"  {n:4d}  {task}")
    empty = [t for t in SEED_TASKS if per_task.get(t, 0) == 0]
    if empty:
        print(f"  NO INSTANCES for: {empty}")
    print(f"\nNext: hand-read a sample before labeling —  "
          f"python skills/hpc_generate_tasks.py --framing {args.framing} --show 12")
    return 0


if __name__ == "__main__":
    sys.exit(main())
