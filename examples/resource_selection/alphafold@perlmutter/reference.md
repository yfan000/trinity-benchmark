# Reference answer — alphafold@perlmutter

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
A single AlphaFold prediction job requires exactly 1 GPU (from build defaults: "Single GPU per run typical"). Each job in the sweep runs one prediction independently.

**Ranks and GPUs from build defaults (not agent's choice):**
- Ranks per node: 1 (single MPI rank; AlphaFold is not MPI-parallel — it uses srun -n 1)
- GPUs per rank: 1
- GPUs per node requested: 1

**Node count (agent's choice):** 1 node per job. The scaling note explicitly states to parallelize by submitting multiple independent jobs, not by scaling a single job across nodes.

**Walltime estimation:**
No measured timing is provided. For a 76-residue monomer with full database search and 5 models with relaxation, MSA search dominates for small proteins but the total pipeline is typically well under 2 hours for short sequences. A reasonable assumption is ~1.5 hours of compute, with a margin added to reach 2 hours (7200 seconds). This is an assumption, not a measured value.

**Queue elimination (walltime needed: 2h = 7200s; nodes: 1):**
- debug: max 30 min (1800s) — eliminates on walltime (2h > 30min)
- express_amsc: max 6h — survives walltime; max 16 nodes — survives node count (1 ≤ 16); however, this queue is a shared demo allocation and the build defaults specify account 'dasrepo', not amsc013. The regular queue is the standard production queue and better suited for sweep jobs.
- regular: max 48h — survives
- premium: max 48h — survives, but charges 4× and higher priority is not needed for a routine sweep
- shared: max 48h — survives; suitable for 1-2 GPUs, charged per GPU; valid choice
- preempt: 1-128 nodes, max 48h — survives but jobs are preemptable, risking interruption of sweep runs
- interactive: max 4h — survives walltime; max 4 nodes — survives; but intended for interactive sessions, not batch sweeps
- jupyter: max 6h — survives; but intended for notebook sessions
- overrun: max 48h — no charge but lowest priority; acceptable for cost savings if sweep is not urgent

**Recommended queue: regular** — standard production queue, supports 1 node, 2h walltime comfortably within 48h cap, appropriate for a batch parameter sweep.

Alternatively, **shared** is valid: the job uses only 1 GPU on a node, and the shared queue charges only for GPUs used rather than the full node, making it cost-efficient for a large sweep of single-GPU jobs.

**Legal queue check for regular, 1 node, 2h:**
| Criterion | Requested | Limit | Verdict |
|---|---|---|---|
| Node minimum | 1 | 1 | PASS |
| Node maximum | 1 | no upper limit | PASS |
| Maximum walltime | 2h (7200s) | 48h (172800s) | PASS |

**Scaling guidance honoured:** Each job in the sweep is one independent prediction on 1 GPU. The sweep is parallelized by submitting multiple jobs, not by multi-node MPI scaling within a single job, consistent with the build defaults.

**Final specification:**
- Nodes: 1
- Ranks per node: 1
- Total ranks: 1 × 1 = 1
- GPUs per node: 1
- Walltime: 2 hours (7200 seconds) — assumed, not measured; includes margin over estimated ~1.5h for a 76-residue monomer
- Queue: regular (or shared for per-GPU billing efficiency)
- Each run in the parameter sweep is submitted as a separate job with this same specification.
````
