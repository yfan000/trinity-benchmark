# Trinity agent benchmark

Can a cheaper open-weight model be trusted with the four pre-submission stages of an HPC job —
**software selection → input preparation → resource selection → batch job creation**?

## Result

Corpus v8, rubric r28, judged by `gpt56terra` at k=3. Passes out of 20 attempts per cell
(10 anchors × 2 prompt arms).

| Model | Software | Input prep | Resource | Batch | Total |
|---|---|---|---|---|---|
| nemotron-3-ultra | 16 | 6 | 18 | 20 | **60/80 · 75%** |
| gemma-4-31b | 16 | 6 | 19 | 16 | **57/80 · 71%** |
| gpt-oss-120b | 10 | 4 | 20 | 10 | **44/80 · 55%** |
| llama-3.1-8b | 18 | 0 | 7 | 12 | **37/80 · 46%** |
| **All models** | 60/80 | **16/80** | 64/80 | 58/80 | **198/320 · 62%** |

```bash
python -m audit.matrix          # prints exactly this table, no API calls
```

**Three subtasks are usable. Input preparation is 20% and no model exceeds 6 of 20.** That number
survived every repair to the measurement, and the remaining failures were checked by reading the
judge's evidence one at a time — declared atom counts that do not match the coordinates written,
a haemoglobin sequence under a ubiquitin header, invented configuration schemas. It is a
capability limit, not a grading artefact.

Two caveats belong next to the table rather than in a footnote. Twenty of the 320 cells flip
between judge replicates, so a single cell is ±1–2 rows. And one severity call is worth more than
that: scoring `BATCH.common.no_directive_comments` as minor rather than major reads 206/320
instead of 198 — `python -m audit.matrix --demote BATCH.common.no_directive_comments` prices it.
The library keeps it major because ALCF documents that a trailing comment on a `#PBS` line stops
the script submitting, and none of the 146 real scripts in the archive do it.

Open [`site/index.html`](site/index.html) for the report and four evidence browsers, or
[`examples/`](examples/) for one end-to-end walkthrough per subtask.

## Layout

```
judge/          everything that grades an answer
  client.py       provider dispatch, retries, budget guard
  grade.py        judge_one (hybrid) · judge_one_skill (judge decides all) · derive_scores
  checks.py       the deterministic checks
  rejudge.py      k replicates, consensus, paired diff
  skills/         THE JUDGING SKILL — the versioned rubric
    requirements/   _common + one directory per subtask
    registry.json   r0…r28, each change with the rows that motivated it (r27 reconstructed)
    format_contracts.yaml

benchmark/      generating prompts, collecting answers
  catalog.py      one normalized reader for the facility catalog
  prompt.py       builds the prompt and the reference answer
  generate.py     sample generation, leak enforcement
  arm.py          derives the enriched A/B arm by insertion, not regeneration
  run.py          collects answers from the model endpoints

audit/          gates and analysis
  gates.py        leak · prompt coherence · worked-example coverage
  oracle.py       frozen-verdict regression over the v7 corpus
  ab.py           paired A/B statistics
  matrix.py       the published table, re-derived from the shipped grades

tools/          build_report.py · build_examples.py · refresh_catalog.sh
data/           catalog (vendored, pinned) · worked examples · the v8 corpus
examples/       one prompt → answer → verdict walkthrough per subtask
site/           report PDF and four evidence browsers
docs/           methodology · findings · the upstream catalog bug report
                  + the original pipeline design note (2026-09-14)
```

## Running it

```bash
pip install -r requirements.txt
set -a; . /path/to/.env; set +a          # ALCF token — 48 h lifetime, refresh when it expires

python -m audit.gates                     # must pass before generating anything
python -m benchmark.generate --subset --out data/corpus/v9/samples_v9base.jsonl
python -m benchmark.arm --derive --src samples_v9base.jsonl --dst samples_v9rich.jsonl
python -m benchmark.arm --verify --src samples_v9base.jsonl --dst samples_v9rich.jsonl
TRINITY_VER=v9base python -m benchmark.run --answer
python -m judge.rejudge --corpus v9base --judge gpt56terra --rubric r28 --runs 3
python -m audit.ab --rubric r28 --mode skill --runs 3
```

Reproduce the published numbers with **no API calls**:

```bash
python -m audit.matrix                       # the result table
python -m audit.ab --rubric r27 --runs 3     # the A/B, which was null
python tools/build_report.py                 # the PDF and site/index.html, from the same numbers
```

Two things that will bite otherwise:

- **`benchmark.generate` resumes.** It keeps any sample already in the output file, so a change
  to prompt-building code has no effect until the output file is moved aside. A no-op run looks
  almost identical to a real one.
- **`audit.oracle` is the refactor gate.** `--snapshot` then `--diff` proves a change moved no
  verdict. `benchmark/catalog.py` returns `{}` for a file it cannot read, so a wrong path fails
  silently — this is the check that catches it.

## How a grade is produced

A prompt is generated from the facility catalog, with a leak check that forbids it containing
the answer. Four models answer. Then, per answer, the rubric for that `(subtask, application,
system)` is composed from the YAML, the judge rules on every requirement and returns a verdict
with evidence, and **the 0–2 dimension scores are computed in Python** from those verdicts — not
by the judge, which once produced different scores from identical verdicts on 19 of 159 rows.

See [`docs/methodology.md`](docs/methodology.md).

## What is unfinished

- **`judge/skills/format_contracts.yaml` needs a domain reviewer.** The mandatory-section lists
  are a careful reading of each format, not measured from runs. Every rule reading them is
  `major`, never `fatal`, until someone who writes these decks confirms them.
- **`fenced_blocks()` concatenates every code block into one string**, so per-file rules cannot
  tell files apart — a valid `.par` masks a garbage `.udf`.
- **26 catalog entries name a queue their own system lacks.** `prior_block()` guards against it;
  the upstream data is still wrong. See [`docs/catalog_issues.md`](docs/catalog_issues.md).
- **Judge self-preference is unmeasured.** `gpt-oss-120b` is graded and the judge is GPT. The
  plan called for grading with both judges to size the bias; it was never run.
- **TEST split never opened.** 28 rubric versions were fit against DEV labels.
- **The registry has a hole at r27.** Rubric ids r0–r26 record their change set and the rows that
  motivated it; r27 was minted without one. Its entry is reconstructed from the artifacts — the
  graded requirement ids prove it is r28 plus one rule — and says so. That gap is why the first
  published headline (203/320) could not be reproduced by anything in this repository: it had
  been scored with a severity override that never reached the YAML and with replicates averaged
  rather than voted. `audit/matrix.py` exists so the table has one definition.
- **Slurm rules have no execution evidence.** The run archive is PBS-only.

## Provenance

`gpt56terra` (Argo, reasoning, 16384 tokens) grades everything. Claude writes the prompts and the
reference answers and never grades. Every grade row records `judge_model`, `rubric_id` and
`rubric_sha256`, so two grades under different rules can never be silently compared.

The facility catalog in `data/catalog/` is vendored from
[zhenghh04/application_catalog](https://github.com/zhenghh04/application_catalog) at a pinned
commit — see [`data/catalog/PROVENANCE.md`](data/catalog/PROVENANCE.md) for the SHA, the
verification command, and its licence status.
