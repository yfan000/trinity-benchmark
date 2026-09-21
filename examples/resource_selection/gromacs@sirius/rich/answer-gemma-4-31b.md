# gemma-4-31b — gromacs@sirius, rich arm

Resource selection. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 2 of 10 requirements violated).

````
### Reasoning

**1. Sizing the Work and Walltime**
*   **Workload:** 5 ns production run, ~34,000 atoms.
*   **System Performance Assumption:** For a small system (~34k atoms) on A100 GPUs, GROMACS typically achieves high throughput (often >500 ns/day). Assuming a conservative 200 ns/day for this specific configuration:
    *   $5\text{ ns} / 200\text{ ns/day} = 0.025\text{ days} \approx 36\text{ minutes}$.
*   **Margin:** Because no prior measurement exists, I will add a significant margin to account for PME overhead and system initialization. I will request **2 hours** to ensure completion.

**2. Queue Selection**
*   **Queue Table Analysis:**
    *   `workq`: Max walltime 24h, node range 1–4.
*   **Elimination:** No other queues were provided in the target system description. `workq` is the only available option and it accommodates the requested 2 hours and the node count.

**3. Queue Limit Verification**
I have chosen 1 node to maximize efficiency for a small 34k atom system, as scaling across multiple nodes for such a small workload often introduces MPI communication overhead that exceeds the computation gain.

| Limit | Requested Value | Queue Limit | Result |
| :--- | :--- | :--- | :--- |
| Node Minimum | 1 | 1 | **PASS** |
| Node Maximum | 1 | 4 | **PASS** |
| Max Walltime | 2 hours | 24 hours | **PASS** |

**4. Scaling and Resource Mapping**
*   **Ranks per node:** Following the build defaults, 8 ranks per node are used.
*   **GPU Mapping:** Following scaling notes, one MPI rank per GPU is recommended. With 4 GPUs per node and a build default of 8 ranks per node, the ranks will be mapped to GPUs using `-gpu_id 01230123` (or similar) to ensure all GPUs are utilized.
*   **Threading:** With 64 CPU cores and 8 MPI ranks, `-ntomp 8` will be used to utilize all cores.
*   **Scaling Note:** Multi-node scaling is not pursued here because the system size (34k atoms) is too small to justify the latency of multi-node communication; a single node with 4 A100s is more than sufficient for 5 ns of simulation.

### Resource Specification

*   **Nodes:** 1
*   **Ranks per node:** 8
*   **Total ranks:** 8 (1 node × 8 ranks/node)
*   **GPUs per node:** 4
*   **Walltime:** 2 hours
*   **Queue:** workq
````
