# llama-3.1-8b — pytorch@sophia, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Step 1: Size the work and derive the walltime needed**

To determine the walltime, we need to estimate the training time for the ResNet-50 model on the 100,000-image subset. Assuming a batch size of 256 per GPU, we can estimate the total batch size as:

Total batch size = 100,000 images / 256 images per batch = 390.625 batches

With 10 epochs, the total number of batches is:

Total batches = 10 epochs × 390.625 batches per epoch = 3906.25 batches

The training time for ResNet-50 on a single A100 GPU is approximately 30-40 minutes per epoch in mixed precision. Assuming a linear scaling with the number of epochs, we can estimate the total training time as:

Total training time = 35 minutes per epoch × 10 epochs = 350 minutes

However, since we have multiple GPUs, we can distribute the batch size across the GPUs. Assuming 8 GPUs per node, the total batch size per node is:

Total batch size per node = 256 images per batch × 8 GPUs per node = 2048 images per batch

The total number of nodes required to process the entire batch size is:

Total nodes = 390.625 batches / 2048 images per batch ≈ 0.19 nodes

Since we cannot have a fraction of a node, we round up to the nearest whole number to ensure we have enough nodes to process the entire batch size. Therefore, we need at least 1 node to process the entire batch size.

However, to account for potential overheads and inefficiencies in the training process, we add a 20% margin to the estimated training time:

Walltime = 350 minutes × 1.2 = 420 minutes

**Step 2: Eliminate queues with insufficient walltime or node range**

We will go through the queue table and eliminate every queue whose maximum walltime is below 420 minutes or whose node range excludes our node count.

| Queue | Node Range | Max Walltime |
| --- | --- | --- |
| by-gpu | 1-1 nodes | 24 hours |
| by-node | 1-8 nodes | 24 hours |
| bigmem | 1-1 nodes | 24 hours |

Eliminating queues with insufficient walltime:

* bigmem: max walltime is 24 hours, which is less than 420 minutes, so it is eliminated.

Eliminating queues with insufficient node range:

* by-gpu: only allows 1 node, which is less than our required 1 node, so it is eliminated.

The remaining queues are:

| Queue | Node Range | Max Walltime |
| --- | --- | --- |
| by-node | 1-8 nodes | 24 hours |

**Step 3: Choose a queue and verify the limits**

We choose the by-node queue, which has a maximum walltime of 24 hours and allows up to 8 nodes.

| Queue | Node Count | Limit | Verdict |
| --- | --- | --- | --- |
| by-node | 1 node | 1-8 nodes | PASS |
| by-node | 1 node | 24 hours | PASS |
| by-node | 1 node | maximum walltime | PASS |

**Step 4: Determine ranks-per-node and GPUs-per-rank**

From the application defaults, we know that:

* ranks-per-node = 8 (since we have 8 GPUs per node)
* GPUs-per-rank = 1 (since each rank corresponds to a single GPU)

**Step 5: Determine total ranks and walltime**

We have determined that we need 1 node, and each node has 8 ranks. Therefore, the total number of ranks is:

Total ranks = 1 node × 8 ranks per node = 8 ranks

We have also determined that the walltime is 420 minutes.

**Resource specification**

* nodes: 1
* ranks per node: 8
* total ranks: 8
* GPUs per node: 8
* walltime: 420 minutes
* queue: by-node

Total ranks = nodes × ranks per node: 1 node × 8 ranks per node = 8 ranks
````
