# Verdicts — qmcpack@aurora, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `79f1535225d9`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses 6 ranks per node for Aurora's 6 Intel GPU tiles, i.e. one rank per tile, consistent with the supplied scaling note. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The throughput and block-step values are explicitly labeled assumptions, and the answer states "No measured timing or throughput figures are claimed." |
| `RES.common.no_reservation_queue` | major | satisfied | The answer requests "Queue: capacity," not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | It requests 2 nodes and verifies capacity's 1–16-node range: "Node minimum ... PASS" and "Node maximum ... PASS." |
| `RES.common.queue_exists` | fatal | satisfied | The final specification selects the standard Aurora queue "capacity," which is listed in the supplied queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | It explicitly states "Total MPI ranks = nodes × ranks per node = 2 × 6 = 12" and uses 6 GPUs per node with one GPU tile per rank. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This conditional requirement applies where no build default is recorded; Aurora/QMCPACK has a recorded default of 6 ranks per node. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer uses the stated build default of "6 ranks/node" and maps one rank to each of Aurora's six GPU tiles. |
| `RES.common.sizing_not_absurd` | major | satisfied | A 2-node, 12-rank GPU allocation for a 64-atom DMC calculation with 4096 walkers and 200 blocks is a plausible, non-absurd sizing. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | It requests "2 hours" and checks this against capacity's "168 h" maximum with a PASS verdict. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses 6 ranks per node for Aurora's 6 Intel GPU tiles, with one rank per GPU tile and SYCL acknowledged. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The timing is explicitly framed as an "Assumption" and a "conservative estimate," not as measured or observed performance. |
| `RES.common.no_reservation_queue` | major | satisfied | "capacity" is a standard named Aurora queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests 4 nodes and validates capacity's 1-node minimum and 16-node maximum as PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The selected queue is explicitly stated as "capacity," which exists in the Aurora queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer states "Total ranks: 24 (4 nodes × 6 ranks per node)" and maps 6 ranks to the 6 GPUs per node at one GPU per rank. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This fallback requirement applies where no build default is recorded; Aurora QMCPACK has a recorded default of 6 ranks per node. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It uses the supplied build default of 6 ranks per node and states 1 GPU per rank, matching 6 GPU tiles per node. |
| `RES.common.sizing_not_absurd` | major | satisfied | A 4-node, 24-rank GPU allocation for a 64-atom, 4096-walker, 200-block DMC calculation is not an absurd allocation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests 4 hours, below the capacity queue maximum of 168 hours, and marks this PASS. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses 6 GPU tiles and 6 MPI ranks per node, consistent with Aurora's six GPU tiles per node and the QMCPACK SYCL layout. |
| `RES.common.no_fabricated_evidence` | major | satisfied | It explicitly identifies the timing as an assumption and does not claim that an actual timing or throughput value was measured or observed. |
| `RES.common.no_reservation_queue` | major | satisfied | `debug-scaling` is a standard named Aurora queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests 44 nodes and verifies that `debug-scaling` permits 2-256 nodes. |
| `RES.common.queue_exists` | fatal | satisfied | The selected queue is `debug-scaling`, which is listed in the Aurora queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer states 44 nodes × 6 ranks per node = 264 total ranks and 44 × 6 = 264 total GPUs at one GPU per rank. |
| `RES.common.rank_layout_plausible` | major | not_applicable | The catalog supplies a build default of 6 ranks per node, so the layout is governed by the build-default requirement rather than the no-default plausibility fallback. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It uses the supplied build default of 6 ranks per node and states one GPU tile per rank. |
| `RES.common.sizing_not_absurd` | major | satisfied | Although aggressive for a 64-atom cell, 44 nodes provide 264 ranks for 4096 walkers, leaving roughly 15 walkers per rank; this does not defy common sense or exceed the available work. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The requested walltime is 0:30:00, below the `debug-scaling` maximum of 1 hour. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses 6 ranks and 6 GPU tiles per node, i.e. one rank per Intel GPU tile, matching the supplied Aurora/QMCPACK scaling information. |
| `RES.common.no_fabricated_evidence` | major | satisfied | It labels its timing as assumptions and states that no timing or throughput was measured; it does not claim an observed or reported runtime. |
| `RES.common.no_reservation_queue` | major | satisfied | "queue prod" is a standard named PBS queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests 256 nodes; prod permits 256-10624 nodes, so 256 meets both bounds. |
| `RES.common.queue_exists` | fatal | satisfied | The selected queue is "queue prod," which exists in Aurora's supplied queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer explicitly states "1536 = 256 x 6" and specifies 6 GPUs per node with one GPU per rank. |
| `RES.common.rank_layout_plausible` | major | not_applicable | A build default is recorded for this application (6 ranks per node), so the fallback plausibility rule for systems without a build default does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It uses the stated build default of 6 ranks per node and assigns one GPU tile per rank, consistent with Aurora's 6 GPU tiles per node. |
| `RES.common.sizing_not_absurd` | major | satisfied | Although 256 nodes is a large allocation for this cell, 4096 walkers provide work to distribute and the chosen count is not plainly nonsensical under the requirement's high threshold. |
| `RES.common.walltime_within_queue_limit` | fatal | **violated** | The final request is "walltime: 68.24 hours" in prod, but prod has a maximum walltime of 24h; the answer incorrectly calls 24h "above" 68.24h. |
