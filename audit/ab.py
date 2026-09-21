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


def load_runs(arm: str, judge: str, rubric: str, mode: str, runs: int) -> list[dict]:
    tag = "__SKILLMODE" if mode == "skill" else ""
    out = []
    for i in range(1, runs + 1):
        p = TRIN / f"grades_v8{arm}__{judge}__{rubric}{tag}__run{i}.jsonl"
        if p.exists():
            out.append({key(r): r for r in (json.loads(l) for l in p.open())})
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


def report(base: list[dict], rich: list[dict], label: str, keys: list) -> None:
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
    a = ap.parse_args()

    base = load_runs("base", a.judge, a.rubric, a.mode, a.runs)
    rich = load_runs("rich", a.judge, a.rubric, a.mode, a.runs)
    if not base or not rich:
        print(f"missing grades for {a.mode} mode at {a.rubric}; found "
              f"{len(base)} base runs, {len(rich)} rich runs")
        return 1
    keys = sorted(set.intersection(*[set(m) for m in base + rich]))
    print(f"v8 A/B — {a.mode} mode, {a.judge}, {a.rubric}, k={len(base)}/{len(rich)}")
    print(f"{len(keys)} paired rows judged in both arms")

    # The control first: everything that is byte-identical across arms. Read the Input-prep
    # result against THIS, not against zero.
    report(base, rich, "CONTROL — subtasks identical in both arms",
           [k for k in keys if k[1] != ARM_SUBTASK])
    report(base, rich, "TREATED — Input preparation, all anchors",
           [k for k in keys if k[1] == ARM_SUBTASK])
    report(base, rich, "  of which: contract supplied (8 anchors)",
           [k for k in keys if k[1] == ARM_SUBTASK and (k[2], k[3]) not in SPARSE])
    report(base, rich, "  of which: no contract, system context only (placebo)",
           [k for k in keys if k[1] == ARM_SUBTASK and (k[2], k[3]) in SPARSE])

    # Which rules moved — a delta that names its cause is actionable; a pass rate is not.
    ip = [k for k in keys if k[1] == ARM_SUBTASK]
    ch = Counter()
    for k in ip:
        b, r = consensus(base, k), consensus(rich, k)
        for rid in set(b.get("requirements") or {}) | set(r.get("requirements") or {}):
            vb = (b.get("requirements") or {}).get(rid, {}).get("verdict")
            vr = (r.get("requirements") or {}).get(rid, {}).get("verdict")
            if vb != vr:
                ch[f"{rid}: {vb} -> {vr}"] += 1
    if ch:
        print("\n  requirement verdicts that moved (Input preparation):")
        for c, n in ch.most_common(12):
            print(f"    {n:>3}  {c}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
