# gemma-4-31b — qe@aurora, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
### Reasoning

**1. Workload Sizing and Walltime Estimation**
*   **System Size:** 64 atoms, 60 Ry cutoff, $4\times4\times4$ k-grid. This is a small to medium-sized DFT calculation.
*   **Computational Effort:** For a 64-atom system using PBE and ultrasoft pseudopotentials on a modern HPC architecture like Aurora, an SCF convergence typically takes a few minutes to an hour depending on the convergence rate of the charge density.
*   **Assumption:** I assume the calculation will take approximately 30 minutes of compute time. I will add a 100% safety margin to account for I/O overhead on the Lustre filesystem and potential SCF convergence struggles.
*   **Derived Walltime:** 1 hour.

**2. Queue Elimination**
*   **debug:** Max walltime 1h. (Fits, but limited to 2 nodes; may be too small for production throughput).
*   **debug-scaling:** Max walltime 1h. (Fits).
*   **prod:** Node minimum 256. (Excluded: The system size (64 atoms) is too small to scale efficiently to 256 nodes; communication overhead would dominate, making it inefficient/illegal for this workload).
*   **capacity:** Max walltime 168h. (Fits).
*   **visualization:** Max walltime 8h. (Fits).

**3. Queue Selection and Validation**
Given this is a "production DFT campaign" but the workload is small, the `capacity` queue is the most appropriate for a stable production run that avoids the strict 1-hour timeout of the debug queues, while allowing a node count that matches the physics of the problem. I will target 4 nodes to ensure efficient parallelization of the k-points and plane-wave coefficients without hitting the scaling wall.

| Limit | Requested Value | Queue Limit | Result |
| :--- | :--- | :--- | :--- |
| Node Minimum | 4 nodes | 1 node | **PASS** |
| Node Maximum | 4 nodes | 16 nodes | **PASS** |
| Max Walltime | 1 hour | 168 hours | **PASS** |

**4. Ranks and GPU Configuration**
*   **Ranks per node:** The build default is 104. I will use 104 ranks per node to utilize all available CPU cores.
*   **GPUs per node:** The build notes specify a "CPU-only MPI build" because the `pw_gpu` version requires NVIDIA, and Aurora uses Intel GPUs. Therefore, GPUs will not be utilized for this specific build.
*   **Scaling:** 104 CPU cores per node are used. With 4 nodes, the total rank count is 416. For a $4\times4\times4$ k-grid (64 k-points), this provides 6.5 ranks per k-point, which is a reasonable distribution for a system of this size.

### Resource Specification

*   **Nodes:** 4
*   **Ranks per node:** 104
*   **Total ranks:** 416 (4 nodes $\times$ 104 ranks/node)
*   **GPUs per node:** 0
*   **Walltime:** 1 hour
*   **Queue:** capacity
````
