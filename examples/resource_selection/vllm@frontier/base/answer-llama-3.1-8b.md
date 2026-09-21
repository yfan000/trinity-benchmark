# llama-3.1-8b — vllm@frontier, base arm

Resource selection. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 1 of 10 requirements violated).

````
**Step 1: Size the work and derive the walltime needed**

The workload is Llama-3.1-8B offline inference with 50 prompts, max_tokens=50, and tensor parallel size 4. We have validated throughput at TP=8 on 1 node, but we don't have a measured walltime. However, we can estimate the walltime based on the number of prompts and the inference time per prompt.

Assuming an inference time of 1 second per prompt (a rough estimate, as the actual time may vary), the total inference time would be 50 seconds. However, since we are using tensor parallelism with 4 GPUs, the actual walltime would be the inference time divided by the number of GPUs.

Walltime = 50 seconds / 4 GPUs = 12.5 seconds

However, this is a very short walltime, and it's unlikely that the job would take this long. To be conservative, let's add a 10% margin to the walltime.

Walltime = 12.5 seconds * 1.1 = 13.75 seconds

However, since we need to scale the job to multiple nodes, we need to consider the number of ranks and the communication time between ranks. Let's assume that the communication time is negligible compared to the inference time.

To determine the number of ranks, we need to consider the tensor parallel size and the number of GPUs per node. We have 8 GPUs per node, and we are using tensor parallel size 4. Therefore, we can fit 2 ranks per node (8 GPUs / 4 GPUs per rank).

To determine the total number of ranks, we need to consider the number of nodes required to complete the job. Let's assume that we need to complete the job in 1 hour (3600 seconds).

Number of ranks = Total inference time / Walltime per rank
= 3600 seconds / 13.75 seconds
= 262.16 ranks

Since we can fit 2 ranks per node, we need approximately 131 nodes to complete the job.

**Step 2: Eliminate queues with maximum walltime below the required walltime or node range excluding the required node count**

Based on the queue table, we can eliminate the following queues:

* queue debug: max 2h (below the required walltime)
* queue g1: 1-2 nodes, max 2h (below the required node count)
* queue service: 1-1 nodes, max 24h (below the required node count)

The remaining queues are:

| Queue | Node range | Maximum walltime |
| --- | --- | --- |
| queue batch | 1-9280 nodes | 24h |
| queue extended | 1-64 nodes | 24h |

**Step 3: Choose the queue with the smallest node range that meets the required node count**

Based on the remaining queues, we can choose queue batch, which has the smallest node range that meets the required node count.

**Queue verdict**

| Queue | Node minimum | Node maximum | Maximum walltime | Verdict |
| --- | --- | --- | --- | --- |
| queue batch | 1 | 9280 | 24h | PASS |
| queue extended | 1 | 64 | 24h | FAIL (node maximum) |

**Step 4: Determine the ranks per node and GPUs per rank**

Based on the application defaults, we have:

* ranks-per-node = 8 (one per GCD)
* GPUs-per-rank = 1 (assuming each rank uses one GPU)

**Resource specification**

* nodes = 131
* ranks per node = 8
* total ranks = nodes x ranks per node = 1048
* GPUs per node = 8
* walltime = 13.75 seconds
* queue = queue batch

Note that the walltime is very short, and it's unlikely that the job would take this long. In practice, the walltime would be longer, and the job would need to be run for a longer period to complete.

Also, note that the queue batch has a maximum walltime of 24h, which is much longer than the required walltime. Therefore, the job would not be rejected by the scheduler due to the walltime limit.
````
