#!/usr/bin/env python3
"""Re-derive the per-model x subtask matrix from the shipped grades, under any rubric.

WHY THIS EXISTS. The published table is r28; the shipped grades were produced under r27. Those
are not the same number, and the difference is not cosmetic: r28 retired
INP.common.not_copied_from_example, which fired on 18 of 40 Input-preparation rows and was a
false positive in roughly three quarters of them. Re-judging under r28 would cost 960 judge
calls and introduce fresh sampling noise on top of the change being measured.

It does not have to. Scores are derived in Python from the per-requirement verdicts
(`judge.grade.derive_scores`), so a rubric change that only REMOVES rules or only changes
severities can be replayed offline against verdicts already collected — the judge was asked the
same questions, and the retired one is simply not counted. That is exactly what this does, and
it is why the arithmetic was moved out of the judge in the first place.

WHAT IT REFUSES TO DO. If the target rubric contains a rule the grades have no verdict for, the
answer cannot be derived from this corpus and the tool says so and exits non-zero rather than
scoring the row as though the missing rule had passed. `--allow-missing` reports the affected
rules and continues instead, for exploring a draft rubric.

Usage:
    python -m audit.matrix                       # the published table: r27 grades replayed at r28
    python -m audit.matrix --rubric r27          # as graded, no replay
    python -m audit.matrix --per-arm --rules
    python -m audit.matrix --demote BATCH.common.no_directive_comments   # price a severity change
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

import yaml

from judge.grade import derive_scores
from judge.skills.loader import load as load_skill

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "data" / "corpus" / "v8"
GRADED_UNDER = "r27"                       # what the shipped grade files were produced under
SUBTASKS = ["Software selection", "Input preparation",
            "Resource selection", "Batch job creation"]
# The published table is two arms, but the augmentation ablation adds `bare` and `cat`. Arms are a
# parameter everywhere below: two of them were once baked into the arithmetic, so every denominator
# silently assumed exactly two prompt variants per item.
DEFAULT_ARMS = ("base", "rich")

# The knowledge-dependence view (rubric id r29-capability), registered before the unaugmented arms
# were answered. Restricting to `knowledge` separates "it does not know our queue names" from "it
# cannot write a valid deck"; it is a second aggregation of the same verdicts, never a re-judge.
_KD = ROOT / "judge" / "skills" / "knowledge_dependence.yaml"


def rule_classes() -> dict[str, str]:
    d = yaml.safe_load(_KD.read_text()) if _KD.exists() else {}
    return {k: v["class"] for k, v in (d.get("rules") or {}).items()}


def _grade_files(arm: str, judge: str, rubric: str, mode: str, runs: int) -> list[Path]:
    tag = "__SKILLMODE" if mode == "skill" else ""
    return [CORPUS / f"grades_v8{arm}__{judge}__{rubric}{tag}__run{i}.jsonl"
            for i in range(1, runs + 1)]


def _is_pass(r: dict) -> bool:
    return (r.get("correctness") == 2 and r.get("completeness") == 2
            and r.get("usability") == 2 and not r.get("fatal_error"))


def replay(row: dict, rubric: str, demote: frozenset[str] = frozenset(),
           view: str = "all") -> tuple[dict, set[str]]:
    """Re-derive one row's scores under `rubric`. Returns (row, rules with no verdict).

    `demote` forces the named rules to `minor` for this derivation only, without touching the
    library. It exists so a proposed severity change can be PRICED before it is made — the v8
    table was published with BATCH.common.no_directive_comments silently treated as minor while
    the YAML said major, which is how the headline drifted from anything the repo could produce.
    """
    skill = load_skill(row["subtask"], row.get("app"), row.get("system"), rubric_id=rubric)
    if view != "all":
        keep = {k for k, c in rule_classes().items() if c in view.split("+")}
        skill.requirements = [q for q in skill.requirements if q["id"] in keep]
    if demote:
        skill.requirements = [dict(q, severity="minor") if q["id"] in demote else q
                              for q in skill.requirements]
    have = row.get("requirements") or {}
    wanted = {r["id"] for r in skill.requirements}
    # Keep only verdicts the target rubric still asks for; a retired rule stops counting.
    merged = {rid: v for rid, v in have.items() if rid in wanted}
    out = dict(row)
    out["requirements"] = merged
    out.update(derive_scores(merged, skill))
    return out, wanted - set(have)


class Result:
    """Everything a caller needs: the matrix, what failed, and what evidence said so.

    `tools/build_report.py` renders the published report from exactly this object, so the
    report and `python -m audit.matrix` cannot disagree — the bug that produced a published
    table no shipped tool could reproduce.
    """

    def __init__(self, arms=DEFAULT_ARMS) -> None:
        self.arms = tuple(arms)
        self.npass: collections.Counter = collections.Counter()   # (model, subtask, arm)
        self.ntot: collections.Counter = collections.Counter()
        self.cost: collections.Counter = collections.Counter()    # rule -> failing cells
        self.bysub: dict = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
        self.ev: dict = {}                                        # "model|rule" -> [app, evidence]
        self.sev: dict = {}                                       # rule -> severity
        self.missing: set[str] = set()
        self.unstable = 0
        self.cells = 0

    def total(self, model: str, subtasks=SUBTASKS) -> tuple[int, int]:
        return (sum(self.npass[(model, s, a)] for s in subtasks for a in self.arms),
                sum(self.ntot[(model, s, a)] for s in subtasks for a in self.arms))

    def models(self) -> list[str]:
        """Strongest first — the report leads with the recommendation, not the alphabet."""
        ms = {k[0] for k in self.ntot}
        return sorted(ms, key=lambda m: -self.total(m)[0] / max(1, self.total(m)[1]))


def compute(rubric: str = "r28", judge: str = "gpt56terra", mode: str = "skill",
            runs: int = 3, demote: frozenset[str] = frozenset(),
            arms=DEFAULT_ARMS, view: str = "all") -> Result:
    """Score every cell by MAJORITY of the k replicates.

    Majority, not the mean, and not floor(total passes / k). The published v8 table was built
    with floor(sum/3), which is an average dressed as a count: it let a cell that passed one run
    of three contribute a third of a pass to its column. Every other consumer of this corpus —
    `audit.ab`, the traces page, the oracle — takes the majority verdict, and mixing the two put
    six rows of daylight between two numbers that claimed to measure the same thing.
    """
    R = Result(arms)
    replaying = rubric != GRADED_UNDER or bool(demote) or view != "all"
    for arm in R.arms:
        M = []
        for p in _grade_files(arm, judge, GRADED_UNDER, mode, runs):
            if not p.exists():
                raise FileNotFoundError(f"missing {p}")
            M.append({(r["model"], r["subtask"], r["app"], r["system"]): r
                      for r in map(json.loads, p.open())})
        for k in sorted(set.intersection(*[set(m) for m in M])):
            mdl, st, app, _sys = k
            votes, blame, first = [], collections.Counter(), {}
            for m in M:
                r = m[k]
                if replaying:
                    r, miss = replay(r, rubric, demote, view)
                    R.missing |= miss
                votes.append(_is_pass(r))
                for rid, v in (r.get("requirements") or {}).items():
                    if v.get("verdict") == "violated":
                        blame[rid] += 1
                        first.setdefault(rid, v.get("evidence", ""))
            R.cells += 1
            R.unstable += len(set(votes)) > 1
            passed = sum(votes) > len(votes) / 2
            R.ntot[(mdl, st, arm)] += 1
            R.npass[(mdl, st, arm)] += passed
            skill = load_skill(st, app, _sys, rubric_id=rubric)
            R.sev.update({q["id"]: ("minor" if q["id"] in demote else q.get("severity", "major"))
                          for q in skill.requirements})
            for rid, n in blame.items():
                if n <= len(votes) / 2:            # a one-of-three verdict is noise, not a finding
                    continue
                R.bysub[mdl][st][rid] += 1
                R.ev.setdefault(f"{mdl}|{rid}", [app, first.get(rid, "")])
                if not passed:
                    R.cost[rid] += 1
    return R


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rubric", default="r28", help="rubric to score under (default r28)")
    ap.add_argument("--judge", default="gpt56terra")
    ap.add_argument("--mode", choices=["skill", "hybrid"], default="skill")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--per-arm", action="store_true", help="split the arms out")
    ap.add_argument("--view", default="all",
                    help="all | knowledge | knowledge+mixed | supplied — restrict scoring to one "
                         "knowledge-dependence class (r29-capability)")
    ap.add_argument("--arms", default=",".join(DEFAULT_ARMS),
                    help="comma-separated prompt arms to score (default: the published pair)")
    ap.add_argument("--rules", action="store_true", help="list the rules that cost most passes")
    ap.add_argument("--demote", action="append", default=[], metavar="RULE",
                    help="score this rule as minor without editing the library, to price a "
                         "proposed severity change (repeatable)")
    ap.add_argument("--allow-missing", action="store_true",
                    help="continue when the target rubric has rules the grades never judged")
    a = ap.parse_args()

    try:
        arms = tuple(x.strip() for x in a.arms.split(",") if x.strip())
        R = compute(a.rubric, a.judge, a.mode, a.runs, frozenset(a.demote), arms, a.view)
    except FileNotFoundError as e:
        print(e)
        return 1
    npass, ntot, cost, missing = R.npass, R.ntot, R.cost, R.missing
    replaying = a.rubric != GRADED_UNDER

    if missing:
        print(f"{a.rubric} asks {len(missing)} rule(s) the {GRADED_UNDER} grades never judged:")
        for rid in sorted(missing):
            print(f"    {rid}")
        if not a.allow_missing:
            print("  these rows cannot be scored from this corpus — re-judge, or pass "
                  "--allow-missing to treat them as unasked")
            return 2
        print("  --allow-missing: scoring as though the rule were not in the rubric\n")

    arms = list(R.arms) if a.per_arm else [None]
    print(f"corpus v8 - {a.judge}, {a.mode} mode, k={a.runs}, scored under {a.rubric}"
          + (f" (grades collected under {GRADED_UNDER}, replayed offline)"
             if a.rubric != GRADED_UNDER else ""))
    if a.view != "all":
        cl = rule_classes()
        kept = sum(1 for c in cl.values() if c in a.view.split("+"))
        print(f"    view: {a.view} — {kept} of {len(cl)} rules scored (r29-capability)")
    if a.demote:
        base = compute(a.rubric, a.judge, a.mode, a.runs, arms=R.arms)
        for rid in a.demote:
            print(f"    counterfactual: {rid} scored as minor; the library says "
                  f"{base.sev.get(rid, '?')}")
        b = sum(base.npass.values())
        print(f"    without the override the total is {b}/{sum(base.ntot.values())}")
    for arm in arms:
        sel = [arm] if arm else list(R.arms)
        print(f"\n  {'arm ' + arm if arm else 'both arms'}")
        print(f"    {'model':<20}" + "".join(f"{s.split()[0]:>12}" for s in SUBTASKS) + f"{'total':>14}")
        grand = gt = 0
        col, coln = collections.Counter(), collections.Counter()
        for mdl in sorted({k[0] for k in ntot}):
            cells = [sum(npass[(mdl, s, x)] for x in sel) for s in SUBTASKS]
            tots = [sum(ntot[(mdl, s, x)] for x in sel) for s in SUBTASKS]
            for s, c, n in zip(SUBTASKS, cells, tots):
                col[s] += c
                coln[s] += n
            grand += sum(cells)
            gt += sum(tots)
            pct = 100 * sum(cells) / max(1, sum(tots))
            tail = f"{sum(cells)}/{sum(tots)} - {pct:.0f}%"
            print(f"    {mdl:<20}" + "".join(f"{c:>12}" for c in cells) + f"{tail:>16}")
        tail = f"{grand}/{gt} - {100 * grand / max(1, gt):.0f}%"
        print(f"    {'all models':<20}"
              + "".join(f"{col[s]}/{coln[s]}".rjust(12) for s in SUBTASKS)
              + f"{tail:>16}")

    if a.rules:
        print("\n  rules that a failing cell most often violated (majority of replicates):")
        for rid, n in cost.most_common(15):
            print(f"    {n:>3}  {rid}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
