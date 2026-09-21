# Verdicts — pytorch@sophia, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `c03c63fc5fbf`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's facility-specific claim that PyTorch 2.5.0a0 includes MPI and NCCL distributed backends agrees with the authoritative catalog entry; it does not contradict recorded facts. |
| `SOFT.common.correct_application` | fatal | satisfied | PyTorch (MPI) is the catalog-listed application with MPI+NCCL distributed backends, matching multi-GPU NCCL data-parallel ResNet-50 training. |
| `SOFT.common.names_one_application` | major | satisfied | The answer names one selection: "Selected Application: PyTorch (MPI)". |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes software capabilities and suitability but makes no unquantified promise about this run's performance or walltime. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The statement that PyTorch (MPI) is built with MPI and NCCL distributed backends agrees with the authoritative catalog description. |
| `SOFT.common.correct_application` | fatal | satisfied | PyTorch (MPI) is the catalog-listed application with MPI+NCCL distributed backends, matching multi-GPU ResNet-50 data-parallel training with NCCL synchronization. |
| `SOFT.common.names_one_application` | major | satisfied | The answer names one selection: "Selected Application: PyTorch (MPI)". |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | The answer makes no prediction or unquantified performance promise about this run. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's core facility claim—that PyTorch (MPI) is a Sophia-built PyTorch 2.5.0a0 installation with MPI+NCCL backends—matches the authoritative catalog and does not contradict recorded fields. |
| `SOFT.common.correct_application` | fatal | satisfied | PyTorch (MPI) is the catalog-listed Sophia application with MPI+NCCL distributed backends and is appropriate for multi-GPU ResNet-50 data-parallel training. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects one application: "PyTorch (MPI)"; DeepSpeed is only discussed as an alternative. |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes NCCL as providing "highest-throughput intra-node communication," which is a general software/communication characterization rather than an unquantified promise about this run's completion or performance. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's statement that PyTorch (MPI) has NCCL distributed support is consistent with the catalog description “PyTorch 2.5.0a0 with MPI+NCCL distributed backends, built from source on Sophia.” |
| `SOFT.common.correct_application` | fatal | satisfied | PyTorch (MPI) is the catalog-listed application with MPI+NCCL distributed backends, fitting single-node multi-GPU ResNet-50 data-parallel training. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects exactly one application: “PyTorch (MPI).” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It makes no promise about this run's speed, overhead, or completion time; describing PyTorch as “mature and widely-used” is not a run-performance promise. |
