# llama-3.1-8b — nekrs@polaris, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Resource Specification:**

* Nodes: 32
* Ranks per node: 4 (build default)
* Total ranks: 128 (32 nodes * 4 ranks per node)
* GPUs per node: 4 (A100 GPUs per node on Polaris)
* Walltime: 24 hours
* Queue: prod

**Reasoning:**

**(a) Choosing a Legal Queue:**

1. **Size the work and derive the walltime you actually need:**
   We have 20,000 timesteps with statistics collected over the final 10,000. Assuming each timestep takes approximately the same amount of time as the prior 1,000 timesteps (8 minutes), we can estimate the walltime needed for the entire run. 20,000 timesteps / 10,000 timesteps * 8 minutes = 16 minutes per 10,000 timesteps. However, this is not a direct scaling of the walltime, as the actual computation time may be different. We will assume a similar scaling factor, but add a margin for uncertainty. Let's assume the walltime for 20,000 timesteps is 5 times the walltime for 1,000 timesteps. 5 * 8 minutes = 40 minutes. However, this is still a rough estimate, and we will add a 50% margin to account for potential variations in computation time. 40 minutes * 1.5 = 60 minutes. Converting this to hours, we get 1 hour.

   However, this is still not the walltime we need. We need to account for the fact that the problem is more complex than the prior run. The number of spectral elements has increased from 32,000 to 32,000, and the polynomial order is 7. This is a significant increase in complexity, and we will add a 2x margin to account for this. 1 hour * 2 = 2 hours. However, we still need to account for the fact that the run is longer than the prior run. We will add another 50% margin to account for this. 2 hours * 1.5 = 3 hours.

   Therefore, the walltime we need is 3 hours.

2. **Eliminate queues with maximum walltime below the required walltime:**
   We will eliminate the following queues:
   - queue debug: max 1h
   - queue debug-scaling: max 1h
   - queue demand: max 1h
   - queue preemptable: max 72h (this queue has a maximum walltime below the required walltime, but we will consider it later)

3. **Eliminate queues with node range excluding the required node count:**
   We will eliminate the following queues:
   - queue debug: 1-2 nodes
   - queue debug-scaling: 1-10 nodes
   - queue demand: 1-56 nodes
   - queue capacity: 1-4 nodes

   The only queue that remains is:
   - queue prod: 10-496 nodes

4. **Choose from the remaining queues:**
   We will choose the queue prod, as it has the required node range and maximum walltime.

   The verdict against each of the three limits is:
   - Node minimum: 10 (queue prod) vs 32 (required) FAIL
   - Node maximum: 496 (queue prod) vs 32 (required) PASS
   - Maximum walltime: 24h (queue prod) vs 3h (required) FAIL

   We need to adjust the node count to meet the node minimum requirement.

**(b) Ranks per node and GPUs per rank:**
   We will use the build defaults:
   - Ranks per node: 4
   - GPUs per rank: 1 (as specified in the software selected)

**(c) Scaling guidance:**
   We will follow the scaling guidance supplied with the application, which is to scale by increasing node count.

**(d) Scaling guidance and application defaults:**
   The scaling guidance supplied with the application does not apply to this run, as we are scaling by increasing node count, not by increasing ranks per node.

**(e) Restate the resource specification:**
   We will restate the resource specification as follows:
   * Nodes: 16
   * Ranks per node: 4
   * Total ranks: 64
   * GPUs per node: 4
   * Walltime: 3 hours
   * Queue: prod

   However, this is not the correct answer. We need to meet the node minimum requirement of 10 nodes. We will adjust the node count to 10 nodes.

   * Nodes: 10
   * Ranks per node: 4
   * Total ranks: 40
   * GPUs per node: 4
   * Walltime: 3 hours
   * Queue: prod
````
