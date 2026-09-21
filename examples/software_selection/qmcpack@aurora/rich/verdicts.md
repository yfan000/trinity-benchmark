# Verdicts — qmcpack@aurora, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `c03c63fc5fbf`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The stated Aurora architecture claim—“SYCL/OpenMP offload for Intel GPU (PVC) acceleration”—agrees with the catalog description of QMCPACK GPU support. |
| `SOFT.common.correct_application` | fatal | satisfied | QMCPACK directly matches the stated VMC/DMC Quantum Monte Carlo workload and is the catalog-listed Quantum Monte Carlo application for Aurora. |
| `SOFT.common.names_one_application` | major | satisfied | The answer identifies exactly one application: “Selected application: QMCPACK”. |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes QMCPACK's GPU-offload capability but makes no unquantified prediction about this run's performance or completion time. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer’s facility claim that QMCPACK is optimized through “SYCL/OpenMP offload for Intel GPU acceleration” agrees with the authoritative catalog description. |
| `SOFT.common.correct_application` | fatal | satisfied | QMCPACK is the catalog-listed Quantum Monte Carlo application and matches the stated VMC/DMC workload. |
| `SOFT.common.names_one_application` | major | satisfied | The answer names exactly one selection: “Selected Application: QMCPACK.” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes Aurora optimization via “SYCL/OpenMP offload for Intel GPU acceleration” without promising performance for this specific run. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The stated “SYCL/OpenMP offload” and Intel GPU support agree with the catalog description of QMCPACK GPU acceleration on Aurora. |
| `SOFT.common.correct_application` | fatal | satisfied | QMCPACK directly matches the specified VMC/DMC Quantum Monte Carlo workload and is the installed Aurora QMC application. |
| `SOFT.common.names_one_application` | major | satisfied | The answer names exactly one selected application: “QMCPACK.” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes QMCPACK as designed to scale and exploit Aurora hardware, rather than promising a particular performance outcome for this run. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's statement that QMCPACK has “SYCL/OpenMP offload for Intel GPU acceleration” agrees with the authoritative Aurora catalog description. |
| `SOFT.common.correct_application` | fatal | satisfied | QMCPACK is the catalog-listed Quantum Monte Carlo application and directly matches variational and diffusion Monte Carlo using HDF5/XML inputs. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly recommends exactly one application: “QMCPACK.” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes QMCPACK as designed for large-scale electronic-structure simulations but makes no unquantified prediction about this run's performance or completion time. |
