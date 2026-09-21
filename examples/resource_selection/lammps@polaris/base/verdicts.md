# Verdicts — lammps@polaris, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `79f1535225d9`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses 4 ranks with one GPU each on one node and explains that 500,000 atoms is below the supplied >1M-atom multi-node scaling guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | It clearly labels the throughput as "Assumed performance" and states that no measured timing exists; it does not claim an observed or measured result. |
| `RES.common.no_reservation_queue` | major | satisfied | The selected queue is "debug," a standard named queue rather than a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | It requests 1 node on debug and explicitly verifies node minimum 1 and maximum 2 as PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard "debug" queue, which is listed in the supplied Polaris queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final specification states 1 node × 4 ranks per node = 4 total ranks, with 4 GPUs per node at 1 GPU per rank. |
| `RES.common.rank_layout_plausible` | major | not_applicable | A build default is recorded and followed, so the fallback plausibility requirement for systems without a build default does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer uses "4 MPI ranks per node" and "1 GPU/rank," exactly following the supplied build/scaling defaults. |
| `RES.common.sizing_not_absurd` | major | satisfied | A single 4-A100 node for a 500,000-atom Lennard-Jones run is consistent with the supplied guidance for workloads below 1M atoms, and the 30-minute request is within normal first-run safety margin practice. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | It requests 0.5 h (30 min) on debug, below the queue's 1 h maximum, and marks this PASS. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | It uses 4 MPI ranks per node with the node's 4 GPUs and explains that 500,000 atoms is below the supplied >1M-atom scaling threshold. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The timing is explicitly presented as an assumption based on typical performance, not as an observed or measured result. |
| `RES.common.no_reservation_queue` | major | satisfied | `debug` is a named standard queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The final check states 2 requested nodes against `debug` limits of 1 to 2 nodes, with both minimum and maximum marked PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard `debug` queue, which is listed for Polaris. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer states 2 nodes × 4 ranks/node = 8 total ranks and uses 4 GPUs per node for 4 ranks per node. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This fallback plausibility requirement applies where no build default is recorded; Polaris LAMMPS has a recorded 4-ranks-per-node build default. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It uses the supplied build default of 4 ranks per node and allocates 4 GPUs per node for those 4 ranks, implying the required 1 GPU per rank. |
| `RES.common.sizing_not_absurd` | major | satisfied | A legal 2-node, 8-rank GPU allocation with a 1-hour safety-margin request is not a common-sense-defying allocation for a 500,000-atom, 100,000-step LAMMPS run. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests 1 hour in `debug`, whose stated maximum is 1 hour, and explicitly marks the walltime check PASS. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation follows the specified Kokkos mapping of 4 MPI ranks per node with one GPU per rank; using 2 nodes does not conflict with guidance that multi-node scaling is primarily for systems above 1M atoms. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The response labels its throughput as a "Performance assumption" and closes with "no measured timings claimed," without claiming an observed or measured run result. |
| `RES.common.no_reservation_queue` | major | satisfied | "debug-scaling" is a named standard queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests 2 nodes and explicitly checks debug-scaling's 1–10 node range: "Minimum nodes ... 2 ... ≥ 1 ... PASS" and "Maximum nodes ... 2 ... ≤ 10 ... PASS." |
| `RES.common.queue_exists` | fatal | satisfied | The final specification selects the standard Polaris queue "debug-scaling," which is present in the supplied queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final check correctly states "Total ranks = nodes × ranks-per-node = 2 × 4 = 8," with 4 GPUs per node for the four one-GPU ranks. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This fallback plausibility requirement applies where no build default is recorded; the catalog does record the 4-ranks-per-node, one-GPU-per-rank default. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It uses the supplied build layout: "Ranks per node = 4" and "each rank drives 1 GPU," yielding four GPUs per node. |
| `RES.common.sizing_not_absurd` | major | satisfied | A legal 2-node/8-GPU allocation with a 50-minute cap for a 500,000-atom, 100,000-step first run is not an extreme or nonsensical allocation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The requested walltime is 00:50:00, and the answer checks it against debug-scaling's 01:00:00 cap with PASS. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | **violated** ⚠︎ flipped across runs | The supplied guidance says to scale nodes for large systems ">(1M atoms)," but the answer allocates 256 nodes to a 500,000-atom system below that threshold without a justification for contradicting that guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The timing figures are explicitly framed as assumptions (for example, "Assuming" and "we assumed"), not as measured or observed results. |
| `RES.common.no_reservation_queue` | major | satisfied | The answer selects the standard "prod" queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | It requests "256 nodes" and states prod permits "10-496 nodes"; 256 is within that range. |
| `RES.common.queue_exists` | fatal | satisfied | The selected queue is explicitly stated as "Queue: prod", and prod is a listed Polaris queue. |
| `RES.common.rank_arithmetic_consistent` | major | **violated** | Although "256 × 4 = 1024" is correct, the answer states "GPUs per node: 1" despite also specifying 4 ranks per node and 1 GPU per rank, which requires 4 GPUs per node. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This requirement applies only where no build default is recorded; Polaris LAMMPS has a recorded default of 4 ranks per node with one GPU each. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer uses "4 ranks per node and 1 GPU per rank," matching the supplied build layout. |
| `RES.common.sizing_not_absurd` | major | **violated** | Allocating 256 four-GPU nodes (1,024 MPI ranks) to a 500,000-atom Lennard-Jones case is an extreme allocation inconsistent with the supplied guidance that multi-node scaling is for systems above 1M atoms. |
| `RES.common.walltime_within_queue_limit` | fatal | **violated** | The final request is "Walltime: 250,000 s (or 69.44 hours)" on prod, whose supplied maximum is 24 hours. |
