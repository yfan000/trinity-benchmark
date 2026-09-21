# llama-3.1-8b — qmcpack@aurora, base arm

Resource selection. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 1 of 10 requirements violated).

````
**Step (a) - CHOOSE A LEGAL QUEUE**

### 1. Size the work and derive the walltime you actually need

Based on the workload, we have:
- 64 atoms in a 2x2x2 supercell
- 4096 walkers
- 200 DMC blocks
- Timestep: 0.005 Ha^-1

We assume that the number of DMC blocks directly scales with the number of walkers, so we estimate the total walltime as follows:
- Each DMC block takes approximately 1/4096 of the total walltime, since there are 4096 walkers.
- With 200 DMC blocks, the total walltime is approximately 200/4096 = 0.0488 or 4.88% of the total time per block.
- We assume that the total walltime per block is proportional to the number of walkers, so we can scale up the walltime per block by a factor of 4096/64 = 64, since there are 64 atoms in the supercell.
- The total walltime is then approximately 200 * 0.0488 * 64 = 62.4 hours.

We add a 10% margin to account for any potential overheads:
- 62.4 hours * 1.1 = 68.24 hours

### 2. Go through the supplied queue table and eliminate every queue whose maximum walltime is below that figure, or whose node range excludes your node count

We eliminate the following queues:
- queue debug: max walltime 1h (below the required walltime)
- queue debug-scaling: max walltime 1h (below the required walltime)
- queue visualization: max walltime 8h (below the required walltime)
- queue capacity: max walltime 168h (above the required walltime, but we can't use it because it only allows 1-16 nodes)

### 3. Choose from what survives

We are left with:
- queue prod: max walltime 24h (above the required walltime)
- queue capacity is eliminated due to the walltime, however, we can use queue prod for this task

### Queue Survivors

| Queue | Node Minimum | Node Maximum | Max Walltime | PASS/Fail |
| --- | --- | --- | --- | --- |
| queue prod | PASS | PASS | PASS |
| queue capacity | FAIL | FAIL | FAIL |

### Step (b) - TAKE RANKS-PER-NODE AND GPUs-PER-RANK FROM THE SUPPLIED APPLICATION DEFAULTS

- ranks per node (build default): 6
- GPUs per rank: 1 (since there are 6 Intel GPU tiles per node and we are offloading to a single GPU per rank)

### Step (c) - DO NOT CLAIM A TIMING OR THROUGHPUT FIGURE WAS MEASURED OR OBSERVED

We assumed that the total walltime is proportional to the number of walkers and the number of DMC blocks, and we added a 10% margin to account for any potential overheads.

### Step (d) - HONOUR ANY SCALING GUIDANCE SUPPLIED WITH THE APPLICATION

We are not given any scaling guidance, so we will proceed with the default ranks-per-node and GPUs-per-rank values.

### Step (e) - CLOSE WITH A PLAIN RESTATEMENT OF NODES, RANKS PER NODE, TOTAL RANKS, GPUs PER NODE, WALLTIME AND QUEUE

We choose to run on 256 nodes (the minimum allowed by queue prod), which is a reasonable starting point for this calculation.
- nodes: 256
- ranks per node: 6
- total ranks: 256 * 6 = 1536
- GPUs per node: 6
- walltime: 68.24 hours
- queue: queue prod

Total Ranks = nodes x ranks per node
1536 = 256 x 6
PASS

Resource specification: 
- nodes: 256
- ranks per node: 6
- total ranks: 1536
- GPUs per node: 6
- walltime: 68.24 hours
- queue: queue prod
````
