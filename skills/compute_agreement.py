#!/usr/bin/env python3
"""Phase 2b — score the LLM's labels against the human's.

Two views, because one number hides the wrong things:
  * Mean Jaccard over label-sets — the headline "do these agree" figure.
  * Per-tag precision/recall/F1 (+ macro and micro) — which specific tags are the problem.

Decision rule, applied to mean Jaccard:
  >= 0.90  taxonomy validated; run the full-corpus pass as-is.
  0.65-0.90  do not restart. Read the per-tag table bottom-up: the worst tags are usually
             two labels whose boundary is genuinely ambiguous. Merge them, or sharpen their
             descriptions in taxonomy_v1.json, then re-label only the affected slice.
  <= 0.65  the taxonomy itself is wrong, not just fuzzy. Revise the seed list and redo
           discovery on a fresh sample rather than patching.

Usage:
    python skills/compute_agreement.py
"""
from __future__ import annotations
import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "results" / "skills"


def prf(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f = 2 * p * r / (p + r) if p + r else 0.0
    return p, r, f


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=str(OUT_DIR / "human_validation.csv"))
    ap.add_argument("--threshold", type=float, default=0.90)
    args = ap.parse_args()

    rows = [r for r in csv.DictReader(open(args.csv)) if r["human_skills"].strip()]
    if not rows:
        print(f"no rows with human_skills filled in — label {args.csv} first")
        return 1

    # A blind worksheet ships with llm_skills empty so the reviewer isn't anchored; attach
    # the classifier's labels now, after the human's are locked in.
    if not any(r["llm_skills"].strip() for r in rows):
        labels_path = OUT_DIR / "labels_final.jsonl"
        labels = {json.loads(l)["sample_id"]: json.loads(l)["fundamental_skills"]
                  for l in labels_path.open()}
        missing = [r["sample_id"] for r in rows if r["sample_id"] not in labels]
        if missing:
            print(f"{len(missing)} validated items have no entry in {labels_path.name}")
            return 1
        for r in rows:
            r["llm_skills"] = "|".join(labels[r["sample_id"]])
        print(f"blind worksheet — attached classifier labels from {labels_path.name}\n")

    taxonomy = {t["name"] for t in json.loads((OUT_DIR / "taxonomy_v1.json").read_text())}
    split = lambda s: {x.strip() for x in s.split("|") if x.strip()}  # noqa: E731

    unknown = set()
    jaccards, per_tag = [], defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})
    for r in rows:
        llm, hum = split(r["llm_skills"]), split(r["human_skills"])
        unknown |= (hum - taxonomy)
        union = llm | hum
        jaccards.append(len(llm & hum) / len(union) if union else 1.0)
        for tag in taxonomy:
            in_l, in_h = tag in llm, tag in hum
            if in_l and in_h:
                per_tag[tag]["tp"] += 1
            elif in_l:
                per_tag[tag]["fp"] += 1
            elif in_h:
                per_tag[tag]["fn"] += 1

    if unknown:
        print(f"WARNING: {len(unknown)} human label(s) not in taxonomy_v1.json — likely typos, "
              f"they score as pure disagreement: {sorted(unknown)}\n")

    mean_j = sum(jaccards) / len(jaccards)
    scored = {t: prf(**c) for t, c in per_tag.items() if c["tp"] + c["fp"] + c["fn"]}
    macro_f1 = sum(f for _, _, f in scored.values()) / len(scored) if scored else 0.0
    tot = {k: sum(c[k] for c in per_tag.values()) for k in ("tp", "fp", "fn")}
    micro_f1 = prf(**tot)[2]

    print(f"{len(rows)} validated items")
    print(f"  mean Jaccard  {mean_j:.3f}")
    print(f"  macro F1      {macro_f1:.3f}")
    print(f"  micro F1      {micro_f1:.3f}\n")
    print(f"  {'tag':<40} {'P':>6} {'R':>6} {'F1':>6}  {'tp':>4} {'fp':>4} {'fn':>4}")
    for tag, (p, r, f) in sorted(scored.items(), key=lambda kv: kv[1][2]):
        c = per_tag[tag]
        print(f"  {tag:<40} {p:6.2f} {r:6.2f} {f:6.2f}  {c['tp']:4d} {c['fp']:4d} {c['fn']:4d}")

    report = {"n": len(rows), "mean_jaccard": mean_j, "macro_f1": macro_f1, "micro_f1": micro_f1,
              "per_tag": {t: {"precision": p, "recall": r, "f1": f, **per_tag[t]}
                          for t, (p, r, f) in scored.items()}}
    (OUT_DIR / "agreement_report.json").write_text(json.dumps(report, indent=2))

    if mean_j >= args.threshold:
        print(f"\nPASS ({mean_j:.3f} >= {args.threshold}) — proceed to full-corpus labeling")
        return 0
    print(f"\nBELOW THRESHOLD ({mean_j:.3f} < {args.threshold}) — see the decision rule in this "
          f"script's docstring before scaling up")
    return 1


if __name__ == "__main__":
    sys.exit(main())
