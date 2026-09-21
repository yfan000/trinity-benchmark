# Verdicts — qe@aurora, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `c03c63fc5fbf`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | **violated** | The answer claims the catalog lists Quantum ESPRESSO “with Intel oneAPI/GPU support,” but the authoritative catalog fact records gpu_support: false. |
| `SOFT.common.correct_application` | fatal | satisfied | Quantum ESPRESSO matches the stated plane-wave DFT SCF workload and the described PWscf-style CONTROL, SYSTEM, ELECTRONS, and atomic-species input structure. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects only “Quantum ESPRESSO.” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes Quantum ESPRESSO as MPI-parallelized and suitable for parameter sweeps, without promising a particular runtime or performance outcome for this run. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer does not contradict any recorded facility facts; the catalog identifies Quantum ESPRESSO as installed on Aurora for plane-wave DFT with Intel oneAPI. |
| `SOFT.common.correct_application` | fatal | satisfied | Quantum ESPRESSO is the catalogued plane-wave DFT electronic-structure application and matches the CONTROL, SYSTEM, and ELECTRONS input namelists. |
| `SOFT.common.names_one_application` | major | satisfied | The answer names exactly one selection: "Quantum ESPRESSO." |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It makes no prediction about this run's runtime, overhead, or performance; "optimized for the system's architecture" describes software suitability rather than a run-specific promise. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | **violated** | The answer claims "SYCL/OpenMP off-loading" and "native acceleration on Aurora’s Intel Data Center GPUs," but the authoritative catalog records "gpu_support: false" for Quantum ESPRESSO. |
| `SOFT.common.correct_application` | fatal | satisfied | Quantum ESPRESSO is the catalog-listed plane-wave DFT application and matches the described SCF namelist/card input format. |
| `SOFT.common.names_one_application` | major | satisfied | The answer selects exactly one application: "Quantum ESPRESSO". |
| `SOFT.common.no_vague_performance_claims` | minor | **violated** | It makes unquantified performance assertions that it "scales efficiently with MPI+SYCL" and can "fully exploit[] the GPU resources." |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer states that Quantum ESPRESSO is installed and uses Intel oneAPI, consistent with the catalog description; it does not explicitly claim Quantum ESPRESSO itself has GPU support. |
| `SOFT.common.correct_application` | fatal | satisfied | Quantum ESPRESSO is the catalog-listed Plane-wave DFT code for electronic-structure calculations, matching the described SCF workload and QE-style namelist inputs. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly recommends one application: "Quantum ESPRESSO." |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes Quantum ESPRESSO's suitability and capabilities but makes no promise about the performance or completion time of this specific run. |
