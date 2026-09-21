# Verdicts — nekrs@polaris, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `79f1535225d9`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation follows the supplied scaling guidance: 4 ranks/node, one MPI rank per GPU, and scaling by increasing the node count to 16. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The only prior timing cited is supplied by the prompt, while the 80% efficiency and 20% margin are explicitly labeled assumptions rather than observations. |
| `RES.common.no_reservation_queue` | major | satisfied | The answer targets "prod," a named standard queue rather than a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | It requests 16 nodes and explicitly verifies for prod: "PASS (10≤16)" and "PASS (496≥16)," matching the 10–496 node range. |
| `RES.common.queue_exists` | fatal | satisfied | The final specification selects the standard Polaris queue: "Queue \| prod"; prod is listed in the supplied queue catalog. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | It states "Total ranks \| 64 \| 16 nodes × 4 ranks/node" and maps four ranks to the four GPUs per node at one GPU per rank. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This fallback plausibility rule applies only where no build default is recorded; the catalog and prompt provide the NekRS default of 4 ranks per node. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer uses "Ranks per node \| 4" and "1 MPI rank per GPU," which matches the stated NekRS build default of four ranks per Polaris node and one rank per GPU. |
| `RES.common.sizing_not_absurd` | major | satisfied | A 16-node/64-GPU allocation for a 32,000-element, 20,000-timestep turbulent-flow production calculation is not an absurd allocation, and the answer provides a stated scaling-based estimate. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | It requests "0:30:00 (30 min)" and verifies this is "PASS (0.5≤24)" against prod's 24-hour maximum. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses 4 ranks and 4 GPUs per node, honoring the supplied one-MPI-rank-per-GPU guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The stated 8-minute baseline is supplied by the prompt, while the 16-node timing is explicitly framed as an assumption: "Assuming near-linear scaling." |
| `RES.common.no_reservation_queue` | major | satisfied | The answer targets the standard "prod" queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The final verification requests 16 nodes against prod's "10" node minimum and "496" node maximum, with both marked PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The selected queue is explicitly stated as "prod," which is a listed Polaris queue. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer states "Total ranks: 64 (16 nodes × 4 ranks/node)," and maps 4 ranks per node to 4 GPUs per node at one GPU per rank. |
| `RES.common.rank_layout_plausible` | major | not_applicable | The catalog supplies a build default of 4 ranks per node, so this fallback plausibility requirement for cases without a build default does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It specifies "Ranks per node: 4 (as per build default)" and uses one MPI rank per GPU on the four-GPU nodes. |
| `RES.common.sizing_not_absurd` | major | satisfied | A 16-node, 64-rank allocation for a 32,000-element turbulent-flow production case is not an absurd resource choice. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests "20 min" walltime and verifies it against the prod maximum of "24h" as PASS. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses 4 ranks and 4 GPUs per node, i.e. one MPI rank per GPU, and scales by increasing node count to 10. |
| `RES.common.no_fabricated_evidence` | major | satisfied | Its stated 1,000-step/8-minute measurement is supplied by the prompt, while the multi-node timing is clearly presented as theoretical/expected and based on stated assumptions and margins. |
| `RES.common.no_reservation_queue` | major | satisfied | "debug-scaling" is a named standard Polaris queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests 10 nodes in debug-scaling and verifies "Node minimum: 1 ≤ 10 → PASS" and "Node maximum: 10 ≥ 10 → PASS"; the queue allows 1–10 nodes. |
| `RES.common.queue_exists` | fatal | satisfied | The selected queue is explicitly stated as "debug-scaling," which is present in the Polaris queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final specification states "10 × 4 = 40" total ranks, with 4 GPUs per node and one rank per GPU. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This conditional requirement applies where no build default is recorded; here the catalog records the NekRS Polaris default of 4 ranks per node. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It uses "4 ranks / node (one rank per A100)," matching the NekRS Polaris build default of four ranks per node and one GPU per rank. |
| `RES.common.sizing_not_absurd` | major | satisfied | A 10-node, 40-GPU allocation for a 32,000-element turbulent-flow production case is not an absurd allocation, and its 30-minute request is legal and based on an explicit scaled timing assumption. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests "00:30:00" in debug-scaling and verifies "Wall-time limit: 1 h ≥ 30 min → PASS"; the queue maximum is 1 hour. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses 4 ranks and 4 GPUs per node with one GPU per rank, consistent with the supplied NekRS scaling guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The only timing treated as prior measurement is the supplied 1-node, 1,000-step timing; the linear scaling and 20% margin are explicitly stated as assumptions. |
| `RES.common.no_reservation_queue` | major | satisfied | "prod" is a named standard queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests 496 nodes in "prod"; the stated prod range is 10–496 nodes, so 496 is within the inclusive limits. |
| `RES.common.queue_exists` | fatal | satisfied | The final specification selects the existing Polaris standard queue "prod". |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer explicitly gives "496 * 4 = 1984" total ranks and maps one rank to each of the four GPUs per node. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This fallback plausibility rule applies only where no build default is recorded; Polaris/NekRS has the recorded build default of 4 ranks per node. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It uses "Ranks per node: 4 (build default)" and "GPUs per rank: 1," matching NekRS's one-rank-per-GPU, four-ranks-per-node layout. |
| `RES.common.sizing_not_absurd` | major | satisfied ⚠︎ flipped across runs | Although 496 nodes is an aggressive and likely inefficient choice, the substantial turbulent CFD production workload does not make this allocation plainly nonsensical under the stated absurdity threshold. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The final request is "Walltime: 192 minutes" in prod, below prod's 24-hour (1,440-minute) maximum. |
