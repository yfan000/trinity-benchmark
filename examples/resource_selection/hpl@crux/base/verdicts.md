# Verdicts — hpl@crux, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `79f1535225d9`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | **violated** | The scaling notes direct use of all 128 cores per node, whereas the answer allocates and states "4 cores active" and "ranks per node = 4". |
| `RES.common.no_fabricated_evidence` | major | satisfied | The timing figure is explicitly presented as an assumption: "No measured performance data was supplied" and "Assuming a modest per-core HPL performance". |
| `RES.common.no_reservation_queue` | major | satisfied | "debug" is a standard queue in the supplied Crux queue table, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The final check states "Node minimum ... requested 1, limit 1, PASS" and "Node maximum ... requested 1, limit 8, PASS" for debug. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the listed standard queue: "Selected queue: debug". |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final specification states "Total ranks: 4 (= 1 × 4)", consistent with one node and four ranks per node; it also specifies zero GPUs for the CPU-only workload. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This plausibility fallback applies only where no build default is recorded; the catalog records a 128 ranks-per-node default. |
| `RES.common.ranks_match_build_defaults` | major | **violated** | The supplied build default is 128 ranks per node, but the answer explicitly chooses "ranks per node = 4" instead of retaining the build default. |
| `RES.common.sizing_not_absurd` | major | satisfied | A one-node, 30-minute request for N=50000 HPL is not an absurd allocation, even though its rank layout conflicts with the build default and scaling guidance. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests "0.5 h" and verifies against debug's "1 h" maximum with "PASS". |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses the supplied build default of 128 ranks per node, consistent with the guidance to use all 128 CPU cores per node. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The runtime is explicitly presented as an "Assumption" based on typical performance, not as a measured or observed result. |
| `RES.common.no_reservation_queue` | major | satisfied | `debug` is a named standard queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests 1 node and verifies `debug` permits 1–8 nodes. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard `debug` queue, which is listed for Crux. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer states 1 node × 128 ranks/node = 128 total ranks, and specifies 0 GPUs per node on the GPU-free system. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This check applies only where no build default is recorded; Crux HPL has a recorded default of 128 ranks per node. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The final specification states "Ranks per node: 128 (Build default)" and uses zero GPUs on the CPU-only system. |
| `RES.common.sizing_not_absurd` | major | satisfied | A one-node, one-hour HPL allocation for N=50000 is not an absurd resource request. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests 1h and verifies that `debug` has a maximum walltime of 1h. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses 128 ranks per node on a 128-core CPU-only node, consistent with the guidance to use all 128 cores per node. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The timing discussion is presented as an estimate and assumption (including a stated 70% efficiency and 20% margin), not as an observed, measured, or reported result. |
| `RES.common.no_reservation_queue` | major | satisfied | The chosen queue is "debug," a named standard queue rather than a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests 1 node and explicitly checks it against debug's 1–8 node range: "PASS." |
| `RES.common.queue_exists` | fatal | satisfied | The final specification chooses the standard "debug" queue, which is listed in the supplied Crux queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer states "nodes × ranks_per_node = 1 × 128 = 128" and requests 0 GPUs per node on a system with no GPUs. |
| `RES.common.rank_layout_plausible` | major | not_applicable | A build default exists for ranks per node (128), so this fallback plausibility requirement for catalogs without a build default does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It states "Ranks per node – taken from the application build default: 128 MPI ranks per node" and requests 0 GPUs on the CPU-only system. |
| `RES.common.sizing_not_absurd` | major | satisfied | A one-node allocation for N=50000 HPL with a short 10-minute request is not an absurd resource size for the stated workload. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests "00:10:00" and explicitly checks it is below debug's 1-hour maximum walltime. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The selected layout uses 128 ranks per node, matching the guidance to use all 128 CPU cores per node. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The runtime discussion is explicitly framed as an assumption ("Let's assume") rather than an observed or measured result. |
| `RES.common.no_reservation_queue` | major | satisfied | "workq-route" is a named standard queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests "Nodes: 184" in workq-route, whose stated node range is 1–184. |
| `RES.common.queue_exists` | fatal | satisfied | The final specification selects the existing standard queue "workq-route". |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | It states "Total ranks: 184 × 128 = 23552," which is arithmetically correct, and specifies zero GPUs. |
| `RES.common.rank_layout_plausible` | major | not_applicable | A catalog build default for ranks per node exists, so this fallback plausibility requirement does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It specifies "Ranks per node: 128" and "GPUs per rank: 0," consistent with the 128-ppn CPU-only build and zero-GPU system. |
| `RES.common.sizing_not_absurd` | major | satisfied | Although the reasoning for its node count is poor, 184 nodes is a legal free choice under the stated queue and build-ratio constraints; this requirement does not require an optimal allocation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests "Walltime: 24h" in workq-route, equal to rather than greater than its 24h maximum. |
