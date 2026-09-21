# gemma-4-31b — hpl@crux, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
### Reasoning

**1. Resource Scaling & Node Selection**
*   **Process Grid:** The workload specifies a $2 \times 2$ process grid. This means the total number of ranks ($P \times Q$) must be $2 \times 2 = 4$.
*   **Ranks per Node:** The build default is 128 ranks per node. 
*   **Node Count:** To satisfy a total of 4 ranks using the build default of 128 ranks per node is impossible unless we use a fraction of a node. However, HPL performance on Crux is maximized by using all 128 cores per node. To adhere to the $2 \times 2$ grid requirement and the build default, we must allocate nodes to accommodate 4 ranks. Since 4 ranks is significantly less than the 128 cores available on a single node, **1 node** is sufficient to host all 4 ranks.

**2. Walltime Estimation**
*   **Workload Size:** $N=50,000$.
*   **Assumption:** Based on typical HPL performance for a problem size of $N=50,000$ on a single modern high-core-count node, the computation is expected to take approximately 15–30 minutes.
*   **Margin:** I am adding a 100% safety margin to account for system overhead and initialization, resulting in a requested walltime of **1 hour**.

**3. Queue Selection**
*   **Walltime needed:** 1 hour.
*   **Node count:** 1 node.

**Elimination Process:**
*   `debug`: Max 1h, Nodes 1-8. (Potentially viable).
*   `workq-route`: Max 24h, Nodes 1-184. (Potentially viable).
*   `preemptable`: Max 72h, Nodes 1-10. (Risky for deadline-sensitive runs due to preemption).
*   `demand`: Max 1h, Nodes 1-64. (Potentially viable).

To ensure the fastest turnaround (priority) for a short run, the `debug` queue is the standard choice for small-scale tests, but `demand` is also viable. However, given the "deadline-sensitive" nature and the 1-hour requirement, `debug` is the most appropriate for a 1-node request.

**Verification of `debug` queue:**

| Limit | Requested Value | Queue Limit | Result |
| :--- | :--- | :--- | :--- |
| Node Minimum | 1 | 1 | PASS |
| Node Maximum | 1 | 8 | PASS |
| Max Walltime | 1h | 1h | PASS |

### Resource Specification

*   **Nodes:** 1
*   **GPUs per node:** 0
*   **Ranks per node:** 128 (Build default)
*   **Total ranks:** 128 (1 node $\times$ 128 ranks/node) 
    *   *Note: While the HPL.dat specifies a 2x2 grid (4 ranks), the PBS resource allocation must follow the build default of 128 ranks per node to ensure the allocation is consistent with the system's software build.*
*   **Walltime:** 1h
*   **Queue:** debug
````
