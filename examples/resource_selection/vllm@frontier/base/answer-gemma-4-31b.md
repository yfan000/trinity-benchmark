# gemma-4-31b — vllm@frontier, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
### Reasoning

**1. Sizing the Work and Walltime**
*   **Throughput Calculation:** The problem specifies a Tensor Parallel (TP) size of 4. Validated throughput was measured at TP=8 on 1 node. Since TP=4 is smaller and the total prompt count is very low (50 prompts $\times$ 50 tokens = 2,500 total tokens), the compute time will be negligible (likely seconds).
*   **Overhead:** The prior measurement indicates server startup takes ~165 seconds.
*   **Total Estimated Time:** $\text{Startup} (165\text{s}) + \text{Inference} (\approx 30\text{s}) + \text{Buffer/Cleanup} (\approx 60\text{s}) \approx 255\text{s}$.
*   **Requested Walltime:** To be safe, I will request **10 minutes (00:10:00)**. This provides a significant margin over the estimated 4.25 minutes.

**2. Queue Elimination**
*   **batch:** Node range (1-9280) and walltime (24h) are sufficient. $\rightarrow$ **KEEP**
*   **debug:** Max walltime (2h) is sufficient. Node range is not specified but generally fits small jobs. $\rightarrow$ **KEEP**
*   **extended:** Node range (1-64) and walltime (24h) are sufficient. $\rightarrow$ **KEEP**
*   **g1:** Node range (1-2) and walltime (2h) are sufficient. $\rightarrow$ **KEEP**
*   **service:** Node range (1-1) and walltime (24h) are sufficient. $\rightarrow$ **KEEP**

**3. Queue Selection and Validation**
The workload is minimal (50 prompts) and requires a TP size of 4. Since the system defaults specify 1 node for these types of runs and the `g1` queue is designated for small/fast turnaround tests, it is the most appropriate target.

**Validation for `g1` queue (Requested: 1 node, 10 mins):**
| Limit | Requested | Queue Limit | Result |
| :--- | :--- | :--- | :--- |
| Node Minimum | 1 | 1 | **PASS** |
| Node Maximum | 1 | 2 | **PASS** |
| Max Walltime | 10 min | 2 hours | **PASS** |

**4. Scaling and Application Defaults**
*   **Scaling:** The user specified `tensor parallel size 4`. Since one Frontier node contains 8 GCDs (MI250X), the model fits comfortably on a single node. There is no need to scale across multiple nodes, which would introduce unnecessary network latency for such a small prompt set.
*   **Ranks:** Following build defaults, `ranks-per-node = 8` (one per GCD). With 1 node, total ranks = 8.

---

### Resource Specification

*   **Nodes:** 1
*   **Ranks per node:** 8
*   **Total ranks:** 8 (1 node $\times$ 8 ranks per node)
*   **GPUs per node:** 8
*   **Walltime:** 00:10:00
*   **Queue:** g1
````
