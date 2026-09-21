# llama-3.1-8b — alphafold@perlmutter, rich arm

Resource selection. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 5 of 10 requirements violated).

````
## Resource Specification and Reasoning

### Step 1: Size the work and derive the walltime needed

The workload involves a full database search with 5 models and relaxation. Based on the AlphaFold documentation, this process typically takes several hours to a few days, depending on the system and the input size. To be conservative, let's assume it takes around 12 hours for a single run. Since we are doing a parameter sweep with many similar runs, we need to estimate the total walltime required. Let's assume we want to run at least 10-20 jobs in parallel, which is a reasonable number considering the queue policies and the available nodes. This means we need to run each job for at least 12 hours, and we want to run 10-20 jobs in parallel.

### Step 2: Eliminate queues that do not meet the walltime or node requirements

| Queue | Max Walltime | Node Range | Elimination Reason |
| --- | --- | --- | --- |
| express_amsc | 6h | N/A | Walltime too short |
| debug | 30m | 1-8 nodes | Walltime too short |
| regular | 48h | N/A | Walltime too short |
| premium | 48h | N/A | Walltime too short |
| shared | 48h | N/A | Walltime too short |
| preempt | 48h | 1-128 nodes | Walltime too short |
| interactive | 4h | 1-4 nodes | Walltime too short |
| jupyter | 6h | 1-4 nodes | Walltime too short |
| overrun | 48h | N/A | Walltime too short |

The queues that survive the elimination process are:

* preempt (max 48h, 1-128 nodes)
* overrun (max 48h, N/A)

### Step 3: Choose a queue that meets all the requirements

Based on the available queues, we can choose either the preempt or overrun queue. Both queues have a maximum walltime of 48 hours, which meets our requirements.

| Queue | Node Minimum | Node Maximum | Max Walltime | Verdict |
| --- | --- | --- | --- | --- |
| preempt | PASS (1 node) | PASS (128 nodes) | PASS (48h) | PASS |
| overrun | PASS (N/A) | PASS (N/A) | PASS (48h) | PASS |

We can choose either queue, but let's choose the preempt queue since it has a more flexible node range.

### Step 4: Determine ranks-per-node and GPUs-per-rank

According to the Build Defaults, we should use:

* ranks-per-node = 64 (since each node has 64 CPU cores)
* GPUs-per-rank = 1 (since we are using a single GPU per run)

### Step 5: Determine node count and total ranks

Based on our previous choices, we can determine the node count and total ranks. Let's assume we want to run 10 jobs in parallel, which means we need to run each job for 12 hours. We can calculate the total walltime required as:

Total walltime = 12h/jobs × 10 jobs = 120h

Since we are running on the preempt queue, which has a maximum walltime of 48 hours, we need to run multiple jobs in parallel to meet the total walltime requirement. Let's assume we want to run 2 jobs in parallel, which means we need to run each job for 60 hours (120h / 2 jobs). This means we need to run each job for 60 hours, and we want to run 2 jobs in parallel.

Node count = 2 (since we are running 2 jobs in parallel)
Total ranks = node count × ranks-per-node = 2 × 64 = 128

### Resource Specification

Based on our previous choices, the resource specification is:

* nodes = 2
* GPUs = 2
* ranks-per-node = 64
* total ranks = 128
* walltime = 60h
* queue = preempt

Note that the total ranks (128) is equal to the node count (2) × ranks-per-node (64).
````
