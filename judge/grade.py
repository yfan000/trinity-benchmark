#!/usr/bin/env python3
"""Judge one answer against the requirement library, not against a reference answer.

The old judge was handed a prose reference and told to grade against it — an invitation to
score similarity. This one rules on each requirement separately, and the 0-2 dimension scores
are DERIVED from those verdicts by a stated rule, so a score can always be traced back.

Three things differ from judge.judge_trinity:

  1. Deterministic requirements are already decided (judge/checks.py). They arrive as
     settled facts. The judge only adjudicates the residual — about 15 of 50 requirements —
     which is what takes them out of the 2.1-point judge-sampling spread.
  2. The reference answer is demoted to an exemplar, explicitly ONE correct answer rather than
     THE correct answer, with free_choice axes listed so a different-but-valid answer cannot
     be marked down for differing.
  3. Ground truth is rendered in labelled sections with per-section budgets, not serialised
     into one JSON blob and clipped at 3000 characters. That clip silently removed up to 57%
     of the reference on 16 of 40 v6 samples, always the reference because it sorted last.

Usage:
    python skills/trinity_judge.py --corpus v6 --judge gpt56terra --limit 3
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from string import Template

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from judge.client import JudgeError, complete, parse_json  # noqa: E402
from judge.skills.loader import load as load_skill  # noqa: E402
from benchmark import catalog
from judge.checks import (evaluate as run_checks, guard_blocks,  # noqa: E402
                                   cache_get)
from benchmark.generate import CATALOG, app_yaml, grading_key, scheduler  # noqa: E402
from benchmark.task_spec import SUBTASKS  # noqa: E402

TRIN = ROOT / "data" / "corpus" / "v8"

_FC = ROOT / "judge" / "skills" / "format_contracts.yaml"
FORMAT_CONTRACTS = (yaml.safe_load(_FC.read_text()) or {}).get("contracts", {}) \
    if _FC.exists() else {}

# Per-section budgets. The catalog is small and never clipped; the exemplar is the only thing
# that may be, and when it is, the judge is told so rather than left to infer it.
BUDGET = {"prompt": 4500, "answer": 9000, "catalog": 2500, "exemplar": 3500}


def clip(s: str, n: int, label: str) -> str:
    s = s or ""
    return s if len(s) <= n else s[:n] + f"\n[... {label} clipped, {len(s)-n} chars omitted]"


# `string.Template` rather than str.format: the prompt carries a JSON schema, and .format
# would require doubling every brace in it (judge.py:685 already does this and it is a trap).
PROMPT = Template("""You are grading one attempt at an HPC agent subtask. This decides whether
a cheaper model can be trusted with this step of a real pipeline, so be strict and concrete.

Subtask: $subtask — $goal
Target system: $system (scheduler: $sched)

The model answered through a plain chat API with no filesystem, no shell and no access to the
machine. Never penalise it for not creating files, not running anything, or not verifying a
path. Emitting correct file contents as text is a complete answer.

=== THE PROMPT THE MODEL WAS GIVEN ===
$prompt

=== THE MODEL'S ANSWER ===
$answer

=== CATALOG FACTS (authoritative, machine-read from the facility's YAML) ===
$catalog

=== EXEMPLAR — ONE correct answer, not THE correct answer ===
$exemplar

$requirements

=== ALREADY DECIDED (checked in code; treat as settled, do not re-litigate) ===
$checks

HOW TO GRADE

Rule on every requirement listed above that is not already decided. For each, give a verdict
of "satisfied", "violated" or "not_applicable", and one line of evidence quoting what in the
answer decided it.

PRECEDENCE when sources conflict — the earlier wins:
  1. CATALOG FACTS   authoritative about what EXISTS: module names, binaries, which file
                     types are required, queue limits. NOT authoritative that a particular
                     filename, working directory or command form is the only valid one. The
                     catalog records examples as well as constraints, it omits reservation
                     queues, and three of its files do not parse. Where it gives an example
                     path or filename, an answer that uses a different one is NOT wrong.
  2. REQUIREMENTS    each carries its own source; a requirement sourced "model" is a strong
                     prior, not a fact.
  3. EXEMPLAR        one correct answer among several. NEVER deduct for differing from it
                     where the requirements are met and the free-choice axes permit it.

Do NOT compute any scores. Report verdicts only; the scores are calculated from them in code.

Respond with ONLY this JSON:
{"requirements": [{"id": "...", "verdict": "satisfied|violated|not_applicable",
                   "evidence": "..."}],
 "note": "<one sentence>"}""")


def derive_scores(merged: dict, skill) -> dict:
    """Compute the 0-2 scores from the verdicts, in Python.

    This was originally stated in the prompt and left to the judge — which reintroduced
    exactly the sampling noise the deterministic layer exists to remove. Measured on three
    replicates of the gpt56terra/r1 cell: 19 of 159 rows had differing SCORES while every
    requirement verdict agreed. Same inputs, different arithmetic. So the arithmetic moves
    here, where it cannot vary.

    Minor violations do not block a 2. The first version treated any violation as capping the
    dimension at 1, and one over-eager minor requirement (self_check_demonstrated, firing on
    35 of 40 Input-preparation answers) made a pass arithmetically impossible for that whole
    subtask.
    """
    sev = {r["id"]: r.get("severity", "major") for r in skill.requirements}
    dim = {r["id"]: r.get("dimension") for r in skill.requirements}
    viol = [rid for rid, v in merged.items() if v.get("verdict") == "violated"]
    fatal = [rid for rid in viol if sev.get(rid) == "fatal"]

    def score(d: str) -> int:
        bad = [r for r in viol if dim.get(r) == d]
        if any(sev.get(r) == "fatal" for r in bad):
            return 0
        if any(sev.get(r) == "major" for r in bad):
            return 1
        return 2                      # only minor violations, or none

    out = {"correctness": score("correctness"), "completeness": score("completeness"),
           "usability": 0 if fatal else score("usability"), "fatal_error": bool(fatal)}
    if fatal:
        why = f"fatal: {', '.join(sorted(fatal)[:3])}"
    elif viol:
        maj = [r for r in viol if sev.get(r) == "major"]
        why = (f"{len(maj)} major, {len(viol)-len(maj)} minor violations"
               + (f" ({', '.join(sorted(maj)[:3])})" if maj else ""))
    else:
        why = "no requirement violated"
    out["derivation"] = why
    return out


def render_catalog(system: str, app: str, subtask: str) -> str:
    spec = SUBTASKS[subtask]
    key = grading_key(system, app, spec["key_fields"])
    lines = [f"{k}: {json.dumps(v) if not isinstance(v, str) else v}"
             for k, v in key.items()]
    qs = {k: q.raw for k, q in catalog.queues(system).items()}
    if qs and subtask in ("Resource selection", "Batch job creation"):
        lines.append("queues: " + "; ".join(
            f"{q}(nodes {v.get('min_nodes','?')}-{v.get('max_nodes','?')}, "
            f"max walltime {v.get('max_walltime',0)//3600}h)" for q, v in list(qs.items())[:8]))
    return clip("\n".join(lines), BUDGET["catalog"], "catalog")


def render_checks(checks: dict) -> str:
    if not checks:
        return "(none — every requirement for this subtask needs judgement)"
    out = []
    for rid, v in sorted(checks.items(), key=lambda kv: kv[1]["verdict"] != "violated"):
        if v["verdict"] in ("not_evaluated",):
            continue                     # falls through to the judge; do not assert it passed
        out.append(f"  [{rid}] {v['verdict'].upper()} — {v['evidence']}")
    return "\n".join(out) or "(nothing decidable in code for this answer)"


def judge_one(sample: dict, answer: str, judge_id: str = "gpt56terra",
              rubric_id: str = "r1", extracted: dict | None = None) -> dict:
    st, app, system = sample["subtask"], sample["app"], sample["system"]
    spec = SUBTASKS[st]
    skill = load_skill(st, app, system, rubric_id=rubric_id)
    checks = run_checks(st, app, system, answer, extracted)

    decided = {k for k, v in checks.items() if v["verdict"] != "not_evaluated"}
    # Guards apply to judged requirements as well. Asking the judge to rule on a requirement
    # that does not apply invites it to invent a defect, which is what happened to vLLM.
    guarded = {}
    for r in skill.requirements:
        why = guard_blocks(r, app, system)
        if why and r["id"] not in decided:
            guarded[r["id"]] = {"verdict": "not_applicable", "evidence": why,
                                "decided_by": "guard"}
    open_reqs = [r for r in skill.requirements
                 if r["id"] not in decided and r["id"] not in guarded]
    block = ("REQUIREMENTS you must rule on:\n" + "\n".join(
        f"  [{r['id']}]  ({r.get('severity','major')}, affects {r.get('dimension','?')})\n"
        f"      {' '.join(str(r['claim']).split())}" for r in open_reqs))
    if skill.free_choice:
        block += ("\n\nFREE CHOICE — the answer may differ from the exemplar on these axes.\n"
                  "Never deduct for any of them:\n" + "\n".join(
                      f"  - {f['axis']}: {' '.join(str(f['note']).split())}"
                      for f in skill.free_choice))

    prompt = PROMPT.safe_substitute(
        subtask=st, goal=spec["goal"], system=system, sched=scheduler(system),
        prompt=clip(sample["prompt"], BUDGET["prompt"], "prompt"),
        answer=clip(answer, BUDGET["answer"], "answer"),
        catalog=render_catalog(system, app, st),
        exemplar=clip(sample.get("reference", "(none supplied)"), BUDGET["exemplar"],
                      "exemplar"),
        requirements=block, checks=render_checks(checks))

    text, meta = complete(judge_id, prompt)
    v = parse_json(text, require="requirements")
    if not isinstance(v, dict) or "requirements" not in v:
        raise JudgeError(f"unparseable reply ({len(text)} chars)")

    # Merge: code-decided verdicts are authoritative and overwrite anything the judge said
    # about them. The judge cannot overrule arithmetic.
    merged = {rid: {k: x[k] for k in ("verdict", "evidence")} | {"decided_by": "deterministic"}
              for rid, x in checks.items() if x["verdict"] != "not_evaluated"}
    merged.update(guarded)
    for r in v.get("requirements") or []:
        if r.get("id") and r["id"] not in merged:
            merged[r["id"]] = {"verdict": r.get("verdict"), "evidence": r.get("evidence", ""),
                               "decided_by": "judge"}

    scores = derive_scores(merged, skill)
    return {
        **scores,
        "requirements": merged, "note": str(v.get("note", ""))[:300],
        # everything needed to know what produced this row
        "judge_model": judge_id, "judge_provider": meta["provider"],
        "judge_params": {"max_tokens": meta["max_tokens"],
                         "temperature": meta["temperature"]},
        "rubric_id": rubric_id, "rubric_sha256": skill.rubric_sha256,
        "n_deterministic": len(decided), "n_judged": len(open_reqs),
        "checks_unevaluated": sum(1 for x in checks.values()
                                  if x["verdict"] == "not_evaluated"),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="v6")
    ap.add_argument("--judge", default="gpt56terra")
    ap.add_argument("--rubric", default="r1")
    ap.add_argument("--limit", type=int, default=3)
    ap.add_argument("--subtask")
    a = ap.parse_args()

    samples = {(s["subtask"], s["app"], s["system"]): s
               for s in map(json.loads, (TRIN / f"samples_{a.corpus}.jsonl").open())}
    rows = [json.loads(l) for l in (TRIN / f"answers_{a.corpus}.jsonl").open()
            if json.loads(l).get("answer")]
    if a.subtask:
        rows = [r for r in rows if r["subtask"] == a.subtask]
    cp = TRIN / f"extracted_{a.corpus}.json"
    cache = json.loads(cp.read_text()) if cp.exists() else {}

    for r in rows[:a.limit]:
        s = samples[(r["subtask"], r["app"], r["system"])]
        try:
            v = judge_one(s, r["answer"], a.judge, a.rubric,
                          cache_get(cache, r["subtask"], r["model"], r["app"], r["system"]))
        except JudgeError as e:
            print(f"{r['model']:<18}{r['subtask'][:16]:<17}{r['app']:<10} JUDGE FAILED: {e}")
            continue
        viol = [k for k, x in v["requirements"].items() if x["verdict"] == "violated"]
        print(f"{r['model']:<18}{r['subtask'][:16]:<17}{r['app']:<10}"
              f"c{v['correctness']} p{v['completeness']} u{v['usability']}"
              f"{' FATAL' if v['fatal_error'] else '      '}  "
              f"{v['n_deterministic']}det/{v['n_judged']}judged  rubric {v['rubric_sha256']}")
        if v["derivation"]:
            print(f"    derivation: {v['derivation'][:110]}")
        for k in viol[:4]:
            print(f"    violated  {k:<40} {v['requirements'][k]['evidence'][:58]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())


# ---------------------------------------------------------------------------------------
# SKILL MODE — the judge rules on EVERY requirement, and is handed the skill itself.
#
# The default mode decides 274 of 378 rule applications in Python and gives the judge the
# residual as settled fact. That was chosen to keep the three named failure modes off the
# judge's sampling-noise budget (12 of 141 verdicts flip across identical replicates).
#
# It has a measured cost. Every prompt defect found in review was a CODE rule confidently
# wrong the same way on every sample: content_markers_present demanding the amino-acid
# alphabet inside a FASTA (19 of 38 rows), exact_filenames_used failing a correct
# `lysozyme.gro`, grid_matches_ranks grading a different subtask's answer. A reader would
# have caught all three; a string match cannot. And 170 of 378 applications are text-pattern
# checks — reading comprehension written as regex.
#
# So this mode hands the judge the requirement library verbatim, check definitions included,
# and asks it to rule on everything. The Python checks still run, but their verdicts are NOT
# shown to the judge; they are recorded alongside so the two can be compared on identical
# answers. That comparison is the point — without it, swapping the mechanism would replace
# one unmeasured approach with another.
# ---------------------------------------------------------------------------------------

SKILL_PROMPT = Template("""You are grading one attempt at an HPC agent subtask. This decides
whether a cheaper model can be trusted with this step of a real pipeline, so be strict and
concrete.

Subtask: $subtask — $goal
Target system: $system (scheduler: $sched)

The model answered through a plain chat API with no filesystem, no shell and no access to the
machine. Never penalise it for not creating files, not running anything, or not verifying a
path. Emitting correct file contents as text is a complete answer.

=== THE PROMPT THE MODEL WAS GIVEN ===
$prompt

=== THE MODEL'S ANSWER ===
$answer

=== CATALOG FACTS (authoritative, machine-read from the facility's YAML) ===
$catalog

=== EXEMPLAR — ONE correct answer, not THE correct answer ===
$exemplar

=== THE GRADING SKILL — the requirement library, verbatim ===

This is the actual YAML this project grades with. Every requirement carries its claim, the
severity it would apply, the dimension it affects, where it came from, and often a `check:`
block describing how the project would test it mechanically.

Read `check:` as a description of INTENT, not as an instruction to pattern-match. Several of
these checks have been wrong in exactly that way: one applied `input_detection.content_markers`
— a list for RECOGNISING a file's type — as though every marker were mandatory, and so demanded
the literal string ACDEFGHIKLMNPQRSTVWY inside every FASTA file, which no real FASTA contains.
You are being given the mechanism so you can tell when it would misfire. Where the mechanical
test and the requirement's plain claim disagree, follow the CLAIM.

$skill_yaml

=== REQUIREMENTS TO RULE ON ===
$requirements

$free_choice

HOW TO GRADE

Rule on EVERY requirement listed above. For each, give a verdict of "satisfied", "violated" or
"not_applicable", and one line of evidence quoting what in the answer decided it.

Use "not_applicable" when the requirement genuinely does not bear on this sample — the catalog
records nothing for it, or its `applies_if` guard excludes this scheduler or application. Do
not use it to avoid a hard call.

PRECEDENCE when sources conflict — the earlier wins:
  1. CATALOG FACTS   authoritative about what EXISTS: module names, binaries, which file types
                     are required, queue limits. NOT authoritative that a particular filename,
                     working directory or command form is the only valid one. Where it gives
                     an example path or filename, an answer using a different one is NOT wrong.
  2. REQUIREMENTS    each carries its own source. One sourced "model" is our judgement with no
                     run or document behind it — a strong prior, not a fact. One sourced
                     "run:N/N" was seen in that many real archived production runs.
  3. EXEMPLAR        one correct answer among several. NEVER deduct for differing from it where
                     the requirements are met and the free-choice axes permit it.

Do NOT compute any scores. Report verdicts only; the scores are calculated from them in code.

Respond with ONLY this JSON:
{"requirements": [{"id": "...", "verdict": "satisfied|violated|not_applicable",
                   "evidence": "..."}],
 "note": "<one sentence>"}""")


def render_skill_yaml(skill, app: str, budget: int = 9000) -> str:
    """The requirement library as the judge sees it: the real YAML, lightly trimmed.

    `rationale:` is dropped — it is written for us, explains why a rule exists rather than what
    it requires, and on several rules it recounts a defect the rule no longer has. Feeding the
    judge that history invites it to grade the history.
    """
    import yaml as _y
    out = []
    for r in skill.requirements:
        d = {k: v for k, v in r.items() if k != "rationale"}
        out.append(_y.safe_dump([d], sort_keys=False, allow_unicode=True, width=96,
                                default_flow_style=False))
    body = "\n".join(out)
    fc = FORMAT_CONTRACTS.get(app)
    if fc:
        body = ("# judge/skills/format_contracts.yaml — the curated mandatory sections for this format\n"
                + _y.safe_dump({app: fc}, sort_keys=False, allow_unicode=True, width=96)
                + "\n# the requirement library\n" + body)
    return clip(body, budget, "skill")


def judge_one_skill(sample: dict, answer: str, judge_id: str = "gpt56terra",
                    rubric_id: str = "r1", extracted: dict | None = None) -> dict:
    """Judge EVERY requirement with the LLM, with the skill library supplied verbatim.

    The deterministic checks still run and are returned under `code_verdicts`, but they are
    kept out of the prompt so the two mechanisms can be compared on the same answer.
    """
    st, app, system = sample["subtask"], sample["app"], sample["system"]
    spec = SUBTASKS[st]
    skill = load_skill(st, app, system, rubric_id=rubric_id)
    shadow = run_checks(st, app, system, answer, extracted)

    block = "\n".join(
        f"  [{r['id']}]  ({r.get('severity','major')}, affects {r.get('dimension','?')})\n"
        f"      {' '.join(str(r['claim']).split())}" for r in skill.requirements)
    fc = ""
    if skill.free_choice:
        fc = ("FREE CHOICE — the answer may differ from the exemplar on these axes.\n"
              "Never deduct for any of them:\n" + "\n".join(
                  f"  - {f['axis']}: {' '.join(str(f['note']).split())}"
                  for f in skill.free_choice))

    prompt = SKILL_PROMPT.safe_substitute(
        subtask=st, goal=spec["goal"], system=system, sched=scheduler(system),
        prompt=clip(sample["prompt"], BUDGET["prompt"], "prompt"),
        answer=clip(answer, BUDGET["answer"], "answer"),
        catalog=render_catalog(system, app, st),
        exemplar=clip(sample.get("reference", "(none supplied)"), BUDGET["exemplar"], "exemplar"),
        skill_yaml=render_skill_yaml(skill, app),
        requirements=block, free_choice=fc)

    text, meta = complete(judge_id, prompt)
    v = parse_json(text, require="requirements")
    if not isinstance(v, dict) or "requirements" not in v:
        raise JudgeError(f"unparseable reply ({len(text)} chars)")

    merged = {q["id"]: {"verdict": q.get("verdict"), "evidence": q.get("evidence", ""),
                        "decided_by": "judge"}
              for q in v["requirements"] if isinstance(q, dict) and q.get("id")}
    out = derive_scores(merged, skill)
    out.update({"requirements": merged, "note": v.get("note", ""),
                "mode": "skill", "judge_model": judge_id,
                "judge_params": meta, "rubric_id": skill.rubric_id,
                "rubric_sha256": skill.rubric_sha256,
                "n_judged": len(merged), "n_deterministic": 0,
                # kept for comparison, deliberately NOT shown to the judge
                "code_verdicts": {k: {"verdict": x["verdict"], "evidence": x["evidence"]}
                                  for k, x in shadow.items()}})
    return out
