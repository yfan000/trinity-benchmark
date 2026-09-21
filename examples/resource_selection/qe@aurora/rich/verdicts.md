# Verdicts — qe@aurora, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `79f1535225d9`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses 104 CPU MPI ranks per node with the stated CPU-only MKL/ScaLAPACK build and does not claim unsupported Intel-GPU offload. |
| `RES.common.no_fabricated_evidence` | major | satisfied | It explicitly says “Measured/observed timing: none supplied” and presents the timing as an assumption rather than a measured result. |
| `RES.common.no_reservation_queue` | major | satisfied | `capacity` is a named standard PBS Pro queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests 16 nodes and verifies capacity permits 1–16 nodes: “Node maximum ... 16 ... PASS.” |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard `capacity` queue, which is listed for Aurora. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer states and correctly computes “16 × 104 = 1,664” total ranks; it also states that no GPUs are used by the CPU-only application. |
| `RES.common.rank_layout_plausible` | major | not_applicable | The catalog supplies a build default of 104 ranks per node, so this fallback plausibility rule for cases without a default does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It uses the supplied build default of 104 ranks per node and correctly identifies the CPU-only build as using zero application GPUs. |
| `RES.common.sizing_not_absurd` | major | satisfied | A legal 16-node CPU allocation for a 64-atom, 64-k-point plane-wave SCF workload is not an absurd allocation under the stated standard. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The requested walltime is 02:00:00, below the capacity maximum of 168 h, explicitly marked PASS. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses all 104 CPU cores as MPI ranks on the documented CPU-only Intel MKL/ScaLAPACK build and does not claim unsupported Intel-GPU offload. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The timing is expressly framed as an assumption: "I assume a baseline execution time of 30 minutes" with a stated 2x safety margin, not as measured or observed evidence. |
| `RES.common.no_reservation_queue` | major | satisfied | It explicitly targets "Queue: capacity," a named standard queue rather than a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests 4 nodes and verifies capacity's 1-node minimum and 16-node maximum as PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard Aurora queue "capacity," which is present in the supplied queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer states "416 (4 nodes × 104 ranks/node)," which is arithmetically correct; its CPU-only allocation specifies 0 GPUs per node. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This fallback plausibility rule applies only where no build default is recorded; the catalog records a 104-ranks-per-node build default and the answer follows it. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It uses "Ranks per node: 104," matching the supplied CPU-only MPI build default, and specifies 0 GPUs per node because this build does not use Aurora's Intel GPUs. |
| `RES.common.sizing_not_absurd` | major | satisfied | A 4-node CPU allocation for a 64-atom, 4x4x4-k-point plane-wave SCF workload is not an absurd allocation under the stated threshold, even if a smaller allocation could also be reasonable. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The requested walltime is "1 hour" and the answer correctly compares it with capacity's 168-hour maximum, reporting PASS. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses 104 CPU MPI ranks per node, matching the stated 104 CPU cores per node and CPU-only Intel MKL/ScaLAPACK build. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The timing is framed as a typical estimate and assumption ('typically needs', 'Expected', and a stated safety margin), not as observed or measured evidence. |
| `RES.common.no_reservation_queue` | major | satisfied | `capacity` is a named standard queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | It requests 2 nodes on `capacity`, and explicitly verifies the queue range of 1–16 nodes as PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard Aurora `capacity` queue, which is present in the supplied queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | It states total ranks as 2 × 104 = 208, consistent with the requested node and rank counts; zero GPUs per node is consistent with CPU-only execution. |
| `RES.common.rank_layout_plausible` | major | not_applicable | A build default is supplied for this application (104 ranks per node), so the fallback plausibility rule for absent defaults does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer uses the supplied build default of 104 ranks per node and correctly assigns zero GPUs to the CPU-only MPI build. |
| `RES.common.sizing_not_absurd` | major | satisfied | Two CPU nodes for a 64-atom plane-wave SCF calculation is a modest, legal allocation and does not defy common sense. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | It requests 00:20:00 on `capacity`, explicitly checking this against the 168-hour maximum as PASS. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses 104 CPU MPI ranks per node, matching the stated 104 CPU cores per node and CPU-only Intel MKL/ScaLAPACK build. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The timing is explicitly framed as assumptions and estimates, e.g. "a rough estimate" and "Assuming," rather than as observed or measured evidence. |
| `RES.common.no_reservation_queue` | major | satisfied | The selected "prod" queue is a named standard queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | **violated** | The final specification requests "Nodes: 16" and "Queue: prod", but prod requires 256-10624 nodes; 16 is below the 256-node minimum. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard Aurora queue "prod", which exists in the supplied queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer states "16 nodes x 104 ranks per node = 1664 ranks," which is arithmetically correct; it also consistently specifies 0 GPUs per node for the CPU-only build. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This requirement applies only where no build default is recorded; the catalog supplies a 104-ranks-per-node build default. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer uses "Ranks per node: 104 (build default)" and specifies zero GPUs because the supplied build is CPU-only on Intel GPUs. |
| `RES.common.sizing_not_absurd` | major | satisfied | Although likely inefficient for this modest SCF workload, 16 nodes is not an absurd allocation under the stated guidance and the answer maintains the required per-node rank layout. |
| `RES.common.walltime_within_queue_limit` | fatal | **violated** | The final specification requests "Walltime: 38 hours" in "Queue: prod", but prod has a maximum walltime of 24 hours. |
