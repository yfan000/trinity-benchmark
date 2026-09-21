# Verdicts — lammps@polaris, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `79f1535225d9`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The answer uses 4 ranks with one GPU each on a node and chooses one node for a 500,000-atom case, consistent with guidance to scale nodes for systems above 1 million atoms. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The throughput is explicitly labeled a performance assumption and the answer states that no measured timing exists. |
| `RES.common.no_reservation_queue` | major | satisfied | The selected `debug` queue is a standard named queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | For `debug`, the answer requests 1 node and explicitly verifies it against the allowed 1–2 node range with PASS for both minimum and maximum. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard Polaris queue `debug`, which is listed in the supplied queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer states 1 node × 4 ranks per node = 4 total MPI ranks, with 4 GPUs per node and 1 GPU per rank. |
| `RES.common.rank_layout_plausible` | major | not_applicable | The catalog provides an explicit build default for ranks per node and GPU mapping, so this fallback plausibility requirement does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer uses 4 MPI ranks per node and 1 GPU per rank, matching the supplied Kokkos build defaults. |
| `RES.common.sizing_not_absurd` | major | satisfied | A one-node, four-A100 allocation for a 500,000-atom first-run LAMMPS job is consistent with the supplied below-1M scaling guidance, and the requested 45-minute walltime is legal. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests 0:45:00 and verifies that 45 minutes is within the `debug` maximum walltime of 60 minutes. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses 4 MPI ranks and 4 GPUs per node, i.e. one rank per GPU as specified by the Kokkos scaling guidance; 2 nodes for a sub-1M-atom case does not contradict the guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The 5,000 timesteps/s figure is expressly introduced as an assumption and a “typical baseline,” not as an observed or measured result. |
| `RES.common.no_reservation_queue` | major | satisfied | `debug` is a standard named queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests 2 nodes in `debug`; its own check states the queue range is 1–2 nodes and both minimum and maximum checks PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects queue `debug`, which is listed for Polaris. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer states 2 nodes × 4 ranks/node = 8 total ranks, with 4 GPUs/node at one GPU per rank. |
| `RES.common.rank_layout_plausible` | major | not_applicable | A build default is recorded and applied, so the fallback plausibility rule for systems without a recorded default does not bear on this allocation. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It uses the supplied build default of 4 ranks per node and explicitly states 1 GPU per rank, yielding 4 GPUs per node. |
| `RES.common.sizing_not_absurd` | major | satisfied | Two A100 nodes and a 30-minute debug allocation for a first 500,000-atom, 100,000-step LAMMPS run is not an absurd allocation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests 0.5 hours in `debug`, below the stated 1-hour maximum, and marks the walltime check PASS. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | It uses the prescribed 4 ranks/node and one GPU/rank, and explains that 500,000 atoms is below the supplied >1M-atom multi-node scaling threshold. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The throughput is identified as a "Performance assumption" and a "typical" value; the answer does not claim it was observed, measured, or reported for this workload. |
| `RES.common.no_reservation_queue` | major | satisfied | The selected queue is "debug," a standard queue rather than a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | For debug it requests 1 node and explicitly verifies node minimum 1 and maximum 2, both PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard Polaris queue "debug," which is present in the supplied queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final specification states 1 node × 4 ranks per node = 4 total ranks, with 4 GPUs per node at one GPU per rank. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This requirement applies only where no build default is recorded; Polaris LAMMPS has an explicit default of 4 ranks per node with one GPU each. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer uses "4 MPI ranks per node" and "1 GPU per rank," matching the supplied build/scaling defaults. |
| `RES.common.sizing_not_absurd` | major | satisfied | A 1-node, 4-A100 allocation for a 500,000-atom, 100,000-step LJ run is consistent with the supplied scaling guidance and has a stated conservative walltime margin. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | It requests "00:30:00" on debug, whose stated maximum is "01:00:00," and marks the walltime check PASS. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | **violated** | The answer allocates only "GPUs per node: 1" while also specifying 4 MPI ranks per node and 1 GPU per rank; this conflicts with the Kokkos guidance of one GPU for each of the four ranks. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The timing is explicitly presented as an assumption—"no measurement is provided"—rather than as observed or measured performance. |
| `RES.common.no_reservation_queue` | major | satisfied | "capacity" is a standard named queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | **violated** | The final specification requests "Nodes: 560", while the capacity queue permits only 1-4 nodes; 560 exceeds its maximum of 4. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects "Queue: capacity", which is a listed Polaris queue. |
| `RES.common.rank_arithmetic_consistent` | major | **violated** | Although "560 × 4 = 2240" is arithmetically correct, 4 ranks per node with "1 GPU per rank" requires 4 GPUs per node, contradicting the stated "GPUs per node: 1". |
| `RES.common.rank_layout_plausible` | major | not_applicable | A catalog build default is present, so this fallback plausibility requirement does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied ⚠︎ flipped across runs | The answer uses "Ranks per node: 4" and states "1 GPU per rank," matching the supplied build layout. |
| `RES.common.sizing_not_absurd` | major | **violated** | Allocating all 560 Polaris nodes to a 500,000-atom Lennard-Jones run defies the supplied guidance to scale nodes for systems larger than 1 million atoms and is an extreme over-allocation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The requested "Walltime: 30.57 hours" is below the capacity queue maximum walltime of 168 hours. |
