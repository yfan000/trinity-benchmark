# Verdicts — nekrs@polaris, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `79f1535225d9`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The 20-node allocation retains 4 MPI ranks and 4 GPUs per node, i.e. one MPI rank per GPU as required by the NekRS scaling guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The only baseline timing cited is the supplied prior 1-node measurement, while the 70% efficiency and 100% margin are explicitly identified as assumptions. |
| `RES.common.no_reservation_queue` | major | satisfied | The answer targets "prod," a named standard queue rather than a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | It requests 20 nodes in prod and explicitly verifies "20 ≥ 10" and "20 ≤ 496," matching prod's 10–496 node range. |
| `RES.common.queue_exists` | fatal | satisfied | The final specification selects the standard Polaris queue "prod," which is present in the supplied queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final table states 20 nodes × 4 ranks per node = 80 total ranks, with 4 GPUs per node and one GPU per rank. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This fallback requirement applies where no build default is recorded; here the catalog explicitly provides the 4-ranks-per-node build default. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer uses 4 ranks per node and 1 GPU per rank, exactly following the supplied NekRS one-rank-per-GPU, four-GPU-per-node default. |
| `RES.common.sizing_not_absurd` | major | satisfied | Twenty nodes for a 32,000-element, 20,000-timestep production turbulent-flow run is a plausible allocation, and the answer provides a stated scaling estimate and margin. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | It requests 30 minutes (0.5 h) and verifies this is within prod's 24-hour maximum. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses 4 ranks per node and 1 GPU per rank on Polaris's 4-GPU nodes, consistent with the NekRS scaling guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The only asserted baseline timing, "1,000 timesteps took 8 minutes," is explicitly supplied by the prompt; the scaling behavior and margin are clearly labeled assumptions. |
| `RES.common.no_reservation_queue` | major | satisfied | The selected queue is "prod," a standard queue rather than a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The final validation requests 16 nodes against prod's stated 10-node minimum and 496-node maximum, with both marked PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard Polaris queue "prod," which is listed in the supplied queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer states "Total Ranks: 64 (16 nodes × 4 ranks per node)" and uses 1 GPU per rank with 4 GPUs per node. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This fallback requirement applies where no build default is recorded, but the catalog explicitly records a 4-ranks-per-node build default. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It states "4 ranks per node" and "1 GPU per rank," matching the supplied NekRS one-rank-per-GPU, four-ranks-per-node default. |
| `RES.common.sizing_not_absurd` | major | satisfied | A 16-node, 64-GPU allocation for a 32,000-element turbulent-flow production run is not an absurd allocation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests 3h 20m walltime and validates it against the prod maximum of 24h as PASS. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses 4 MPI ranks and 4 GPUs per node, i.e. one rank per GPU as required by the NekRS scaling guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | Its statement that the 1-node timing was measured relies on the prompt's explicitly supplied prior measurement; the scaling and margin figures are clearly presented as assumptions. |
| `RES.common.no_reservation_queue` | major | satisfied | `prod` is a standard named Polaris queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests 10 nodes and verifies `10 >= 10` and `10 <= 496` for the `prod` queue. |
| `RES.common.queue_exists` | fatal | satisfied | The selected queue is explicitly `prod`, which is listed in the Polaris queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer states `10 nodes × 4 ranks = 40` total MPI ranks and maps 4 ranks per node to 4 GPUs per node at one GPU per rank. |
| `RES.common.rank_layout_plausible` | major | not_applicable | A catalog build default exists for this application (4 ranks per node), so the fallback plausibility rule for missing defaults does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It uses 4 ranks per node and states one MPI rank per GPU, matching the supplied NekRS build/scaling default on Polaris. |
| `RES.common.sizing_not_absurd` | major | satisfied | A 10-node, 40-GPU production allocation for a 32,000-element turbulent-flow run is reasonable and is driven by the minimum node count of the selected production queue. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The requested walltime is 20 minutes, and the answer verifies it is below the `prod` maximum of 24 hours (1440 minutes). |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The final allocation uses 4 MPI ranks per node and 4 GPUs per node, consistent with NekRS's one-rank-per-GPU guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The answer labels its timing quantities as assumptions and margins; its use of the prior 8-minute timing is supported by the prompt's supplied prior measurement. |
| `RES.common.no_reservation_queue` | major | satisfied | The answer requests "Queue: prod," not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The final stated request is "Nodes: 10" in prod, whose allowed range is 10–496 nodes. |
| `RES.common.queue_exists` | fatal | satisfied | The final specification selects the standard Polaris queue "prod," which is listed in the supplied queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final restatement gives "Nodes: 10," "Ranks per node: 4," and "Total ranks: 40," which satisfies 10 × 4 = 40; it also states 1 GPU per rank and 4 GPUs per node. |
| `RES.common.rank_layout_plausible` | major | not_applicable | The catalog provides a build default of 4 ranks per node, so the conditional requirement for cases with no recorded build default does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer uses "Ranks per node: 4 (build default)" and explicitly states "GPUs per rank: 1." |
| `RES.common.sizing_not_absurd` | major | satisfied | A 10-node, 40-GPU production allocation for a 32,000-element turbulent pipe-flow case is not an obviously absurd allocation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The final request is "Walltime: 3 hours" in prod, below prod's 24-hour maximum. |
