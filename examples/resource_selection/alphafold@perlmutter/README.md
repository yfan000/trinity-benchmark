# alphafold@perlmutter — Resource selection

Choose nodes, ranks, walltime and queue for a stated job, within the limits the prompt states.

**6 of 8 attempts passed.**

| model | base arm | enriched arm |
|---|---|---|
| `nemotron-3-ultra` | pass (10 rules) | pass (10 rules) |
| `gemma-4-31b` | pass (10 rules) | pass (10 rules) |
| `gpt-oss-120b` | pass (10 rules) | pass (10 rules) |
| `llama-3.1-8b` | **fail** (3/10 violated) | **fail** (5/10 violated) |

- [`prompt.base.md`](prompt.base.md) — what the models saw
- the enriched arm's prompt is byte-identical to the base arm's: enrichment touches Input preparation only, so this anchor is one of the 30 that act as the A/B control
- [`reference.md`](reference.md) — Claude's reference answer
- [`base/`](base/) · [`rich/`](rich/) — each model's answer and `verdicts.md`
