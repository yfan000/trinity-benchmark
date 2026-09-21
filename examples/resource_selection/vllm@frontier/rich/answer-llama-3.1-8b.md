# llama-3.1-8b — vllm@frontier, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
Based on the workload and system specifications, we will follow the steps to determine the required specifications.

(a) Size the work and derive the walltime needed:

Given the workload:
- Problem: Llama-3.1-8B offline inference, 50 prompts, max_tokens=50, tensor parallel size 4
- System: Frontier (OLCF)

The validated throughput at TP=8 on 1 node is not provided, so we will assume a throughput of 1 prompt per second for a single node with 8 GCD devices. This is a conservative estimate, and we will add a 50% margin to account for potential overheads.

Throughput = 1 prompt/second * 8 GCD devices * 50 prompts = 400 seconds

Walltime = Throughput / (number of nodes * throughput per node)
= 400 seconds / (1 node * 1 prompt/second)
= 400 seconds

However, we need to consider the total number of prompts and the tensor parallel size. Since we are using 4 tensor parallelism, we can process 4 prompts in parallel. Therefore, the total walltime is:

Walltime = (total prompts / tensor parallel size) * (time per prompt / number of nodes)
= (50 prompts / 4) * 400 seconds
= 5000 seconds

We will add a 50% margin to account for potential overheads:

Walltime = 5000 seconds * 1.5
= 7500 seconds

(b) Go through the queue table and eliminate every queue whose maximum walltime is below that figure, or whose node range excludes our node count:

Queue table:

| Queue | Node Range | Max Walltime |
| --- | --- | --- |
| batch | 1-9280 | 24h |
| debug | max 2h | - |
| extended | 1-64 | 24h |
| g1 | 1-2 | 2h |
| service | 1-1 | 24h |

Eliminate queues with maximum walltime below 7500 seconds or node range excluding 1 node:

* debug: max walltime is below 7500 seconds
* g1: max walltime is below 7500 seconds
* service: max walltime is below 7500 seconds

Queue table after elimination:

| Queue | Node Range | Max Walltime |
| --- | --- | --- |
| batch | 1-9280 | 24h |
| extended | 1-64 | 24h |

(c) Choose from what survives, and state the verdict against each of the three limits separately:

| Queue | Node Minimum | Node Maximum | Max Walltime | Verdict |
| --- | --- | --- | --- | --- |
| batch | PASS | PASS | PASS |
| extended | PASS | FAIL | PASS |

We cannot use the extended queue because its node maximum is 64, which is below our required node count of 1.

(d) Choose a queue that meets all the limits:

We can use the batch queue, which meets all the limits.

(e) Determine ranks-per-node and GPUs-per-rank:

Given the application defaults:
- ranks-per-node = 8 (one per GCD)
- GPUs-per-rank = 1 (since each GCD device is a GPU)

(f) Restate nodes, ranks per node, total ranks, GPUs per node, walltime and queue:

* Nodes = 1
* Ranks per node = 8
* Total ranks = nodes * ranks per node = 1 * 8 = 8
* GPUs per node = 8 (since each node has 8 GCD devices)
* Walltime = 7500 seconds
* Queue = batch

The final specification is:

- Nodes: 1
- Ranks per node: 8
- Total ranks: 8
- GPUs per node: 8
- Walltime: 7500 seconds
- Queue: batch
````
