# Verdicts — nekrs@polaris, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `c03c63fc5fbf`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's facility-related claims that NekRS is installed on Polaris and has GPU support agree with the catalog; no recorded catalog field is contradicted. |
| `SOFT.common.correct_application` | fatal | satisfied | NekRS matches the catalog description: a GPU-accelerated spectral element Navier-Stokes solver, fitting incompressible spectral-element CFD on A100 GPUs. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects exactly one application: "Selected application: NekRS". |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes NekRS as GPU-accelerated and suitable for A100s but makes no unquantified prediction about this run's performance or completion time. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's facility-relevant statement that NekRS is GPU-accelerated is consistent with the catalog entry's "gpu_support: true" and GPU-accelerated Navier-Stokes description. |
| `SOFT.common.correct_application` | fatal | satisfied | NekRS matches the required GPU-accelerated spectral-element incompressible Navier-Stokes CFD workload on Polaris A100 GPUs and supports restart from field files. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects exactly one application: "Selected Application: NekRS". |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes NekRS as GPU-accelerated and optimized for GPU architectures, but makes no promise about performance or completion time for this specific run. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's facility-related claim that NekRS is available and GPU-accelerated agrees with the catalog fields app: NekRS, system: polaris, and gpu_support: true. |
| `SOFT.common.correct_application` | fatal | satisfied | NekRS matches the catalog description: a GPU-accelerated spectral-element Navier-Stokes solver, fitting incompressible spectral-element CFD on A100 GPUs. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects exactly one application: “NekRS”. |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It says NekRS is “optimized for the large-scale GPU nodes of Polaris,” which describes the software rather than promising a specific run outcome. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The claims that NekRS is GPU-accelerated, supports Navier-Stokes spectral-element CFD, and is installed on Polaris do not contradict the catalog entry. |
| `SOFT.common.correct_application` | fatal | satisfied | NekRS matches the catalog and workload: it is the GPU-accelerated spectral-element Navier-Stokes solver appropriate for incompressible flow and A100 GPUs. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly recommends exactly one application: "NekRS". |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes NekRS as GPU-accelerated and optimized for A100 GPUs, but makes no unquantified promise about this run's runtime or overhead. |
