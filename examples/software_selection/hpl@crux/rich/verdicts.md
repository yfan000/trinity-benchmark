# Verdicts — hpl@crux, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `c03c63fc5fbf`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The statement that HPL is a "CPU-only build" matches the authoritative catalog fact "gpu_support: false" and its CPU-only description; no conflicting facility details are claimed. |
| `SOFT.common.correct_application` | fatal | satisfied | HPL is the catalog-listed High Performance LINPACK benchmark and directly matches the requested dense linear algebra Linpack-style workload. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects exactly one application: "Selected Application: HPL". |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes HPL as the standard Linpack benchmark and notes architecture compatibility, without promising runtime or performance for this run. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer’s statement that HPL is designed for the Linpack benchmark is consistent with the catalog description and makes no contradictory facility-specific claims. |
| `SOFT.common.correct_application` | fatal | satisfied | HPL is the installed High Performance LINPACK benchmark and directly matches the stated Linpack-style dense linear algebra workload. |
| `SOFT.common.names_one_application` | major | satisfied | The answer names exactly one application: “Selected Application: HPL”. |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes HPL’s intended purpose and makes no prediction or unquantified promise about this run's performance. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer’s facility-relevant statement that HPL is CPU-only agrees with the catalog fact “gpu_support: false” and “CPU-only build”; it makes no contradictory module, path, or dependency claims. |
| `SOFT.common.correct_application` | fatal | satisfied | HPL is the catalog-listed High Performance LINPACK benchmark and directly matches a Linpack-style dense linear-algebra workload. |
| `SOFT.common.names_one_application` | major | satisfied | The answer selects exactly one application: “HPL – High-Performance LINPACK benchmark (CPU-only build).” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes HPL’s intended benchmark purpose and CPU suitability without promising a runtime, efficiency, or performance outcome for this run. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The statement that HPL is a "CPU-only build" agrees with the catalog field gpu_support: false and description "High Performance LINPACK benchmark (CPU-only build)"; no facility fact is contradicted. |
| `SOFT.common.correct_application` | fatal | satisfied | HPL is explicitly the High Performance LINPACK benchmark and directly matches the stated Linpack-style dense linear algebra workload. |
| `SOFT.common.names_one_application` | major | satisfied | The answer recommends exactly one application: "HPL". |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes HPL's purpose and CPU-only suitability but makes no unquantified promise about this run's performance or completion time. |
