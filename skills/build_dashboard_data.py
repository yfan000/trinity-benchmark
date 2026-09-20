#!/usr/bin/env python3
"""Add a cross-benchmark "Fundamental Skills" tab to results/category_breakdown.html.

The dashboard's renderer is already generic over `DATA.benchmarks[key].categories[label]
[model] = {pct, n}` — nothing in it assumes a grouping key comes from a single benchmark.
So a skill view is a data-only change: pool every (sample, model, score) observation across
all benchmarks by skill tag, write one more entry into the embedded DATA blob, and add the
key to BENCH_KEYS.

The script that originally generated this HTML is no longer in the repo, so the deployed
file is patched in place (its DATA blob parsed out, extended, and re-spliced) rather than
regenerated — regenerating would risk silently dropping the existing tabs.

Usage:
    python skills/build_dashboard_data.py
"""
from __future__ import annotations
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from skills.join_correctness import join, load_labels  # noqa: E402

DASHBOARD = ROOT / "results" / "category_breakdown.html"
SKILL_KEY = "skills"


def build_skill_categories(rows: list[dict]) -> dict:
    agg: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for r in rows:
        for skill in r["skills"]:
            agg[skill][r["model"]].append(r["score"])
    return {
        skill: {model: {"pct": round(100 * sum(v) / len(v), 1), "n": len(v)}
                for model, v in sorted(models.items())}
        for skill, models in sorted(agg.items())
    }


def main() -> int:
    rows = join(load_labels())
    if not rows:
        print("no joined rows — run label_full_corpus.py first")
        return 1
    categories = build_skill_categories(rows)

    text = DASHBOARD.read_text()
    m = re.search(r'^const DATA = (\{.*?\n\});$', text, re.S | re.M)
    data = json.loads(m.group(1))
    data["benchmarks"][SKILL_KEY] = {
        "label": "Fundamental Skills",
        "field_label": "Skill",
        "unit": "pct",
        "categories": categories,
    }
    text = text[:m.start(1)] + json.dumps(data, indent=1) + text[m.end(1):]

    keys_re = re.compile(r'^const BENCH_KEYS = (\[.*?\]);$', re.M)
    km = keys_re.search(text)
    keys = json.loads(km.group(1))
    if SKILL_KEY not in keys:
        keys.insert(0, SKILL_KEY)
        text = text[:km.start(1)] + json.dumps(keys, separators=(",", ":")) + text[km.end(1):]

    DASHBOARD.write_text(text)

    n_obs = sum(v["n"] for models in categories.values() for v in models.values())
    print(f"{len(categories)} skills, {n_obs:,} (sample x model) observations")
    print(f"  -> {DASHBOARD}")
    empty = [s for s, models in categories.items() if not models]
    if empty:
        print(f"  no coverage: {empty}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
