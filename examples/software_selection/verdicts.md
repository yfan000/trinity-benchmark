# Verdicts — nemotron-3-ultra on nwchem@polaris

Majority across three judge replicates, judged by gpt56terra under rubric **r27**. Severities shown are the current library, **r28** (sha `c03c63fc5fbf`).

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | **satisfied** | The answer does not contradict recorded facility facts; its CPU-oriented description is consistent with the catalog’s gpu_support: false and 0 GPUs per node benchmark. |
| `SOFT.common.correct_application` | fatal | **satisfied** | NWChem is the cataloged application with the exact measured benchmark “H2O B3LYP/6-31G* single-point energy, 4 MPI ranks” on one node in 5 seconds. |
| `SOFT.common.names_one_application` | major | **satisfied** | The answer names exactly one selection: “Selected application: NWChem”. |
| `SOFT.common.no_vague_performance_claims` | minor | **satisfied** | It describes NWChem as MPI-parallelized and a natural match, but makes no unquantified promise about this run's performance. |
