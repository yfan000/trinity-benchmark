# gemma-4-31b — vllm@frontier, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
### Reasoning

**1. Size the work and derive walltime**
*   **Startup Time:** The prompt specifies server startup takes ~165 seconds.
*   **Inference Time:** The workload is very small (50 prompts, 50 tokens each = 2,500 total tokens). Since throughput was validated at TP=8 on 1 node, and this run uses TP=4, the inference phase will be extremely fast (likely under 1 minute).
*   **Total Estimated Time:** $\approx 3$ minutes.
*   **Requested Walltime:** I will request **30 minutes (0.5 hours)**. This provides a significant margin (roughly 10x) over the estimated 3 minutes to account for environment loading and potential I/O delays without requesting excessive resources.

**2. Queue Elimination**
*   **Queue `batch`:** Node range 1-9280, Max 24h. (Possible)
*   **Queue `debug`:** Max 2h. (Possible)
*   **Queue `extended`:** Node range 1-64, Max 24h. (Possible)
*   **Queue `g1`:** Node range 1-2, Max 2h. (Possible)
*   **Queue `service`:** Node range 1-1, Max 24h. (Possible)
*   *Note: No queues are eliminated based on the walltime (30m) or the minimal node count (1), but `g1` is the preferred target for small, short-duration tests according to system sizing defaults.*

**3. Queue Verdict (Target: `g1`)**
| Limit | Requested Value | Queue Limit | Status |
| :--- | :--- | :--- | :--- |
| Node Minimum | 1 node | 1 node | **PASS** |
| Node Maximum | 1 node | 2 nodes | **PASS** |
| Max Walltime | 0.5 hours | 2 hours | **PASS** |

**Scaling and Ranks**
*   **Scaling:** The workload specifies a Tensor Parallel (TP) size of 4. One node on Frontier contains 8 GCDs. Since TP=4 fits entirely within a single node, there is no need to scale across multiple nodes. Using a single node minimizes communication overhead.
*   **Ranks:** Per build defaults, ranks-per-node is 8 (one per GCD). To satisfy TP=4, the application will utilize 4 of these ranks for the model and 4 as available/idle or for auxiliary tasks, but the Slurm allocation must match the build default of 8 ranks per node to ensure correct GPU mapping.

### Resource Specification

*   **Nodes:** 1
*   **Ranks per node:** 8
*   **Total ranks:** 8 (1 node $\times$ 8 ranks/node)
*   **GPUs per node:** 8
*   **Walltime:** 00:30:00
*   **Queue:** g1
````
