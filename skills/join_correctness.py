"""Join per-sample skill labels to per-model per-item correctness.

The corpus's `sample_id` index is the same index as the item's position in each result
file's `details` array (proven by skills/verify_join.py), so the join is positional — no
text matching. A sample carrying three skill labels contributes one observation to each of
the three, which is what makes cross-benchmark skill aggregation possible.

Correctness field varies by benchmark: most use `correct`, the code benchmarks use `passed`,
MT-Bench is a 1-5 judge score (normalized to 0-1), and InfoBench's `details` are one row per
decomposed sub-question, so its per-instruction score is the fraction of its own
sub-questions satisfied rather than a boolean.
"""
from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

SOPHIA_MODELS = [
    "meta-llama/Meta-Llama-3.1-8B-Instruct", "google/gemma-4-E4B-it",
    "meta-llama/Meta-Llama-3.1-70B-Instruct", "openai/gpt-oss-20b",
    "google/gemma-4-31B-it", "openai/gpt-oss-120b",
]
ARGO_MODELS = ["gemini25pro", "gpt41nano", "gpt5", "gemini35flash", "gpto3",
               "claudehaiku45", "claudesonnet5", "gpt56terra", "claudeopus48"]
MINERVA_MODELS = ["nemotron-3-ultra", "inkling-bf16"]

SHORT = {
    "meta-llama/Meta-Llama-3.1-8B-Instruct": "Llama-3.1-8B",
    "google/gemma-4-E4B-it": "gemma-4-E4B",
    "meta-llama/Meta-Llama-3.1-70B-Instruct": "Llama-3.1-70B",
    "openai/gpt-oss-20b": "gpt-oss-20b",
    "google/gemma-4-31B-it": "gemma-4-31B",
    "openai/gpt-oss-120b": "gpt-oss-120b",
    **{m: m for m in ARGO_MODELS + MINERVA_MODELS},
}

SOURCE_DIR = {**{m: "public_full" for m in SOPHIA_MODELS},
              **{m: "argo_full_run" for m in ARGO_MODELS},
              **{m: "minerva_full" for m in MINERVA_MODELS}}

# Benchmarks excluded from skill aggregation: SWE-bench is pulled from reporting, and the
# two domain-science benchmarks are reported separately (very different score ranges).
EXCLUDED = {"labbench", "matscibench"}


def _item_score(bench: str, d: dict) -> float | None:
    """Per-item correctness in 0-1, or None if the item wasn't scored."""
    if bench in ("humaneval", "bigcodebench"):
        return 1.0 if d.get("passed") else 0.0
    if bench == "mt_bench":
        scores = [s for s in (d.get("turn_scores") or []) if isinstance(s, (int, float))]
        return (sum(scores) / len(scores) - 1) / 4 if scores else None
    if "correct" in d:
        return 1.0 if d["correct"] else 0.0
    return None


def load_labels(path: Path | None = None) -> dict[str, dict]:
    path = path or RESULTS / "skills" / "labels_final.jsonl"
    with path.open() as f:
        return {r["sample_id"]: r for r in map(json.loads, f)}


def _details_by_index(bench: str, details: list[dict]) -> dict[int, float]:
    """Map corpus index -> score. InfoBench collapses its sub-question rows per instruction."""
    if bench != "infobench":
        return {i: s for i, d in enumerate(details) if (s := _item_score(bench, d)) is not None}
    grouped, order = defaultdict(list), []
    for d in details:
        key = d.get("id")
        if key not in grouped:
            order.append(key)
        grouped[key].append(1.0 if d.get("correct") else 0.0)
    return {i: sum(grouped[k]) / len(grouped[k]) for i, k in enumerate(order)}


def join(labels: dict[str, dict]) -> list[dict]:
    """One row per (sample, model) with its skill labels and that model's score on it."""
    by_bench: dict[str, list[str]] = defaultdict(list)
    for sid in labels:
        by_bench[sid.split("::")[0]].append(sid)
    for sids in by_bench.values():
        sids.sort(key=lambda s: int(s.split("::")[1]))

    rows = []
    for bench, sids in by_bench.items():
        if bench in EXCLUDED:
            continue
        for model, dirname in SOURCE_DIR.items():
            path = RESULTS / dirname / f"{bench}_results.json"
            if not path.exists():
                continue
            entry = next((e for e in json.loads(path.read_text()) if e.get("model") == model), None)
            if not entry or not entry.get("details"):
                continue
            scores = _details_by_index(bench, entry["details"])
            for idx, sid in enumerate(sids):
                if idx not in scores:
                    continue
                skills = labels[sid].get("fundamental_skills") or []
                if not skills:
                    continue
                rows.append({"sample_id": sid, "benchmark": bench, "model": SHORT[model],
                             "score": scores[idx], "skills": skills})
    return rows
