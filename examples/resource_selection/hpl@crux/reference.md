# Reference answer — hpl@crux

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
Node count: The process grid is 2×2 = 4 MPI ranks total. With the build default of 128 ranks per node, 4 ranks fit on a single node (ranks per node ≤ 128). One node is therefore sufficient and correct.

GPUs per node: 0. Crux is a CPU-only cluster; the HPL build has no GPU support.

Ranks per node: 128 (build default). The scaling notes require all 128 cores per node to be used. With only 4 ranks needed (2×2 grid) and 128 cores available, each rank runs with ample core resources; the build default of 128 ppn governs the PBS -l select line, but only 4 ranks are launched by mpiexec matching the P×Q grid.

Walltime reasoning: No measured runtime is available. HPL at N=50000 is a modest problem size. A conservative upper-bound estimate on a single 128-core EPYC node (well-tuned BLAS via cray-libsci) is on the order of a few minutes of compute; 30 minutes (1800 s) is a safe assumption with margin, and is the application catalog default. Because turnaround is the priority, the walltime should not be padded beyond what is needed.

Queue elimination:
- debug: max 1h (3600 s) — walltime of 1800 s fits; node range 1–8 — 1 node fits. SURVIVES. However, debug is intended for short tests and is not the production path; for a deadline run workq-route is preferred. Both are legal.
- workq-route: max 24h — 1800 s fits; node range 1–184 — 1 node fits. SURVIVES. This is the correct production queue.
- preemptable: max 72h — fits; node range 1–10 — fits. However, jobs are killed without warning; unacceptable for a deadline run. ELIMINATED on operational grounds (reliability).
- demand: by request only; max 1h — fits; node range 1–64 — fits. Not available without prior arrangement. ELIMINATED (access).

Chosen queue: workq-route.

Legal-queue check for workq-route with 1 node, 1800 s walltime:
  Node minimum (1):    requested 1, limit 1,   PASS
  Node maximum (184):  requested 1, limit 184,  PASS
  Max walltime (86400s): requested 1800s, limit 86400s, PASS

Final specification:
  Nodes:          1
  Ranks per node: 128  (build default; all 128 cores used)
  Total ranks:    1 × 128 = 128  (mpiexec launched with -n 4 matching P×Q=2×2, but ppn=128 fills the node)
  GPUs per node:  0
  Walltime:       00:30:00 (1800 s) — assumed, no measured data; catalog default; margin included
  Queue:          workq-route

Note on total ranks: The PBS resource line requests 1 node with ppn=128 (filling the node). The mpiexec call uses -n 4 to match the 2×2 HPL process grid. The distinction is between cores allocated (128) and MPI ranks active in the HPL grid (4). The build default of 128 ppn governs allocation; the HPL.dat P×Q governs the rank count the benchmark actually uses.
````
