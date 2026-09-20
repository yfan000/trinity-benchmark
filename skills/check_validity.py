#!/usr/bin/env python3
"""Construct-validity check that needs no human labeling.

Each benchmark was built to test something specific. If the classifier is working, its
labels should independently rediscover that design intent — Coreference resolution should
concentrate on WinoGrande, Code generation on HumanEval/BigCodeBench, and so on. These are
falsifiable predictions made from the benchmarks' documentation, not from the labels, so
agreement is evidence the labels track something real.

This does not replace human validation: it can only catch gross errors, and a classifier
that simply memorized "benchmark X -> skill Y" would pass it. It is a floor, not a ceiling.

Usage:
    python skills/check_validity.py
"""
from __future__ import annotations
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LABELS = ROOT / "results" / "skills" / "labels_final.jsonl"

# (benchmark, tag, min_share) — the tag should appear on at least this fraction of the
# benchmark's items, because that is what the benchmark exists to measure.
EXPECTED = [
    ("winogrande", "Coreference resolution", 0.50),
    ("humaneval", "Code generation", 0.90),
    ("bigcodebench", "Code generation", 0.90),
    ("gsm8k", "Numerical reasoning", 0.80),
    ("gsm1k", "Numerical reasoning", 0.80),
    ("math", "Mathematical problem solving", 0.70),
    ("aime2024", "Mathematical problem solving", 0.70),
    ("olympiadbench", "Mathematical problem solving", 0.70),
    ("ifeval", "Instruction/format following", 0.80),
    ("followbench", "Instruction/format following", 0.60),
    ("infobench", "Instruction/format following", 0.50),
    ("truthfulqa", "Truthfulness/calibration", 0.40),
    ("clutrr_regen", "Relational/multi-hop inference", 0.70),
    ("longbench_v2", "Reading comprehension (long-context)", 0.70),
    ("hellaswag", "Commonsense reasoning", 0.50),
    ("gpqa", "Expert domain knowledge", 0.50),
    ("mt_bench", "Multi-turn dialogue coherence", 0.40),
]

# Tags that must NOT dominate a benchmark they have no business on — catches a classifier
# that sprays a popular tag everywhere.
FORBIDDEN = [
    ("gsm8k", "Code generation", 0.10),
    ("winogrande", "Mathematical problem solving", 0.10),
    ("humaneval", "Ethical/normative judgment", 0.10),
    ("mmlu", "Multi-turn dialogue coherence", 0.10),
]


def main() -> int:
    rows = [json.loads(l) for l in LABELS.open()]
    by_bench: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_bench[r["benchmark"]].append(r)

    print(f"{len(rows)} labeled samples across {len(by_bench)} benchmarks\n")
    failures = 0

    print("EXPECTED (benchmark's design intent should show up in its labels)")
    for bench, tag, floor in EXPECTED:
        items = by_bench.get(bench, [])
        if not items:
            continue
        share = sum(tag in r["fundamental_skills"] for r in items) / len(items)
        ok = share >= floor
        failures += not ok
        print(f"  {'ok  ' if ok else 'MISS'} {bench:<15} {tag:<38} {share:5.0%} (need {floor:.0%})")

    print("\nFORBIDDEN (tag should not bleed onto benchmarks it has no business on)")
    for bench, tag, ceiling in FORBIDDEN:
        items = by_bench.get(bench, [])
        if not items:
            continue
        share = sum(tag in r["fundamental_skills"] for r in items) / len(items)
        ok = share <= ceiling
        failures += not ok
        print(f"  {'ok  ' if ok else 'BLED'} {bench:<15} {tag:<38} {share:5.0%} (max {ceiling:.0%})")

    tags = Counter(s for r in rows for s in r["fundamental_skills"])
    taxonomy = [t["name"] for t in json.loads((ROOT / "results/skills/taxonomy_v1.json").read_text())]
    print(f"\nCORPUS-WIDE TAG COVERAGE ({len(tags)}/{len(taxonomy)} tags used, "
          f"{sum(len(r['fundamental_skills']) for r in rows) / len(rows):.2f} tags/item)")
    for t in sorted(taxonomy, key=lambda x: -tags.get(x, 0)):
        n = tags.get(t, 0)
        print(f"  {n:5d} ({n / len(rows):5.1%})  {t}")

    print(f"\n{failures} check(s) failed" if failures else "\nall checks passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
