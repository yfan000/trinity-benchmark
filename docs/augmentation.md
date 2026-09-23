# What the prompt supplies

*Added 2026-09-23. Interactive version: [`site/trinity_augmentation_v8.html`](../site/trinity_augmentation_v8.html);
per-item evidence: [`site/trinity_bare_vs_rich_v8.html`](../site/trinity_bare_vs_rich_v8.html).*

The published benchmark hands the model most of the facility knowledge the task is about — the
installed-software list (making Software selection 1-of-21 multiple choice, the answer always in
the list), the queue table, the required-file inventory, the module lines, and a worked example.
Both existing prompt arms sit at that augmented end, so nothing measured how much of the reported
62% was the model and how much was our prompt.

`bare` strips that material and keeps only the task, the workload and the output contract. It is
derived from the published prompts by heading-span deletion, verified reversible byte-for-byte, so
the arms stay paired item-for-item. Same four models, same judge, same rubric document, k=3.

## Result

| stage | all 56 requirements | | capability only | |
|---|---|---|---|---|
| | **bare** | **rich** | **bare** | **rich** |
| Software selection | 16 | 29 | 16 | 29 |
| Input preparation | 4 | 10 | 4 | 11 |
| Resource selection | 6 | 31 | 30 | 35 |
| Batch job creation | 1 | 29 | 13 | 29 |
| **total / 160** | **27 · 17%** | **99 · 62%** | **63 · 39%** | **104 · 65%** |

**The prompt is worth 72 of 160 items — 45 points.** Exact McNemar: 75 items gained against 3
lost, p = 5×10⁻¹⁹, and significant for each model separately (2×10⁻⁵ to 1×10⁻⁴).

**Roughly half of that is information the orchestrator could inject, and half is not.** Restricted
to requirements a model could satisfy without the catalog (`r29-capability`, registered before
these answers were collected), the gap narrows from 45 points to 26 but does not close.

## Per model and per stage

Passes out of 10 attempts, unaugmented → augmented, all requirements:

| model | Software | Input | Resource | Batch | Δ |
|---|---|---|---|---|---|
| nemotron-3-ultra | 4→8 | 2→4 | 2→9 | 1→10 | **+22** |
| gemma-4-31b | 5→8 | 2→3 | 2→9 | 0→8 | **+19** |
| gpt-oss-120b | 4→4 | 0→3 | 1→10 | 0→5 | **+17** |
| llama-3.1-8b | 3→9 | 0→0 | 1→3 | 0→6 | **+14** |

And the same grid restricted to capability requirements:

| model | Software | Input | Resource | Batch | Δ |
|---|---|---|---|---|---|
| gpt-oss-120b | 4→4 | 0→3 | 4→10 | 2→5 | **+12** |
| llama-3.1-8b | 3→9 | 0→0 | 6→6 | 0→6 | **+12** |
| nemotron-3-ultra | 4→8 | 2→5 | 10→9 | 7→10 | **+9** |
| gemma-4-31b | 5→8 | 2→3 | 10→10 | 4→8 | **+8** |

Five things in those grids are worth more than the totals:

1. **The weakest model gains most from the catalog list, and it is not a capability gain.**
   `llama-3.1-8b` goes 3→9 on Software selection, the largest single-cell move in the study.
   Given 10–30 installed applications to choose from it picks correctly; asked to recall what a
   facility installs, it does not. The list is doing the model's work.
2. **`gpt-oss-120b` gains nothing on Software selection — 4→4 in both views.** It is the one model
   that picks the wrong application *even when handed the list*, so supplying the list cannot help
   it. Its failure is comprehension, not knowledge.
3. **Resource selection is almost entirely information.** +25 across models on all requirements,
   +5 on capability requirements. Two models are already perfect on the capability rules
   unaugmented (gemma 10/10, nemotron 10/10). They can size a job; they cannot recall that Crux's
   queue is `workq-route` or that Polaris `prod` has a 10-node minimum.
4. **Batch job creation is the opposite, and it is where the scaffolding earns its place.** +28 on
   all requirements, still +16 on capability requirements. Without the site conventions and the
   worked script, the models write structurally worse scripts — missing `select`, wrong launcher,
   directive comments — not merely scripts with wrong module strings.
5. **Input preparation resists augmentation from both directions.** +6 all-requirements, +7
   capability, and `llama-3.1-8b` scores 0/10 with the full prompt and 0/10 without it. This is
   the same stage where the earlier enrichment A/B was null. Prompt material is not the binding
   constraint there, which is the central finding of the benchmark restated from the other side.

One cell moves the wrong way: nemotron's capability-only Resource selection goes 10→9. That is one
item, well inside replicate noise.

## One directive is worth 12 rows

`BATCH.common.filesystems_declared` — the ALCF `#PBS -l filesystems=` line — is violated on 31 of
40 unaugmented Batch items and is fatal, so one omission fails the item. Scored as minor, the
unaugmented Batch stage recovers from 1/40 to 13/40. Several of those answers are otherwise
correct scripts: right queue, walltime, select, account, module, launcher and rank count, missing
exactly that one line. "Models cannot write batch scripts unaugmented" would be the wrong reading;
"they write good scripts that omit one site-specific directive, and that directive is fatal" is
the right one.

## What this comparison cannot tell you

- **There is no internal control.** In the base/rich A/B, 120 of 160 items had byte-identical
  prompts and calibrated the noise floor at ±4 rows. Every item differs here, so the noise floor
  is imported: ±4 rows from that control, and 20 of 320 cells flip between judge replicates. The
  effect is an order of magnitude larger than either, but the absence is a real limitation.
- **The ladder has a hole.** `cat` — catalog facts without the worked example — is derived and
  gate-checked but not yet answered, so `bare → rich` cannot be split into *knowledge* and
  *demonstration*.
- **The capability/supplied split is a judgement call.** It is recorded rule by rule with its
  argument in [`judge/skills/knowledge_dependence.yaml`](../judge/skills/knowledge_dependence.yaml)
  and registered as `r29-capability` before these answers existed, so it can be argued with — but
  it is ours, not a measurement.
- **Unaugmented answers are judged slightly *more* consistently**, not less: 3 of 135 rows flip
  between replicates against 5% on the augmented arm. Blunt failures are easy to judge. So the
  gap is not inflated by judge noise on the stripped arm.

## Reproducing

The harness for this experiment is on the `experiment/augmentation-ablation` branch:

```bash
python -m benchmark.strip --derive --arms bare,cat     # build the arms from samples_v8base
python -m benchmark.strip --verify                     # prove the deletion is reversible
TRINITY_VER=v8bare python -m benchmark.run --answer
python -m judge.rejudge --corpus v8bare --rubric r27 --mode skill --runs 3
python -m audit.matrix --arms bare,rich --per-arm --view knowledge+mixed
python -m audit.ab --arms bare,rich --runs 3
python tools/build_result_page.py && python tools/build_ab_report.py --arms bare,rich
```
