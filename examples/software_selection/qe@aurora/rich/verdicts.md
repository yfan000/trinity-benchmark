# Verdicts — qe@aurora, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `c03c63fc5fbf`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | **violated** | The answer claims the installed version provides “Intel Xe GPU (XPU) accelerators via SYCL/DPC++ offload,” but the authoritative catalog records “gpu_support: false” for Quantum ESPRESSO on Aurora. |
| `SOFT.common.correct_application` | fatal | satisfied | Quantum ESPRESSO is explicitly the installed Aurora application for plane-wave DFT electronic-structure calculations and matches the QE-style CONTROL, SYSTEM, and ELECTRONS input namelists. |
| `SOFT.common.names_one_application` | major | satisfied | The answer names only “Quantum ESPRESSO” as the selected application. |
| `SOFT.common.no_vague_performance_claims` | minor | **violated** ⚠︎ flipped across runs | It makes an unquantified performance assurance: “ensuring optimized performance ... which is critical for the high-throughput parameter sweep.” |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer does not make any facility-specific claim that contradicts the Quantum ESPRESSO catalog entry. |
| `SOFT.common.correct_application` | fatal | satisfied | Quantum ESPRESSO is the catalog-listed plane-wave DFT electronic-structure application and matches the described SCF input namelists. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects exactly one application: “Selected Application: Quantum ESPRESSO.” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It makes no prediction or unquantified promise about the performance of this run. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | **violated** | The answer claims "Intel oneAPI SYCL off-loading" and that it can exploit "PVC accelerators," but the authoritative catalog records "gpu_support: false" for Quantum ESPRESSO on Aurora. |
| `SOFT.common.correct_application` | fatal | satisfied | Quantum ESPRESSO is the installed plane-wave DFT application matching SCF electronic-structure calculations and the described QE namelist/card input format. |
| `SOFT.common.names_one_application` | major | satisfied | The response selects exactly one application: "Quantum ESPRESSO." |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | The performance statements describe the software/version generally (e.g., "delivers strong performance"), rather than promising a specific outcome or completion time for this run. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer makes no claim contradicting catalog-recorded facility facts; its statement that Quantum ESPRESSO is installed on Aurora is consistent with the catalog. |
| `SOFT.common.correct_application` | fatal | satisfied | Quantum ESPRESSO matches the catalog entry for a plane-wave DFT electronic-structure code on Aurora and matches the described QE-style namelists and species blocks. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly recommends exactly one application: “Quantum ESPRESSO.” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes Quantum ESPRESSO as suited to HPC and plane-wave DFT but makes no unquantified prediction about this run's performance or completion time. |
