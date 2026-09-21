# Verdicts — pytorch@sophia, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `c03c63fc5fbf`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's facility-specific claim that PyTorch 2.5.0a0 was built on Sophia with MPI+NCCL backends agrees with the authoritative catalog entry. |
| `SOFT.common.correct_application` | fatal | satisfied | PyTorch (MPI) is the catalog-listed Sophia application with MPI+NCCL distributed backends, fitting single-node multi-GPU ResNet-50 data-parallel training. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly identifies one selection: "Selected Application: PyTorch (MPI)." |
| `SOFT.common.no_vague_performance_claims` | minor | **violated** | It makes an unquantified run-performance claim by stating PyTorch "minimizes overhead and complexity" for the workload. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The statement that PyTorch (MPI) is built with MPI and NCCL distributed backends agrees with the authoritative catalog description. |
| `SOFT.common.correct_application` | fatal | satisfied | PyTorch (MPI) is the catalog-listed Sophia application with MPI+NCCL distributed backends, matching the required multi-GPU NCCL data-parallel training. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects exactly one application: “PyTorch (MPI).” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It makes no prediction or unquantified promise about the production run's performance. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | **violated** | It incorrectly states “SLURM on Sophia,” whereas the target system is explicitly specified as using PBS Pro. |
| `SOFT.common.correct_application` | fatal | satisfied | PyTorch (MPI) is the catalog-listed application with MPI+NCCL distributed backends, directly matching single-node multi-GPU NCCL data-parallel ResNet-50 training. |
| `SOFT.common.names_one_application` | major | satisfied | It explicitly identifies one answer: “Selected application: PyTorch (MPI).” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | The response makes no unquantified prediction about this run's performance or completion time. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The stated facility-relevant claim that PyTorch (MPI) is installed on Sophia and supports NCCL aligns with the catalog description: “PyTorch 2.5.0a0 with MPI+NCCL distributed backends, built from source on Sophia.” |
| `SOFT.common.correct_application` | fatal | satisfied | PyTorch (MPI) is the catalog-listed Sophia application with MPI+NCCL distributed backends and fits ResNet-50 multi-GPU data-parallel training. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly recommends one application: “PyTorch (MPI).” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It makes no promise about this run's speed, overhead, or ability to complete within a walltime. |
