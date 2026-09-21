# Reference answer — qmcpack@aurora

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
Sizing reasoning:

1. Walltime estimate
No measured timing is available. For a small single-node QMCPACK run (64-atom cell, 4096 walkers, 200 DMC blocks) with GPU offload, 1 hour is a standard conservative first estimate for a reproducing run. A safety margin is built in by requesting the full 1-hour cap of the debug queue. This is an assumption, not a measured figure.

2. Node count
The build default is 6 MPI ranks per node, one rank per GPU tile, matching Aurora's 6 GPU tiles per node. QMCPACK's scaling note confirms 6 tiles per node. For a 64-atom cell with 4096 walkers the workload is modest; 1 node (6 ranks, 6 GPUs) is the natural starting point for reproducing a prior result and fits the debug queue perfectly. The agent must not change ranks-per-node — that is fixed by the build.

3. Queue elimination
- debug: 1-2 nodes, max 1h — 1 node is in range, 1h walltime fits. SURVIVES.
- debug-scaling: min 2 nodes — 1 node fails the minimum. ELIMINATED (node minimum).
- prod: min 256 nodes — 1 node fails the minimum. ELIMINATED (node minimum).
- capacity: 1-16 nodes, max 168h — node range fits, walltime fits. SURVIVES.
- visualization: by request only, non-exclusive. Not appropriate for a compute job. ELIMINATED (policy).

Surviving queues: debug, capacity.
Debug is preferred for a reproducing/validation run: immediate turnaround, 1-job-per-user limit is acceptable for a single reproducing attempt.

4. Final queue check against debug:
| Criterion        | Requested | Limit     | Verdict |
|------------------|-----------|-----------|---------|
| Node minimum     | 1 node    | 1 node    | PASS    |
| Node maximum     | 1 node    | 2 nodes   | PASS    |
| Maximum walltime | 3600 s    | 3600 s    | PASS    |

5. Scaling guidance
The build default places one MPI rank per GPU tile (6 ranks, 6 GPUs per node). For a single-node reproducing run there is no need to scale beyond one node; the guidance to use 6 ranks per node is honoured exactly.

Final specification:
- Nodes: 1
- Ranks per node: 6 (build default, fixed)
- Total ranks: 1 × 6 = 6
- GPUs per node: 6 (Intel Data Center GPU Max Series, SYCL offload)
- Walltime: 3600 s (1 hour) — assumed, with full debug-queue margin; no measured figure available
- Queue: debug
````
