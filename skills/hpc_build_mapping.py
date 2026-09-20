#!/usr/bin/env python3
"""Read the fundamental-skill → HPC-task mapping off the labeled instances.

The mapping is measured, not asserted: for HPC task T and fundamental skill S,

    share(T,S) = fraction of T's instances the classifier labeled with S

A cell counts as a real association at share >= MIN_SHARE and >= MIN_N instances, so one
stray label never creates an edge. Raw shares are always reported; the threshold only
governs what is drawn as an edge.

Two framings are profiled separately and compared:
  advisory  — a user asks the help desk a question; the model answers.
  execution — an agent must carry the task out: emit the script, issue the command, fix the
              directive. Advisory instances never invoke a tool or obey an output constraint,
              so reporting only advisory would understate what HPC work actually demands.

Also computes, per task, the *coverage* of its skill profile by our benchmark corpus. Skills
with almost no benchmark questions behind them (Tool use, Diagnosis, Code understanding,
Evidence evaluation) cannot support a trustworthy readiness score, so coverage is what makes
that visible instead of silently wrong — see hpc_readiness.py.

Usage:
    python skills/hpc_build_mapping.py
"""
from __future__ import annotations
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

HPC = ROOT / "results" / "skills" / "hpc"
FRAMINGS = {"advisory": HPC / "labels.jsonl", "execution": HPC / "labels_execution.jsonl"}
BENCH_LABELS = ROOT / "results" / "skills" / "labels_final.jsonl"
TAXONOMY = ROOT / "results" / "skills" / "taxonomy_v1.json"
OUT = HPC / "mapping.json"

# The two categories discovery added are dropped: they came from ALCF's doc structure rather
# than from the operational task list this analysis is for.
EXCLUDE_TASKS = {"Data management", "Environment and software"}

MIN_SHARE = 0.25     # a skill must appear on a quarter of a task's instances to count as an edge
MIN_N = 5            # ...and on at least this many, so tiny tasks can't manufacture edges
MEASURABLE_MIN = 30  # benchmark questions needed before a skill's model scores mean anything


def profile_framing(rows: list[dict], taxonomy: list[str], measurable: dict) -> dict:
    """Per-task skill shares, normalized profile, edges and coverage for one framing."""
    by_task: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        if r["hpc_task"] not in EXCLUDE_TASKS:
            by_task[r["hpc_task"]].append(r)

    tasks = {}
    for task, items in sorted(by_task.items()):
        counts = Counter(s for it in items for s in it["fundamental_skills"])
        n = len(items)
        shares = {s: counts[s] / n for s in taxonomy if counts[s]}
        total = sum(shares.values())
        profile = {s: v / total for s, v in shares.items()} if total else {}
        tasks[task] = {
            "n_instances": n,
            "counts": {s: counts[s] for s in shares},
            "shares": shares,
            "profile": profile,
            "edges": {s: v for s, v in shares.items() if v >= MIN_SHARE and counts[s] >= MIN_N},
            "coverage": sum(w for s, w in profile.items() if measurable[s]),
            "unmeasured": sorted(((s, w) for s, w in profile.items() if not measurable[s]),
                                 key=lambda kv: -kv[1]),
            "top_skills": sorted(shares.items(), key=lambda kv: -kv[1])[:8],
        }
    return tasks


def weighted_mean_share(framing: dict, skill: str) -> float:
    """Share of a skill across a whole framing, weighted by task instance count."""
    num = sum(t["shares"].get(skill, 0) * t["n_instances"] for t in framing.values())
    den = sum(t["n_instances"] for t in framing.values())
    return num / den if den else 0.0


def main() -> int:
    taxonomy = [t["name"] for t in json.loads(TAXONOMY.read_text())]

    # How much benchmark evidence stands behind each skill — decides what is measurable.
    bench_counts = Counter()
    for r in map(json.loads, BENCH_LABELS.open()):
        for s in r["fundamental_skills"]:
            bench_counts[s] += 1
    measurable = {s: bench_counts.get(s, 0) >= MEASURABLE_MIN for s in taxonomy}

    per_framing_rows = {name: [json.loads(l) for l in path.open()]
                        for name, path in FRAMINGS.items() if path.exists()}
    # "combined" is the headline view — a task's total skill demand, however it is asked.
    # The separate framings are kept for the advisory-vs-execution comparison only.
    all_rows = [r for rs in per_framing_rows.values() for r in rs]
    framings = {"combined": profile_framing(all_rows, taxonomy, measurable)}
    framings.update({name: profile_framing(rs, taxonomy, measurable)
                     for name, rs in per_framing_rows.items()})
    if not framings.get("combined"):
        print("no labeled instances found — run the generate + label steps first")
        return 1

    # Inverse index (edges only), per framing: which tasks demand a given skill.
    skill_to_tasks = {}
    for name, framing in framings.items():
        by_skill: dict[str, list] = defaultdict(list)
        for task, d in framing.items():
            for s, v in d["edges"].items():
                by_skill[s].append((task, round(v, 3)))
        skill_to_tasks[name] = {s: sorted(v, key=lambda kv: -kv[1])
                                for s, v in sorted(by_skill.items())}

    OUT.write_text(json.dumps({
        "min_share": MIN_SHARE, "min_n": MIN_N, "measurable_min": MEASURABLE_MIN,
        "taxonomy": taxonomy, "bench_counts": dict(bench_counts), "measurable": measurable,
        "framings": framings, "skill_to_tasks": skill_to_tasks,
    }, indent=1))

    n_all = sum(t["n_instances"] for f in framings.values() for t in f.values())
    print(f"{n_all} instances across {len(framings)} framings -> {OUT}")

    for name, framing in framings.items():
        print(f"\n=== {name.upper()} ===")
        print(f"{'HPC task':<26}{'n':>4}{'edges':>7}{'cover':>8}  top skills (share)")
        for task, d in sorted(framing.items(), key=lambda kv: kv[1]["coverage"]):
            top = ", ".join(f"{s} {v:.0%}" for s, v in d["top_skills"][:3])
            flag = "  <-- LOW" if d["coverage"] < 0.7 else ""
            print(f"{task:<26}{d['n_instances']:>4}{len(d['edges']):>7}"
                  f"{d['coverage']:>7.0%}  {top}{flag}")

    if len(framings) > 1:
        a, e = framings["advisory"], framings["execution"]
        print("\n=== ADVISORY vs EXECUTION: where the skill demand moves ===")
        deltas = [(s, weighted_mean_share(a, s), weighted_mean_share(e, s)) for s in taxonomy]
        deltas = [(s, av, ev, ev - av) for s, av, ev in deltas if av or ev]
        for s, av, ev, d in sorted(deltas, key=lambda x: -abs(x[3]))[:12]:
            print(f"  {'UP  ' if d > 0 else 'DOWN'} {s:<36} {av:5.0%} -> {ev:5.0%}  ({d:+.0%})")
        print("\n  coverage by framing:")
        for name, f in framings.items():
            cov = {t: d["coverage"] for t, d in f.items()}
            lo = min(cov, key=cov.get)
            print(f"    {name:<10} mean {sum(cov.values()) / len(cov):.0%}, "
                  f"lowest {lo} at {cov[lo]:.0%}")

    print("\n=== skills our corpus cannot measure, and the HPC weight resting on them ===")
    for s in taxonomy:
        if measurable[s]:
            continue
        for name, framing in framings.items():
            used = [(t, d["profile"].get(s, 0)) for t, d in framing.items()
                    if d["profile"].get(s, 0) > 0]
            if used:
                worst = max(used, key=lambda kv: kv[1])
                print(f"  {s:<24} bench_n={bench_counts.get(s, 0):<4} [{name:<9}] "
                      f"{len(used)} task(s), heaviest {worst[0]} at {worst[1]:.0%}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
