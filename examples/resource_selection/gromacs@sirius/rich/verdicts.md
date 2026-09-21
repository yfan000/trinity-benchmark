# Verdicts — gromacs@sirius, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `79f1535225d9`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation follows the supplied one-rank-per-GPU guidance: 4 local ranks map to the node's 4 GPUs via "-gpu_id 0123." |
| `RES.common.no_fabricated_evidence` | major | **violated** | Although it labels 50 ns/day/GPU an assumption, it additionally asserts unsupported external evidence: "literature reports 100–200+ ns/day for similar sizes," despite the prompt supplying no reported throughput figure. |
| `RES.common.no_reservation_queue` | major | satisfied | `workq` is identified as the standard queue and is not presented as a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests 1 node and checks "Request 1 ≥ 1" and "Request 1 ≤ 4" for workq. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the existing Sirius queue: "Chosen queue: `workq`". |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer states "Total ranks = Nodes × Ranks per node = 1 × 4 = 4" and consistently specifies 4 GPUs/node at 1 GPU/rank. |
| `RES.common.rank_layout_plausible` | major | not_applicable | The catalog does record a build default/rank guidance, so this fallback plausibility requirement for systems with no build default does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It correctly applies the build/scaling default as one MPI rank per GPU on the actual 4-GPU Sirius node: "4 ranks per node (1 rank per GPU)" and "1 GPU per rank." |
| `RES.common.sizing_not_absurd` | major | satisfied | One 4-A100 node and a 4-hour request for a 34,000-atom, 5-ns restart are a reasonable, non-absurd allocation and fit the stated queue limits. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The requested "04:00:00" walltime is explicitly checked as "Request 4 h ≤ 24 h" for workq. |

## gemma-4-31b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | **violated** | The allocation uses 8 MPI ranks on a node with 4 GPUs and explicitly shares GPUs via `-gpu_id 01230123`, conflicting with the supplied recommendation of one MPI rank per GPU. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The throughput is explicitly framed as an assumption: “Assuming a conservative 200 ns/day,” rather than as an observed or measured result. |
| `RES.common.no_reservation_queue` | major | satisfied | `workq` is presented as a standard queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The compliance table requests 1 node against `workq` limits of 1–4 nodes, with both minimum and maximum marked PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects `workq`, which is the supplied Sirius queue. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied ⚠︎ flipped across runs | The final specification states 1 node × 8 ranks/node = 8 total ranks, and the stated repeated GPU mapping consistently assigns those 8 ranks across 4 GPUs. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This requirement applies only where no build default is recorded; the catalog records a default of 8 ranks per node. |
| `RES.common.ranks_match_build_defaults` | major | **violated** ⚠︎ flipped across runs | Although it retains the build-default 8 ranks per node, it maps 8 ranks onto only 4 GPUs using `-gpu_id 01230123`, i.e. two ranks per GPU, contrary to the supplied one-MPI-rank-per-GPU default/guidance. |
| `RES.common.sizing_not_absurd` | major | satisfied | One node and a 2-hour request for a 34,000-atom, 5-ns restart are not an absurd allocation, and the request remains within queue limits. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests 2 hours against the `workq` 24-hour maximum and explicitly marks the check PASS. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | **violated** | The allocation keeps 8 ranks on a node with only 4 GPUs and explicitly uses "two ranks per GPU," contradicting the supplied one-MPI-rank-per-GPU recommendation. |
| `RES.common.no_fabricated_evidence` | major | satisfied | It expressly labels the 4 ns/h figure as a "typical" assumed rate and states that no actual Sirius throughput measurement is available. |
| `RES.common.no_reservation_queue` | major | satisfied | "workq" is a standard queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests 1 node and explicitly checks it against workq's 1–4 node range, with both minimum and maximum marked PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects "Queue: workq," which is the listed Sirius queue. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer states "Total MPI ranks: 8 = 1 × 8" and consistently describes 8 ranks sharing the 4 GPUs as two ranks per GPU. |
| `RES.common.rank_layout_plausible` | major | not_applicable | A catalog build default for ranks per node is recorded (ppn: 8), so this fallback requirement for systems with no build default does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer uses "Ranks per node (MPI): 8" and states this is the supplied build default. |
| `RES.common.sizing_not_absurd` | major | satisfied | One node and a 3-hour request for a ~34,000-atom, 5 ns GROMACS restart are not an absurd allocation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The requested walltime is "03:00:00" and the answer checks it against workq's 24-hour maximum, marked PASS. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | **violated** | The answer allocates 8 ranks/GPUs per node despite Sirius having only 4 GPUs per node; this conflicts with the supplied one-MPI-rank-per-GPU guidance and its claimed "GPUs per node: 8" is impossible. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The throughput is explicitly framed as an assumption: "we assume that each time step will take approximately 10-20 μs," not as a measurement or observation. |
| `RES.common.no_reservation_queue` | major | satisfied | It explicitly chooses "queue: workq," not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The final request is for 4 nodes, and workq permits 1–4 nodes. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard Sirius queue "workq," which is listed in the catalog. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | It states "total ranks: 4 × 8 = 32" and consistently derives its claimed 8 GPUs per node from 8 one-GPU ranks. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This requirement applies only where no build default is recorded; the catalog records a default of 8 ranks per node. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer uses the supplied build default of 8 ranks per node and states one GPU per rank. |
| `RES.common.sizing_not_absurd` | major | satisfied | Using four nodes for a 34,000-atom GPU MD workload is not inherently an absurd allocation under this deliberately permissive requirement, although its GPU mapping and walltime are invalid. |
| `RES.common.walltime_within_queue_limit` | fatal | **violated** | The final specification requests "walltime: 41.25 hours," while workq has a 24-hour maximum; its table incorrectly labels this as PASS. |
