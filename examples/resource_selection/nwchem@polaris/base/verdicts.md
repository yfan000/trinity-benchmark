# Verdicts — nwchem@polaris, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `79f1535225d9`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation retains the required 4 MPI ranks per node and uses multiple node counts for the stated scaling study, while acknowledging that a one-water system will not scale efficiently. |
| `RES.common.no_fabricated_evidence` | major | satisfied | Its "Measured baseline" of 5 s is explicitly identified as given by the prompt; the 30 s bound and 20× margin are clearly presented as assumptions rather than observed results. |
| `RES.common.no_reservation_queue` | major | satisfied | "debug-scaling" is a named standard queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The final verification states 4 requested nodes against debug-scaling limits of 1–10 nodes, with both node-minimum and node-maximum checks marked PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The answer chooses the standard Polaris queue "debug-scaling," which is listed in the supplied queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer explicitly verifies "4 × 4 = 16" total MPI ranks; the CPU-only configuration consistently uses 0 GPUs per node. |
| `RES.common.rank_layout_plausible` | major | not_applicable | A build default exists for this application (4 ranks per node), so the fallback hardware-plausibility requirement does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer uses "MPI ranks per node \| 4," matching the supplied build default, and requests 0 GPUs for the CPU-only build. |
| `RES.common.sizing_not_absurd` | major | satisfied | Four nodes and a 10-minute debug-scaling allocation are modest and legal for a deliberately small multi-node scaling benchmark. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The requested walltime is "0:10:00," below the debug-scaling maximum of 1 hour, explicitly marked PASS. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The answer retains the prescribed 4 MPI ranks per node and explains that the multi-node choice is for a deliberate scaling benchmark, despite the tiny molecule not being expected to scale efficiently. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The 5-second baseline is supplied by the prompt, while the 10x overhead and 10-minute request are explicitly presented as assumptions and margin rather than observed results. |
| `RES.common.no_reservation_queue` | major | satisfied | The selected queue is `debug-scaling`, a named standard queue rather than a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests 8 nodes and verifies `debug-scaling` permits 1 to 10 nodes, with both node-minimum and node-maximum checks marked PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The final specification selects the standard `debug-scaling` queue, which is listed for Polaris. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final specification explicitly gives 32 total ranks as 8 nodes × 4 ranks per node, and specifies 0 GPUs per node for the CPU-only layout. |
| `RES.common.rank_layout_plausible` | major | not_applicable | A build default is recorded and followed, so the fallback plausibility rule for applications without a build default does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It states the build default is 4 MPI ranks per node and uses 4; it also correctly selects 0 GPUs per node for the CPU-only build. |
| `RES.common.sizing_not_absurd` | major | satisfied | Eight nodes for a very short single-water calculation is reasonable in the stated context of intentionally characterizing strong-scaling behavior, and remains within the scaling queue's range. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests 00:10:00 and verifies that this is below the `debug-scaling` maximum walltime of 1 hour. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The answer follows the scaling note's required layout of 4 MPI ranks per node; using 8 nodes for an explicitly requested scaling benchmark does not conflict with the guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | Its reference to a 5-second single-node timing is supported by the prompt's supplied prior timing, and the 5-minute walltime is clearly presented as an added safety margin. |
| `RES.common.no_reservation_queue` | major | satisfied | The answer targets the standard "debug-scaling" queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The verification table requests 8 nodes and states debug-scaling permits 1-10 nodes; both the minimum and maximum checks are marked PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The selected queue is explicitly stated as "debug-scaling," which is listed in the supplied Polaris queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final specification states "8 × 4 = 32" total MPI ranks, consistent with 8 nodes and 4 ranks per node; the CPU-only allocation uses zero GPUs. |
| `RES.common.rank_layout_plausible` | major | not_applicable | A build default is recorded and used (4 ranks per node), so this fallback plausibility requirement for cases with no catalog build default does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It uses the supplied build default of "4 MPI ranks per node" and specifies "GPUs per node = 0" for the CPU-only build. |
| `RES.common.sizing_not_absurd` | major | satisfied | An 8-node allocation for a deliberately small scaling benchmark is not an absurd allocation under the stated threshold, and it is legal in debug-scaling. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests "00:05:00" and correctly compares it with debug-scaling's 1-hour maximum, reporting PASS. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses the supplied guidance of 4 MPI ranks per node and does not select a conflicting GPU layout. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The answer's 5-second statement is supplied by the prompt, while its linear scaling and 1-hour duration are explicitly framed as assumptions. |
| `RES.common.no_reservation_queue` | major | satisfied | "debug-scaling" is a standard named queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests "Nodes: 4" on debug-scaling; that queue permits 1-10 nodes. |
| `RES.common.queue_exists` | fatal | satisfied | The final specification selects queue "debug-scaling," which is a listed Polaris queue. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer explicitly states "Total ranks: 4 x 4 = 16," consistent with 4 nodes times 4 ranks per node; the CPU-only configuration requests zero GPUs. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This plausibility fallback applies where no build default is recorded, but the catalog records a 4-ranks-per-node build default. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer states "Ranks per node: 4 (build default)" and uses "GPUs per node: 0 (CPU-only build)," consistent with the CPU-only build. |
| `RES.common.sizing_not_absurd` | major | satisfied | A 4-node, 16-rank allocation for a deliberately requested scaling benchmark of a very small calculation is not an absurd resource choice. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The final specification requests "Walltime: 1h" and debug-scaling has a maximum walltime of 1h. |
