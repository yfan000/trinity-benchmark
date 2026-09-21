# Verdicts — nekrs@polaris, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `c03c63fc5fbf`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The claims that NekRS is GPU-accelerated and a spectral-element Navier-Stokes solver agree with the authoritative catalog entry; no facility fact is contradicted. |
| `SOFT.common.correct_application` | fatal | satisfied | NekRS matches the catalog's GPU-accelerated spectral-element Navier-Stokes solver and the workload's incompressible spectral-element CFD restart on A100 GPUs. |
| `SOFT.common.names_one_application` | major | satisfied | The answer names exactly one selection: “Selected Application: NekRS.” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes NekRS as GPU-accelerated and built for NVIDIA GPUs, but makes no promise about this run's speed, overhead, or walltime. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's facility-relevant claim that NekRS is GPU-accelerated is consistent with the catalog field "gpu_support: true"; it makes no contradictory module, path, dependency, or loading claims. |
| `SOFT.common.correct_application` | fatal | satisfied | NekRS matches the workload as a GPU-accelerated spectral-element Navier-Stokes CFD solver suitable for incompressible flow and A100 GPUs. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects exactly one application: "Selected Application: NekRS". |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes NekRS as "GPU-accelerated" and "optimized for the A100 GPU architecture," which are software/architecture characteristics rather than promises about this run's performance. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's facility-facing claim that NekRS is installed and GPU-ready agrees with the catalog entry: system Polaris and gpu_support: true. |
| `SOFT.common.correct_application` | fatal | satisfied | NekRS matches the catalog description of a GPU-accelerated spectral element Navier-Stokes CFD solver and fits the A100 restartable CFD workload. |
| `SOFT.common.names_one_application` | major | satisfied | The answer selects exactly one application: “NekRS.” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes NekRS as GPU-optimized but makes no unquantified prediction about this run's speed, overhead, or walltime. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The statements that NekRS is GPU-accelerated, spectral-element, and a Navier-Stokes solver agree with the authoritative catalog facts; no facility fact is contradicted. |
| `SOFT.common.correct_application` | fatal | satisfied | NekRS matches the catalog entry and workload: a GPU-accelerated spectral-element Navier-Stokes solver for Polaris A100 GPUs. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly recommends exactly one application: "NekRS." |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes NekRS as GPU-accelerated and optimized for Polaris, but does not promise a particular run will finish quickly or have minimal overhead. |
