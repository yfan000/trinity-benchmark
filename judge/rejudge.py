#!/usr/bin/env python3
"""Grade a frozen corpus as (judge x rubric x replicate) cells, and diff two cells.

Two changes are on the table at once — the judge moves from claudeopus5 to gpt56terra, and the
rubric moves from prose (r0) to the requirement library (r1). Changing both together would
confound them, so each cell varies exactly one thing:

    v6 x claudeopus5 x r0     the existing baseline, reproduced
    v6 x gpt56terra  x r0     judge changed, rubric held
    v6 x gpt56terra  x r1     rubric changed, judge held

Every cell is run k times. The gating experiment measured the judge disagreeing with ITSELF:
re-judging identical answers under an identical config moved the pass rate 2.1 points and
flipped 12 of 141 verdicts, with Resource selection worst at 21%. A single run of a cell is
therefore not a measurement. k=3 with a per-dimension median is.

Cells are written to their own files, so a re-judge can never overwrite the rows it is meant
to be compared against — which is how the v2/v4/v6 grade rows came to be copies of each other.

Usage:
    python skills/trinity_rejudge.py --corpus v6 --judge gpt56terra --rubric r1 --runs 3
    python skills/trinity_rejudge.py --diff v6:claudeopus5:r0 v6:gpt56terra:r1
"""
from __future__ import annotations
import argparse
import json
import statistics
import sys
import threading
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from judge.client import JudgeError  # noqa: E402
from judge.checks import cache_get  # noqa: E402
from judge.grade import judge_one  # noqa: E402

TRIN = ROOT / "data" / "corpus" / "v8"


def cell_path(corpus: str, judge: str, rubric: str, run: int) -> Path:
    return TRIN / f"grades_{corpus}__{judge}__{rubric}__run{run}.jsonl"


def load(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.open()] if p.exists() else []


def key(r: dict) -> tuple:
    return (r["model"], r["subtask"], r["app"], r["system"])


def is_pass(g: dict) -> bool:
    return (g.get("correctness") == 2 and g.get("completeness") == 2
            and g.get("usability") == 2 and not g.get("fatal_error"))


def run_cell(corpus: str, judge: str, rubric: str, run: int, workers: int) -> None:
    samples = {(s["subtask"], s["app"], s["system"]): s
               for s in map(json.loads, (TRIN / f"samples_{corpus}.jsonl").open())}
    answers = [a for a in map(json.loads, (TRIN / f"answers_{corpus}.jsonl").open())
               if a.get("answer") and not a.get("error")]
    cp = TRIN / f"extracted_{corpus}.json"
    cache = json.loads(cp.read_text()) if cp.exists() else {}

    dest = cell_path(corpus, judge, rubric, run)
    have = {key(r) for r in load(dest)}
    todo = [a for a in answers if key(a) not in have]
    if not todo:
        print(f"  {judge}/{rubric} run{run}: complete ({len(have)} rows)")
        return
    print(f"  {judge}/{rubric} run{run}: {len(todo)} to judge -> {dest.name}", flush=True)

    lock, buf, done, failed = threading.Lock(), [], [0], [0]

    def one(a):
        s = samples[(a["subtask"], a["app"], a["system"])]
        ex = cache_get(cache, a["subtask"], a["model"], a["app"], a["system"])
        try:
            return a, judge_one(s, a["answer"], judge, rubric, ex)
        except JudgeError as e:
            return a, {"judge_failed": True, "error": str(e)}

    with ThreadPoolExecutor(max_workers=workers) as pool:
        for fut in as_completed([pool.submit(one, a) for a in todo]):
            a, v = fut.result()
            with lock:
                done[0] += 1
                # A judge failure is never written. Persisting it would score an
                # infrastructure problem as a model's zero.
                if v.get("judge_failed"):
                    failed[0] += 1
                else:
                    buf.append({**{k: a[k] for k in ("model", "subtask", "app", "system")},
                                "judge_run": run, **v})
                if len(buf) >= 5:
                    with dest.open("a") as f:
                        for r in buf:
                            f.write(json.dumps(r) + "\n")
                    buf.clear()
                if done[0] % 25 == 0:
                    print(f"     {done[0]}/{len(todo)}  ({failed[0]} judge failures)",
                          flush=True)
    with dest.open("a") as f:
        for r in buf:
            f.write(json.dumps(r) + "\n")
    print(f"     done: {len(load(dest))} rows, {failed[0]} judge failures")


def consensus(corpus: str, judge: str, rubric: str) -> dict[tuple, dict]:
    """Per-dimension median across replicates — the cell's actual verdict."""
    runs = defaultdict(list)
    for p in sorted(TRIN.glob(f"grades_{corpus}__{judge}__{rubric}__run*.jsonl")):
        for r in load(p):
            runs[key(r)].append(r)
    out = {}
    for k, rows in runs.items():
        med = {d: int(statistics.median([r[d] for r in rows]))
               for d in ("correctness", "completeness", "usability")}
        med["fatal_error"] = sum(bool(r.get("fatal_error")) for r in rows) > len(rows) / 2
        med["n_replicates"] = len(rows)
        med["unstable"] = any(len({r[d] for r in rows}) > 1
                              for d in ("correctness", "completeness", "usability"))
        med["subtask"], med["model"] = rows[0]["subtask"], rows[0]["model"]
        med["requirements"] = rows[0].get("requirements", {})
        out[k] = med
    return out


def _signed_ranks(nz: list[float]) -> list[float]:
    """Ranks of |x|, ties averaged. Scipy is not a dependency here."""
    order = sorted(range(len(nz)), key=lambda i: abs(nz[i]))
    ranks = [0.0] * len(nz)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and abs(nz[order[j + 1]]) == abs(nz[order[i]]):
            j += 1
        avg = (i + j) / 2 + 1
        for t in range(i, j + 1):
            ranks[order[t]] = avg
        i = j + 1
    return ranks


def _wilcoxon_z(nz: list[float]) -> float:
    """Normal approximation with a continuity correction and tie adjustment.

    n is around 38 here, comfortably inside where the approximation holds.
    """
    ranks = _signed_ranks(nz)
    w = sum(r for x, r in zip(nz, ranks) if x > 0)
    n = len(nz)
    mu = n * (n + 1) / 4
    tie = 0.0
    seen: dict[float, int] = {}
    for x in nz:
        seen[abs(x)] = seen.get(abs(x), 0) + 1
    for c in seen.values():
        tie += c ** 3 - c
    var = n * (n + 1) * (2 * n + 1) / 24 - tie / 48
    if var <= 0:
        return 0.0
    return (w - mu - (0.5 if w > mu else -0.5)) / (var ** 0.5)


def _wilcoxon_p(nz: list[float]) -> float:
    from math import erfc
    return min(1.0, erfc(abs(_wilcoxon_z(nz)) / (2 ** 0.5)))


def diff(a_spec: str, b_spec: str) -> int:
    (ca, ja, ra), (cb, jb, rb) = (s.split(":") for s in (a_spec, b_spec))
    A, B = consensus(ca, ja, ra), consensus(cb, jb, rb)
    common = sorted(set(A) & set(B))
    if not common:
        print(f"no overlap between {a_spec} and {b_spec}")
        return 1
    pa = sum(is_pass(A[k]) for k in common)
    pb = sum(is_pass(B[k]) for k in common)
    print(f"{a_spec}  vs  {b_spec}")
    print(f"  {len(common)} rows judged in both\n")
    print(f"  pass rate   {pa}/{len(common)} = {pa/len(common):.0%}   ->   "
          f"{pb}/{len(common)} = {pb/len(common):.0%}   ({(pb-pa)/len(common)*100:+.0f} pts)")

    # McNemar on the paired flips: the arms share items, so the discordant pairs are the
    # whole test. Comparing two independent proportions at n=159 would resolve nothing.
    b_only = [k for k in common if not is_pass(A[k]) and is_pass(B[k])]
    a_only = [k for k in common if is_pass(A[k]) and not is_pass(B[k])]
    n_dis = len(b_only) + len(a_only)
    print(f"  discordant  {n_dis}  ({len(b_only)} fail->pass, {len(a_only)} pass->fail)")
    if n_dis:
        from math import comb
        k_ = min(len(b_only), len(a_only))
        p = min(1.0, 2 * sum(comb(n_dis, i) for i in range(k_ + 1)) / 2 ** n_dis)
        # State the detection floor next to the p-value. With b one-directional flips the exact
        # p is 2/2^b, so b >= 6 is required to clear 0.05 no matter how real the effect is.
        # Reporting "not significant" without that is how a genuine 4-row shift gets written off.
        note = "  (significant at 0.05)"
        if p >= 0.05:
            # Say WHY it missed. With all flips one way, p = 2/2^n_dis, so 6 discordant pairs
            # is the floor; with a split, the imbalance has to be large enough on top of that.
            note = (f"  (not significant — {len(b_only)}/{len(a_only)} split. Even a perfect "
                    f"{n_dis}/0 split needs n>=6 to clear 0.05, so read this alongside the "
                    f"signed-rank test below rather than as evidence of no effect)")
        print(f"  McNemar exact p = {p:.4f}{note}")

    # PRIMARY ENDPOINT. Pass/fail throws away almost everything: Input preparation has no
    # minor-severity rules, so a single violation is a non-pass and a row that went from 6
    # violations to 1 counts the same as one that did not move. The violation COUNT per row
    # spans 0-10 with median 2, so the signed-rank test reads the whole distribution.
    d = []
    for k in common:
        na = sum(1 for q in (A[k].get("requirements") or {}).values()
                 if q.get("verdict") == "violated")
        nb = sum(1 for q in (B[k].get("requirements") or {}).values()
                 if q.get("verdict") == "violated")
        d.append(na - nb)                      # positive = B has fewer violations = better
    nz = [x for x in d if x]
    print(f"\n  violations/row   {sum(1 for x in d if x > 0)} improved, "
          f"{sum(1 for x in d if x < 0)} worsened, {len(d)-len(nz)} unchanged"
          f"   mean delta {statistics.mean(d):+.2f}")
    if len(nz) >= 6:
        ranks = _signed_ranks(nz)
        w_pos = sum(r for x, r in zip(nz, ranks) if x > 0)
        w_neg = sum(r for x, r in zip(nz, ranks) if x < 0)
        print(f"  Wilcoxon signed-rank  W+={w_pos:.0f} W-={w_neg:.0f}  "
              f"z={_wilcoxon_z(nz):+.2f}  p~{_wilcoxon_p(nz):.4f}")
    elif nz:
        print(f"  Wilcoxon signed-rank: only {len(nz)} non-zero pairs, too few to test")

    print(f"\n  {'subtask':<22}{'A pass':>8}{'B pass':>8}{'flips':>7}")
    for st in sorted({A[k]["subtask"] for k in common}):
        ks = [k for k in common if A[k]["subtask"] == st]
        print(f"  {st:<22}{sum(is_pass(A[k]) for k in ks):>8}"
              f"{sum(is_pass(B[k]) for k in ks):>8}"
              f"{sum(1 for k in ks if is_pass(A[k]) != is_pass(B[k])):>7}")

    for label, cell in ((a_spec, A), (b_spec, B)):
        uns = sum(1 for k in common if cell[k]["unstable"])
        reps = statistics.mean(cell[k]["n_replicates"] for k in common)
        print(f"\n  {label}: {reps:.1f} replicates/row, {uns}/{len(common)} rows unstable "
              f"across replicates")

    # Requirement-level diff — more actionable than a pass-rate delta, because it names the
    # rule that changed rather than the score.
    ch = Counter()
    for k in common:
        ra_, rb_ = A[k].get("requirements") or {}, B[k].get("requirements") or {}
        for rid in set(ra_) | set(rb_):
            va = (ra_.get(rid) or {}).get("verdict")
            vb = (rb_.get(rid) or {}).get("verdict")
            if va != vb:
                ch[f"{rid}: {va} -> {vb}"] += 1
    if ch:
        print("\n  requirement verdict changes (top 12):")
        for c, n in ch.most_common(12):
            print(f"    {n:>4}  {c}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="v6")
    ap.add_argument("--judge", default="gpt56terra")
    ap.add_argument("--rubric", default="r1")
    ap.add_argument("--runs", type=int, default=0)
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--diff", nargs=2, metavar=("A", "B"))
    a = ap.parse_args()
    if a.diff:
        return diff(*a.diff)
    if a.runs:
        print(f"corpus {a.corpus} x {a.judge} x {a.rubric}, {a.runs} replicates")
        for r in range(1, a.runs + 1):
            run_cell(a.corpus, a.judge, a.rubric, r, a.workers)
    cons = consensus(a.corpus, a.judge, a.rubric)
    if cons:
        p = sum(is_pass(v) for v in cons.values())
        print(f"\nconsensus: {p}/{len(cons)} pass = {p/len(cons):.0%}, "
              f"{sum(v['unstable'] for v in cons.values())} rows unstable")
    return 0


if __name__ == "__main__":
    sys.exit(main())
