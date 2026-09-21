# Verdicts — vllm@frontier, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `79f1535225d9`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The one-node, 8-rank allocation follows the supplied sizing default, and its two TP=4 replicas use the eight available GCDs without requiring multi-node scaling. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The answer identifies the 165 s startup as supplied prior measurement and explicitly labels TP=4 throughput and the sub-30-second inference duration as assumptions/estimates. |
| `RES.common.no_reservation_queue` | major | satisfied | The selected queue is "g1"; it is a named standard partition, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | For g1, the answer requests 1 node and verifies "Node minimum \| 1 \| 1 \| PASS" and "Node maximum \| 1 \| 2 \| PASS." |
| `RES.common.queue_exists` | fatal | satisfied | The answer chooses the standard Frontier partition "g1," which is listed in the supplied queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final specification states "Total ranks: 8 (= 1 × 8)" with 1 node, 8 ranks per node, and 8 GCD GPUs with one GPU per rank. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This fallback plausibility rule applies where no build default is recorded, but the prompt supplies the build default of 8 ranks per node, one per GCD. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It states "Ranks-per-node: 8 (one per GCD)" and "GPUs-per-rank: 1," matching the supplied one-rank-per-GCD build layout. |
| `RES.common.sizing_not_absurd` | major | satisfied | A single node and ten-minute request for a 50-prompt offline inference run, including a stated startup and safety margin, is not disproportionate. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests "00:10:00" on g1 and verifies "Maximum walltime \| 0.167 h \| 2 h \| PASS." |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | It keeps the supplied one-rank-per-GCD layout on one 8-GCD node and correctly notes TP=4 fits within one node, with four TP ranks active. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The answer identifies the supplied startup time and labels the inference duration as "likely" and the total as an "Estimated Time," rather than claiming an unsupplied measurement. |
| `RES.common.no_reservation_queue` | major | satisfied | "g1" is presented as a standard named queue/partition, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The selected g1 verdict table states 1 requested node against a 1-node minimum and 2-node maximum, both marked PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The answer explicitly selects "Queue: g1," which is a listed Frontier queue. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final specification states "Total ranks: 8 (1 node × 8 ranks/node)" and "GPUs per node: 8," consistent with one rank per GCD. |
| `RES.common.rank_layout_plausible` | major | satisfied ⚠︎ flipped across runs | The proposed one-node layout has 8 ranks and 8 GCD devices, which is within the stated 64 CPU cores and 8 GCDs per node. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It uses "ranks-per-node is 8 (one per GCD)" and explains this is "Per build defaults," consistent with one GPU/GCD per rank. |
| `RES.common.sizing_not_absurd` | major | satisfied | A one-node, 30-minute g1 allocation for a 50-prompt offline inference run with approximately 165 seconds of startup is proportionate and within queue limits. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests "00:30:00" and checks it against g1's 2-hour maximum walltime, marked PASS. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The one-node allocation uses the supplied 8 ranks/GCDs and TP=4 as two TP-4 groups; it does not contradict the supplied single-node TP=8 validation. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The only stated measured figure, "start-up ... ≈165 s," is supplied by the prompt; generation time and margin are explicitly presented as assumptions. |
| `RES.common.no_reservation_queue` | major | satisfied | It explicitly chooses "Queue (partition): debug," not a reservation identifier. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The request is for 1 node; the answer identifies debug as admitting the short one-node request, and no conflicting debug node limit is supplied. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard Frontier partition "debug," which is listed in the supplied queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | It states "Total ranks: 1 × 8 = 8" and allocates 8 one-GPU ranks across the node's 8 GCD devices. |
| `RES.common.rank_layout_plausible` | major | not_applicable | A build default is supplied for this application, so the fallback plausibility rule for applications without a recorded default does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer uses "ranks-per-node = 8" and states "each rank using 1 GPU," matching the supplied one-rank-per-GCD sizing default. |
| `RES.common.sizing_not_absurd` | major | satisfied | One Frontier node and a 10-minute allocation for 50 short offline-inference prompts is a plainly non-absurd allocation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The requested walltime is "00:10:00" and the answer checks it against debug's "2 h" maximum. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses one node with the supplied default of eight ranks/GCDs and does not contradict any stated scaling-layout constraint. |
| `RES.common.no_fabricated_evidence` | major | satisfied | It labels its throughput as an assumption: "we will assume a throughput of 1 prompt per second" and does not claim this figure was measured or observed. |
| `RES.common.no_reservation_queue` | major | satisfied | "batch" is a standard named queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests "Nodes = 1" and selects batch, whose stated node range is "1-9280." |
| `RES.common.queue_exists` | fatal | satisfied | The final specification selects "Queue = batch," which is a listed Frontier queue. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final restatement gives "Total ranks = nodes * ranks per node = 1 * 8 = 8" and eight GPUs/GCDs for eight one-GPU ranks. |
| `RES.common.rank_layout_plausible` | major | not_applicable | A build default for the rank/GPU layout is supplied, so this fallback plausibility requirement does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer explicitly uses "ranks-per-node = 8 (one per GCD)" and "GPUs-per-rank = 1," matching the supplied build defaults. |
| `RES.common.sizing_not_absurd` | major | satisfied | A one-node allocation for 50 short offline inference prompts is not an absurd resource size, and the requested walltime remains legal for the selected queue. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests "Walltime = 7500 seconds" on batch; 7500 seconds is below batch's 24-hour maximum. |
