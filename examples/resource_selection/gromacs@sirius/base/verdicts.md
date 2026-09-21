# Verdicts — gromacs@sirius, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `79f1535225d9`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | **violated** | The allocation keeps 8 MPI ranks on a node with 4 GPUs and proposes “two ranks per GPU,” contradicting the supplied guidance that one MPI rank per GPU is recommended. |
| `RES.common.no_fabricated_evidence` | major | satisfied | It expressly says “No measured throughput supplied” and labels 100 ns/day as an “Assumption,” rather than claiming it was measured or observed. |
| `RES.common.no_reservation_queue` | major | satisfied | `workq` is presented as the standard queue and not as a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | It requests 1 node and explicitly checks it against workq’s 1–4 node range, with both minimum and maximum marked PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects “Chosen queue: `workq`,” which is the defined Sirius queue. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final specification states “Total ranks = nodes × ranks per node = 1 × 8 = 8,” and consistently states 4 GPUs per node for the 8-rank layout. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This requirement applies only where no build default is recorded; Sirius/GROMACS has a recorded default of 8 ranks per node. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It uses “Ranks per node (build default): 8,” matching the catalog default ppn of 8. |
| `RES.common.sizing_not_absurd` | major | satisfied | A single node and 2-hour request for a 34,000-atom, 5 ns GPU-accelerated restart is not an absurd allocation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The requested walltime is “02:00:00” and the answer checks it against workq’s 24 h maximum as PASS. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses one MPI rank per GPU: 4 ranks for Sirius's 4 GPUs per node, consistent with the supplied one-rank-per-GPU guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The 200 ns/day figure is explicitly presented as a conservative assumption, not as an observed or measured throughput. |
| `RES.common.no_reservation_queue` | major | satisfied | `workq` is a standard queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | It requests 1 node and explicitly checks that `workq` permits 1–4 nodes, with both minimum and maximum marked PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects `workq`, which is the supplied Sirius queue. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer states 1 node × 4 ranks per node = 4 total ranks and maps the 4 ranks to the 4 GPUs using `-gpu_id 0123`. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This requirement applies only where the catalog has no build default; Sirius/GROMACS has a recorded default of 8 ranks per node. |
| `RES.common.ranks_match_build_defaults` | major | satisfied ⚠︎ flipped across runs | The answer uses 4 ranks for 4 GPUs, i.e. one rank per GPU; the nominal 8-rank build default corresponds to the supplied one-rank-per-GPU layout on an 8-GPU node, while Sirius has only 4 GPUs per node. |
| `RES.common.sizing_not_absurd` | major | satisfied | One four-GPU node and a 3-hour walltime are reasonable for a roughly 34,000-atom, 5 ns restarted GROMACS production run. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | It requests 3 hours and checks this against the `workq` maximum of 24 hours, marked PASS. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | **violated** | The allocation keeps 8 MPI ranks on a 4-GPU node and proposes two ranks per GPU, contradicting the supplied recommendation of one MPI rank per GPU. |
| `RES.common.no_fabricated_evidence` | major | satisfied | It calls the performance figure a typical estimate and explicitly states that no measured throughput is available. |
| `RES.common.no_reservation_queue` | major | satisfied | `workq` is presented as a standard queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | It requests 1 node and verifies this against workq's stated 1–4 node range. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects `workq`, which is the supplied Sirius queue. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer consistently states 1 node × 8 ranks per node = 8 total ranks, with 8 ranks mapped as two ranks per each of 4 GPUs. |
| `RES.common.rank_layout_plausible` | major | not_applicable | The catalog does record a build default (`ppn: 8`), whereas this requirement applies where no build default is recorded. |
| `RES.common.ranks_match_build_defaults` | major | satisfied ⚠︎ flipped across runs | The answer uses the supplied build default of 8 ranks per node: “ranks-per-node = 8” and requests 8 ranks on its one node. |
| `RES.common.sizing_not_absurd` | major | satisfied | One node and a two-hour request for a 34,000-atom, 5 ns GROMACS restart are not an absurd allocation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | It requests `02:00:00` and verifies that it is below workq's 24-hour maximum. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | **violated** | The answer chooses 8 one-GPU MPI ranks per node on hardware with only 4 GPUs per node, contradicting the one-rank-per-GPU guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The throughput figures are explicitly framed as assumptions and a "typical range," not as observed, measured, or reported evidence. |
| `RES.common.no_reservation_queue` | major | satisfied | "workq" is a standard queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The final request is 4 nodes and workq permits 1–4 nodes. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects "workq", which is the catalogued Sirius queue. |
| `RES.common.rank_arithmetic_consistent` | major | **violated** | Although 4 × 8 = 32 is correct, 8 ranks per node at the stated 1 GPU per rank requires 8 GPUs per node, while the answer states Sirius has only 4 GPUs per node. |
| `RES.common.rank_layout_plausible` | major | not_applicable | The catalog records a build default of 8 ranks per node, so this fallback requirement for cases without a build default does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer uses the supplied build default of 8 ranks per node and states one GPU per rank. |
| `RES.common.sizing_not_absurd` | major | satisfied | A 4-node allocation for this production MD workload is not intrinsically absurd under the requirement's high threshold, even though its GPU rank mapping is invalid. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The final request is 24h and workq has a 24h maximum, so it does not exceed the cap. |
