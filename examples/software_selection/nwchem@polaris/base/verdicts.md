# Verdicts — nwchem@polaris, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `c03c63fc5fbf`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer does not contradict recorded facility facts; its CPU-oriented description is consistent with the catalog’s gpu_support: false and 0 GPUs per node benchmark. |
| `SOFT.common.correct_application` | fatal | satisfied | NWChem is the cataloged application with the exact measured benchmark “H2O B3LYP/6-31G* single-point energy, 4 MPI ranks” on one node in 5 seconds. |
| `SOFT.common.names_one_application` | major | satisfied | The answer names exactly one selection: “Selected application: NWChem”. |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes NWChem as MPI-parallelized and a natural match, but makes no unquantified promise about this run's performance. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer makes no contradictory facility-specific claims; its MPI statement is consistent with the catalog benchmark using 4 MPI ranks, and it does not claim GPU support, paths, modules, or loading details. |
| `SOFT.common.correct_application` | fatal | satisfied | NWChem is the catalog application benchmarked for the exact "H2O B3LYP/6-31G* single-point energy, 4 MPI ranks" workload. |
| `SOFT.common.names_one_application` | major | satisfied | The answer names exactly one selected application: "NWChem." |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | The response makes no prediction or unquantified promise about the runtime or performance of this specific run. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's CPU-only MPI characterization agrees with the catalog's “gpu_support: false”; it makes no contradictory facility-path, module, dependency, or loading claim. |
| `SOFT.common.correct_application` | fatal | satisfied | NWChem is the catalog application with the exact measured benchmark “H2O B3LYP/6-31G* single-point energy, 4 MPI ranks” on one CPU-only node in 5 seconds. |
| `SOFT.common.names_one_application` | major | satisfied | The answer identifies only one selection: “Selected application: NWChem.” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It cites the prompt's quantified prior result (“a few seconds,” matching the reported “~5 s”) rather than making an unquantified promise about this run. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer does not contradict cataloged facility facts; NWChem is cataloged as a CPU-only high-performance computational chemistry application with the matching measured benchmark. |
| `SOFT.common.correct_application` | fatal | satisfied | NWChem is the cataloged application for the exact H2O B3LYP/6-31G* single-point benchmark using 4 MPI ranks. |
| `SOFT.common.names_one_application` | major | satisfied | The answer selects only "NWChem" as the recommended application. |
| `SOFT.common.no_vague_performance_claims` | minor | **violated** | It makes an unquantified prediction for this run: "NWChem should be able to scale to 4 MPI ranks ... and provide a similar or slightly improved performance." |
