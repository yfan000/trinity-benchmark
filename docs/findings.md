# Findings

Corpus v8, rubric r28, `gpt56terra` at k=3, majority of replicates. Every number here is derived
from the graded corpus rather than typed in, by `audit/matrix.py` — which is not in this
repository but is in its history (`git checkout 77514d0 -- benchmark audit tools data`, then
`python -m audit.matrix`). The per-answer evidence behind all of it is in
[`examples/`](../examples/).

## The result

| Model | Software | Input prep | Resource | Batch | Total |
|---|---|---|---|---|---|
| nemotron-3-ultra | 16 | 6 | 18 | 20 | **60/80 · 75%** |
| gemma-4-31b | 16 | 6 | 19 | 16 | **57/80 · 71%** |
| gpt-oss-120b | 10 | 4 | 20 | 10 | **44/80 · 55%** |
| llama-3.1-8b | 18 | 0 | 7 | 12 | **37/80 · 46%** |
| **All models** | 60/80 | **16/80** | 64/80 | 58/80 | **198/320 · 62%** |

**Three subtasks are usable; one is not.** Software selection, Resource selection and Batch job
creation land between 58 and 64 of 80. Input preparation is 16 of 80 and no model exceeds 6 of
20 — a different kind of result, not a worse score on the same scale.

## Why Input preparation is the finding

Its failures were read individually rather than counted, because most of the subtask's early
score was measurement error and it was reasonable to suspect the rest was too. It is not. What
remains:

| rows | severity | rule |
|---|---|---|
| 48 | major | `values_match_physical_system` |
| 27 | fatal | `no_invented_keywords` |
| 24 | major | `mandatory_sections_present` |
| 19 | major | `no_truncation` |
| 10 | fatal | `all_required_files_present` |

Concretely: a `conf.gro` declaring 13 atoms for a 34,000-atom system; `nat=64` written above 16
coordinates; a haemoglobin sequence under a ubiquitin FASTA header; water geometry at 90°; an
`input.json` AlphaFold configuration language invented entire, with fields such as `num_recycle`
that do not exist. These are answers that look right and would not run.

The distinction that matters operationally: **the other three subtasks fail loudly, this one
fails quietly.** A wrong queue name is rejected at submission. A plausible-looking input deck with
the wrong atom count consumes the allocation and produces numbers.

## What each model gets wrong

**nemotron-3-ultra (60/80).** Quantitative slips inside otherwise sound work — 80 NaCl pairs into
a 6.245 nm box giving 0.55 M where 0.15 M was asked. Clean on Batch job creation: no rule failed
in a majority of runs on any of its 20 attempts. The only candidate for unattended use, and only
outside Input preparation.

**gemma-4-31b (57/80).** Single-token errors in precise work: `vdw-type` for `vdwtype`;
`#PBS -l select=1:system=polaris` submitted to Sirius — the right directive carrying a machine
name copied from the worked example. Broad but shallow; usually one defect per answer.

**gpt-oss-120b (44/80).** Abbreviates when asked for complete files, which drives four separate
Input-preparation rules at once ("… (remaining protein atoms) …", "a very small illustrative
system"). Weakest on Software selection, genuinely naming the wrong code. Its Batch score is the
one most sensitive to a rubric judgement call — see the severity note below.

**llama-3.1-8b (37/80).** Fabricates formats that look correct, and is the only model that
violates queue limits the prompt states explicitly or fails rank arithmetic. Zero on Input
preparation across 20 attempts. Its 18/20 on Software selection is the highest of any model,
which says more about that subtask than about the model.

## What each subtask fails on

**Software selection — 60/80.** Only one rule actually costs anyone a pass:
`correct_application` (fatal, 13 rows), concentrated on two anchors — GROMACS@Sirius and
LAMMPS@Polaris. The most frequent violation, `no_vague_performance_claims` (16 rows), is minor
and never blocks a pass.

**Resource selection — 64/80.** Failures are llama's almost entirely: `walltime_within_queue_limit`
and `nodes_within_queue_limits` are fatal and fire 6 and 3 times, on a prompt that states the
limits. The most frequent rule here, `allocation_matches_scaling_notes` (11 rows), is minor —
arguably backwards, since a GPU-to-rank misunderstanding wastes an allocation while the cosmetic
rules above it are graded harder.

**Batch job creation — 58/80.** `invokes_application` (fatal, 6) and `inputs_reachable` (6) are
the substantive failures. The most frequent, `no_directive_comments` (9 rows, 8 of them gpt-oss),
is the severity call discussed below.

## One severity call moves the headline

`BATCH.common.no_directive_comments` forbids a trailing comment on a `#PBS` line. Scored as minor
rather than major, the total reads **206/320 instead of 198** — larger than the judge's own
test–retest spread, and almost all of it gpt-oss, which does it on 8 of 8 attempts.

The library keeps it **major**: ALCF documents that `qsub` reads the trailing text as further
directives so the script does not submit, and 0 of 146 real scripts in the run archive do it. But
the call is a judgement, so it is priced rather than hidden:

```bash
python -m audit.matrix --demote BATCH.common.no_directive_comments   # from commit 77514d0
```

The first published version of this table applied that demotion silently while the YAML said
`major`, and aggregated replicates as `floor(sum/3)` instead of by majority, reading 203/320 —
a number no tool could reproduce. That is why `audit/matrix.py` was written: one definition of
the table, which the report renderer calls too.

## The prompt-enrichment A/B was null

The question was whether feeding more of the facility catalog into the Input-preparation prompt
(format contracts, setup blocks, run commands, scaling notes) raises the score. Two arms over the
same 40 anchors, the enriched arm derived from the base arm by verified-reversible text
insertion, so the comparison is paired and free of regeneration noise.

```
CONTROL (30 anchors byte-identical in both arms)   base 93 → rich 89   Wilcoxon p=0.039
TREATED (Input preparation, 10 anchors)            base  1 → rich  5   Wilcoxon p=0.21
  of which contract supplied (8 anchors)                  1 →      2
  of which placebo, system context only (2)               0 →      3
```

**The control moved further than the treatment, and in the wrong direction.** The placebo
stratum — the two sparse anchors that receive no format contract — improved more (+3 of 8) than
the stratum that got the full enrichment (+1 of 32). Enrichment did reduce the violations it
targeted (`no_invented_keywords` 16 → 11), but Input preparation is all-or-nothing: no minor-
severity rules, so one surviving violation is still a non-pass.

**Conclusion: the enrichment is not worth shipping on this evidence.** The honest reading is that
this design cannot resolve an effect of the size available — the control's own drift is ±4 rows.

## What the reported number survived

Reported scores moved by tens of rows through measurement repairs alone, with no model changing:

| repair | effect |
|---|---|
| `content_markers_present` demanded the literal amino-acid alphabet inside every FASTA | removed in r26 |
| `not_copied_from_example` penalised the HPLinpack header another rule requires **fatally** | removed in r28: 188/320 → 198/320 |
| three prompts told models to author compiled binaries (`.tpr`, `.re2`, `.h5`) that fatal rules forbid | prompts fixed |
| one prompt named `queue workq` on Crux, which has no such queue; all four models obeyed and were failed fatally | `_legal_queue()` |
| the prompt builder truncated worked examples at 44 lines, so GROMACS models saw 1 of 3 formats | per-file budget |
| the extraction cache was not keyed by subtask, so an HPL grid rule graded the Resource-selection answer | `cache_key()` |

Every one of these inflated or deflated a model's score without the model changing. The rate at
which they were found is the main reason the caveats below are stated as strongly as they are.

## What this does not establish

- **The TEST split was never opened.** 28 rubric versions were fit against DEV labels.
- **Judge self-preference is unmeasured.** `gpt-oss-120b` is graded and the judge is GPT. It also
  scores second-lowest, which is the wrong direction for the obvious bias, but that is not a
  measurement.
- **Ten anchors per cell.** 20 of 320 cells flip between judge replicates; a cell is ±1–2 rows and
  differences under about 5 points are not resolvable.
- **Slurm rules have no execution evidence.** The run archive is PBS-only.
- **`format_contracts.yaml` is careful reading, not measurement** — which is why every rule that
  reads it is `major`, never `fatal`, and why `mandatory_sections_present` (24 rows) should be
  treated as provisional until a domain reviewer confirms those lists.
- **`fenced_blocks()` concatenates every code block into one string**, so per-file rules cannot
  tell files apart: a valid `.par` can mask a garbage `.udf`. This biases Input preparation
  *upward*, not down.
