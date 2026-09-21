# Verdicts — hpl@crux, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `c03c63fc5fbf`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The statement that HPL is a “CPU-only” build matches the authoritative catalog fact gpu_support: false and the catalog description. |
| `SOFT.common.correct_application` | fatal | satisfied | HPL is explicitly the High Performance LINPACK benchmark and directly matches the requested Linpack-style dense linear algebra workload. |
| `SOFT.common.names_one_application` | major | satisfied | The answer identifies only one application: “Selected Application: HPL.” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes HPL’s intended purpose and scalability but makes no unquantified prediction about the performance of this specific run. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's CPU-only statement agrees with the catalog field "gpu_support: false" and it makes no contradictory facility-specific claims. |
| `SOFT.common.correct_application` | fatal | satisfied | HPL is the cataloged High Performance LINPACK benchmark and directly matches the stated Linpack-style dense linear algebra workload. |
| `SOFT.common.names_one_application` | major | satisfied | The answer names exactly one application: "HPL". |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes HPL as designed for dense linear algebra but makes no prediction or unquantified performance promise for this run. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's facility-relevant statement that HPL is a CPU-only build agrees with the catalog fact “gpu_support: false” and description “CPU-only build”; it makes no contradictory module, path, or dependency claims. |
| `SOFT.common.correct_application` | fatal | satisfied | HPL is explicitly the High Performance LINPACK benchmark and directly matches the stated Linpack-style dense linear algebra workload. |
| `SOFT.common.names_one_application` | major | satisfied | The answer selects exactly one application: “HPL — High Performance LINPACK benchmark (CPU-only build).” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes HPL's intended purpose and CPU-only suitability without promising a particular runtime or performance outcome for this run. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer states that HPL is installed and CPU-only, consistent with the catalog entry “High Performance LINPACK benchmark (CPU-only build).” |
| `SOFT.common.correct_application` | fatal | satisfied | HPL is the installed High Performance LINPACK benchmark and directly matches the stated Linpack-style dense linear algebra workload. |
| `SOFT.common.names_one_application` | major | satisfied | The answer recommends exactly one application: “HPL (High Performance LINPACK) benchmark application.” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes HPL’s intended purpose and CPU-only suitability but makes no unquantified prediction about this run’s performance or completion time. |
