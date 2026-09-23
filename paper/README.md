# IPDPS paper draft

`main.tex` is an anonymous IEEE-conference paper draft built from the benchmark evidence in `../docs/` and `../examples/`. It deliberately scopes results to the evaluated pre-submission tasks and keeps the DEV-only, LLM-judge, small-cell, and no-execution-validation limitations in the body.

`abstract.txt` is the standalone submission abstract (239 words).

The system-design description is grounded in the [Trinity Hub documentation](https://docs.trinityscience.org/) and treats the [Application Catalog](https://github.com/zhenghh04/application_catalog) as the facility-aware knowledge plane. It distinguishes the public Hub registry from the runtime workspace, and records the catalog revision used by the benchmark: `4c6a192242452d798afb6b7f1e44362f263a1c7d`.

Build locally with:

```bash
cd paper
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

Before submission: replace the anonymous author block, freeze the result version/date, confirm the IPDPS track and page limit for the target year, and update the artifact/reproducibility section to the conference's current required format.
