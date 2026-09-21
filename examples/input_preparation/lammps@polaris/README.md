# lammps@polaris — Input preparation

Write the input files the application needs, complete and runnable, for the physical system the prompt describes.

**4 of 8 attempts passed.**

| model | base arm | enriched arm |
|---|---|---|
| `nemotron-3-ultra` | pass (9 rules) | pass (9 rules) |
| `gemma-4-31b` | pass (9 rules) | pass (9 rules) |
| `gpt-oss-120b` | **fail** (1/9 violated) | **fail** (1/9 violated) |
| `llama-3.1-8b` | **fail** (2/9 violated) | **fail** (1/9 violated) |

- [`prompt.base.md`](prompt.base.md) — what the models saw
- [`prompt.rich.md`](prompt.rich.md) — the enriched arm's prompt
- [`reference.md`](reference.md) — Claude's reference answer
- [`base/`](base/) · [`rich/`](rich/) — each model's answer and `verdicts.md`
