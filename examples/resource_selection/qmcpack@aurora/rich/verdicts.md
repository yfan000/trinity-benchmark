# Verdicts — qmcpack@aurora, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `79f1535225d9`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The answer assigns six ranks and six GPU tiles per node, with "one per rank / GPU tile," consistent with Aurora's six Intel GPU tiles per node and the SYCL build. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The answer explicitly says "No prior timing exists" and labels its throughput and walltime figures as assumptions rather than measurements. |
| `RES.common.no_reservation_queue` | major | satisfied | The selected queue is "capacity," a named standard queue rather than a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The final check states "Node minimum: 1 ≤ 2 PASS" and "Node maximum: 16 ≥ 2 PASS" for capacity. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard Aurora queue "capacity," which is listed in the supplied queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The closure explicitly gives "Total ranks: 2 × 6 = 12" and the layout consistently uses six GPUs per node with one GPU per rank. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This fallback requirement applies only where no build default is recorded; Aurora/QMCPACK has a recorded six-ranks-per-node build default, which the answer follows. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It uses "6 (build default)" ranks per node and specifies one GPU per rank, yielding the six GPU-tile layout. |
| `RES.common.sizing_not_absurd` | major | satisfied | A two-node, twelve-rank GPU allocation for a 64-atom DMC calculation with 4096 walkers is a plausible, non-absurd allocation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests "45 minutes (0:45:00)" and states for capacity "Maximum walltime: 168 h ≥ 0.75 h PASS." |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The selected layout uses 6 ranks and 6 Intel GPU tiles per node, explicitly stating "1 GPU per rank," which is consistent with Aurora's six-tile SYCL-targeted QMCPACK configuration. |
| `RES.common.no_fabricated_evidence` | major | satisfied | It labels performance values as assumptions, e.g. "I assume a conservative throughput" and "Estimated Walltime," rather than claiming measurements or observations. |
| `RES.common.no_reservation_queue` | major | satisfied | `capacity` is a named standard queue in the supplied Aurora queue table, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests "4 nodes" and verifies capacity's "1 node" minimum and "16 nodes" maximum, both marked PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard Aurora queue: "I will target the `capacity` queue." |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer explicitly gives "Total ranks: 24 (4 nodes × 6 ranks/node)" and maps 6 ranks per node to 6 GPUs per node at one GPU per rank. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This fallback requirement applies where no build default is recorded; Aurora QMCPACK has a recorded build default of 6 ranks per node. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer states "Ranks per node: The build default is 6" and uses six GPUs per node with "1 GPU per rank," yielding the required one-rank-per-GPU-tile layout. |
| `RES.common.sizing_not_absurd` | major | satisfied | A four-node, 24-rank allocation for 4,096 DMC walkers is a plausible workload division and does not defy common sense for the described calculation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The requested "3.2 hours" is below the capacity queue's stated "168 hours" maximum, which the answer marks PASS. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses 6 ranks and 6 GPUs per node, consistent with Aurora's 6 Intel GPU tiles per node and the QMCPACK SYCL GPU-targeting notes. |
| `RES.common.no_fabricated_evidence` | major | satisfied | It explicitly says no measured timing is supplied and labels the 12-hour figure as a conservative assumption rather than an observed or reported result. |
| `RES.common.no_reservation_queue` | major | satisfied | `capacity` is a standard named Aurora queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests 4 nodes; `capacity` permits 1–16 nodes, and it explicitly checks 4 >= 1 and 4 <= 16 as PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The selected queue is `capacity`, which is listed in the Aurora queue catalog. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer states 4 nodes x 6 ranks per node = 24 total MPI ranks and 4 x 6 = 24 total GPUs, consistent with one GPU per rank. |
| `RES.common.rank_layout_plausible` | major | not_applicable | A build default is recorded for this application (6 ranks per node), so the conditional rule for systems with no build default does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It uses the supplied build default of 6 ranks per node and maps the 6 ranks to the node's 6 GPU tiles, stating one rank per GPU. |
| `RES.common.sizing_not_absurd` | major | satisfied | A 4-node, 24-GPU allocation for a 64-atom DMC calculation with 4096 walkers is not an obviously unreasonable resource choice. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests 4 h walltime; `capacity` has a 168 h maximum, and it explicitly reports 4 h <= 168 h as PASS. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The selected layout uses 6 ranks and 6 GPUs per node, consistent with Aurora's six Intel GPU tiles per node. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The timing rate is explicitly framed as an "Assuming" rough estimate rather than as observed, measured, or reported evidence. |
| `RES.common.no_reservation_queue` | major | satisfied | "prod" is a standard named queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The final specification requests 1024 nodes, and prod admits 256-10624 nodes. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard Aurora queue "prod," which is listed in the supplied queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The stated arithmetic is correct: 1024 nodes × 6 ranks per node = 6144 total ranks, with 6 GPUs per node and one GPU per rank. |
| `RES.common.rank_layout_plausible` | major | not_applicable ⚠︎ flipped across runs | This fallback requirement applies only where no build default is recorded; Aurora QMCPACK has a recorded default of 6 ranks per node. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer uses "Ranks per node: 6 (build default)" and specifies one GPU per rank, yielding the intended six-rank/six-GPU-tile node layout. |
| `RES.common.sizing_not_absurd` | major | **violated** | The answer allocates 1024 nodes/6144 ranks to a modest 64-atom, 4096-walker reproduction run without scaling justification; it even has more MPI ranks than walkers, making this hundreds-of-nodes allocation defy common-sense sizing. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The final specification requests 12h in prod, whose stated maximum walltime is 24h. |
