# lammps@polaris — Batch job creation

Write the submission script: directives, environment, launch command.

**7 of 8 attempts passed.**

| model | base arm | enriched arm |
|---|---|---|
| `nemotron-3-ultra` | pass (11 rules) | pass (11 rules) |
| `gemma-4-31b` | pass (11 rules) | pass (11 rules) |
| `gpt-oss-120b` | pass (11 rules) | **fail** (1/11 violated) |
| `llama-3.1-8b` | pass (11 rules) | pass (11 rules) |

- [`prompt.base.md`](prompt.base.md) — what the models saw
- the enriched arm's prompt is byte-identical to the base arm's: enrichment touches Input preparation only, so this anchor is one of the 30 that act as the A/B control
- [`reference.md`](reference.md) — Claude's reference answer
- [`base/`](base/) · [`rich/`](rich/) — each model's answer and `verdicts.md`
