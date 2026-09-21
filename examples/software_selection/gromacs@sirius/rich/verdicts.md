# Verdicts — gromacs@sirius, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `c03c63fc5fbf`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's GPU-acceleration statement is consistent with the catalog's recorded CUDA GPU offload support and makes no contradictory facility-specific claims. |
| `SOFT.common.correct_application` | fatal | satisfied | GROMACS matches the catalogued Sirius application for high-performance biomolecular molecular dynamics with CUDA GPU offload, and the stated binary run-input matches its .tpr format. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects exactly one application: "Selected Application: GROMACS". |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes GROMACS as optimized for GPU-accelerated MD scaling but makes no unquantified promise about the performance or completion time of this specific run. |

## gemma-4-31b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer makes no contradictory claims about recorded Sirius facility facts such as a module, installation path, or GPU-support field. |
| `SOFT.common.correct_application` | fatal | **violated** | The authoritative Sirius catalog identifies GROMACS as the installed biomolecular MD application with CUDA GPU offload; the answer instead selects NAMD. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects exactly one application: “Selected Application: NAMD.” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes NAMD as “optimized for high scalability,” which is a statement about the software's design rather than an unquantified promise for this specific run. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer does not contradict any recorded facility fact for the catalogued Sirius GROMACS entry. |
| `SOFT.common.correct_application` | fatal | **violated** | The authoritative Sirius catalog identifies GROMACS as the installed CUDA-GPU biomolecular MD application fitting this workload; the answer instead selects NAMD. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects exactly one application: "Selected application: NAMD." |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | The statements describe NAMD's general intended GPU-scaling capabilities rather than promising a specific performance outcome for this run. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's facility-relevant GPU claim is consistent with the catalog entry stating CUDA GPU offload and gpu_support: true. |
| `SOFT.common.correct_application` | fatal | satisfied | GROMACS matches the catalogued high-performance biomolecular molecular-dynamics application with CUDA GPU offload for the stated GPU-node scaling workload. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly recommends one application: “GROMACS”. |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied ⚠︎ flipped across runs | It describes GROMACS as GPU-accelerated and scalable, but does not promise a specific performance outcome for this run. |
