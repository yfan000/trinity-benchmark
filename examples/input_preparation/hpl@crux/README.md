# hpl@crux — Input preparation

Write the input files the application needs, complete and runnable, for the physical system the prompt describes.

**6 of 8 attempts passed.**

| model | base arm | enriched arm |
|---|---|---|
| `nemotron-3-ultra` | pass (13 rules) | pass (13 rules) |
| `gemma-4-31b` | pass (13 rules) | pass (13 rules) |
| `gpt-oss-120b` | pass (13 rules) | pass (13 rules) |
| `llama-3.1-8b` | **fail** (2/13 violated) | **fail** (2/13 violated) |

- [`prompt.base.md`](prompt.base.md) — what the models saw
- [`prompt.rich.md`](prompt.rich.md) — the enriched arm's prompt
- [`reference.md`](reference.md) — Claude's reference answer
- [`base/`](base/) · [`rich/`](rich/) — each model's answer and `verdicts.md`
