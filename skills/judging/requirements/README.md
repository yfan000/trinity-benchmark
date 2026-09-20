# The judging requirement library

**The requirements are the judging skill.** Not a prose rubric with separate per-sample
checklists — one versioned library, organised by subtask and by software, written once and
reused. The judge returns a verdict on each requirement; the 0-2 dimension scores are derived
from those verdicts by a stated rule, so every score traces back to the rules behind it.

Editing these files *is* how the skill improves.

## Layout

```
_common.yaml                        holds for every subtask
software_selection/_common.yaml
input_preparation/
  _common.yaml                      required files present, no binary contents, counts match
  qe.yaml  hpl.yaml  gromacs.yaml   per-software format rules
  ...
resource_selection/_common.yaml     queue legality, rank layout, arithmetic
batch_job_creation/
  _common.yaml                      scheduler-family rules
  polaris.yaml                      site rules that do NOT transfer between machines
```

Input-format rules are keyed on **software** because they transfer between machines: QE
namelist syntax is the same on Polaris and Aurora. Queue, module and directive rules are keyed
on **(software, system)** because they do not.

## One requirement

```yaml
- id: BATCH.common.filesystems_declared
  claim: "The job declares every filesystem it touches with -l filesystems="
  decided_by: deterministic          # deterministic | judge
  check: {kind: regex, pattern: '(?m)^\s*#PBS\s+-l\s+filesystems='}
  dimension: usability               # which score this feeds
  severity: fatal                    # fatal | major | minor
  source: "run:138/138"              # run:N/M | catalog:<path>#<field> | format:<spec> | model
  rationale: "present in every PBS script in the archive, across all six applications"
```

## Fields

| field | meaning |
|---|---|
| `id` | stable, dotted: `SUBTASK.scope.name`. Never reused after removal. |
| `claim` | one sentence a human reviewer can agree or disagree with |
| `decided_by` | `deterministic` runs in Python before the judge; `judge` needs reading comprehension |
| `check` | how a deterministic requirement is evaluated. Absent for `judge` items. |
| `dimension` | `correctness`, `completeness` or `usability` |
| `severity` | `fatal` forces usability 0 and `fatal_error: true` |
| `source` | provenance — see below |
| `support` | for mined rules, how many runs back it |
| `applies_if` | optional guard, e.g. `{scheduler: "PBS Pro"}` |

## Provenance is load-bearing

`source` is not decoration. Mining the real runs showed that rules derived from documentation
and from LLM defect-clustering were **wrong in specific, measurable ways**:

- `cd ${PBS_O_WORKDIR}` was written into the site conventions as a rule. It appears in
  **3 of 138** real scripts. A judge enforcing it would fail 98% of working scripts.
- `place=scatter` was proposed by defect-clustering as the highest-reach Batch fix
  ("reaches ~38"). It is optional in practice — never universal in any application.
- `filesystems=` ordering: both `home:eagle` (97) and `eagle:home` (45) appear in successful
  runs, so ordering is free choice, which no catalog states.

So: `source: model` means an LLM asserted it and nothing has confirmed it — provisional, and
the first thing to doubt when a human disagrees with a verdict. `source: run:N/M` means N of M
real successful runs did it.

## free_choice

A requirement is not the only way to be right. Where successful runs disagree with each other,
that disagreement is evidence that the judge must not deduct — recorded as `free_choice`
entries rather than left to the judge's discretion. This is the one thing that cannot be
derived from a catalog and can only come from several runs of the same code.

## Known inconsistency: the prompts still teach a convention the runs contradict

`skills/trinity_site.py` supplies site conventions **into the prompt** for Batch job creation.
Two of them are contradicted by the mined runs:

- it states `cd ${PBS_O_WORKDIR}` as a rule (3 of 138 real scripts do this)
- it gives one `filesystems=` ordering (both orderings appear, 97 vs 45)

So a model is told one thing and graded by a library that knows better. **Decided 2026-09-15:
fix the judging side only for now; regenerate samples later.** Changing the prompts means
re-running all four models and would invalidate the v6 comparison series mid-experiment.

This is handled correctly rather than ignored: both appear as `free_choice` in
`batch_job_creation/_common.yaml`, so a model that follows the prompt's advice and a model
that follows real practice are both accepted. Neither is penalised for the mismatch.

When the samples are regenerated, correct `trinity_site.py` first and drop these two
free_choice axes to plain requirements.

## Changing the library

Every change needs a reason that names rows. See `skills/judging/registry.json`: each version
records its parent, a rationale, and the specific samples that motivated each edit. A change
that cannot name at least two rows it would fix should not be made.
