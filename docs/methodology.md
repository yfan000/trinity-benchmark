# How a grade is produced

One answer, end to end. Everything here is code in this repository; where a step has a known
weakness it is stated at that step rather than collected at the bottom.

## 1. An anchor

An anchor is a `(subtask, application, system)` triple — `(Input preparation, gromacs, sirius)`.
Ten anchors per subtask, chosen to spread across schedulers (PBS Pro and Slurm), across
application families (MD, quantum chemistry, CFD, LLM inference, benchmarks), and across how much
the catalog knows about them: two anchors, `vllm@frontier` and `pytorch@sophia`, are deliberately
sparse and act as a placebo stratum in the A/B.

## 2. The prompt

`benchmark/prompt.py` and `benchmark/generate.py` build it from the vendored facility catalog.
The governing rule, enforced by `audit/gates.py` and not by discipline:

> **The prompt states the task explicitly and never contains the answer being tested.**

For Software selection that means the prompt may describe the workload but must not name the
application. For Resource selection it may state the science goal and the queue limits but not
the node count. `audit/gates.py` runs four checks per sample — positive (the task is stated),
forbidden (the answer is absent), redaction (fields the subtask hides are hidden), negative
control (a deliberately leaky variant is caught) — plus two that came out of real defects:

- **Prompt coherence**, 6 invariants over all 39 anchors, because two sections of one prompt
  contradicted each other: an inventory listed files the contract told the model not to write.
- **Worked-example coverage**, which reads the *generated prompts* rather than the source files.
  It had passed three times while the prompt builder silently truncated examples at 44 lines, so
  GROMACS models saw one of three required formats. A gate that inspects inputs rather than
  outputs proves nothing.

A prompt may carry a worked example — a real deck for a *different* system, supplied to teach
grammar, never to be copied. One retired rule (`not_copied_from_example`, removed in r28)
penalised models for using it; see [findings.md](findings.md).

## 3. The reference answer

Claude writes one correct answer per anchor, stored with the sample. It is treated as *one*
correct answer, not the only one — the rubric carries an explicit `free_choice` list per subtask
(numerical convergence parameters, filenames, comment style) and the judge is told never to
deduct on those axes. Claude never grades.

## 4. The answers

Four open-weight models on ALCF endpoints, `temperature=1.0`: `nemotron-3-ultra`, `gemma-4-31b`,
`gpt-oss-120b`, `llama-3.1-8b`. That temperature is the reason the A/B is derived by text
insertion rather than regeneration — see below.

## 5. The rubric

`judge/skills/` is the judging skill: YAML requirements composed most-general-first for each
anchor (`_common.yaml` → `<subtask>/_common.yaml` → `<subtask>/<app>.yaml` → the scheduler family
→ the system). Each requirement carries

```yaml
- id: INP.common.no_binary_contents
  claim: "No text contents are invented for a binary or runtime-generated file"
  decided_by: deterministic          # or: judge
  check: {kind: no_contents_for, field: "__rubric.binary_files"}
  dimension: correctness             # correctness | completeness | usability
  severity: fatal                    # fatal | major | minor
  source: "format:per-application"
  rationale: >-
    Measured repeatedly: text written into NWChem .db and .movecs …
```

`source` and `rationale` are not decoration. A rule with no measured row behind it is how the
library grew rules that could not be satisfied; requiring each one to name its evidence is what
made those visible on re-reading.

Every version is recorded in `registry.json` with its change set and the rows that motivated it.
One id, r27, was minted without an entry; its entry is reconstructed from the artifacts and
labelled as such.

## 6. Judging

`judge/grade.py`, in **skill mode**: the judge is handed the composed rubric YAML verbatim and
rules on every requirement, returning `satisfied` / `violated` / `not_applicable` /
`not_evaluated` with evidence quoted from the answer. It is told to read `check:` as a statement
of intent rather than a pattern to match, and that where the mechanical test and the plain claim
disagree it must follow the claim.

The deterministic checks in `judge/checks.py` still run, and their verdicts are stored as
`code_verdicts` — but they are **not shown to the judge**, so the two are independent and their
disagreements are measurable. Skill mode and the earlier hybrid (code decides, judge fills gaps)
scored 96 and 97 of 160 on the same rubric: indistinguishable. Skill mode was kept because it
keeps one authority over a rule rather than two.

## 7. The scores are computed in Python, not by the judge

`judge.grade.derive_scores` turns verdicts into three 0–2 dimensions:

- any violated **fatal** rule in a dimension → 0, and the whole answer is `fatal_error`
- otherwise any violated **major** rule → 1
- only minor violations, or none → 2

A pass is 2/2/2 with no fatal. The arithmetic moved out of the judge after three replicates of
the same cell produced *different scores from identical verdicts* on 19 of 159 rows. Minor
violations deliberately do not block a 2: when they did, one over-eager minor rule made a pass
arithmetically impossible across a whole subtask.

## 8. Replicates and consensus

k=3 judge replicates per answer; the cell's verdict is the majority. Test–retest at k=3 flips
about 7% of rows, and 20 of 320 cells in v8 flip between replicates, so differences under roughly
5 points are not resolvable. **Majority, never the mean** — the first published v8 table scored
cells with `floor(total passes / 3)`, an average dressed as a count, which put six rows between
two numbers that claimed to measure the same thing. `audit/matrix.py` is now the single
definition.

## 9. Re-scoring without re-judging

Because scores are derived from verdicts, a rubric change that only *removes* rules or changes
severities can be replayed offline against verdicts already collected: the judge was asked the
same questions and the retired one stops counting. `audit/matrix.py --rubric` does this, and
refuses — exit code 2 — if the target rubric contains a rule the grades have no verdict for,
rather than scoring the row as though the missing rule had passed. `--demote RULE` prices a
proposed severity change the same way, without editing the library.

## 10. Regression and A/B

- **`audit/oracle.py`** freezes `{(model, subtask, app, system, req_id): verdict}` over the v7
  corpus. Every refactor must move zero verdicts. This is what catches a path constant pointing
  at the wrong directory — `benchmark/catalog.py` returns `{}` for a file it cannot read, so a
  wrong path is silent everywhere else.
- **`benchmark/arm.py`** derives the enriched A/B arm from the base arm by **mechanical text
  insertion**, verified reversible byte-for-byte (`--verify`). Regenerating the arm instead would
  put ~3 points of sampling noise per 10-sample cell against a ~4-point effect.
- **`audit/ab.py`** reports the paired Wilcoxon on violation counts as the primary endpoint.
  McNemar on pass/fail needs ≥6 one-directional flips to clear 0.05 and cannot see an effect this
  size; the violation count per row spans 0–10 and is the more sensitive endpoint. Thirty of the
  40 anchors are byte-identical across arms and act as the control.

## What this pipeline does not establish

The TEST split was never opened: 28 rubric versions were fit against DEV labels. Judge
self-preference is unmeasured — `gpt-oss-120b` is graded and the judge is GPT. The Slurm rules
have no execution evidence behind them; the run archive is PBS-only. And
`judge/skills/format_contracts.yaml`, which decides what sections a format genuinely requires, is
careful reading rather than measurement, which is why every rule reading it is `major` and never
`fatal`.
