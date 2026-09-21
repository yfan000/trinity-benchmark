# Verdicts — vllm@frontier, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `79f1535225d9`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The answer keeps the run on one node, notes that TP=4 fits within its 8 GCDs, and does not make a multi-node allocation that conflicts with the supplied one-node TP=8 validation. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The 165 s startup figure is explicitly supplied as a prior measurement, while the TP=4 throughput and 5× margin are clearly identified as assumptions rather than measurements. |
| `RES.common.no_reservation_queue` | major | satisfied | The selected queue is "g1" and is presented as a normal queue/partition, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The final verification requests 1 node against g1's 1–2-node range and explicitly marks both node-minimum and node-maximum checks PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard Frontier partition "g1", which is listed in the supplied queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final specification states "Total ranks: 8 (= 1 × 8)" and consistently assigns one GCD GPU to each of the 8 ranks. |
| `RES.common.rank_layout_plausible` | major | not_applicable ⚠︎ flipped across runs | A build default for the rank/GPU layout is supplied and followed, so the fallback plausibility rule for absent defaults does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It uses "Ranks-per-node = 8 (one per GCD)" and "GPUs-per-rank = 1," matching the supplied one-rank-per-GCD build default. |
| `RES.common.sizing_not_absurd` | major | satisfied | One node and a 30-minute request for 50 short offline-inference prompts, including a documented 165 s startup cost and safety margin, is a reasonable non-absurd allocation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests 30 minutes (0.5 h), below the g1 maximum walltime of 2 h, and explicitly marks this PASS. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation remains on one node with the supplied default of eight ranks/one per GCD, and does not contradict the provided TP=4 workload or one-node sizing guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The 30-second inference component is explicitly approximate ("≈30s") and the answer labels the result an estimate; the only stated prior measurement, 165-second startup, was supplied in the prompt. |
| `RES.common.no_reservation_queue` | major | satisfied | The selected queue is "g1," a named standard partition rather than a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests 1 node and validates it against g1's 1-node minimum and 2-node maximum, with both marked PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard Frontier queue "g1," which is listed in the supplied queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final specification states "Total ranks: 8 (1 node × 8 ranks per node)" and specifies 8 GPUs per node with one rank per GCD. |
| `RES.common.rank_layout_plausible` | major | not_applicable | A build-default rank layout is supplied and used, so the fallback plausibility rule for cases without a catalog default does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It explicitly uses "ranks-per-node = 8 (one per GCD)," consistent with the supplied build default of eight ranks per node and one GCD/GPU per rank. |
| `RES.common.sizing_not_absurd` | major | satisfied | A one-node, ten-minute g1 request for a 50-prompt offline inference run is a reasonable, non-absurd allocation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests "00:10:00" and validates it against the g1 maximum walltime of 2 hours, marked PASS. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | A single node supplies the required TP=4 capacity, while retaining the required build-default layout of 8 ranks per node; no multi-node scaling is claimed or required. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The only figure called "observed," the 165 s startup, is explicitly supplied as a prior measurement; the 0.1 s/token figure is clearly presented as a conservative estimate. |
| `RES.common.no_reservation_queue` | major | satisfied | It requests "Queue / Partition: debug," not a reservation identifier. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied ⚠︎ flipped across runs | It requests 1 node and identifies debug as admitting the request; the supplied debug policy gives no node-range limit that excludes one node. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard Frontier "debug" queue, which is listed in the supplied queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | It explicitly states "Total ranks: 1 × 8 = 8" and uses one GPU per rank across 8 GPUs. |
| `RES.common.rank_layout_plausible` | major | satisfied ⚠︎ flipped across runs | The stated layout is 8 ranks and 8 GCD GPUs per node, within Frontier's 64 CPU cores and 8 GCD devices per node. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer uses "ranks-per-node = 8" and "1 GPU per rank," matching the supplied one-rank-per-GCD build default. |
| `RES.common.sizing_not_absurd` | major | satisfied | One node and a five-minute request for a 50-prompt, 50-token offline inference run is a plausible non-absurd allocation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The requested "00:05:00" walltime is below debug's stated maximum of "02:00:00." |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | Although the allocation is highly excessive, no supplied scaling rule makes a 131-node allocation inherently invalid; the answer retains the stipulated one-rank-per-GCD layout. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The unsupported timing is explicitly framed as an assumption: "Assuming an inference time of 1 second per prompt" and "let's assume," rather than as a measurement. |
| `RES.common.no_reservation_queue` | major | satisfied | "queue batch" is a standard named Frontier queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests "nodes = 131" on batch, whose stated range is "1-9280 nodes," so 131 is within the limits. |
| `RES.common.queue_exists` | fatal | satisfied | The selected queue is explicitly stated as "queue = queue batch," and batch is listed in the Frontier queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final specification gives "131" nodes, "8" ranks per node, and "total ranks ... = 1048"; 131 × 8 = 1048, with one GPU per rank and 8 GPUs per node. |
| `RES.common.rank_layout_plausible` | major | not_applicable | A build default for ranks per node is supplied, so this fallback requirement for cases with no recorded build default does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It states "ranks-per-node = 8 (one per GCD)" and "GPUs-per-rank = 1," matching the supplied one-rank-per-GCD build layout. |
| `RES.common.sizing_not_absurd` | major | **violated** | Allocating 131 nodes / 1,048 ranks to only 50 prompts with at most 50 generated tokens each is more ranks than the work can sensibly divide across and defies common-sense sizing. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests "walltime = 13.75 seconds" on batch, whose maximum walltime is 24h. |
