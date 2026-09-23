# Trinity agent benchmark — results

Can a cheaper open-weight model be trusted with the four pre-submission stages of an HPC job —
**software selection → input preparation → resource selection → batch job creation**?

This repository holds the **answer and the evidence for it**: the judging skill that defined a
pass, every graded answer the benchmark produced, and the write-up. The harness that generated
and graded them is not here; see [Where the code is](#where-the-code-is).

## Result

Corpus v8, rubric r28, judged by `gpt56terra` at k=3, majority of replicates. Each cell is passes
out of 20 attempts (10 anchors × 2 prompt arms).

| Model | Software | Input prep | Resource | Batch | Total |
|---|---|---|---|---|---|
| nemotron-3-ultra | 16 | 6 | 18 | 20 | **60/80 · 75%** |
| gemma-4-31b | 16 | 6 | 19 | 16 | **57/80 · 71%** |
| gpt-oss-120b | 10 | 4 | 20 | 10 | **44/80 · 55%** |
| llama-3.1-8b | 18 | 0 | 7 | 12 | **37/80 · 46%** |
| **All models** | 60/80 | **16/80** | 64/80 | 58/80 | **198/320 · 62%** |

**Three subtasks are usable. Input preparation is 20% and no model exceeds 6 of 20.** That
number survived every repair to the measurement, and the remaining failures were checked by
reading the judge's evidence one at a time — declared atom counts that do not match the
coordinates written, a haemoglobin sequence under a ubiquitin header, invented configuration
schemas. It is a capability limit, not a grading artefact.

Two caveats belong beside the table, not in a footnote. Twenty of the 320 cells flip between
judge replicates, so a single cell is ±1–2 rows. And one severity call is worth more than that
spread: scoring `BATCH.common.no_directive_comments` as minor rather than major reads 206/320
instead of 198. The library keeps it major because ALCF documents that a trailing comment on a
`#PBS` line stops the script submitting, and none of the 146 real scripts in the run archive do
it. Both readings are recorded in [`judge/skills/registry.json`](judge/skills/registry.json)
under r28.

## What is here

```
judge/skills/         THE JUDGING SKILL — what a pass meant
  requirements/         _common.yaml + one directory per subtask; every rule carries its
                        claim, severity, dimension, source and the rows that motivated it
  registry.json         r0…r28, each version's change set (r27 reconstructed — see below)
  format_contracts.yaml curated mandatory sections per input format

examples/             ALL 320 GRADED ANSWERS, as markdown
  <subtask>/<app>@<system>/
    prompt.base.md      the prompt, exactly as the models received it
    prompt.rich.md      the enriched arm's prompt, where the arms differ
    reference.md        Claude's reference answer
    base/ rich/         answer-<model>.md ×4, and verdicts.md — every requirement, the
                        majority verdict, and the judge's quoted evidence

docs/
  findings.md           the result and what it does not support
  augmentation.md       how much of the result is the prompt rather than the model
  methodology.md        how a grade was produced, step by step
  pipeline_design_note.md  the original design agreement, 2026-09-14

site/                 index.html — the report PDF and four evidence browsers
```

Start at [`examples/README.md`](examples/README.md) for the corpus, or
[`docs/findings.md`](docs/findings.md) for the argument.

`site/*.html` are self-contained pages; open `site/index.html` from a local clone. GitHub's
viewer will not render them from the web UI.

## How to read a verdict

Everything the benchmark decided is in `examples/<subtask>/<app>@<system>/<arm>/verdicts.md`:

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.mandatory_sections_present` | major | **violated** | `system.gro` declares `34216` atoms but supplies only a small subset of coordinate records |

The rule id resolves to a block in `judge/skills/requirements/`, which states the claim being
tested, what decides it, and why it exists. Scores were **computed in Python** from these
verdicts — fatal → 0, major → 1, minor still allows 2 — and never by the judge, which once
produced different scores from identical verdicts on 19 of 159 rows. A pass is 2/2/2 with no
fatal violation, taken as the majority of three judge replicates.

Grades were collected under rubric r27 and scored under r28; r28 removes exactly one rule
(`INP.common.not_copied_from_example`), which is listed in the verdict tables but not counted.
That replay is exact for a rubric change that only removes rules.

## Where the code is

The harness — catalog reader, prompt builder, leak gates, judge client, deterministic checks,
regression oracle, A/B statistics, the corpus itself — was removed from this repository to keep
it to the result and its evidence. It is in this repository's own history:

```bash
git show 77514d0 --stat                          # the full tree
git checkout 77514d0 -- benchmark audit tools data   # restore it locally
python -m audit.matrix                           # re-derives the table above, no API calls
python tools/build_examples.py                   # regenerates everything under examples/
```

It also lives in the parent repository, `llm-inference-benchmarks`, under `skills/`. The
augmentation ablation — the `bare` corpus, `benchmark/strip.py`, and the report generators — is on
the **`experiment/augmentation-ablation`** branch, which carries the full harness.

## What this does not establish

- **The TEST split was never opened.** 28 rubric versions were fit against DEV labels.
- **Judge self-preference is unmeasured.** `gpt-oss-120b` is graded and the judge is GPT.
- **Ten anchors per cell**, and 20 of 320 cells flip between replicates: differences under about
  5 points are not resolvable.
- **Slurm rules have no execution evidence.** The run archive is PBS-only.
- **`format_contracts.yaml` is careful reading, not measurement** — which is why every rule that
  reads it is `major` and never `fatal`. `mandatory_sections_present` (24 rows) is provisional
  until a domain reviewer confirms those lists.
- **The registry has a hole at r27.** r0–r26 record their change set; r27 was minted without one.
  Its entry is reconstructed from the artifacts and says so. That gap is why the first published
  headline (203/320) could not be reproduced: it had been scored with a severity override that
  never reached the YAML, and with replicates averaged rather than voted.

## Provenance

`gpt56terra` (Argo, reasoning, 16384 tokens) graded everything. Claude wrote the prompts and the
reference answers and never graded. Every grade row records `judge_model`, `rubric_id` and
`rubric_sha256`, so two grades under different rules cannot be silently compared.

Prompts were generated from a vendored copy of
[zhenghh04/application_catalog](https://github.com/zhenghh04/application_catalog) at commit
`4c6a192242452d798afb6b7f1e44362f263a1c7d`, verified byte-identical to upstream. That copy is
not in this repository; upstream carries no licence, so it should not be redistributed. Issues
found in it while wiring it up were written up separately for its author.
