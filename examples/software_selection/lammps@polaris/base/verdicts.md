# Verdicts — lammps@polaris, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `c03c63fc5fbf`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer does not contradict any recorded catalog field; the supplied catalog facts record LAMMPS GPU support but do not record conflicting GROMACS facility details. |
| `SOFT.common.correct_application` | fatal | **violated** | The authoritative Polaris catalog entry matching this classical GPU-accelerated MD workload is LAMMPS, while the answer selects GROMACS. |
| `SOFT.common.names_one_application` | major | satisfied | The answer identifies exactly one application: "Selected Application: GROMACS". |
| `SOFT.common.no_vague_performance_claims` | minor | **violated** | It makes unquantified run-specific performance promises, including "consistently delivers the fastest time-to-solution on Polaris" and "minimizing both queue wait and wall-clock time". |

## gemma-4-31b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer makes no claim contradicting the recorded LAMMPS catalog facts; the catalog does not record a conflicting NAMD facility field. |
| `SOFT.common.correct_application` | fatal | **violated** | The authoritative Polaris catalog entry identifies LAMMPS as the installed classical MD application with GPU acceleration via Kokkos; the answer instead selects NAMD. |
| `SOFT.common.names_one_application` | major | satisfied | The answer names exactly one application: "Selected Application: NAMD". |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | The throughput and GPU-residency statements describe NAMD's design rather than making a specific unquantified completion-time promise for this run. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | Although it makes unsupported facility-specific assertions about GROMACS, these do not directly contradict any recorded catalog field; the supplied catalog facts only record LAMMPS and its GPU support. |
| `SOFT.common.correct_application` | fatal | **violated** | The authoritative Polaris catalog entry identifies LAMMPS as the installed classical MD application with GPU acceleration via Kokkos; the answer instead selects GROMACS. |
| `SOFT.common.names_one_application` | major | satisfied | The response names exactly one selection: “Selected application: GROMACS.” |
| `SOFT.common.no_vague_performance_claims` | minor | **violated** | It makes unquantified run-specific turnaround promises, including “This typically results in the shortest queue times” and “delivering the shortest time-to-result.” |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer does not contradict any recorded catalog field such as an install path, module, dependency, or GPU-support field. |
| `SOFT.common.correct_application` | fatal | **violated** | The authoritative Polaris catalog identifies LAMMPS as the installed classical-MD application with GPU acceleration via Kokkos; the answer instead selects GROMACS. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects one application: "the selected application is GROMACS." |
| `SOFT.common.no_vague_performance_claims` | minor | **violated** | It makes unquantified turnaround claims for this workload, including that GROMACS "allows for fast execution times" and is "well-matched" to the minimal-wait, shortest-time-to-result priority. |
