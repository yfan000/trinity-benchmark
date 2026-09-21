# Verdicts — pytorch@sophia, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `79f1535225d9`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The 1-rank-per-GPU layout and use of NCCL for GPU collectives are consistent with the supplied PyTorch MPI/NCCL guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | It explicitly labels the throughput and runtime as assumptions/estimates and states that no measured data exists; it does not claim a measurement or prior observed run. |
| `RES.common.no_reservation_queue` | major | satisfied | The selected queue is "by-node," a named standard queue rather than a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The final request is 2 nodes in "by-node," whose stated node range is 1–8; the answer's final limit check shows 1 ≤ 2 ≤ 8. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard Sophia queue "by-node," which is listed in the catalog queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final specification states 2 nodes × 8 ranks per node = 16 total ranks, with one GPU per rank and 8 GPUs per node. |
| `RES.common.rank_layout_plausible` | major | satisfied | The answer requests 8 ranks per node with 1 GPU per rank, exactly mapping to Sophia's 8 A100 GPUs per node and not exceeding the stated GPU hardware. |
| `RES.common.ranks_match_build_defaults` | major | not_applicable | The supplied catalog build defaults record nodes, walltime, and queue but no ranks-per-node or GPUs-per-rank default to match deterministically. |
| `RES.common.sizing_not_absurd` | major | satisfied | A 2-node, 16-GPU allocation for a ResNet-50 distributed training test is within the system limits and is not an extreme or nonsensical allocation for the workload. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The final request is 00:10:00 in "by-node," below that queue's 24-hour maximum walltime. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses one rank per GPU and identifies NCCL-oriented distributed GPU communication; nothing in the selected 4-node layout contradicts the supplied MPI/NCCL guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The throughput figures are explicitly presented as assumptions or typical estimates, and the answer states that no prior timing measurements exist. |
| `RES.common.no_reservation_queue` | major | satisfied | `by-node` is a named standard queue rather than a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The final validation states 4 requested nodes against `by-node` limits of 1–8 nodes, with both minimum and maximum marked PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard `by-node` queue, which is listed for Sophia. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final specification states 4 nodes × 8 ranks per node = 32 total ranks, and the stated 1 GPU per rank is consistent with 8 GPUs per node. |
| `RES.common.rank_layout_plausible` | major | satisfied | The layout uses 8 ranks and 8 GPUs per node with 1 GPU per rank, matching the stated 8 A100 GPUs per Sophia node. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It uses 8 ranks per node and explicitly states 1 GPU per rank, the expected full-node one-rank-per-A100 PyTorch distributed layout. |
| `RES.common.sizing_not_absurd` | major | satisfied | A 4-node/32-GPU allocation with a 2-hour safety-margin walltime for a distributed ResNet-50 training run is within the legal small-to-medium scale and is not plainly unreasonable. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests 2 hours and validates this against the `by-node` 24-hour maximum walltime as PASS. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The one-GPU-per-rank layout across all 8 A100s is compatible with NCCL GPU collectives and does not contradict the supplied scaling guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | It explicitly says no measured timing exists and presents the throughput and resulting duration as a reasoned estimate with a stated 2× margin. |
| `RES.common.no_reservation_queue` | major | satisfied | `by-gpu` is a named standard queue rather than a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The final check states requested 1 node against `by-gpu` limits of 1–1 nodes, with PASS for both minimum and maximum. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard `by-gpu` queue, which is listed in the Sophia queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final specification explicitly gives `1 node × 8 ranks = 8` total ranks and states 1 rank equals 1 GPU. |
| `RES.common.rank_layout_plausible` | major | satisfied | The layout uses 8 ranks and 8 GPUs on an 8-GPU node, with one GPU per rank and no unsupported CPU-core oversubscription claimed. |
| `RES.common.ranks_match_build_defaults` | major | satisfied ⚠︎ flipped across runs | It uses 8 ranks per node and 1 GPU per rank, i.e. one rank for each of Sophia's 8 A100 GPUs. |
| `RES.common.sizing_not_absurd` | major | satisfied | A single full 8-GPU node for a 100,000-image ResNet-50 training run is a reasonable, non-absurd allocation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests `0:10:00`, explicitly comparing it with the `by-gpu` 24-hour maximum and marking it PASS. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The numerical allocation does not itself contradict the supplied NCCL/CUDA-awareness notes, although its ranks-per-node setting violates the separate build-default requirement. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The timing values are presented as assumptions and estimates (for example, "can be estimated" and "Let's assume"), not as observed or measured results. |
| `RES.common.no_reservation_queue` | major | satisfied | "by-node" is a standard queue name, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | **violated** | The final specification requests "Nodes: 24" in "by-node", whose stated node range is 1–8; the answer itself reports "Node maximum: 8 ... 24 ... FAIL". |
| `RES.common.queue_exists` | fatal | satisfied | The answer chooses "Queue: by-node", which is a listed Sophia queue. |
| `RES.common.rank_arithmetic_consistent` | major | **violated** | It states 1 rank per node and 1 GPU per rank, which implies 1 allocated GPU per node, but the final specification states "GPUs per node: 8" without ranks to consume those eight GPUs. |
| `RES.common.rank_layout_plausible` | major | not_applicable ⚠︎ flipped across runs | A build-default rank layout is supplied for this PyTorch MPI application, so the fallback plausibility rule for applications with no recorded build default does not apply. |
| `RES.common.ranks_match_build_defaults` | major | **violated** | The answer specifies "Ranks-per-node: 1", whereas the supplied PyTorch MPI distributed launch default is 8 ranks per node with one GPU per rank. |
| `RES.common.sizing_not_absurd` | major | satisfied ⚠︎ flipped across runs | While the 24-node, 276.48-hour request is invalid under queue policy, the workload is a distributed deep-learning training run and the allocation is not intrinsically absurd under the requirement's high threshold. |
| `RES.common.walltime_within_queue_limit` | fatal | **violated** | The final specification requests "Walltime: 276.48 hours" in by-node, whose maximum walltime is 24 hours; the answer itself reports this limit as "FAIL". |
