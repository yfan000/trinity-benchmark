# Reference answer — nwchem@polaris

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
**Sizing the work**

The measured wall time for a single water molecule B3LYP/6-31G* single-point energy on 1 node (4 MPI ranks) is 5 s. This problem is trivially small; even at 10 nodes the calculation itself will complete in well under a minute. For a scaling benchmark we need to run the same problem at several node counts (e.g. 1, 2, 4, 8, 10 nodes) and collect timing data at each point. Each individual run will take only seconds. Allowing generous overhead for job startup, file I/O, and repeated runs, 30 minutes (1800 s) is a safe and conservative walltime. I am assuming the per-run cost is dominated by MPI startup rather than computation, and I am adding a large proportional margin (>20×) to the raw 5 s measurement.

**Ranks per node and GPU assignment**

The build default is 4 MPI ranks per node. This is a CPU-only build; GPU support is experimental and not part of this installation. Therefore GPUs per node = 0 (not requested; the code does not use them). Only the node count is the agent's choice.

**Scaling guidance**

The application notes say: 'Scale nodes for larger molecular systems.' A single water molecule is the smallest possible test system and will not scale efficiently beyond a handful of nodes — strong scaling efficiency will collapse quickly. However, the purpose here is precisely to observe that collapse and characterise the scaling curve, so running across a range up to ~10 nodes is the right experimental design. Going beyond 10 nodes would waste allocation on a problem that is already communication-bound, and would push into the prod queue minimum (10 nodes) unnecessarily.

**Queue elimination**

Target node count: up to 10 nodes (to sweep 1, 2, 4, 8, 10). Derived walltime needed: 1800 s (30 min).

- debug: max 2 nodes — excludes node counts above 2; ELIMINATED (node maximum too low for a multi-point scaling sweep).
- debug-scaling: 1-10 nodes, max 1 h (3600 s) — covers all target node counts and the walltime. SURVIVES.
- prod: minimum 10 nodes — a sweep starting at 1 node fails the node minimum; ELIMINATED.
- demand: by request only (not generally available); ELIMINATED on access grounds.
- preemptable: 1-10 nodes, max 72 h — survives on limits, but jobs are killed without warning when demand queue jobs arrive; inappropriate for a timing benchmark where interrupted runs produce invalid data. ELIMINATED on reliability grounds.
- capacity: max 4 nodes — excludes 8- and 10-node points; ELIMINATED (node maximum too low).

**Chosen queue: debug-scaling**

Verification table for the chosen allocation (10 nodes, 1800 s walltime):

| Criterion        | Requested | Limit       | Verdict |
|------------------|-----------|-------------|---------|
| Node minimum     | 10        | 1           | PASS    |
| Node maximum     | 10        | 10          | PASS    |
| Maximum walltime | 1800 s    | 3600 s      | PASS    |

Note: debug-scaling allows max 1 job per user (running/accruing/queued). The scaling sweep should therefore be structured as a single job that runs the different node counts sequentially within one allocation, or the agent must be aware of the single-job limit and submit accordingly.

**Final specification**

| Parameter       | Value                              |
|-----------------|------------------------------------|
| Nodes           | 10 (sweep points: 1,2,4,8,10)     |
| Ranks per node  | 4 (build default, not negotiable)  |
| Total MPI ranks | 40 (= 10 × 4)                     |
| GPUs per node   | 0 (CPU-only build)                 |
| Walltime        | 1800 s (30 min)                   |
| Queue           | debug-scaling                      |

Total ranks = nodes × ranks per node = 10 × 4 = 40.
````
