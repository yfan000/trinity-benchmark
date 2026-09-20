#!/usr/bin/env python3
"""Predict per-model readiness for each HPC task — and refuse to predict where we can't.

    readiness(m,T) = Σ_S w(T,S) · score(m,S)

where score(m,S) is model m's measured accuracy on fundamental skill S across the benchmark
corpus, and w(T,S) is task T's skill profile restricted to *measurable* skills and
renormalized. Coverage — the share of T's unrestricted profile that sits on measurable
skills — decides whether the number is worth printing at all.

This is a projection, not a measurement. No model was ever run against an HPC task here; the
claim is only "given what this task demands and how models do on those demands elsewhere,
here is the expected ordering." Anything below MIN_COVERAGE is reported as not estimable,
naming the skills responsible, because a confident-looking number resting on skills we never
measured is worse than an admitted gap.

Usage:
    python skills/hpc_readiness.py
"""
from __future__ import annotations
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from skills.join_correctness import join, load_labels  # noqa: E402

MAPPING = ROOT / "results" / "skills" / "hpc" / "mapping.json"
OUT = ROOT / "results" / "skills" / "hpc" / "readiness.json"
MIN_COVERAGE = 0.70

MODEL_ORDER = ["Llama-3.1-8B", "gemma-4-E4B", "Llama-3.1-70B", "gpt-oss-20b", "gpt-oss-120b",
               "gemma-4-31B", "nemotron-3-ultra", "inkling-bf16", "gemini25pro", "gpt41nano",
               "gpt5", "claudehaiku45", "gemini35flash", "gpto3", "claudesonnet5",
               "gpt56terra", "claudeopus48"]
ONPREM = set(MODEL_ORDER[:8])


def skill_scores() -> dict[str, dict[str, float]]:
    """model -> skill -> accuracy %, from the already-labeled benchmark corpus."""
    acc: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    for r in join(load_labels()):
        for s in r["skills"]:
            acc[r["model"]][s].append(r["score"])
    return {m: {s: 100 * sum(v) / len(v) for s, v in d.items()} for m, d in acc.items()}


def main() -> int:
    m = json.loads(MAPPING.read_text())
    measurable = m["measurable"]
    scores = skill_scores()

    out = {"min_coverage": MIN_COVERAGE, "model_order": MODEL_ORDER, "framings": {}}

    for framing, tasks in m["framings"].items():
        rows = {}
        for task, d in tasks.items():
            prof = d["profile"]
            w = {s: v for s, v in prof.items() if measurable.get(s)}
            tot = sum(w.values())
            w = {s: v / tot for s, v in w.items()} if tot else {}
            cov = d["coverage"]
            est = cov >= MIN_COVERAGE
            per_model = {}
            for model in MODEL_ORDER:
                sc = scores.get(model, {})
                usable = {s: wt for s, wt in w.items() if s in sc}
                denom = sum(usable.values())
                per_model[model] = (sum(wt * sc[s] for s, wt in usable.items()) / denom
                                    if denom else None)
            rows[task] = {
                "coverage": cov,
                "estimable": est,
                "weights": dict(sorted(w.items(), key=lambda kv: -kv[1])[:8]),
                "unmeasured": d["unmeasured"],
                "readiness": per_model if est else None,
            }
        out["framings"][framing] = rows

    OUT.write_text(json.dumps(out, indent=1))

    for framing, rows in out["framings"].items():
        print(f"\n=== {framing.upper()} — projected readiness (best / worst of 17 models) ===")
        print(f"{'HPC task':<26}{'cover':>7}  {'best':<34}{'worst':<26}")
        for task, d in sorted(rows.items(), key=lambda kv: -(kv[1]["coverage"])):
            if not d["estimable"]:
                miss = ", ".join(f"{s} {w:.0%}" for s, w in d["unmeasured"][:2])
                print(f"{task:<26}{d['coverage']:>6.0%}  NOT ESTIMABLE — weight on unmeasured: {miss}")
                continue
            r = {k: v for k, v in d["readiness"].items() if v is not None}
            b, w_ = max(r.items(), key=lambda kv: kv[1]), min(r.items(), key=lambda kv: kv[1])
            bo = max(((k, v) for k, v in r.items() if k in ONPREM), key=lambda kv: kv[1])
            print(f"{task:<26}{d['coverage']:>6.0%}  {b[0]} {b[1]:.1f}%"
                  f"{'':<{max(1, 22 - len(b[0]))}}on-prem {bo[0]} {bo[1]:.1f}%   low {w_[1]:.1f}%")

    print(f"\nAll numbers are PROJECTIONS from fundamental-skill scores — no model was run "
          f"against an HPC task.\nEstimable only where coverage >= {MIN_COVERAGE:.0%} -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
