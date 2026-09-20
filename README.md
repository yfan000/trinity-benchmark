# Trinity agent benchmark

Measures whether a cheaper open-weight model can be trusted with the four pre-submission stages
of an HPC job: **software selection → input preparation → resource selection → batch job
creation**.

Forked from `llm-inference-benchmarks` on 2026-09-20 with the Trinity work only — the parent
repo is 3.8 GB of unrelated benchmarks. Nothing here was deleted from the parent.

## Result (corpus v8, rubric r28, judge gpt56terra at k=3)

Passes out of 20 attempts per cell (10 anchors × 2 prompt arms).

| Model | Software | Input prep | Resource | Batch | Total |
|---|---|---|---|---|---|
| nemotron-3-ultra | 16 | 7 | 18 | 20 | **61/80 · 76%** |
| gemma-4-31b | 16 | 6 | 19 | 16 | **57/80 · 71%** |
| gpt-oss-120b | 10 | 4 | 19 | 17 | **50/80 · 62%** |
| llama-3.1-8b | 18 | 0 | 6 | 11 | **35/80 · 44%** |
| **All** | 60/80 | **17/80** | 62/80 | 64/80 | **203/320 · 63%** |

Open `site/index.html` for the report and the four evidence browsers.

**The finding:** three subtasks are usable; **Input preparation is 21% and no model exceeds
35%**. That number survived every repair to the measurement, and the residual failures were
verified by reading judge evidence individually — declared atom counts that do not match the
coordinates written, a haemoglobin sequence under a ubiquitin header, invented configuration
schemas. It is a capability limit, not a grading artefact.

## Layout

```
skills/                    the machinery
  catalog.py               single normalized reader for the facility catalog
  catalog_repairs/         line-level fixes for 2 upstream YAML syntax errors, sha-guarded
  format_contracts.yaml    curated mandatory sections per input format  ← needs domain review
  judging/requirements/    the rubric: 56 requirements as versioned YAML
  judging/registry.json    rubric history r0…r28, each change with its motivating rows
  trinity_generate.py      prompt generation, leak enforcement
  trinity_arm.py           derives the enriched A/B arm by insertion, not regeneration
  trinity_checks.py        deterministic checks
  trinity_judge.py         judge_one (hybrid) and judge_one_skill (judge decides all)
  trinity_ab.py            paired A/B analysis
  trinity_oracle.py        regression oracle over frozen verdicts
  leak_audit.py            gates: leak, prompt coherence, example coverage
results/skills/trinity/
  catalog/                 cached github.com/zhenghh04/application_catalog @ 2026-05-13
  samples_v8{base,rich}    the two prompt arms, 40 anchors each
  answers_v8{base,rich}    160 answers per arm
  grades_v8*SKILLMODE*     k=3 judging, both arms
  *_v7, oracle_v7.json     frozen corpus + verdict oracle for regression testing
site/                      report PDF and four evidence browsers
docs/                      meeting note, upstream catalog issues
```

## Running it

```bash
set -a; . ../cluade_test/.env; set +a          # ALCF token, 48 h lifetime
python skills/leak_audit.py                     # must pass before generating
python skills/trinity_generate.py --subset --out results/skills/trinity/samples_v9base.jsonl
python skills/trinity_arm.py --derive --src samples_v9base.jsonl --dst samples_v9rich.jsonl
python skills/trinity_arm.py --verify --src samples_v9base.jsonl --dst samples_v9rich.jsonl
TRINITY_VER=v9base python skills/trinity_run_v2.py --answer
python skills/trinity_ab.py --rubric r28 --mode skill --runs 3
```

`trinity_generate` **resumes**: it keeps any sample already in the output file. A change to
prompt-building code has no effect unless the output file is moved aside first.

## What is unfinished

- **`format_contracts.yaml` needs a domain reviewer.** The mandatory-section lists are my
  reading of each format, not measured from runs. Every rule that reads them is `major`, never
  `fatal`, until someone who writes these decks confirms them.
- **`fenced_blocks()` concatenates every code block into one string**, so per-file rules cannot
  tell files apart — a valid `.par` masks a garbage `.udf`. Affects the shadow deterministic
  checks, not the skill-mode scores.
- **26 catalog entries name a queue their own system lacks.** `prior_block()` now guards
  against it; the upstream data is still wrong. See `docs/catalog_issues_for_huihuo.md`.
- **Judge self-preference is unmeasured.** `gpt-oss-120b` is graded and the judge is GPT. The
  original plan called for grading with both judges to measure the bias; that was never run.
- **TEST split never opened.** 28 rubric versions were fit against DEV labels.
- **Slurm rules have no execution evidence.** The run archive is PBS-only.

## Provenance

Judge `gpt56terra` (Argo, reasoning, 16384 tokens) for all grading; Claude writes the reference
answers and the prompts, and never grades. Every grade row records `judge_model`, `rubric_id`
and `rubric_sha256`.
