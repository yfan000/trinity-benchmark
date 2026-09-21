# llama-3.1-8b — qe@aurora, rich arm

Resource selection. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 2 of 10 requirements violated).

````
To determine the optimal resource specification for the production DFT campaign on Aurora, we will follow the steps outlined below.

**Step 1: Size the work and derive the walltime**

Using the provided workload, we can estimate the walltime required for the SCF total-energy calculation. Assuming a 4x4x4 Monkhorst-Pack k-grid and a 2x2x2 conventional supercell, the total number of k-points is 64. With 4 k-points per node in the k-grid, we can estimate the walltime as follows:

* 64 k-points / 4 k-points per node = 16 nodes (to achieve good parallelization)
* Assuming a linear scaling of walltime with the number of k-points, we can estimate the walltime as follows:
	+ 1 k-point: 1 hour (a rough estimate for a single-point calculation)
	+ 16 k-points: 16 hours (assuming a linear scaling)

However, we should also consider the number of atoms in the supercell (64 atoms) and the fact that we are performing a SCF calculation. This will likely increase the walltime. A more realistic estimate would be:

* 16 hours * 2 (to account for the number of atoms) = 32 hours

Adding a 20% margin to account for any potential overhead or unexpected issues, we can estimate the walltime as follows:

* 32 hours * 1.2 (20% margin) = 38.4 hours

Rounding down to the nearest hour, we can estimate the walltime as follows:

* 38.4 hours ≈ 38 hours

**Step 2: Eliminate queues with insufficient walltime or node range**

| Queue | Maximum Walltime | Node Range | Node Minimum | Node Maximum |
| --- | --- | --- | --- | --- |
| debug | 1 hour | 1-2 | PASS | PASS |
| debug-scaling | 1 hour | 2-256 | FAIL (node minimum) | PASS |
| prod | 24 hours | 256-10624 | PASS | PASS |
| capacity | 168 hours | 1-16 | FAIL (node minimum) | PASS |
| visualization | 8 hours | 1-32 | FAIL (node minimum) | PASS |

**Step 3: Choose a queue that meets the requirements**

Based on the previous step, we can choose the `prod` queue, which meets all the requirements.

| Queue | Verdict |
| --- | --- |
| debug | FAIL (walltime) |
| debug-scaling | FAIL (walltime) |
| prod | PASS |
| capacity | FAIL (walltime) |
| visualization | FAIL (walltime) |

**Step 4: Determine ranks per node and GPUs per node**

Based on the provided application defaults, we can determine the ranks per node and GPUs per node as follows:

* Ranks per node: 104 (build default)
* GPUs per node: 0 (since the build is CPU-only and Aurora uses Intel GPUs)

**Step 5: Determine the resource specification**

Based on the previous steps, we can determine the resource specification as follows:

* Node count: 16 (to achieve good parallelization)
* Ranks per node: 104 (build default)
* Total ranks: 16 nodes x 104 ranks per node = 1664 ranks
* GPUs per node: 0 (since the build is CPU-only and Aurora uses Intel GPUs)
* Walltime: 38 hours
* Queue: prod

The resource specification is:

* Nodes: 16
* Ranks per node: 104
* Total ranks: 1664
* GPUs per node: 0
* Walltime: 38 hours
* Queue: prod

Note that the total ranks is calculated as the product of the node count and ranks per node.
````
