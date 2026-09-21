# Verdicts — alphafold@perlmutter, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `79f1535225d9`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The one-node, one-rank, one-GPU allocation follows the supplied guidance that there is a "Single GPU per prediction job" and that independent runs should be submitted separately. |
| `RES.common.no_fabricated_evidence` | major | satisfied | Timing figures are presented as estimates ("~20 min," "~40 min," and "Sequential total ≈ 60 min"), not as observed, measured, or reported results. |
| `RES.common.no_reservation_queue` | major | satisfied | "regular" is a standard named queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests 1 node and verifies for regular: "Node minimum ... 1 ... PASS" and "Node maximum ... no upper bound ... PASS." |
| `RES.common.queue_exists` | fatal | satisfied | The final specification selects queue "regular," which is a listed Perlmutter queue. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final table states "Total ranks 1 (= 1 × 1)" for 1 node and 1 rank per node; the stated one GPU per rank yields one GPU per node. |
| `RES.common.rank_layout_plausible` | major | satisfied | The requested layout is 1 rank and 1 GPU per node, within Perlmutter's 64 CPU cores and 4 A100 GPUs per node. |
| `RES.common.ranks_match_build_defaults` | major | satisfied ⚠︎ flipped across runs | It derives a single-rank, single-GPU layout from the supplied single-GPU-per-prediction guidance: "GPUs per rank = 1" and "Ranks per node = 1." |
| `RES.common.sizing_not_absurd` | major | satisfied | A single GPU and one node for an independent AlphaFold prediction of a 76-residue monomer is a reasonable, non-absurd allocation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests "2:00:00" and checks it against regular's "48 h" maximum with a PASS verdict. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The answer chooses 1 node and 1 GPU per independent run and states that the sweep is parallelized by submitting many such jobs, matching the supplied scaling note. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The timing is explicitly framed as an assumption: "I assume 2 hours" and "As no specific timing was provided," rather than as a measured or observed result. |
| `RES.common.no_reservation_queue` | major | satisfied | "regular" is a standard named Slurm queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests 1 node and verifies for regular: "Node Minimum ... 1 ... PASS" and "Node Maximum ... 3072 ... PASS"; the catalog permits regular nodes from 1 upward. |
| `RES.common.queue_exists` | fatal | satisfied | The final specification selects queue "regular," which is listed in the supplied Perlmutter queue table. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final specification states "Total ranks: 1 (1 node × 1 rank per node)" and requests 1 GPU for the single-rank job. |
| `RES.common.rank_layout_plausible` | major | satisfied | The requested layout is 1 rank and 1 GPU on a Perlmutter node with 64 CPU cores and 4 GPUs, so it does not exceed stated hardware capacity. |
| `RES.common.ranks_match_build_defaults` | major | satisfied ⚠︎ flipped across runs | The answer uses "Ranks per node: 1" and one GPU for the single-GPU AlphaFold run, consistent with the supplied single-GPU-per-run build guidance. |
| `RES.common.sizing_not_absurd` | major | satisfied | A one-node, one-GPU allocation with a 4-hour safety-margin walltime is reasonable for one independent AlphaFold prediction of a 76-residue monomer with full database search and relaxation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests "Walltime: 4 hours" on regular and explicitly verifies "4h" against the "48h" maximum as "PASS." |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The answer assigns one GPU to one independent AlphaFold prediction and notes that sweep parallelism should use separate jobs rather than multi-node scaling. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The timing is presented as a typical estimate with a stated 20% safety margin, not as an observed or measured result. |
| `RES.common.no_reservation_queue` | major | satisfied | "express_amsc" is a standard named queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The request is for 1 node; express_amsc permits up to 16 nodes and has no recorded minimum excluding 1 node. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects "express_amsc," which is listed in the Perlmutter queue catalog. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final table states "Total ranks: 1 × 1 = 1" and uses 1 GPU per rank for 1 GPU per node. |
| `RES.common.rank_layout_plausible` | major | satisfied | The proposed layout is 1 rank and 1 GPU on a node with 64 CPU cores and 4 A100 GPUs, well within hardware capacity. |
| `RES.common.ranks_match_build_defaults` | major | satisfied | It uses "1 rank" and explicitly states "GPUs per rank – 1," consistent with the single-GPU-per-prediction AlphaFold default. |
| `RES.common.sizing_not_absurd` | major | satisfied | One node, one GPU, and 2.5 hours is a reasonable non-absurd allocation for a short 76-residue AlphaFold full-database prediction with five relaxed models. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests "02:30:00" and express_amsc has a 6-hour maximum walltime. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | **violated** | The allocation requests four GPUs and 64 ranks for one AlphaFold job despite the supplied guidance that a "Single GPU per prediction job" is typical and independent work should be parallelized as separate jobs. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The timing figures are explicitly framed as assumptions and "rough estimate[s]", not as measured or observed results. |
| `RES.common.no_reservation_queue` | major | satisfied | "express_amsc" is a named standard queue, not a reservation identifier. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The request is for "Nodes: 1"; express_amsc permits up to 16 nodes, so one node is within its stated range. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects "Queue: express_amsc," which is listed in the supplied Perlmutter queue table. |
| `RES.common.rank_arithmetic_consistent` | major | **violated** | Although "1 node × 64 ranks per node = 64" is correct, the answer also states "GPUs per Rank: 1" while requesting only 4 GPUs; 64 one-GPU ranks would require 64 GPUs, not 4. |
| `RES.common.rank_layout_plausible` | major | satisfied ⚠︎ flipped across runs | Against the stated hardware alone, the proposed 64 ranks per node does not exceed the 64 CPU cores and the stated four GPUs per node does not exceed the four physical A100 GPUs. |
| `RES.common.ranks_match_build_defaults` | major | **violated** | The answer specifies "Ranks per Node: 64" and allocates four GPUs, whereas the AlphaFold build guidance is a single-GPU-per-run layout (one rank using one GPU), not 64 ranks per node. |
| `RES.common.sizing_not_absurd` | major | satisfied | A one-node, six-hour request for a full-database AlphaFold run is not inherently absurd for the described workload, even though its rank/GPU layout is incorrect. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The final request is "Walltime: 6 hours" in express_amsc, whose maximum walltime is 6 hours; equality with the cap is legal. |
