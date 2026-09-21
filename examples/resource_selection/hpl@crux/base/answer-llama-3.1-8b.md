# llama-3.1-8b — hpl@crux, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**(a) Determine the PBS Pro resource specification**

### Step 1: Derive the walltime needed for the workload

To determine the walltime needed, we'll use the problem size N=50000, block size NB=232, and a 2x2 process grid. The HPL LINPACK benchmark scales as O(N^3), so the walltime will be approximately proportional to N^3.

Let's assume a linear scaling for simplicity, and add a 10% margin to account for any overheads.

Walltime needed = (N^3) × 1.1 ≈ (50000^3) × 1.1 ≈ 1.38 × 10^9 seconds

To convert this to a more manageable unit, let's use hours:

Walltime needed ≈ 1.38 × 10^9 seconds / (60 × 60 × 24) ≈ 16157 hours

### Step 2: Eliminate queues with maximum walltime below the needed walltime

| Queue        | Maximum Walltime | Node Range         |
|--------------|------------------|---------------------|
| debug        | 1h                | 1-8 nodes           |
| workq-route  | 24h               | 1-184 nodes         |
| preemptable  | 72h               | 1-10 nodes          |
| demand       | 1h                | 1-64 nodes          |

Queues that can be eliminated due to their maximum walltime being below the needed walltime:

* debug (1h < 16157h)
* demand (1h < 16157h)

### Step 3: Eliminate queues with node range excluding the node count

We need at least 256 nodes to run the workload. Queues that can be eliminated due to their node range excluding the node count:

* debug (1-8 nodes < 256 nodes)
* demand (1-64 nodes < 256 nodes)
* preemptable (1-10 nodes < 256 nodes)

### Step 4: Choose the remaining queue

Only one queue survives: workq-route (1-184 nodes, max 24h)

### Queue Verdict

| Queue        | Node Minimum | Node Maximum | Maximum Walltime |
|--------------|--------------|--------------|------------------|
| workq-route  | PASS         | PASS         | PASS             |

### Step 5: Determine the nodes, walltime, and queue

Based on the queue chosen, we can set the nodes to 184 (the maximum allowed), and the walltime to 24h (the maximum allowed).

Nodes: 184
Walltime: 24h
Queue: workq-route

### (b) Determine ranks per node and GPUs per node

According to the application defaults, we should use:

Ranks per node: 128
GPUs per rank: 0 (since the workload is CPU-only)

### (c) Scaling guidance and assumptions

The scaling guidance mentions maximizing performance by using all 128 cores per node. We've assumed a linear scaling for the walltime, and added a 10% margin to account for any overheads.

### (d) Honouring scaling guidance

We've honoured the scaling guidance by using all 128 cores per node.

### (e) Restate the resource specification

Nodes: 184
Ranks per node: 128
Total ranks: 184 × 128 = 23552
GPUs per node: 0
Walltime: 24h
Queue: workq-route
````
