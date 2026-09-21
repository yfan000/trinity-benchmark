# Verdicts — qmcpack@aurora, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `c03c63fc5fbf`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The statement that Aurora's QMCPACK uses "SYCL/OpenMP offload for Intel Data Center GPU (PVC) acceleration" is consistent with the authoritative catalog fact that it has SYCL/OpenMP offload for Intel GPU acceleration. |
| `SOFT.common.correct_application` | fatal | satisfied | QMCPACK is the catalog-listed Quantum Monte Carlo application and matches the stated VMC/DMC electron-correlation workload. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects exactly one application: "Selected application: QMCPACK". |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes QMCPACK's supported methods and Aurora GPU-offload build without making a prediction about this run's speed, overhead, or completion time. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The claim that QMCPACK has “SYCL/OpenMP offload for Intel GPU acceleration” agrees with the authoritative catalog description and GPU-support field. |
| `SOFT.common.correct_application` | fatal | satisfied | QMCPACK is the installed Quantum Monte Carlo application and directly fits the requested variational and diffusion Monte Carlo electron-correlation workload. |
| `SOFT.common.names_one_application` | major | satisfied | The answer names exactly one application: “Selected Application: QMCPACK.” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes QMCPACK as optimized for Aurora hardware but makes no unquantified prediction about the performance of this specific run. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's Aurora GPU statement matches the catalog description: "Quantum Monte Carlo code with SYCL/OpenMP offload for Intel GPU acceleration." |
| `SOFT.common.correct_application` | fatal | satisfied | QMCPACK is the installed Quantum Monte Carlo application and directly supports the required VMC and DMC workload. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects one application: "QMCPACK". |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | Statements that QMCPACK is optimized for Aurora and has demonstrated scaling describe software capability/history, not an unquantified promise about this specific run. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The statement that QMCPACK uses “SYCL/OpenMP offloading for Intel GPU acceleration” agrees with the catalog description; no facility fact is contradicted. |
| `SOFT.common.correct_application` | fatal | satisfied | QMCPACK directly matches the described variational and diffusion Quantum Monte Carlo workload and the authoritative catalog identifies it as the Aurora Quantum Monte Carlo code. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly recommends only “QMCPACK” as the selected application. |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes QMCPACK's intended Aurora optimization but makes no unquantified prediction about this run's performance or completion time. |
