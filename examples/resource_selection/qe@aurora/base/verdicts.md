# Verdicts — qe@aurora, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `79f1535225d9`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The 1-node, 104-rank CPU-only allocation follows the supplied 104-core/node CPU-only MKL and ScaLAPACK scaling notes. |
| `RES.common.no_fabricated_evidence` | major | satisfied | It explicitly labels the timing as an assumed estimate and states that no measurement or observation is claimed. |
| `RES.common.no_reservation_queue` | major | satisfied | The selected `capacity` target is a standard named queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | It requests 1 node and explicitly verifies `capacity` has a 1-node minimum and 16-node maximum, with both checks marked PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard Aurora `capacity` queue, which is listed in the supplied queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer states 1 node × 104 ranks per node = 104 total ranks, and consistently states zero GPUs are used by the CPU-only workload. |
| `RES.common.rank_layout_plausible` | major | not_applicable | A catalog build default exists for this application (104 ranks per node), so the conditional plausibility rule for cases without a build default does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer uses the supplied build default of 104 ranks per node and correctly specifies zero GPU use for the CPU-only MPI build. |
| `RES.common.sizing_not_absurd` | major | satisfied | A single 104-core node with a 1-hour margin is a reasonable non-absurd allocation for the described 64-atom plane-wave SCF calculation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | It requests 1:00:00 and verifies this is below the `capacity` maximum walltime of 168:00:00. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation follows the CPU-only Intel MKL/ScaLAPACK guidance and uses one MPI rank per stated CPU core. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The timing is explicitly presented as an assumption with a safety margin rather than as a measured or observed result. |
| `RES.common.no_reservation_queue` | major | satisfied | `capacity` is a standard named queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests 4 nodes and verifies that capacity permits 1–16 nodes. |
| `RES.common.queue_exists` | fatal | satisfied | The selected queue is `capacity`, which is listed in the Aurora queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The stated total of 416 ranks equals 4 nodes × 104 ranks per node, and the stated GPU allocation is consistently zero. |
| `RES.common.rank_layout_plausible` | major | not_applicable ⚠︎ flipped across runs | A build default is recorded and used (104 ranks per node), so the fallback plausibility rule for systems with no build default does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It uses the supplied build default of 104 ranks per node and correctly identifies the CPU-only build as using no GPUs. |
| `RES.common.sizing_not_absurd` | major | satisfied | A 4-node CPU allocation with a one-hour request for this 64-atom SCF workload is not an obviously absurd allocation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests 1 hour and verifies that capacity permits up to 168 hours. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses 104 CPU MPI ranks on the 104-core node and no GPUs, consistent with the CPU-only Intel MKL/ScaLAPACK build notes. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The 45-minute runtime is presented as a hedged estimate—"From experience" and "roughly"—rather than an explicitly observed, measured, or reported result. |
| `RES.common.no_reservation_queue` | major | satisfied | The answer targets the standard "debug" queue and does not use a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The final check states 1 requested node against debug limits of 1–2 nodes, with node minimum and maximum both marked PASS. |
| `RES.common.queue_exists` | fatal | satisfied | The selected target queue is "debug," which is listed in the Aurora queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The summary gives "Total ranks: 1 × 104 = 104" and consistently specifies 0 GPUs per rank and 0 GPUs per node. |
| `RES.common.rank_layout_plausible` | major | not_applicable | A build default is recorded and used (104 ranks per node), so the fallback plausibility rule for cases with no catalog build default does not apply. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It uses "Ranks per node – default from the build: 104" and correctly identifies the CPU-only build as using "0 GPUs per rank." |
| `RES.common.sizing_not_absurd` | major | satisfied | A one-node, 104-rank allocation with a 55-minute estimate is a reasonable non-absurd choice for the described 64-atom SCF workload. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests "0 h 55 m 00 s" while debug has a 1-hour maximum, explicitly marked PASS. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses 104 ranks per node, matching the stated 104 CPU cores per node and CPU-only Intel MKL/ScaLAPACK build guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The timing statements are explicitly framed as assumptions (for example, "Let's assume" and "Assuming"), not as observed or measured results. |
| `RES.common.no_reservation_queue` | major | satisfied | The selected queue is "prod", not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The final specification requests 256 nodes in "prod"; the answer identifies the prod range as 256–10624 nodes, so 256 meets both bounds. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard Aurora queue "prod", which is listed in the supplied queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer states "Total ranks: 256 x 104 = 26624," which is arithmetically correct; it also consistently requests zero GPUs for the CPU-only build. |
| `RES.common.rank_layout_plausible` | major | not_applicable | This requirement applies where no build default is recorded, but the catalog and prompt explicitly provide a 104-ranks-per-node build default. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | The answer uses "Ranks per node: 104" and "GPUs per node: 0" for the stated CPU-only MPI build, consistent with the 104-rank build default and no GPU use. |
| `RES.common.sizing_not_absurd` | major | **violated** | The answer allocates 256 nodes and 26,624 MPI ranks for one modest 64-atom SCF calculation; this is an extreme over-allocation with far more ranks than this workload can plausibly divide effectively. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The final specification requests 24 hours in "prod", and the answer identifies prod's maximum walltime as 24 hours. |
