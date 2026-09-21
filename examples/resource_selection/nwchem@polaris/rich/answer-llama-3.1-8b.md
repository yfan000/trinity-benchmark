# llama-3.1-8b — nwchem@polaris, rich arm

Resource selection. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 1 of 10 requirements violated).

````
## Task: Determine the PBS Pro resource specification for a benchmarking run on Polaris

## Step (a): Choose a legal queue

### 1. Size the work and derive the walltime needed

Given the workload, we are scaling a single water molecule using NWChem. The prior timing for a single-node run of this exact calculation is 5 s wall time. We will assume that the walltime scales linearly with the number of nodes. For a small range of node counts, we can use a rough estimate of walltime.

Let's assume we want to run with 16 nodes. The walltime would be approximately 16 × 5 s = 80 s. To be safe, we'll add a 20% margin for any unexpected delays, so the actual walltime needed is 96 s.

### 2. Eliminate queues with insufficient walltime or node range

| Queue | Max Walltime | Node Range | Eliminated |
| --- | --- | --- | --- |
| debug | 1h | 1-2 nodes | FAIL (walltime) |
| debug-scaling | 1h | 1-10 nodes | FAIL (walltime) |
| demand | 1h | 1-56 nodes | FAIL (walltime) |
| preemptable | 72h | 1-10 nodes | FAIL (walltime) |
| capacity | 168h | 1-4 nodes | FAIL (walltime) |
| prod | 24h | 10-496 nodes | FAIL (walltime) |

| Queue | Max Walltime | Node Range | Eliminated |
| --- | --- | --- | --- |
| debug | 1h | 1-2 nodes | FAIL (node range) |
| debug-scaling | 1h | 1-10 nodes | FAIL (node range) |
| demand | 1h | 1-56 nodes | FAIL (node range) |
| preemptable | 72h | 1-10 nodes | FAIL (node range) |
| capacity | 168h | 1-4 nodes | FAIL (node range) |
| prod | 24h | 10-496 nodes | PASS |

| Queue | Max Walltime | Node Range | Eliminated |
| --- | --- | --- | --- |
| debug | 1h | 1-2 nodes | FAIL (walltime) |
| debug-scaling | 1h | 1-10 nodes | FAIL (walltime) |
| demand | 1h | 1-56 nodes | FAIL (walltime) |
| preemptable | 72h | 1-10 nodes | FAIL (node range) |
| capacity | 168h | 1-4 nodes | FAIL (node range) |
| prod | 24h | 10-496 nodes | FAIL (node range) |

### 3. Choose a queue that meets all limits

Based on the above, the only queue that meets all limits is `prod`. However, we need to check if our node count (16) is within the allowed range.

| Queue | Node Minimum | Node Maximum | Walltime | Verdict |
| --- | --- | --- | --- | --- |
| prod | 10 | 496 | 24h | PASS |

The queue `prod` passes all limits.

## Step (b): Determine ranks-per-node and GPUs-per-rank

Based on the application defaults, we will use the following values:

* ranks-per-node: 4 (build default)
* GPUs-per-rank: 1 (since we are using a CPU-only build)

## Step (c): Determine the total ranks and walltime

We will use the following values:

* total ranks: nodes × ranks-per-node = 16 × 4 = 64
* walltime: 96 s (with a 20% margin)

## Step (d): Honour any scaling guidance supplied with the application

The scaling guidance supplied with the application is to use 4 MPI ranks per node. We will honour this guidance.

## Step (e): Restate the resource specification

Here is the resource specification:

* nodes: 16
* ranks-per-node: 4
* total ranks: 64
* GPUs-per-node: 4 (since we are using 4 GPUs per rank, and each node has 4 ranks)
* walltime: 96 s
* queue: prod

The final answer is:

* nodes: 16
* ranks-per-node: 4
* total ranks: 64
* GPUs-per-node: 4
* walltime: 96 s
* queue: prod
````
