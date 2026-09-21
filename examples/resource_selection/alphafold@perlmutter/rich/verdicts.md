# Verdicts — alphafold@perlmutter, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `79f1535225d9`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The allocation uses one GPU for one independent prediction job and recommends sweep parallelism across jobs, matching the supplied single-GPU-per-run scaling guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The answer explicitly labels runtime values as estimates and states that no measured timings were supplied; it does not claim an observed or measured benchmark result. |
| `RES.common.no_reservation_queue` | major | satisfied | The selected queue is `regular`, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests 1 node; `regular` admits nodes 1 through no stated upper limit, so 1 node is valid. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects the standard Perlmutter queue `regular`, which is present in the supplied queue catalog. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The answer states total ranks are 1 = 1 node × 1 rank per node, and its 1 GPU per rank is consistent with 1 GPU per node. |
| `RES.common.rank_layout_plausible` | major | satisfied | The answer uses 1 rank and 1 GPU per node, which is within the stated Perlmutter capacity of 64 CPU cores and 4 GPUs per node. |
| `RES.common.ranks_match_build_defaults` | major | not_applicable ⚠︎ flipped across runs | The authoritative catalog facts provide defaults for nodes, walltime, queue, constraint, and account, but record no ranks-per-node or GPUs-per-rank build default to match. |
| `RES.common.sizing_not_absurd` | major | satisfied | A one-node, one-GPU allocation with a 4-hour safety-margin walltime is reasonable for a short AlphaFold target with full database search, five models, and relaxation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests 4 hours on `regular`, whose maximum walltime is 48 hours. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The one-node, one-rank, one-GPU allocation follows the supplied guidance that AlphaFold uses a "Single GPU per prediction job" and sweep runs should be submitted independently. |
| `RES.common.no_fabricated_evidence` | major | satisfied | Timing values are presented as estimates and an explicit assumption: "typically," "roughly," and "I assume a total runtime of ~4 hours." |
| `RES.common.no_reservation_queue` | major | satisfied | The answer selects the standard "regular" queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests "1 Node" on regular; the catalog permits regular nodes from 1 with no upper limit. |
| `RES.common.queue_exists` | fatal | satisfied | The selected queue is explicitly stated as "regular," which exists in the Perlmutter queue catalog. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | It states "Total ranks: 1 (1 node × 1 rank per node)" and requests one GPU for one rank at one GPU per rank. |
| `RES.common.rank_layout_plausible` | major | satisfied | The answer specifies "Ranks per node: 1" and "GPUs per rank: 1," within Perlmutter's 64 CPU cores and 4 GPUs per node. |
| `RES.common.ranks_match_build_defaults` | major | satisfied ⚠︎ flipped across runs | The answer uses one rank per node and states “GPUs per rank: 1,” consistent with the supplied single-GPU-per-prediction/run guidance. |
| `RES.common.sizing_not_absurd` | major | satisfied | A single GPU/node for a 76-residue AlphaFold monomer is reasonable, and the stated 5-hour estimate includes full database-search and I/O margin. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The final request is "Walltime: 5 hours" on regular, whose maximum walltime is 48 hours. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | satisfied | The answer chooses one GPU for one independent prediction and states that the sweep is handled as separate runs, matching the single-GPU scaling guidance. |
| `RES.common.no_fabricated_evidence` | major | satisfied | The timing is framed as an estimate—“usually finishes” and “we add a safety margin”—rather than as observed or measured evidence. |
| `RES.common.no_reservation_queue` | major | satisfied | `express_amsc` is named as a standard queue, not presented as a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests “Node count: 1”; express_amsc permits up to 16 nodes in the catalog, so 1 node is admitted. |
| `RES.common.queue_exists` | fatal | satisfied | The answer selects `express_amsc`, which is a listed Perlmutter queue. |
| `RES.common.rank_arithmetic_consistent` | major | satisfied | The final table explicitly gives “Total ranks: 1 × 1 = 1” for 1 node and 1 rank per node, with 1 GPU assigned to that rank. |
| `RES.common.rank_layout_plausible` | major | satisfied | The stated layout is 1 rank and 1 GPU per node, well within Perlmutter's 64 CPU cores and 4 GPUs per node. |
| `RES.common.ranks_match_build_defaults` | major | satisfied ⚠︎ flipped across runs | The answer uses “1 rank on the node” and “1 GPU per rank,” consistent with the supplied single-GPU-per-prediction AlphaFold build/scaling guidance. |
| `RES.common.sizing_not_absurd` | major | satisfied | A 1-node, 1-GPU allocation with a 2h45m allowance is reasonable for a 76-residue AlphaFold job with full database search, five models, and relaxation. |
| `RES.common.walltime_within_queue_limit` | fatal | satisfied | The answer requests “02:45:00” and states the express_amsc maximum is “06:00:00”; 2h45m is below the 6h cap. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `RES.common.allocation_matches_scaling_notes` | minor | **violated** | The allocation treats two nodes as one job to run jobs in parallel, whereas the supplied guidance says AlphaFold uses a single GPU per prediction and should be parallelized by submitting multiple independent jobs, not by expanding a single prediction job across nodes. |
| `RES.common.no_fabricated_evidence` | major | satisfied | Timing statements are explicitly framed as assumptions (for example, "let's assume it takes around 12 hours") rather than measured or observed evidence. |
| `RES.common.no_reservation_queue` | major | satisfied | "preempt" is a standard named queue, not a reservation ID. |
| `RES.common.nodes_within_queue_limits` | fatal | satisfied | The answer requests "nodes = 2" and preempt permits "1-128 nodes," so 2 is within the range. |
| `RES.common.queue_exists` | fatal | satisfied | The final specification selects "queue = preempt", which is a listed Perlmutter queue. |
| `RES.common.rank_arithmetic_consistent` | major | **violated** | Although "2 × 64 = 128" is arithmetically correct for ranks, the answer states "GPUs-per-rank = 1" and 128 total ranks while requesting only "GPUs = 2"; one GPU per rank would require 128 GPUs, not 2. |
| `RES.common.rank_layout_plausible` | major | **violated** ⚠︎ flipped across runs | The answer states "ranks-per-node = 64" and "GPUs-per-rank = 1" while requesting only 2 GPUs for 2 nodes, implying 64 GPU-consuming ranks per node despite Perlmutter having only 4 GPUs per node. |
| `RES.common.ranks_match_build_defaults` | major | **violated** ⚠︎ flipped across runs | The answer sets "ranks-per-node = 64" solely because the node has 64 CPU cores, despite AlphaFold's single-GPU-per-prediction layout; this does not follow the intended one prediction rank with one GPU-per-rank build layout. |
| `RES.common.sizing_not_absurd` | major | satisfied ⚠︎ flipped across runs | While inefficient and internally inconsistent, a two-node allocation for a full-database AlphaFold sweep is not the kind of extreme, plainly nonsensical scale required to violate this rule. |
| `RES.common.walltime_within_queue_limit` | fatal | **violated** | The final request is "walltime = 60h" on preempt, but preempt has a maximum walltime of 48h; the answer itself acknowledges the 48h cap but nevertheless submits 60h. |
