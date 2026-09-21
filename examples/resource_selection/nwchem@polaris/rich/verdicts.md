# Verdicts — nwchem@polaris, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `79f1535225d9`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation retains the prescribed 4 MPI ranks per node, and the answer appropriately explains that the multi-node use is to characterize poor strong-scaling behavior for the intentionally tiny benchmark. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The only stated measurement is the supplied 5 s single-node timing; the 30 s multi-node estimate and 5-minute request are clearly labeled assumptions with margin. |
| `RES.common.no_reservation_queue` | major | satisfied | `debug-scaling` is identified as a normal queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The final check requests 10 nodes against `debug-scaling` limits of 1–10 nodes and marks both minimum and maximum as PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the existing Polaris standard queue `debug-scaling`. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer explicitly verifies total ranks as 10 nodes × 4 ranks per node = 40, with no GPUs requested for the CPU-only build. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This conditional requirement applies only where no build default is recorded; the catalog and prompt provide a 4-ranks-per-node build default. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It uses the supplied build default of 4 MPI ranks per node and specifies 0 GPUs because the selected NWChem build is CPU-only. |
| `RES.common.sizing_not_absurd` | major | satisfied | A 1–10-node-scale target, with 10 nodes as the selected upper point and a 5-minute walltime, is not an absurd allocation for an explicitly requested scaling benchmark. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests 00:05:00 against the `debug-scaling` maximum of 01:00:00, explicitly marked PASS. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation retains the prescribed 4 MPI ranks per node and uses multiple nodes specifically for the requested scaling benchmark; it does not conflict with the guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The only stated prior timing, "a single-node run took 5 seconds," is supplied by the prompt, while the remaining timing statements are framed as assumptions and estimates. |
| `RES.common.no_reservation_queue` | major | satisfied | The selected queue is `debug-scaling`, a standard named queue rather than a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The final verification states 8 requested nodes against the `debug-scaling` range of 1 to 10 nodes, with PASS for both minimum and maximum. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard `debug-scaling` queue, which is listed for Polaris. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer explicitly gives 8 nodes × 4 ranks per node = 32 total ranks; the CPU-only allocation uses 0 GPUs per node. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This fallback plausibility requirement applies where no build default is recorded; the catalog supplies a 4-ranks-per-node build default. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It uses the supplied build default of 4 MPI ranks per node and specifies 0 GPUs per node because the build is CPU-only. |
| `RES.common.sizing_not_absurd` | major | satisfied | An 8-node allocation for a deliberately requested 1, 2, 4, and 8-node scaling sweep of a tiny system is not an absurd allocation, even though efficiency will be poor. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests 0:15:00 (0.25 hours), below the `debug-scaling` maximum walltime of 1 hour. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The answer follows the supplied scaling layout of 4 MPI ranks per node and uses a modest 4-node allocation for the stated scaling benchmark. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The answer's 5-second timing is explicitly grounded in the supplied prior timing, and its 10-minute duration is clearly labeled as an assumed safety-margin request rather than a measured result. |
| `RES.common.no_reservation_queue` | major | satisfied | "debug-scaling" is a named standard queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The final request is 4 nodes, and the answer verifies for debug-scaling: "request 4 ≥ 1 → PASS" and "request 4 ≤ 10 → PASS." |
| `RES.common.queue_exists` | fatal | satisfied | The selected queue is explicitly stated as "debug-scaling," which is listed in the supplied Polaris queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final table states "Total MPI ranks 4 × 4 = 16," consistent with 4 nodes and 4 ranks per node; CPU-only operation uses 0 GPUs per node. |
| `RES.common.rank_layout_plausible` | major | not_applicable | A build default exists for this application (4 ranks per node), so the fallback plausibility rule for applications without a recorded default does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer uses the supplied CPU-only build layout: "4 MPI ranks per node" and "0 GPUs per node." |
| `RES.common.sizing_not_absurd` | major | satisfied | A 4-node, 16-rank, 10-minute debug-scaling request is a legal and non-absurd small-scale allocation for a deliberate scaling benchmark of this tiny test case. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The final walltime is "00:10:00" and the answer verifies it is within debug-scaling's 1-hour maximum: "request 10 min ≤ 1 h → PASS." |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | It uses the supplied scaling layout of 4 MPI ranks per node; using an enlarged node count for a scaling experiment does not itself conflict with the guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | It bases the 5 s figure on the prompt's supplied prior timing and labels the 16-node estimate and 20% margin as assumptions rather than unsupported measurements. |
| `RES.common.no_reservation_queue` | major | satisfied | `prod` is a standard named queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests 16 nodes, and its selected `prod` queue permits 10-496 nodes. |
| `RES.common.queue_exists` | fatal | satisfied | The final specification selects `queue: prod`, which is a listed Polaris PBS Pro queue. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied ⚠︎ flipped across runs | The answer consistently states 16 nodes × 4 ranks per node = 64 total ranks, and its stated 1 GPU per rank corresponds internally to 4 GPUs per node. |
| `RES.common.rank_layout_plausible` | major | not_applicable | A build default is supplied for this application (4 ranks per node), so this fallback plausibility rule does not apply. |
| `RES.common.ranks_match_build_defaults` | major | **violated** | Although it correctly uses the 4-ranks-per-node build default, it states `GPUs-per-rank: 1` and ultimately requests 4 GPUs per node despite the supplied CPU-only build; the appropriate GPU allocation is 0 GPUs per rank/node. |
| `RES.common.sizing_not_absurd` | major | satisfied | A 16-node allocation for an explicitly requested scaling benchmark is not the kind of extreme, plainly nonsensical allocation required to violate this default-satisfied rule. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The requested walltime is 96 s, which is below the `prod` maximum walltime of 24 h. |
