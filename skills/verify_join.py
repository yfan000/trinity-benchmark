#!/usr/bin/env python3
"""Prove the reconstructed corpus lines up with the published results before spending any
LLM budget on labeling it.

Two independent checks per benchmark:
  1. Length — reconstructed item count vs. each result file's `details` length.
  2. Content — for benchmarks whose `details` carry a category-equivalent field, that field
     must match the reconstructed `original_category` at *every* index. This is the check
     that actually proves the index join is valid; a matching length alone would still pass
     if the sampling order had drifted.

InfoBench is the one documented exception: its `details` are one row per decomposed
sub-question (2250) while the corpus holds one row per instruction (500), so it is checked
by grouping `details` on `id` instead.
"""
from __future__ import annotations
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

RESULT_DIRS = ["public_full", "argo_full_run", "minerva_full"]

# details field that should equal the corpus's original_category, per benchmark
CATEGORY_FIELD = {
    "mmlu": "subject", "mmlu_pro": "category", "gpqa": "category", "gpqa_main": "category",
    "olympiadbench": "subfield", "math": "type", "bbh": "task", "mt_bench": "category",
    "hle": "category", "longbench_v2": "domain", "sealqa": "category",
    "clutrr_regen": "category", "followbench": "category", "matscibench": "category",
}


def load_corpus() -> dict[str, list[dict]]:
    by_bench = defaultdict(list)
    with (ROOT / "results" / "skills" / "samples.jsonl").open() as f:
        for line in f:
            row = json.loads(line)
            by_bench[row["benchmark"]].append(row)
    return by_bench


def main() -> int:
    corpus = load_corpus()
    problems, checked = [], 0

    for bench, samples in sorted(corpus.items()):
        cat_field = CATEGORY_FIELD.get(bench)
        for dirname in RESULT_DIRS:
            path = ROOT / "results" / dirname / f"{bench}_results.json"
            if not path.exists():
                continue
            for entry in json.loads(path.read_text()):
                model, details = entry.get("model"), entry.get("details") or []
                if not details:
                    continue
                checked += 1
                label = f"{bench}/{dirname}/{model}"

                if bench == "infobench":
                    n_parents = len({d.get("id") for d in details})
                    if n_parents != len(samples):
                        problems.append(f"{label}: {n_parents} parent ids vs {len(samples)} samples")
                    continue

                if len(details) != len(samples):
                    problems.append(f"{label}: {len(details)} details vs {len(samples)} samples")
                    continue

                if cat_field:
                    bad = [i for i, (d, s) in enumerate(zip(details, samples))
                           if str(d.get(cat_field)) != str(s["original_category"])]
                    if bad:
                        problems.append(
                            f"{label}: {len(bad)} category mismatches "
                            f"(first at index {bad[0]}: details={details[bad[0]].get(cat_field)!r} "
                            f"corpus={samples[bad[0]]['original_category']!r})")

    print(f"checked {checked} benchmark x model result sets")
    if problems:
        print(f"\n{len(problems)} PROBLEMS:")
        for p in problems:
            print(f"  {p}")
        return 1
    print("all length and category checks passed — index join is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
