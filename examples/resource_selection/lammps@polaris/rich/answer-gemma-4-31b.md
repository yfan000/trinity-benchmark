# gemma-4-31b — lammps@polaris, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
### Reasoning

**1. Workload Sizing and Walltime Estimation**
*   **Problem Size:** 500,000 atoms is a medium-sized system. According to the scaling notes, node scaling is typically reserved for systems >1M atoms. Therefore, a small number of nodes will suffice to maintain high efficiency.
*   **Computational Load:** 100,000 timesteps for a Lennard-Jones system on A100 GPUs is computationally efficient. 
*   **Assumption:** Assuming a conservative throughput of 5,000 timesteps per second (a typical baseline for LJ on A100s), the core compute time is $\approx 20$ seconds. However, accounting for initialization, I/O, and the fact that this is a first run (no prior data), I assume a total runtime of 15 minutes.
*   **Margin:** I will add a 100% safety margin to account for overhead and potential scaling inefficiencies, resulting in a requested walltime of **30 minutes (0.5 hours)**.

**2. Queue Elimination**
I will evaluate the queues based on a request for 2 nodes and 0.5 hours walltime:
*   `debug`: (1-2 nodes, 1h) $\rightarrow$ **Keep**
*   `debug-scaling`: (1-10 nodes, 1h) $\rightarrow$ **Keep**
*   `prod`: (10-496 nodes, 24h) $\rightarrow$ **Eliminate** (Node count 2 is below the minimum of 10)
*   `demand`: (1-56 nodes, 1h) $\rightarrow$ **Keep**
*   `preemptable`: (1-10 nodes, 72h) $\rightarrow$ **Keep**
*   `capacity`: (1-4 nodes, 168h) $\rightarrow$ **Keep**

**3. Queue Selection and Verification**
Since this is the first run of this workload on the system, the `debug` queue is the most appropriate for validation.

| Limit | Requested Value | Queue Limit | Status |
| :--- | :--- | :--- | :--- |
| Node Minimum | 2 | 1 | **PASS** |
| Node Maximum | 2 | 2 | **PASS** |
| Max Walltime | 0.5h | 1h | **PASS** |

**4. Scaling and Build Defaults**
*   **Scaling Guidance:** The note suggests scaling nodes for systems >1M atoms. Since this system is 0.5M atoms, 2 nodes are sufficient to provide ample GPU memory and compute power without incurring excessive communication overhead.
*   **Build Defaults:** 
    *   Ranks per node: 4
    *   GPUs per node: 4 (1 GPU per rank)

### Resource Specification

*   **Nodes:** 2
*   **Ranks per node:** 4
*   **Total ranks:** 8 (2 nodes $\times$ 4 ranks/node)
*   **GPUs per node:** 4
*   **Walltime:** 0.5 hours
*   **Queue:** debug
````
