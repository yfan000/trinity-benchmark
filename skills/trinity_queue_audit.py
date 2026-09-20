#!/usr/bin/env python3
"""Check every Resource-selection answer's allocation against the real queue limits.

This is an audit independent of the grading judge: the queue table comes from the catalog,
the answer's own choice is extracted structurally, and the comparison is arithmetic. If the
judge and this disagree, one of them is wrong and it is worth knowing which.

Usage:
    python skills/trinity_queue_audit.py --ver v2
"""
from __future__ import annotations
import argparse, json, re, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import judge  # noqa: E402
from skills import catalog  # noqa: E402
from skills.trinity_generate import CATALOG  # noqa: E402

TRIN = ROOT / "results" / "skills" / "trinity"

EXTRACT = """Read this HPC resource-sizing answer and extract what it finally requests.
If it gives several options, take the one it recommends. If a value is absent, use null.

Return ONLY JSON:
{{"queue": "<queue name or null>", "nodes": <int or null>,
  "walltime_seconds": <int or null>, "ranks_per_node": <int or null>}}

Answer:
{answer}"""


def queues(system: str) -> dict:
    return {k: q.raw for k, q in catalog.queues(system).items()}


def hms(sec) -> str:
    return f"{sec // 3600}h{(sec % 3600) // 60:02d}" if isinstance(sec, int) else "?"


def audit(ver: str, workers: int) -> None:
    G = [json.loads(l) for l in (TRIN / f"grades_{ver}.jsonl").open()]
    A = {(a["model"], a["subtask"], a["app"], a["system"]): a["answer"]
         for a in map(json.loads, (TRIN / f"answers_{ver}.jsonl").open()) if a.get("answer")}
    rows = [g for g in G if g["subtask"] == "Resource selection"]

    def one(g):
        ans = A.get((g["model"], g["subtask"], g["app"], g["system"]))
        if not ans:
            return None
        try:
            msg = judge._get_client().with_options(timeout=300).messages.create(
                model=judge.TRINITY_JUDGE_MODEL, max_tokens=2500,
                messages=[{"role": "user", "content": EXTRACT.format(answer=ans[:9000])}])
            m = re.search(r"\{.*\}", judge._text_of(msg), re.DOTALL)
            return g, (json.loads(m.group()) if m else None)
        except Exception:
            return g, None

    out = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for fut in as_completed([pool.submit(one, g) for g in rows]):
            r = fut.result()
            if r and r[1]:
                out.append(r)

    stats = {"parsed": 0, "queue_unknown": 0, "walltime_over": 0, "nodes_over": 0,
             "nodes_under": 0, "ok": 0}
    bad = []
    for g, x in out:
        qs = queues(g["system"])
        q, wt, nd = x.get("queue"), x.get("walltime_seconds"), x.get("nodes")
        stats["parsed"] += 1
        if not q or q not in qs:
            stats["queue_unknown"] += 1
            bad.append((g, q, wt, nd, None, "queue not in this system's table"))
            continue
        lim, probs = qs[q], []
        if isinstance(wt, int) and lim.get("max_walltime") and wt > lim["max_walltime"]:
            stats["walltime_over"] += 1
            probs.append(f"walltime {hms(wt)} > cap {hms(lim['max_walltime'])}")
        if isinstance(nd, int) and lim.get("max_nodes") and nd > lim["max_nodes"]:
            stats["nodes_over"] += 1
            probs.append(f"nodes {nd} > max {lim['max_nodes']}")
        if isinstance(nd, int) and lim.get("min_nodes") and nd < lim["min_nodes"]:
            stats["nodes_under"] += 1
            probs.append(f"nodes {nd} < min {lim['min_nodes']}")
        if probs:
            bad.append((g, q, wt, nd, lim, "; ".join(probs)))
        else:
            stats["ok"] += 1

    print(f"\n=== {ver}: {stats['parsed']} Resource-selection answers audited "
          f"against the catalog queue table ===")
    print(f"  legal on every limit        {stats['ok']}")
    print(f"  walltime over the cap       {stats['walltime_over']}")
    print(f"  node count out of range     {stats['nodes_over'] + stats['nodes_under']}")
    print(f"  queue not on that system    {stats['queue_unknown']}")
    if bad:
        print(f"\n  {len(bad)} illegal requests:")
        for g, q, wt, nd, lim, why in sorted(bad, key=lambda b: b[0]["model"]):
            passed = (g["correctness"] == 2 and g["completeness"] == 2
                      and g["usability"] == 2 and not g["fatal_error"])
            print(f"    {g['model']:16} {g['app']:9}@{g['system']:10} q={str(q):14} "
                  f"{why:46} judge_passed={passed}")
    miss = sum(1 for g, x in out if not x.get("queue"))
    print(f"\n  (answers naming no queue at all: {miss})")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ver", default="v2")
    ap.add_argument("--workers", type=int, default=5)
    a = ap.parse_args()
    audit(a.ver, a.workers)
    return 0


if __name__ == "__main__":
    sys.exit(main())
