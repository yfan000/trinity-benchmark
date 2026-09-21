# Verdicts — gromacs@sirius, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `c03c63fc5fbf`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's facility-related GPU claim is consistent with the catalog's recorded CUDA GPU offload support and does not contradict any recorded facility fact. |
| `SOFT.common.correct_application` | fatal | satisfied | GROMACS is catalogued on Sirius as a high-performance biomolecular molecular-dynamics package with CUDA GPU offload, matching the biomolecular GPU-node scaling workload. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects exactly one application: “Selected Application: GROMACS.” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes GROMACS as having GPU acceleration and multi-node scaling capability, rather than promising a particular performance outcome for this run. |

## gemma-4-31b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer makes no contradictory claim about recorded Sirius facility facts such as a module, path, dependency, or documented GPU support. |
| `SOFT.common.correct_application` | fatal | **violated** | The authoritative Sirius catalog identifies GROMACS as the installed biomolecular MD application with CUDA GPU offload; the answer instead selects NAMD. |
| `SOFT.common.names_one_application` | major | satisfied | The response explicitly identifies a single selection: "Selected Application: NAMD." |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes NAMD as engineered for scalability and parallel efficiency, but does not promise a specific performance outcome for this run. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied ⚠︎ flipped across runs | The answer makes no claim contradicting any recorded catalog field; the supplied catalog facts record GROMACS details but no conflicting NAMD facility fact. |
| `SOFT.common.correct_application` | fatal | **violated** | The catalogued application fitting this Sirius biomolecular GPU-scaling workload is GROMACS, with CUDA GPU offload; the answer instead selects NAMD. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects one application: “Selected application: NAMD.” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | The statements describe NAMD’s general design and typical use (“scales efficiently” and “routinely used”), rather than promising a performance outcome for this specific run. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The claims that GROMACS is for biomolecular MD and supports GPU acceleration agree with the catalog description and gpu_support: true. |
| `SOFT.common.correct_application` | fatal | satisfied | GROMACS matches the catalogued Sirius application for high-performance biomolecular molecular dynamics with CUDA GPU offload. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly recommends one application: “I recommend GROMACS.” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes GROMACS as GPU-optimized and able to scale, but does not promise a specific performance outcome for this run. |
