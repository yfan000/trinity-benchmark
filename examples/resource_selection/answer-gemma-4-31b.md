# Answer — gemma-4-31b

lammps@polaris, Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2).

````
### Reasoning

**1. Workload Sizing and Walltime Estimation**
*   **System Size:** 500,000 atoms.
*   **Complexity:** 100,000 timesteps with a standard LJ cutoff.
*   **Scaling Guidance:** The provided notes suggest scaling nodes for systems $>1\text{M}$ atoms. Since this system is $0.5\text{M}$ atoms, a small number of nodes is sufficient to maintain high efficiency.
*   **Assumption:** Based on typical LAMMPS Kokkos performance on A100s for LJ systems, I assume a throughput of approximately 500 to 1,000 timesteps per second per GPU. For 100,000 steps, the raw compute time is estimated at 100–200 seconds. Even with overhead and conservative estimates, the runtime is very short.
*   **Margin:** I will add a generous margin for I/O and initialization, requesting **1 hour** of walltime.

**2. Queue Selection and Elimination**
*   **Proposed Node Count:** Since the system is $<1\text{M}$ atoms and the runtime is short, I will start with **2 nodes** to ensure sufficient memory and parallel efficiency.
*   **Evaluation:**
    *   `debug`: 1-2 nodes, max 1h $\rightarrow$ **Possible**.
    *   `debug-scaling`: 1-10 nodes, max 1h $\rightarrow$ **Possible**.
    *   `prod`: 10-496 nodes, max 24h $\rightarrow$ **Eliminated** (Node count 2 is below minimum 10).
    *   `demand`: 1-56 nodes, max 1h $\rightarrow$ **Possible**.
    *   `preemptable`: 1-10 nodes, max 72h $\rightarrow$ **Possible**.
    *   `capacity`: 1-4 nodes, max 168h $\rightarrow$ **Possible**.

**3. Final Queue Verdict**
I choose the `debug` queue for a first-run workload to ensure fast turnaround.

| Limit | Requested Value | Queue Limit | Result |
| :--- | :--- | :--- | :--- |
| Node Minimum | 2 nodes | 1 node | **PASS** |
| Node Maximum | 2 nodes | 2 nodes | **PASS** |
| Max Walltime | 1 hour | 1 hour | **PASS** |

### Resource Specification

*   **Nodes:** 2
*   **Ranks per node:** 4 (Per build defaults)
*   **GPUs per node:** 4 (Per system spec: 4 x A100 per node)
*   **Total ranks:** 8 (2 nodes $\times$ 4 ranks/node)
*   **Walltime:** 1 hour
*   **Queue:** debug
````
