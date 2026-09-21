# Verdicts — lammps@polaris, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `c03c63fc5fbf`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | Although it makes capability claims about GROMACS, it does not contradict any recorded catalog field; the supplied catalog facts only record LAMMPS GPU support via Kokkos. |
| `SOFT.common.correct_application` | fatal | **violated** | The authoritative Polaris catalog identifies LAMMPS as the installed classical MD application with Kokkos GPU acceleration, but the answer selects GROMACS. |
| `SOFT.common.names_one_application` | major | satisfied | The response names only one selection: "Selected application: GROMACS". |
| `SOFT.common.no_vague_performance_claims` | minor | **violated** | It makes unquantified run-specific promises, including "provides the shortest time-to-solution" and "ensuring the urgent result deadline is met". |

## gemma-4-31b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer does not contradict any recorded facility fact in the supplied catalog; the catalog records GPU support for LAMMPS but contains no conflicting NAMD facility fields. |
| `SOFT.common.correct_application` | fatal | **violated** | The authoritative Polaris catalog identifies LAMMPS, described as "Classical molecular dynamics with GPU acceleration via Kokkos," as the fitting installed application; the answer instead selects NAMD. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects exactly one application: "Selected Application: NAMD". |
| `SOFT.common.no_vague_performance_claims` | minor | **violated** | It makes unquantified turnaround claims for this workload, including that NAMD "minimizes CPU-GPU data transfer overhead" and is critical for "achieving the shortest time-to-result". |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | Although it makes unsupported statements about GROMACS CUDA tuning and queue usage, these do not directly contradict any recorded catalog field; the supplied catalog facts record only LAMMPS GPU support via Kokkos. |
| `SOFT.common.correct_application` | fatal | **violated** | The authoritative Polaris catalog identifies LAMMPS, with Kokkos GPU acceleration, as the installed application matching the classical GPU-accelerated MD workload; the answer instead selects GROMACS. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects exactly one application: "GROMACS". |
| `SOFT.common.no_vague_performance_claims` | minor | **violated** | It makes unquantified turnaround promises for this run, including "delivering the highest per-node performance," "minimizing wall-clock time," and "typically allocated to the ‘short-run / high-throughput’ partition" for minimal wait. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | Although the answer incorrectly attributes Kokkos to GROMACS, the supplied catalog records no GROMACS facility fields that this statement directly contradicts; it only records LAMMPS's Kokkos support. |
| `SOFT.common.correct_application` | fatal | **violated** | The authoritative Polaris catalog identifies LAMMPS as the classical MD application with GPU acceleration via Kokkos; the answer instead selects GROMACS and attributes the Kokkos backend to it. |
| `SOFT.common.names_one_application` | major | satisfied | The answer clearly selects one application: "I recommend using GROMACS." |
| `SOFT.common.no_vague_performance_claims` | minor | **violated** | It makes an unquantified run-specific performance prediction: GPU acceleration "should provide fast turnaround times on the A100 GPUs in Polaris." |
