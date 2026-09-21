# Reference answer — qe@aurora

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
Node count: 1 node
Ranks per node: 104 (build default; CPU-only MPI build, 104 cores per node)
GPUs per node: 0 (CPU-only build; the installed Quantum ESPRESSO on Aurora does not use Intel GPUs)
Total ranks: 1 × 104 = 104

Walltime reasoning:
No measured timing is available. For a 64-atom 3C-SiC SCF calculation with a 60 Ry plane-wave cutoff, a 4×4×4 k-grid (8 irreducible k-points in the cubic BZ), and ultrasoft pseudopotentials, this is a modest workload. On 104 CPU cores with Intel MKL FFTs and ScaLAPACK, a single SCF cycle on a system of this size typically converges in a few minutes. Assuming ~10–20 minutes per SCF run, and applying a conservative 3× safety margin to cover k-point parallelism startup overhead, I/O, and repeated runs in a campaign, an estimated walltime of 1 hour per job is reasonable. No observed timing is claimed.

Queue elimination:
- debug: 1–2 nodes ✓, max 1h — 1 node fits, 1h fits. Survives node and walltime filters. However, the task specifies a *production campaign*; debug allows only 1 job at a time and is intended for testing, not campaign throughput. Eliminated on campaign-use grounds.
- debug-scaling: min 2 nodes — our 1-node request is below the minimum. ELIMINATED (node minimum = 2, requested = 1).
- prod: min 256 nodes — our 1-node request is far below the minimum. ELIMINATED (node minimum = 256, requested = 1).
- visualization: 1–32 nodes ✓, max 8h ✓ — but this queue is by-request only and is not appropriate for a DFT compute campaign. Eliminated on suitability grounds.
- capacity: 1–16 nodes, max 168h — 1 node is within range, 1h is within the 168h cap. This queue is designed for small jobs that do not need prod, supports small production campaigns (up to 5 jobs per project, up to 128 total nodes across jobs), and has a walltime ceiling well above the needed 1h. SURVIVES.

Chosen queue: capacity

Verification against capacity limits:
| Criterion       | Requested | Limit      | Result |
|-----------------|-----------|------------|--------|
| Node minimum    | 1         | 1          | PASS   |
| Node maximum    | 1         | 16         | PASS   |
| Max walltime    | 3600 s (1h) | 604800 s (168h) | PASS |

Scaling guidance:
The build defaults specify 104 MPI ranks per node (one per CPU core) with Intel MKL FFT and ScaLAPACK. This is a CPU-only build; no GPU ranks apply. The application's scaling notes confirm 104 CPU cores per node. For a 64-atom system with a relatively small k-grid, scaling beyond a single node would yield diminishing returns and is not warranted for a campaign of this size. 1 node is appropriate.

Final specification:
- Nodes: 1
- Ranks per node: 104
- Total ranks: 1 × 104 = 104
- GPUs per node: 0 (CPU-only build)
- Walltime: 1 hour (3600 s) — assumed, with 3× safety margin; no measured time available
- Queue: capacity
````
