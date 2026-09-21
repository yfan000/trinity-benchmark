# Verdicts — pytorch@sophia, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `79f1535225d9`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses one rank per GPU and NCCL for GPU collectives, consistent with the supplied GPU communication guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The iteration duration is explicitly labeled an "Est." and the answer states that no prior timing measurements exist; it does not claim observed or measured performance. |
| `RES.common.no_reservation_queue` | major | satisfied | "by-node" is a named standard queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The chosen by-node verification states requested 2 nodes against the queue range 1–8, with both minimum and maximum checks marked PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The final specification selects queue "by-node," which is listed in the Sophia queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final specification states 2 nodes × 8 ranks per node = 16 total ranks, with 1 GPU per rank and 8 GPUs per node. |
| `RES.common.rank_layout_plausible` | major | satisfied | The answer uses 8 ranks per node with 1 GPU per rank on hardware stated to have 8 A100 GPUs per node. |
| `RES.common.ranks_match_build_defaults` | major | not_applicable | The supplied catalog/build defaults specify nodes, walltime, queue, and communication backends but record no numerical ranks-per-node or GPUs-per-rank default to match. |
| `RES.common.sizing_not_absurd` | major | satisfied | A 2-node/16-GPU allocation and 30-minute request for a 100,000-image, 10-epoch mixed-precision ResNet-50 run is not an absurd resource choice. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests "00:30:00" on by-node and explicitly verifies it is below the 24:00:00 maximum walltime. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The 1-GPU-per-rank, 8-rank single-node layout is compatible with using NCCL GPU collectives and does not contradict any supplied scaling guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The throughput is explicitly presented as a conservative assumption based on typical A100 performance, not as an observed or measured result. |
| `RES.common.no_reservation_queue` | major | satisfied | `by-node` is a named standard queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The selected `by-node` queue permits 1–8 nodes, and the answer requests 1 node; its validation table records both node-minimum and node-maximum as PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects queue `by-node`, which is listed in the Sophia queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final specification states 1 node × 8 ranks per node = 8 total ranks, and the reasoning states 1 GPU per rank across the 8 GPUs on the node. |
| `RES.common.rank_layout_plausible` | major | satisfied | The answer uses 8 ranks per node with 1 GPU per rank on hardware stated to have 8 A100 GPUs per node, so it does not exceed the available GPUs. |
| `RES.common.ranks_match_build_defaults` | major | not_applicable | The supplied catalog facts record defaults for nodes, walltime, and queue but do not record a ranks-per-node or GPUs-per-rank build default to match deterministically. |
| `RES.common.sizing_not_absurd` | major | satisfied | A single 8-GPU node and one-hour walltime for ten epochs of ResNet-50 training on 100,000 images is a plausible, non-absurd allocation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests 1 hour on `by-node`, whose stated maximum is 24 hours; its validation table records maximum walltime as PASS. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The 1-GPU-per-rank, 8-rank layout uses all 8 A100 GPUs on the node and does not conflict with the supplied NCCL GPU-collective guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | It expressly labels the throughput as an assumption: “No empirical timing was supplied, therefore we assumed ... 18 k images·s⁻¹.” |
| `RES.common.no_reservation_queue` | major | satisfied | `by-node` is a named standard PBS queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests 1 node and verifies that `by-node` permits 1–8 nodes: “Minimum nodes ... PASS” and “Maximum nodes ... PASS.” |
| `RES.common.queue_exists` | fatal | satisfied | The final specification selects queue `by-node`, which is listed in the Sophia queue catalog. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final table explicitly states “Total ranks: 1 × 8 = 8,” consistent with 1 node and 8 ranks per node, with one GPU per rank. |
| `RES.common.rank_layout_plausible` | major | satisfied | The answer uses 8 ranks per node and 1 GPU per rank on hardware with 8 GPUs per node: “Ranks per node: 8 ... GPUs per rank: 1.” |
| `RES.common.ranks_match_build_defaults` | major | not_applicable | The authoritative catalog facts provide no numeric ranks-per-node or GPUs-per-rank build default against which to perform this deterministic default-match check. |
| `RES.common.sizing_not_absurd` | major | satisfied | A single full 8-GPU node for 10 epochs of ResNet-50 training on 100,000 images is a plausible, non-absurd allocation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests `00:05:00`, and `by-node` has a 24-hour maximum; its limit check states “Maximum wall-time ... PASS.” |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The 8-rank, one-GPU-per-rank single-node layout is compatible with the available 8 A100 GPUs and does not contradict the NCCL/MPI scaling notes. |
| `RES.common.no_fabricated_evidence` | major | satisfied | Timing is explicitly framed as an assumption and estimate, e.g. "Assuming" and "we can estimate," rather than as measured or observed performance. |
| `RES.common.no_reservation_queue` | major | satisfied | "by-node" is a standard queue listed in the supplied queue table, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests "nodes: 1" and selects by-node, whose stated node range is "1-8 nodes". |
| `RES.common.queue_exists` | fatal | satisfied | The final resource specification explicitly selects the existing Sophia queue: "queue: by-node". |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | It states "Total ranks = 1 node × 8 ranks per node = 8 ranks," consistent with the final 1-node, 8-ranks-per-node allocation and one GPU per rank. |
| `RES.common.rank_layout_plausible` | major | satisfied | The answer uses "ranks-per-node = 8" and "GPUs-per-rank = 1" on a node stated to have 8 A100 GPUs, consuming one GPU per rank without exceeding the GPU count. |
| `RES.common.ranks_match_build_defaults` | major | not_applicable | No ranks-per-node or GPUs-per-rank build default is recorded in the authoritative catalog; the answer's "ranks-per-node = 8" and "GPUs-per-rank = 1" are therefore assessed for hardware plausibility instead. |
| `RES.common.sizing_not_absurd` | major | satisfied | A one-node, eight-GPU allocation for 10 epochs of ResNet-50 training on 100,000 images is not an absurd allocation, and the requested 7-hour walltime remains within queue policy. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The requested "walltime: 420 minutes" is 7 hours, below the by-node maximum of "24 hours". |
