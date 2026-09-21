# llama-3.1-8b — nwchem@polaris, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
## Resource Specification

- Nodes: 4
- Ranks per node: 4
- Total ranks: 16
- GPUs per node: 0 (CPU-only build)
- Walltime: 1h
- Queue: debug-scaling

## Reasoning

### (a) Choose a legal queue

#### 1. Size the work and derive the walltime you actually need

The single-node run of this exact calculation completed in 5 s wall time. Since we're doing a scaling benchmark, we'll assume that the walltime will increase linearly with the number of nodes. However, to be conservative, we'll add a margin to account for any potential overheads. Let's assume the walltime will increase by a factor of 4 for 4 nodes, which is a generous estimate. Therefore, the walltime for 4 nodes would be 20 s. To make it a more realistic benchmark, let's assume the walltime will be 1h (3600 s) for 4 nodes.

#### 2. Go through the supplied queue table and eliminate every queue whose maximum walltime is below that figure, or whose node range excludes your node count

| Queue        | Node Range | Max Walltime |
|--------------|------------|--------------|
| debug        | 1-2        | 1h           |
| debug-scaling| 1-10       | 1h           |
| prod         | 10-496     | 24h          |
| demand       | 1-56       | 1h           |
| preemptable  | 1-10       | 72h          |
| capacity     | 1-4        | 168h         |

We can eliminate the following queues:

- debug: max walltime is 1h, which is below our requirement
- debug-scaling: node range excludes our node count of 4
- demand: max walltime is 1h, which is below our requirement
- capacity: node range excludes our node count of 4

We are left with the following queues:

- prod: max walltime is 24h, which is above our requirement
- preemptable: max walltime is 72h, which is above our requirement

#### 3. Choose from what survives, and state the verdict against each of the three limits separately

| Queue        | Node Minimum | Node Maximum | Max Walltime |
|--------------|--------------|--------------|--------------|
| prod         | PASS         | PASS         | PASS         |
| preemptable  | PASS         | PASS         | PASS         |

We can choose either queue prod or queue preemptable.

### (b) Take ranks-per-node and GPUs-per-rank from the supplied application defaults

- Ranks per node: 4 (build default)
- GPUs per rank: 0 (CPU-only build)

### (c) Do not claim a timing or throughput figure was measured or observed when the prompt supplies none

We assumed the walltime will increase linearly with the number of nodes and added a margin to account for potential overheads.

### (d) Honour any scaling guidance supplied with the application, or say why it does not apply to this run

The scaling guidance is to set 4 MPI ranks per node. We are following this guidance.

### (e) Close with a plain restatement of nodes, ranks per node, total ranks, GPUs per node, walltime, and queue

- Nodes: 4
- Ranks per node: 4
- Total ranks: 4 x 4 = 16
- GPUs per node: 0
- Walltime: 1h
- Queue: debug-scaling
````
