# llama-3.1-8b — nekrs@polaris, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
(a) Determining nodes, walltime, and queue:

1. Size the work and derive the walltime you actually need:

- Problem size: 32,000 spectral elements at polynomial order 7, 20,000 timesteps, statistics collected over the final 10,000
- Prior measurement: 1,000 timesteps completed in approximately 8 minutes wall time
- Scaling assumption: walltime scales linearly with the number of timesteps
- Total walltime = (20,000 / 1,000) * 8 minutes = 160 minutes
- Added 20% margin for safety: 160 minutes * 1.2 = 192 minutes

2. Go through the supplied queue table and eliminate every queue whose maximum walltime is below that figure, or whose node range excludes your node count:

- queue debug: max walltime = 1h (60 minutes) FAILS
- queue debug-scaling: max walltime = 1h (60 minutes) FAILS
- queue prod: max walltime = 24h (1,440 minutes) PASS
- queue demand: max walltime = 1h (60 minutes) FAILS
- queue preemptable: max walltime = 72h (4,320 minutes) PASS
- queue capacity: max walltime = 168h (10,080 minutes) PASS

3. Choose from what survives:

| Queue | Node Minimum | Node Maximum | Walltime |
| --- | --- | --- | --- |
| prod | 10 | 496 | PASS |
| preemptable | 1 | 10 | PASS |
| capacity | 1 | 4 | PASS |

(b) Ranks per node and GPUs per rank:

- ranks per node (build default): 4
- GPUs per rank: 1 (since NekRS uses 1 MPI rank per GPU)

(c) Scaling guidance and assumptions:

- Scaling guidance: Precompile kernels on first run (--build-only) to avoid timeout.
- Assumption: The scaling behavior is linear with the number of nodes.

(d) Scaling guidance and application:

- Scaling guidance: Scale by increasing node count.
- Application: NekRS uses 1 MPI rank per GPU (4 per node on Polaris). This matches the build default ranks per node.

(e) Resource specification:

- Nodes: 496 (prod queue has the maximum node count)
- Ranks per node: 4 (build default)
- Total ranks: 496 * 4 = 1984
- GPUs per node: 4 (1 GPU per rank, 4 ranks per node)
- Walltime: 192 minutes
- Queue: prod

Resource specification: 
496 nodes, 4 ranks/node, total 1984 ranks, 4 GPUs/node, walltime 192 minutes, prod queue.
````
