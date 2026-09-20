#!/usr/bin/env python3
"""Phase 3 — label every sample against the locked taxonomy.

~3,600 items. Sequential calls would take hours, so this runs a bounded thread pool and
appends each result as it lands: interrupting and re-running resumes from what's on disk
rather than re-paying for it.

Run this only after compute_agreement.py clears its threshold — labeling the whole corpus
against a taxonomy that hasn't been validated just produces a lot of labels nobody trusts.

Usage:
    python skills/label_full_corpus.py --workers 8
    python skills/label_full_corpus.py --limit 50        # small trial first
    python skills/label_full_corpus.py --stratified 250  # just the validation subset

--stratified draws the same benchmark-balanced subset build_validation_worksheet.py will
draw, so the validation worksheet compares human labels against *fixed-taxonomy* labels
rather than the open-vocabulary discovery output.
"""
from __future__ import annotations
import argparse
import json
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import judge  # noqa: E402
from skills.discovery import stratify  # noqa: E402

OUT_DIR = ROOT / "results" / "skills"
SAMPLES_PATH = OUT_DIR / "samples.jsonl"
LABELS_PATH = OUT_DIR / "labels_final.jsonl"
TAXONOMY_PATH = OUT_DIR / "taxonomy_v1.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--limit", type=int)
    ap.add_argument("--stratified", type=int, help="label only a benchmark-balanced subset")
    ap.add_argument("--seed", type=int, default=7, help="must match the worksheet's seed")
    args = ap.parse_args()

    if not TAXONOMY_PATH.exists():
        print(f"missing {TAXONOMY_PATH} — lock the taxonomy from the discovery review first")
        return 1
    taxonomy = json.loads(TAXONOMY_PATH.read_text())

    samples = [json.loads(l) for l in SAMPLES_PATH.open()]
    if args.stratified:
        samples = stratify(samples, args.stratified, min_per_bench=1, seed=args.seed)
    done = set()
    if LABELS_PATH.exists():
        done = {json.loads(l)["sample_id"] for l in LABELS_PATH.open()}
    todo = [s for s in samples if s["sample_id"] not in done]
    if args.limit:
        todo = todo[:args.limit]

    print(f"{len(samples)} samples, {len(done)} already labeled, {len(todo)} to go "
          f"({len(taxonomy)} tags, {args.workers} workers)")
    if not todo:
        return 0

    lock = threading.Lock()
    t0 = time.perf_counter()
    written = 0

    def work(s: dict) -> dict:
        r = judge.judge_skills_final(s["question"], s["answer"], s["benchmark"],
                                     s["original_category"], taxonomy)
        return {**s, "fundamental_skills": r["fundamental_skills"],
                "label_confidence": r["confidence"]}

    with LABELS_PATH.open("a") as out, ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(work, s) for s in todo]
        for fut in as_completed(futures):
            row = fut.result()
            with lock:
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
                out.flush()
                written += 1
                if written % 100 == 0:
                    rate = (time.perf_counter() - t0) / written
                    print(f"  {written}/{len(todo)} ({rate:.2f}s/item, "
                          f"~{rate * (len(todo) - written) / 60:.0f} min left)", flush=True)

    n_empty = sum(1 for l in LABELS_PATH.open() if not json.loads(l)["fundamental_skills"])
    print(f"done in {(time.perf_counter() - t0) / 60:.1f} min; {n_empty} items got no labels")
    return 0


if __name__ == "__main__":
    sys.exit(main())
