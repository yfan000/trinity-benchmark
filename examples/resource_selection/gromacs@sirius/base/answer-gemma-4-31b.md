# gemma-4-31b — gromacs@sirius, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
### Reasoning

**1. Work Sizing and Walltime Estimation**
*   **Workload:** 5 ns production run, ~34,000 atoms.
*   **Assumption:** For a system of this size (small/medium) on A100 GPUs using GROMACS with PME offload, a conservative throughput estimate is ~200 ns/day. 
*   **Calculation:** $5\text{ ns} / 200\text{ ns/day} = 0.025\text{ days} \approx 36\text{ minutes}$.
*   **Margin:** Since no prior measurement exists, I will add a significant safety margin (5x) to account for potential I/O overhead, checkpoint loading, and conservative throughput estimates.
*   **Estimated Walltime Needed:** 3 hours.

**2. Queue Selection**
*   **Available Queues:** `workq` (1–4 nodes, max 24h).
*   **Evaluation:**
    *   `workq`: Max walltime (24h) $\ge$ 3h; Node range (1–4) includes my choice of 1 node.
*   **Verdict:**
    | Limit | Requested Value | Queue Limit | Result |
    | :--- | :--- | :--- | :--- |
    | Node Minimum | 1 | 1 | **PASS** |
    | Node Maximum | 1 | 4 | **PASS** |
    | Max Walltime | 3h | 24h | **PASS** |

**3. Node Count and Scaling**
*   **Scaling Guidance:** The guidance suggests one MPI rank per GPU. 
*   **System Capacity:** Each node has 4 GPUs. To follow the "one rank per GPU" recommendation for GPU offloading, 4 ranks per node is optimal for hardware utilization.
*   **Node Choice:** Because the system size is very small (~34k atoms), scaling across multiple nodes often introduces MPI communication overhead that outweighs the computational gain (strong scaling limit). A single node with 4 GPUs is sufficient to complete this task well within the walltime limit.

**4. Ranks and GPU Mapping**
*   **Ranks per Node:** Following the build default and scaling notes for GPU offload, I will use 4 ranks per node (one per A100 GPU).
*   **GPU Mapping:** As per the build defaults, `-gpu_id 0123` will be used to map the 4 MPI ranks to the 4 available GPUs on the node.

### Resource Specification

*   **Nodes:** 1
*   **Ranks per node:** 4
*   **Total ranks:** 4 (1 node $\times$ 4 ranks per node)
*   **GPUs per node:** 4
*   **Walltime:** 3 hours
*   **Queue:** workq
````
