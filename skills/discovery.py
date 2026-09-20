#!/usr/bin/env python3
"""Phase 1 — taxonomy discovery.

Runs the open-vocabulary classifier over a stratified sample of the corpus so the taxonomy
is decided from what the questions actually contain, rather than asserted up front. The
output is reviewed by hand to produce the locked taxonomy_v1.json.

Stratification is proportional-with-a-floor: every benchmark contributes at least
--min-per-bench items so a 21-item benchmark still gets a voice, with the remainder split
by size so the big benchmarks aren't under-sampled either.

Usage:
    python skills/discovery.py --n 400              # run the pass
    python skills/discovery.py --summarize          # tag frequencies from an existing run
"""
from __future__ import annotations
import argparse
import json
import random
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import judge  # noqa: E402

OUT_DIR = ROOT / "results" / "skills"
SAMPLES_PATH = OUT_DIR / "samples.jsonl"
RESULTS_PATH = OUT_DIR / "discovery_results.jsonl"
SEED_PATH = Path(__file__).parent / "taxonomy_seed.json"


def load_samples() -> list[dict]:
    with SAMPLES_PATH.open() as f:
        return [json.loads(line) for line in f]


def stratify(samples: list[dict], n: int, min_per_bench: int, seed: int) -> list[dict]:
    by_bench: dict[str, list[dict]] = defaultdict(list)
    for s in samples:
        by_bench[s["benchmark"]].append(s)

    rng = random.Random(seed)
    picked: list[dict] = []
    remaining = n - min_per_bench * len(by_bench)
    total = len(samples)

    for bench, rows in sorted(by_bench.items()):
        share = min_per_bench + int(remaining * len(rows) / total) if remaining > 0 else min_per_bench
        picked.extend(rng.sample(rows, min(share, len(rows))))
    return picked


def summarize(rows: list[dict]) -> None:
    seed_names = {t["name"] for t in json.loads(SEED_PATH.read_text())}
    applied = Counter(s for r in rows for s in r.get("proposed_skills", []))
    novel = Counter(r["novel_tag_suggested"] for r in rows if r.get("novel_tag_suggested"))
    per_item = [len(r.get("proposed_skills", [])) for r in rows]

    print(f"\n{len(rows)} labeled items, {sum(per_item) / max(len(per_item), 1):.1f} skills/item avg\n")
    print("SEED TAG FREQUENCY (candidates to drop at the bottom, to split at the top):")
    for name in sorted(seed_names, key=lambda x: -applied.get(x, 0)):
        count = applied.get(name, 0)
        pct = 100 * count / max(len(rows), 1)
        print(f"  {count:5d} ({pct:5.1f}%)  {name}")

    off_taxonomy = {k: v for k, v in applied.items() if k not in seed_names}
    if off_taxonomy:
        print("\nAPPLIED BUT NOT IN SEED LIST:")
        for name, count in sorted(off_taxonomy.items(), key=lambda kv: -kv[1]):
            print(f"  {count:5d}  {name}")

    print("\nPROPOSED NEW TAGS (recurring ones are real gaps; singletons are noise):")
    for name, count in novel.most_common(25):
        print(f"  {count:5d}  {name}")

    co = Counter()
    for r in rows:
        skills = sorted(set(r.get("proposed_skills", [])))
        for i, a in enumerate(skills):
            for b in skills[i + 1:]:
                co[(a, b)] += 1
    print("\nTOP CO-OCCURRING PAIRS (near-total overlap = merge candidates):")
    for (a, b), count in co.most_common(12):
        both = min(applied[a], applied[b]) or 1
        print(f"  {count:5d} ({100 * count / both:5.1f}% of the rarer tag)  {a}  +  {b}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--min-per-bench", type=int, default=8)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--summarize", action="store_true")
    args = ap.parse_args()

    if args.summarize:
        with RESULTS_PATH.open() as f:
            summarize([json.loads(line) for line in f])
        return 0

    seed_skills = [t["name"] for t in json.loads(SEED_PATH.read_text())]
    picked = stratify(load_samples(), args.n, args.min_per_bench, args.seed)
    print(f"labeling {len(picked)} stratified samples with {judge.JUDGE_MODEL}")

    # Append-and-flush per item: a crash or interrupt keeps everything already paid for.
    done = set()
    if RESULTS_PATH.exists():
        with RESULTS_PATH.open() as f:
            done = {json.loads(line)["sample_id"] for line in f}
        print(f"  resuming — {len(done)} already labeled")

    t0 = time.perf_counter()
    with RESULTS_PATH.open("a") as out:
        for i, s in enumerate(picked, 1):
            if s["sample_id"] in done:
                continue
            r = judge.judge_skills_discovery(
                s["question"], s["answer"], s["benchmark"],
                s["original_category"], seed_skills)
            out.write(json.dumps({"sample_id": s["sample_id"], "benchmark": s["benchmark"],
                                  "original_category": s["original_category"], **r}) + "\n")
            out.flush()
            if i % 25 == 0:
                rate = (time.perf_counter() - t0) / i
                print(f"  {i}/{len(picked)} ({rate:.1f}s/item, "
                      f"~{rate * (len(picked) - i) / 60:.0f} min left)", flush=True)

    with RESULTS_PATH.open() as f:
        summarize([json.loads(line) for line in f])
    return 0


if __name__ == "__main__":
    sys.exit(main())
