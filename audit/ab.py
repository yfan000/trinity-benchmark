#!/usr/bin/env python3
"""Compare the two A/B arms on the frozen v8 corpus.

The arms share every item: same 40 anchors, same four models, same judge, same rubric. Only the
Input-preparation prompt differs, and only by insertion — `trinity_arm.py --verify` asserts that
stripping the inserted blocks returns the base prompt byte-for-byte. So the comparison is
PAIRED, and the paired statistic is the one that matters.

WHY NOT McNEMAR AS THE HEADLINE. McNemar on pass/fail is the obvious test and it cannot detect
an effect this size: with b one-directional flips its exact p is 2/2^b, so it needs b >= 6 to
clear 0.05, and the reachable effect is around 4 rows. Worse, Input preparation has no
minor-severity rules, so one violation is a non-pass and a row that went from six violations to
one counts as no change. The violation COUNT per row spans 0-10 and is the more sensitive
endpoint.

THREE CONTROLS ARE BUILT IN, and they are the reason to trust or distrust the number:
  - 30 of 40 anchors are byte-identical across arms (every subtask except Input preparation).
    Any movement there is model sampling noise, and it calibrates how large the Input-prep
    delta has to be before it means anything.
  - The two sparse anchors (vllm@frontier, pytorch@sophia) get no format contract, only the
    system-context block. They bound the contract-free part of any effect.
  - k=3 per arm, so the per-run spread is visible rather than assumed.

Usage:
    python skills/trinity_ab.py --judge gpt56terra --rubric r27 --mode skill --runs 3
"""
from __future__ import annotations
import argparse
import json
import statistics
import sys
from collections import Counter, defaultdict
from math import comb, erfc
from pathlib import Path

import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from audit.matrix import replay as _replay   # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
TRIN = ROOT / "data" / "corpus" / "v8"

SPARSE = {("vllm", "frontier"), ("pytorch", "sophia")}
ARM_SUBTASK = "Input preparation"


def key(r: dict) -> tuple:
    return (r["model"], r["subtask"], r["app"], r["system"])


def is_pass(r: dict) -> bool:
    return (r.get("correctness") == 2 and r.get("completeness") == 2
            and r.get("usability") == 2 and not r.get("fatal_error"))


def n_viol(r: dict) -> int:
    return sum(1 for q in (r.get("requirements") or {}).values()
               if q.get("verdict") == "violated")


def load_runs(arm: str, judge: str, rubric: str, mode: str, runs: int,
              score_rubric: str | None = None) -> list[dict]:
    """Grades are COLLECTED under `rubric` and SCORED under `score_rubric`.

    Without this the statistics ran on the stored r27 scores while audit/matrix.py and the HTML
    reported an r28 replay, so the same comparison produced two different pass counts (rich 94
    vs 99). One rubric for every consumer, or the numbers cannot be quoted together.
    """
    tag = "__SKILLMODE" if mode == "skill" else ""
    out = []
    for i in range(1, runs + 1):
        p = TRIN / f"grades_v8{arm}__{judge}__{rubric}{tag}__run{i}.jsonl"
        if p.exists():
            rows = [json.loads(l) for l in p.open()]
            if score_rubric and score_rubric != rubric:
                rows = [_replay(r, score_rubric)[0] for r in rows]
            out.append({key(r): r for r in rows})
    return out


def consensus(M: list[dict], k) -> dict | None:
    """Majority verdict across replicates; the median row for the score fields."""
    rows = [m[k] for m in M if k in m]
    if not rows:
        return None
    r = dict(rows[0])
    for f in ("correctness", "completeness", "usability"):
        r[f] = statistics.median_low([x.get(f, 0) for x in rows])
    r["fatal_error"] = sum(bool(x.get("fatal_error")) for x in rows) > len(rows) / 2
    r["_n_viol"] = statistics.median_low([n_viol(x) for x in rows])
    r["_unstable"] = len({is_pass(x) for x in rows}) > 1
    return r


def signed_rank(nz: list[float]) -> tuple[float, float]:
    """(z, two-sided p) for the Wilcoxon signed-rank test, normal approximation."""
    order = sorted(range(len(nz)), key=lambda i: abs(nz[i]))
    ranks = [0.0] * len(nz)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and abs(nz[order[j + 1]]) == abs(nz[order[i]]):
            j += 1
        for t in range(i, j + 1):
            ranks[order[t]] = (i + j) / 2 + 1
        i = j + 1
    w = sum(r for x, r in zip(nz, ranks) if x > 0)
    n = len(nz)
    mu = n * (n + 1) / 4
    tie = sum(c ** 3 - c for c in Counter(abs(x) for x in nz).values())
    var = n * (n + 1) * (2 * n + 1) / 24 - tie / 48
    if var <= 0:
        return 0.0, 1.0
    z = (w - mu - (0.5 if w > mu else -0.5)) / var ** 0.5
    return z, min(1.0, erfc(abs(z) / 2 ** 0.5))


def mcnemar(b_only: int, a_only: int) -> float:
    n = b_only + a_only
    if not n:
        return 1.0
    k = min(b_only, a_only)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


# Below this many paired items, the exact test cannot reach p<0.05 no matter how one-sided the
# result: it needs >=6 one-directional flips. Reporting a p-value for a 10-item cell invites the
# reader to treat "not significant" as evidence of no effect, when the design simply cannot see one.
MIN_TESTABLE = 12


def report(base: list[dict], rich: list[dict], label: str, keys: list,
           primary: str = "wilcoxon") -> None:
    if not keys:
        return
    B = [consensus(base, k) for k in keys]
    R = [consensus(rich, k) for k in keys]
    pb, pr = sum(map(is_pass, B)), sum(map(is_pass, R))
    d = [b["_n_viol"] - r["_n_viol"] for b, r in zip(B, R)]   # +ve = rich has fewer
    nz = [x for x in d if x]
    up, dn = sum(1 for x in d if x > 0), sum(1 for x in d if x < 0)
    b_only = sum(1 for b, r in zip(B, R) if not is_pass(b) and is_pass(r))
    a_only = sum(1 for b, r in zip(B, R) if is_pass(b) and not is_pass(r))

    print(f"\n  {label}  (n={len(keys)})")
    print(f"    pass          base {pb:>3}   rich {pr:>3}   {pr-pb:+d}")
    print(f"    violations    {up} rows improved, {dn} worsened, {len(d)-len(nz)} unchanged"
          f"   mean {statistics.mean(d):+.2f}")
    if len(nz) >= 6:
        z, p = signed_rank(nz)
        print(f"    Wilcoxon      z={z:+.2f}  p={p:.4f}"
              + ("  significant" if p < 0.05 else "  not significant"))
    elif nz:
        print(f"    Wilcoxon      only {len(nz)} non-zero pairs — too few to test")
    p_mc = mcnemar(b_only, a_only)
    if primary == "mcnemar":
        # For a large expected effect the endpoint flips: pass/fail is the quantity the headline
        # claims, and violation counts are CENSORED in an unaugmented arm (a queue absent from the
        # catalog table makes _queue_limit return not_evaluated, so one bad queue costs one
        # violation instead of three). Counts would understate the degradation.
        verdict = ("too few paired items to test" if len(keys) < MIN_TESTABLE else
                   "significant" if p_mc < 0.05 else "not significant")
        print(f"    McNemar*      {b_only} {'\u2192'} pass, {a_only} {'\u2192'} fail, "
              f"exact p={p_mc:.2g}  {verdict}")
        if len(keys) < MIN_TESTABLE:
            print(f"                  (n={len(keys)}; the exact test needs >=6 one-directional "
                  f"flips, so no result here can clear 0.05)")
        return
    note = "" if p_mc < 0.05 else (f"  (needs >=6 one-directional flips; "
                                   f"have {b_only}/{a_only})")
    print(f"    McNemar       {b_only} fail->pass, {a_only} pass->fail, p={p_mc:.4f}{note}")
    uns = sum(1 for x in B + R if x["_unstable"])
    print(f"    unstable      {uns}/{len(B)+len(R)} rows flipped across replicates")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--judge", default="gpt56terra")
    ap.add_argument("--rubric", default="r27")
    ap.add_argument("--mode", choices=["skill", "hybrid"], default="skill")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--arms", default="base,rich",
                    help="the two arms to compare, least-augmented first")
    ap.add_argument("--score-rubric", default="r28",
                    help="replay the collected verdicts under this rubric before scoring "
                         "(default r28, matching audit.matrix and the HTML)")
    ap.add_argument("--primary", choices=["wilcoxon", "mcnemar"], default=None,
                    help="default: wilcoxon for base/rich (small effect), mcnemar otherwise")
    a = ap.parse_args()

    lo, hi = [x.strip() for x in a.arms.split(",")][:2]
    primary = a.primary or ("wilcoxon" if {lo, hi} == {"base", "rich"} else "mcnemar")
    base = load_runs(lo, a.judge, a.rubric, a.mode, a.runs, a.score_rubric)
    rich = load_runs(hi, a.judge, a.rubric, a.mode, a.runs, a.score_rubric)
    if not base or not rich:
        print(f"missing grades for {a.mode} mode at {a.rubric}; found "
              f"{len(base)} {lo} runs, {len(rich)} {hi} runs")
        return 1
    keys = sorted(set.intersection(*[set(m) for m in base + rich]))
    print(f"v8 A/B — {a.mode} mode, {a.judge}, collected {a.rubric}, scored {a.score_rubric}, "
          f"k={len(base)}/{len(rich)}")
    print(f"{len(keys)} paired rows judged in both arms")

    if {lo, hi} == {"base", "rich"}:
        # The control first: everything byte-identical across arms. Read the Input-prep result
        # against THIS, not against zero.
        report(base, rich, "CONTROL — subtasks identical in both arms",
               [k for k in keys if k[1] != ARM_SUBTASK], primary)
        report(base, rich, "TREATED — Input preparation, all anchors",
               [k for k in keys if k[1] == ARM_SUBTASK], primary)
        report(base, rich, "  of which: contract supplied (8 anchors)",
               [k for k in keys if k[1] == ARM_SUBTASK and (k[2], k[3]) not in SPARSE], primary)
        report(base, rich, "  of which: no contract, system context only (placebo)",
               [k for k in keys if k[1] == ARM_SUBTASK and (k[2], k[3]) in SPARSE], primary)
    else:
        # Every row differs, so there is NO within-experiment control stratum and no internal
        # estimate of sampling noise. Say it rather than let the reader assume one.
        print("\n  NOTE: these arms differ on every item, so this comparison has no "
              "byte-identical\n        control stratum. The noise floor must be imported: the "
              "base/rich control moved\n        4 rows on identical prompts, and 20 of 320 cells "
              "flip between judge replicates.")
        report(base, rich, f"ALL ITEMS — {lo} vs {hi}", keys, primary)
        # Clustering: 40 anchors x 4 models, and rows sharing an anchor share a prompt. Pooling
        # all 160 and quoting one p-value treats them as independent, so report per model too.
        for m in sorted({k[0] for k in keys}):
            report(base, rich, f"  model: {m}", [k for k in keys if k[0] == m], primary)
        for st in sorted({k[1] for k in keys}):
            report(base, rich, f"  stage: {st}", [k for k in keys if k[1] == st], primary)

    # Which rules moved — a delta that names its cause is actionable; a pass rate is not.
    ip = [k for k in keys if k[1] == ARM_SUBTASK] if {lo, hi} == {"base", "rich"} else keys
    ch = Counter()
    for k in ip:
        b, r = consensus(base, k), consensus(rich, k)
        for rid in set(b.get("requirements") or {}) | set(r.get("requirements") or {}):
            vb = (b.get("requirements") or {}).get(rid, {}).get("verdict")
            vr = (r.get("requirements") or {}).get(rid, {}).get("verdict")
            if vb != vr:
                ch[f"{rid}: {vb} -> {vr}"] += 1
    if ch:
        scope = "Input preparation" if {lo, hi} == {"base", "rich"} else "all stages"
        print(f"\n  requirement verdicts that moved ({scope}) — this is what turns a score "
              f"change into a finding:")
        for c, n in ch.most_common(12):
            print(f"    {n:>3}  {c}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
