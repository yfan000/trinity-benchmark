# Verdicts — hpl@crux, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `79f1535225d9`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses "128 ranks/node" and states this "uses all cores," consistent with the instruction to maximize performance using all 128 cores per node. |
| `RES.common.no_fabricated_evidence` | major | satisfied | It plainly says "No measured timing supplied" and labels performance and runtime values as assumed estimates rather than observed results. |
| `RES.common.no_reservation_queue` | major | satisfied | The selected "debug" target is a named standard queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests 2 nodes and verifies debug's range as "1–8" with "Node maximum ... PASS". |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard Crux queue: "Selection: debug"; debug is listed in the supplied queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer states "Total ranks = nodes × ranks-per-node = 2 × 128 = 256," which is arithmetically consistent. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This conditional requirement applies where no build default is recorded; Crux/HPL has the recorded 128 ranks-per-node build default. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It explicitly sets "Ranks per node: 128 (build default)" and "GPUs per rank: 0" for the CPU-only, zero-GPU system. |
| `RES.common.sizing_not_absurd` | major | satisfied | A legal two-node CPU allocation for N=50000 HPL is not an obviously nonsensical or extreme resource choice. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests "30 minutes (0.5 h)" and verifies this against debug's "1 h" maximum walltime with PASS. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation requests 128 ranks per node, matching the supplied guidance to use all 128 CPU cores per node. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The runtime is explicitly presented as an assumption—“I assume a runtime of 15 minutes”—rather than as an observed or measured result. |
| `RES.common.no_reservation_queue` | major | satisfied | `debug` is a named standard queue rather than a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The final request is 1 node, and the answer's verification states `debug` permits 1–8 nodes: “Node Minimum ... PASS” and “Node Maximum ... PASS.” |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard `debug` queue, which is listed in the supplied Crux queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final specification states “Total ranks: 128 (1 node × 128 ranks per node),” which matches the requested allocation arithmetic. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This rule applies only where no build default is recorded; the catalog and prompt provide the 128 ranks-per-node build default. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer uses “128 ranks per node” from the stated build default and specifies 0 GPUs per node on the CPU-only system. |
| `RES.common.sizing_not_absurd` | major | satisfied | A one-node, 30-minute allocation for N=50000 HPL is a plausible non-absurd sizing and is legal in the selected queue. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The requested walltime is 0.5h and `debug` has a 1h maximum; the answer explicitly marks the walltime check PASS. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The CPU-only allocation uses 0 GPUs and all 128 cores/ranks per node, consistent with the supplied scaling guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The timing discussion explicitly labels its performance and runtime values as assumptions, e.g. "Assuming 80% of peak" and "No measured runtime was supplied." |
| `RES.common.no_reservation_queue` | major | satisfied | The selected queue is "debug," not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | It requests 8 nodes and explicitly checks "8 ≤ 8" against debug's 1–8-node range. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard Crux queue "debug," which is listed in the supplied queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | It states "Total MPI ranks: 8 × 128 = 1024," which is arithmetically consistent, with 0 GPUs per node. |
| `RES.common.rank_layout_plausible` | major | not_applicable | A build default of 128 ranks per node is recorded, so this fallback plausibility rule for cases with no build default does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer uses "Ranks per node (built-in) ... 128," matching the catalog build default, and specifies 0 GPUs on the CPU-only system. |
| `RES.common.sizing_not_absurd` | major | satisfied | An 8-node CPU allocation for an HPL benchmark with N=50000 is within the legal debug range and is not an obviously nonsensical allocation under the requirement's high threshold. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | It requests "00:15:00" and explicitly checks it is within debug's "01:00:00" maximum. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The answer selects 128 ranks per node and states it will use all 128 CPU cores per node, matching the supplied CPU-only scaling guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The performance figure is explicitly framed as an assumption/estimate ("Assuming" and "estimate"), not as observed or measured evidence. |
| `RES.common.no_reservation_queue` | major | satisfied | "demand" is a named standard queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The final request is 64 nodes on demand, and the answer states demand permits 1–64 nodes. |
| `RES.common.queue_exists` | fatal | satisfied | The final resource specification selects queue "demand," which is present in the supplied Crux queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final specification explicitly calculates "64 × 128 = 8192" total ranks, and specifies 0 GPUs per node for the CPU-only system. |
| `RES.common.rank_layout_plausible` | major | not_applicable | A build default of 128 ranks per node is supplied, so this fallback plausibility requirement for systems without a build default does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer uses "ranks per node: 128" and "GPUs per rank: 0," consistent with the 128-ppn CPU-only build and hardware. |
| `RES.common.sizing_not_absurd` | major | satisfied ⚠︎ flipped across runs | The final allocation is a legal 64-node CPU allocation for an HPL run and does not meet the rule's high threshold for an absurd allocation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The final request is "walltime: 1 hour" on demand, whose supplied maximum walltime is 1 hour. |
