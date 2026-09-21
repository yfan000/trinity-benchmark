# Reference answer — gromacs@sirius

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
**Node count:** 1 node
Sirius has 4 nodes total. The workload is ~34,000 atoms — a small biomolecular system. The build default is 8 ranks per node targeting 8 GPUs, but Sirius has only 4 GPUs per node; therefore 4 ranks per node is the physically achievable maximum on one node. A single node is appropriate for a system of this size; scaling to multiple nodes for ~34k atoms would add communication overhead with little benefit and is not warranted.

**Ranks per node:** 4 (one MPI rank per GPU; build default says one rank per GPU, and there are 4 GPUs per node on Sirius — the node GPU count is the binding constraint)
**GPUs per node:** 4 (all A100s on the node)
**Total ranks:** 1 × 4 = 4

**Walltime derivation:**
No prior throughput measurement is available. For a ~34,000-atom NPT GROMACS simulation with PME on A100 GPUs, a reasonable conservative assumption (stated as an assumption, not a measurement) is ~200–300 ns/day on 4 A100s. At 200 ns/day (pessimistic bound), 5 ns requires ~0.6 hours of compute. This is a restart from checkpoint, so some fraction of the 5 ns is already complete — but the remaining amount is unknown, so the full 5 ns is budgeted for safety. Adding a 2× margin for uncertainty: ~1.2 hours. Round up to 2 hours (7200 s) as the requested walltime. This is well within the 24-hour cap.

**Queue elimination:**
Only one queue exists on Sirius: workq (1–4 nodes, max 24h).
- workq: node range 1–4, max walltime 24h. Requested 1 node and 2h — no limit violated. SURVIVES.

**Queue compliance check for workq:**
| Criterion        | Requested | Limit  | Verdict |
|-----------------|-----------|--------|---------|
| Node minimum    | 1         | 1      | PASS    |
| Node maximum    | 1         | 4      | PASS    |
| Maximum walltime| 2h (7200s)| 24h    | PASS    |

**Scaling guidance honoured:**
The build notes state one MPI rank per GPU. On Sirius with 4 GPUs per node, this means 4 ranks per node. The build default of 8 ranks per node assumes 8 GPUs per node (e.g., Polaris); Sirius has 4, so 4 ranks per node is correct and consistent with the one-rank-per-GPU rule. GPU offload for non-bonded, PME, and update kernels is used.

**Final specification:**
- Nodes: 1
- Ranks per node: 4
- Total ranks: 1 × 4 = 4
- GPUs per node: 4
- Walltime: 2 hours (7200 s)
- Queue: workq
````
