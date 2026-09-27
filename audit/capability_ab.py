#!/usr/bin/env python3
"""Paired comparison for the capability arms: does showing `gpu_support` change the answer?

WHY NOT `audit/ab.py`. That tool is specialised to the base-vs-rich Input-preparation A/B — it
hardcodes the `grades_v8{arm}` filename, pins `ARM_SUBTASK` to Input preparation, and carries a
sparse-anchor stratum that means nothing here. This experiment is Software selection on a v9
corpus, so it needs its own arithmetic rather than a tool bent out of shape.

THE DESIGN. Four arms over the same 39 anchors and the same two models, differing only by a
splice that `arm_capability --verify` proves reversible:

    base         the catalog listing as it has always been rendered
    fieldbool    every line gains  [gpu_support: true|false]
    fieldprose   every line gains  [GPU-accelerated build | CPU-only build; no GPU offload]
    contract     Instructions gain a clause forbidding unrecorded facility claims

PRIMARY ENDPOINT, fixed before the numbers were read: `SOFT.common.claims_true_to_catalog`
satisfied, on the 12 anchors whose correct application records `gpu_support: false` — 24 cells
at two models. Paired against `base` per (model, anchor), tested with an exact two-sided
McNemar. Everything else here is secondary or a guard rail.

GUARD RAIL, and it can fail the experiment on its own: `SOFT.common.correct_application` over
ALL 39 anchors. `task_spec.py` records that a v3 instruction of the `contract` arm's shape
taught models that a sparse catalog entry disqualifies a code, and wrong-application picks went
2/30 to 6/28. A treatment that fixes the claim and breaks the pick has not helped.

OVER-CORRECTION CHECK. The 26 anchors recording `gpu_support: true` are not padding. Tagging
every line invites a model to start denying GPU support where it exists, which contradicts the
catalog just as badly and would show up as `claims_true_to_catalog` getting WORSE on the true
anchors. Reported separately, never pooled with the treated cells.

Usage:
    python -m audit.capability_ab
    python -m audit.capability_ab --rules SOFT.common.no_vague_performance_claims
"""
from __future__ import annotations

import argparse
import collections
import json
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "corpus" / "v8"

ARMS = ("base", "fieldbool", "fieldprose", "contract")
PRIMARY = "SOFT.common.claims_true_to_catalog"
GUARD = "SOFT.common.correct_application"
SECONDARY = "SOFT.common.no_vague_performance_claims"


def _rows(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.open()] if path.exists() else []


def gpu_class() -> dict[tuple[str, str], object]:
    """(app, system) -> gpu_support, from the grading key frozen on each sample."""
    out = {}
    for r in _rows(CORPUS / "samples_v9base.jsonl"):
        out[(r["app"], r["system"])] = (r.get("grading_key") or {}).get("gpu_support")
    return out


def verdicts(arm: str, judge: str, rubric: str, runs: int) -> dict[tuple, dict[str, str]]:
    """(model, app, system) -> {rule: majority verdict over k replicates}.

    Majority, not any-run: re-judging identical answers moves ~7% of rows at k=3, so a single
    replicate is not a measurement. A rule with no majority is recorded as the modal verdict
    and counted in `unstable`.
    """
    acc: dict[tuple, dict[str, list[str]]] = collections.defaultdict(
        lambda: collections.defaultdict(list))
    for i in range(1, runs + 1):
        p = CORPUS / f"grades_v9{arm}__{judge}__{rubric}__SKILLMODE__run{i}.jsonl"
        for g in _rows(p):
            key = (g["model"], g["app"], g["system"])
            for rid, v in (g.get("requirements") or {}).items():
                acc[key][rid].append(v.get("verdict"))
    out: dict[tuple, dict[str, str]] = {}
    for key, rules in acc.items():
        out[key] = {rid: collections.Counter(vs).most_common(1)[0][0] for rid, vs in rules.items()}
    return out


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact McNemar on discordant pairs. b improved, c regressed."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(comb(n, i) for i in range(0, k + 1)) / (2 ** n)
    return min(1.0, 2 * tail)


def compare(base: dict, treat: dict, rule: str, keys: list[tuple]) -> dict:
    ok = lambda d, k: d.get(k, {}).get(rule) == "satisfied"      # noqa: E731
    have = [k for k in keys if k in base and k in treat and rule in base[k] and rule in treat[k]]
    b = sum(1 for k in have if not ok(base, k) and ok(treat, k))     # fixed
    c = sum(1 for k in have if ok(base, k) and not ok(treat, k))     # broken
    return {"n": len(have), "base": sum(ok(base, k) for k in have),
            "treat": sum(ok(treat, k) for k in have),
            "fixed": b, "broke": c, "p": mcnemar_exact(b, c)}


def line(label: str, r: dict) -> str:
    if not r["n"]:
        return f"    {label:<26} no comparable cells"
    return (f"    {label:<26} {r['base']:>3}/{r['n']:<3} -> {r['treat']:>3}/{r['n']:<3}"
            f"   fixed {r['fixed']:>2}  broke {r['broke']:>2}   p={r['p']:.3f}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--judge", default="gpt56terra")
    ap.add_argument("--rubric", default="r28")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--rules", default=f"{PRIMARY},{GUARD},{SECONDARY}")
    a = ap.parse_args()

    cls = gpu_class()
    V = {arm: verdicts(arm, a.judge, a.rubric, a.runs) for arm in ARMS}
    missing = [arm for arm in ARMS if not V[arm]]
    if missing:
        print(f"no grades for: {', '.join(missing)} — run judge.rejudge first")
        return 1

    allk = sorted(V["base"])
    treated = [k for k in allk if cls.get((k[1], k[2])) is False]
    control = [k for k in allk if cls.get((k[1], k[2])) is True]
    print(f"corpus v9 · {a.judge} · rubric {a.rubric} · k={a.runs} · arms {', '.join(ARMS)}")
    print(f"cells: {len(allk)} total, {len(treated)} treated (gpu_support:false), "
          f"{len(control)} control (true)\n")

    for rule in a.rules.split(","):
        short = rule.split(".")[-1]
        print(f"  {rule}")
        for arm in ARMS[1:]:
            scope = [("treated", treated), ("control-true", control), ("all", allk)] \
                if rule == PRIMARY else [("all anchors", allk)]
            for name, keys in scope:
                print(line(f"{arm} · {name}", compare(V["base"], V[arm], rule, keys)))
        print()

    print("  PRIMARY is the treated row of claims_true_to_catalog. GUARD is")
    print(f"  {GUARD} over all anchors: a treatment that")
    print("  breaks more picks than it fixes claims has not helped, whatever its p-value.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
