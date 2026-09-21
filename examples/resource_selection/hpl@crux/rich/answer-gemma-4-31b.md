# gemma-4-31b — hpl@crux, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
### Reasoning

**1. Workload and Node Calculation**
*   **Process Grid:** The workload specifies a $2 \times 2$ process grid.
*   **Total Ranks:** $P \times Q = 2 \times 2 = 4$ total ranks.
*   **Ranks per Node:** Based on the build defaults, we use 128 ranks per node to maximize performance.
*   **Nodes Required:** Since the total ranks needed (4) is significantly less than the capacity of a single node (128), only **1 node** is required to execute this specific process grid.
*   **Scaling Guidance:** The guidance suggests using all 128 cores per node for maximum performance. However, the specific workload request defines a $2 \times 2$ grid (4 ranks total). To adhere strictly to the requested problem configuration while utilizing the system, we allocate 1 node.

**2. Walltime Estimation**
*   **Assumption:** For $N=50,000$ on a modern high-performance node, the compute time is typically measured in minutes. 
*   **Margin:** I assume a runtime of 15 minutes and add a 100% safety margin to account for overhead and system jitter.
*   **Derived Walltime:** 30 minutes (0.5 hours).

**3. Queue Selection**
I evaluate the available queues based on 1 node and a 0.5h walltime:
*   `debug`: Max 8 nodes, Max 1h. (Compatible)
*   `workq-route`: Max 184 nodes, Max 24h. (Compatible)
*   `preemptable`: Max 10 nodes, Max 72h. (Compatible)
*   `demand`: Max 64 nodes, Max 1h. (Compatible)

**Turnaround Priority:** Since turnaround is the priority and the request is small (1 node, 0.5h), the `debug` queue is the most appropriate choice as it is designed for fast turnaround of small jobs.

**Queue Limit Verification (`debug`):**
| Limit | Requested Value | Queue Limit | Result |
| :--- | :--- | :--- | :--- |
| Node Minimum | 1 | 1 | PASS |
| Node Maximum | 1 | 8 | PASS |
| Max Walltime | 0.5h | 1h | PASS |

### Resource Specification
*   **Nodes:** 1
*   **GPUs per node:** 0
*   **Ranks per node:** 128
*   **Total ranks:** 128 (1 node $\times$ 128 ranks per node)
*   **Walltime:** 0.5 hours
*   **Queue:** debug
````
