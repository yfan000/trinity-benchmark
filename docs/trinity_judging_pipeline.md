# Trinity benchmark — judging pipeline redesign

*Meeting note · 2026-09-14*

## Goal

Find an appropriate LLM for Trinity's agentic calls, balancing quality and cost, across the
four pre-submission subtasks: **Software selection → Input preparation → Resource selection →
Batch job creation**. This note records the agreed architecture for generating reference
answers, running candidate models, and judging the results.

## Agreed workflow

```
Benchmark task
  → Claude generates the reference answer
  → Claude orchestrates ALCF open-weight models
  → open-weight model generates an answer
  → GPT judge (gpt56terra) evaluates it
  → judge applies the defined requirements and decides
  → human reviews the judge's decisions
  → feedback refines the judging skill
  → iterate
```

## 1. Reference answer generation

Claude produces the expected answer together with the elements a correct answer must contain.
The output is a **structured requirement list**, not prose, so the judge checks against a
rubric rather than doing fuzzy similarity. Where a real successful run exists, the requirements
are grounded in it and marked as such.

The Claude-generated answer is treated as **one correct answer**, not the only one.

## 2. Open-source model answers

Claude orchestrates models on ALCF inference endpoints (Sophia, Minerva) with a consistent
generation workflow. Largely built. Current targets: `gpt-oss-120b`, `gemma-4-31B`,
`Llama-3.1-8B`, `nemotron-3-ultra`.

## 3. GPT-based judging

The judge is **`gpt56terra`** — the strongest GPT on the Argo roster and the best-scoring model
on this benchmark (61% answer-correct, 46% fully correct across 156 samples, ahead of every
other model tested).

It is **added alongside** the Claude judge, not substituted for it. Replacing it would
invalidate the v2–v6 results as a comparison series, and would make the judge same-family with
`gpt-oss-120b`, one of the graded models. Running both measures that bias rather than absorbing
it. Claude on references plus GPT on judging is the genuinely independent combination, and
breaks the current closed loop in which Claude writes the question, the answer key, and the
grade.

## 4. Judging by requirements, not similarity

**The central agreement.** The reference answer and a model's answer need not match. What the
judge must determine is whether the model *missed a required input*, *produced a syntax error*,
or *requested a walltime exceeding the queue maximum* — a list of concrete requirements derived
per subtask from the catalog and from the real runs.

Most such requirements are decided **deterministically in Python before the judge is called**,
so they cannot be swayed by sampling; the judge adjudicates only the residual. Different but
valid answers are handled by explicit `acceptable_variants` and `free_choice` fields rather
than by prose instructions the judge may ignore.

## 5. The requirements *are* the judging skill

Not a prose rubric with separate per-sample checklists. One **versioned library** of
requirements, organised by subtask and by software, written once and reused across samples;
only their parameters bind per sample.

The judge returns a **verdict on each requirement** — satisfied / violated / not applicable,
with the evidence that decided it — and the 0–2 dimension scores are *derived* from those
verdicts by a stated rule, so every score is traceable to the rules behind it.

Human feedback is a **diff against the library**. A reviewer says whether a requirement should
not apply here, is missing, is wrong, or was simply misjudged; each maps to a concrete edit
that produces the next version. The last category is what separates a defect in the *skill*
from a defect in the *judge* — a distinction the current setup cannot express. Where the judge
repeatedly misjudges something humans find unambiguous, the fix is to move that requirement to
deterministic: the skill improves by needing the LLM less.

Review is blind, on a DEV/TEST split, with an unchanged-version control each round to detect
drift.

## New input: real successful runs

Agentic runs covering all four steps, starting at
`/eagle/DLIO/hzheng/trinity_jobs/polaris` and growing as more are shared.

They are mined for requirements the catalog does not state: the directives every successful job
script carries, the modules and launchers actually used, the observed ranks/nodes/walltime
ranges, and — most valuable — what *varies* across successful runs, which is what legitimately
counts as free choice. Each mined requirement carries a support count and needs sign-off before
entering the library; a convention in one team's runs is not automatically a correctness rule.

Runs are used three ways:

1. **Grounded requirements** — replacing inference with observation.
2. **Judge calibration** — a correct run must score 2/2/2; deliberately mutated copies (wrong
   queue, renamed module, deleted input) must fail. This measures judge precision and recall
   objectively, with no human labelling.
3. **Worked examples in prompts, from a *different* (app, system) pair only.** The pair under
   test is never shown its own run: that would hand over the answer and measure copying rather
   than capability.

## Defects found in the current pipeline

- **The answer key is truncated at 3,000 characters**, and because the reference is serialised
  last the cut always lands on it — 16 of 40 samples affected, as little as 43% retained, worst
  on Input preparation and Resource selection, the two lowest-scoring subtasks.
- **Two grading paths disagree**; the 156-sample run never showed the judge a reference at all.
- **Reference answers are unvalidated** and accepted even when empty.
- **No grade row records which judge or rubric produced it.**
- **Judge test-retest has never been measured.** Grades for unchanged subtasks were carried
  forward deliberately between versions, so the judge has never been run twice on the same
  input.
- The pipeline does not run from a clean checkout, and `skills/` is untracked in git.

## Measurement constraint

A 10-sample cell moved **3 points between two runs of identical prompts** (Software selection,
nemotron: 8/10 → 5/10, with zero truncation involved). Model-vs-model differences under roughly
10 points at n=40 are therefore not resolvable, and several recently reported prompt-tuning
deltas fall inside that band.

Judge accuracy is unaffected by this: judging a **frozen** answer corpus removes model-sampling
noise entirely, so rubric changes are assessed by a paired test on the same items, where a
much smaller change is detectable.

## Decisions

| | |
|---|---|
| Judge model | `gpt56terra`, added alongside Claude rather than replacing it |
| Human review | ~40 stratified, blind decisions per iteration |
| Benchmark size | hold at 40 samples; fix the judge rather than scale up |
| Reference answers | treated as *one* correct answer, not the only one |

## First actions

1. **Measure the judge's own test-retest spread.** It decides whether every later phase costs
   1× or 3×, and it is the cheapest experiment in the plan.
2. **Count how many benchmark anchors have a matching successful run** — this determines how
   much of the benchmark can be grounded in real execution.
