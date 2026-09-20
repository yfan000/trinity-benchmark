#!/usr/bin/env python3
"""Score the judge against the human review. The first measurement of ACCURACY in this project.

Everything before this measured precision or behaviour on known-good scripts:
  replicates      the judge agrees with itself (9/159 unstable under r4)
  calibration     it does not mark down real production runs (5/7 clean)
Neither says it is RIGHT about a model's answer. Only a human comparison does.

Metrics are per REQUIREMENT, because that is the unit both sides ruled on. Reporting only a
score delta would hide which rule is wrong, and the rule is the thing that gets edited.

Cohen's kappa is reported alongside raw agreement because agreement alone is inflated when one
category dominates — most verdicts here are "satisfied", so a judge that said satisfied to
everything would score well on agreement and zero on kappa.

Usage:
    python skills/compute_judge_agreement.py --csv results/skills/trinity/review/<file>.csv
"""
from __future__ import annotations
import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from skills.judging.loader import load as load_skill  # noqa: E402

TRIN = ROOT / "results" / "skills" / "trinity"
V = ["satisfied", "violated", "not_applicable"]


def kappa(pairs: list[tuple[str, str]]) -> float:
    """Cohen's kappa, unweighted — the categories here are nominal, not ordered."""
    n = len(pairs)
    if not n:
        return float("nan")
    po = sum(a == b for a, b in pairs) / n
    ha, ja = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum((ha[c] / n) * (ja[c] / n) for c in set(ha) | set(ja))
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")


def decided_by() -> dict[str, str]:
    """Which side was supposed to decide each requirement."""
    out = {}
    for st in ("Software selection", "Input preparation", "Resource selection",
               "Batch job creation"):
        for app in (None, "qe", "hpl", "gromacs"):
            try:
                for r in load_skill(st, app, "polaris").requirements:
                    out[r["id"]] = r.get("decided_by", "judge")
            except Exception:
                pass
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--split", choices=["DEV", "TEST", "both"], default="both")
    a = ap.parse_args()

    rows = [r for r in csv.DictReader(open(a.csv))
            if r["human"] and r["judge"]]           # unmarked rows are not disagreements
    skipped = sum(1 for r in csv.DictReader(open(a.csv)) if not r["human"])
    if a.split != "both":
        rows = [r for r in rows if r["split"] == a.split]

    dec = decided_by()
    pairs = [(r["human"], r["judge"]) for r in rows]
    agree = sum(h == j for h, j in pairs)
    print(f"{len(rows)} marked requirement verdicts"
          + (f" ({skipped} left unmarked, excluded)" if skipped else ""))
    print(f"\noverall agreement  {agree}/{len(rows)} = {agree/len(rows):.0%}"
          f"   kappa {kappa(pairs):.2f}")

    # Who decides matters most: code-decided rules should agree near-perfectly, because the
    # human is checking arithmetic. Judged rules are where the real disagreement lives.
    print(f"\n{'decided by':<16}{'n':>5}{'agree':>8}{'kappa':>8}")
    for side in ("deterministic", "judge", "unknown"):
        sub = [r for r in rows if dec.get(r["requirement"], "unknown") == side]
        if not sub:
            continue
        p = [(r["human"], r["judge"]) for r in sub]
        print(f"{side:<16}{len(sub):>5}{sum(h==j for h,j in p)/len(p):>8.0%}"
              f"{kappa(p):>8.2f}")

    print(f"\n{'subtask':<22}{'n':>5}{'agree':>8}{'kappa':>8}")
    for st in sorted({r["subtask"] for r in rows}):
        sub = [r for r in rows if r["subtask"] == st]
        p = [(r["human"], r["judge"]) for r in sub]
        print(f"{st:<22}{len(sub):>5}{sum(h==j for h,j in p)/len(p):>8.0%}{kappa(p):>8.2f}")

    # Direction of error: is the judge systematically lenient or strict?
    lenient = sum(1 for h, j in pairs if h == "violated" and j != "violated")
    strict = sum(1 for h, j in pairs if h != "violated" and j == "violated")
    print(f"\ndirection of disagreement")
    print(f"  judge too LENIENT (human violated, judge did not) {lenient}")
    print(f"  judge too STRICT  (judge violated, human did not) {strict}")
    print(f"  n/a mismatches                                    "
          f"{sum(1 for h,j in pairs if (h=='not_applicable') != (j=='not_applicable'))}")

    print(f"\nworst requirements  (>=3 marks, sorted by disagreement)")
    print(f"{'requirement':<46}{'n':>4}{'agree':>7}{'lenient':>9}{'strict':>8}")
    by = defaultdict(list)
    for r in rows:
        by[r["requirement"]].append((r["human"], r["judge"]))
    for rid, p in sorted(by.items(), key=lambda kv: sum(h == j for h, j in kv[1]) / len(kv[1])):
        if len(p) < 3:
            continue
        ag = sum(h == j for h, j in p) / len(p)
        if ag >= 0.9:
            continue
        le = sum(1 for h, j in p if h == "violated" and j != "violated")
        stx = sum(1 for h, j in p if h != "violated" and j == "violated")
        print(f"{rid:<46}{len(p):>4}{ag:>7.0%}{le:>9}{stx:>8}")

    # DEV/TEST, the overfitting guard
    for s in ("DEV", "TEST"):
        sub = [r for r in rows if r["split"] == s]
        if sub:
            p = [(r["human"], r["judge"]) for r in sub]
            print(f"\n{s:<6}{len(sub):>4} marks   agreement {sum(h==j for h,j in p)/len(p):.0%}"
                  f"   kappa {kappa(p):.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
