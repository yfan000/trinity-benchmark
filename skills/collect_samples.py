#!/usr/bin/env python3
"""Reconstruct every benchmark's question set into one flat corpus for skill labeling.

Result files store only derived per-item metadata (category, correctness, a truncated
response snippet) — never the question text. Each benchmark module's `load_items(cfg)` is
deterministic given the same config/seed/n_samples, so re-calling it with the config the
run actually used rebuilds the identical item set, in the identical order. That order is
what makes `sample_id`'s index a valid join key into each result file's `details` array.

Usage:
    python skills/collect_samples.py                      # all benchmarks
    python skills/collect_samples.py --only gpqa,bbh      # a subset
"""
from __future__ import annotations
import argparse
import importlib
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from run_public import BENCHMARK_MODULES  # noqa: E402
from skills.normalize import NORMALIZERS  # noqa: E402

OUT_DIR = ROOT / "results" / "skills"
SAMPLES_PATH = OUT_DIR / "samples.jsonl"
MANIFEST_PATH = OUT_DIR / "samples_manifest.json"
CONFIG_PATH = ROOT / "benchmark_configs" / "full.yaml"


def collect(bench: str, cfg: dict) -> list[dict]:
    module = importlib.import_module(BENCHMARK_MODULES[bench])
    normalize = NORMALIZERS[bench]
    rows = []
    for idx, raw in enumerate(module.load_items(cfg)):
        question, answer, category, difficulty = normalize(raw)
        rows.append({
            "sample_id": f"{bench}::{idx:04d}",
            "benchmark": bench,
            "question": question,
            "answer": answer,
            "original_category": category,
            "original_difficulty": difficulty,
            "fundamental_skills": [],
            "human_validated": False,
            "label_confidence": None,
        })
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma-separated benchmark names")
    args = ap.parse_args()

    configs = yaml.safe_load(CONFIG_PATH.read_text())["benchmarks"]
    wanted = args.only.split(",") if args.only else list(configs)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest, all_rows, failed = {}, [], []

    for bench in wanted:
        cfg = configs.get(bench)
        if cfg is None or not cfg.get("enabled", True):
            continue
        if bench not in NORMALIZERS:
            failed.append((bench, "no normalizer"))
            continue
        try:
            rows = collect(bench, cfg)
        except Exception as e:
            failed.append((bench, f"{type(e).__name__}: {e}"))
            continue
        all_rows.extend(rows)
        manifest[bench] = {
            "n_items": len(rows),
            "config": {k: v for k, v in cfg.items() if k != "enabled"},
        }
        print(f"  {bench}: {len(rows)} samples")

    with SAMPLES_PATH.open("w") as f:
        for row in all_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))

    print(f"\n{len(all_rows)} samples across {len(manifest)} benchmarks -> {SAMPLES_PATH}")
    for bench, err in failed:
        print(f"  FAILED {bench}: {err}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
