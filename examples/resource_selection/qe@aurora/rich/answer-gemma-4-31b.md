# gemma-4-31b — qe@aurora, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
### Reasoning

**1. Workload Sizing and Walltime Estimation**
*   **System Size:** 64 atoms (2x2x2 supercell of 3C-SiC) is a small to medium-sized DFT calculation.
*   **Complexity:** A plane-wave cutoff of 60 Ry and a 4x4x4 k-grid is standard for production PBE calculations.
*   **Estimation:** Given the small atom count and the high performance of Aurora nodes (104 cores), an SCF calculation for this system typically completes in minutes to a few hours on a small number of nodes.
*   **Assumption:** I assume a baseline execution time of 30 minutes for the SCF convergence. I will add a 2x safety margin to account for convergence overhead or I/O, resulting in a requested walltime of **1 hour**.

**2. Queue Elimination**
*   **Debug:** Node limit (1-2). Potential fit, but the prompt specifies a "production campaign."
*   **Debug-scaling:** Node limit (2-256). Potential fit.
*   **Prod:** Node minimum (256). **ELIMINATED**. The system size (64 atoms) is far too small to scale to 256 nodes; communication overhead would dominate, and the request would be inefficient.
*   **Capacity:** Node limit (1-16). Potential fit.
*   **Visualization:** Node limit (1-32). Potential fit, but intended for visualization tasks.

**3. Queue Selection and Validation**
To balance the "production" requirement with the small size of the workload, the **capacity** queue is the most appropriate choice as it allows for production-length stability without the massive node minimum of the `prod` queue. I will request **4 nodes** to ensure fast turnaround while remaining well within scaling efficiency limits for 64 atoms.

| Limit | Requested Value | Queue Limit | Result |
| :--- | :--- | :--- | :--- |
| Node Minimum | 4 nodes | 1 node | **PASS** |
| Node Maximum | 4 nodes | 16 nodes | **PASS** |
| Max Walltime | 1 hour | 168 hours | **PASS** |

**4. Application Defaults and Scaling**
*   **Ranks per node:** The build default is 104. Since this is a CPU-only MPI build using Intel MKL, I will utilize all 104 cores per node.
*   **GPUs per node:** The provided notes state the build is CPU-only and GPU offload via `pw_gpu` requires NVIDIA (not present on Aurora's Intel GPU architecture). Therefore, GPUs per node is 0.
*   **Scaling:** For a 64-atom system, 4 nodes (416 total ranks) provides a healthy balance. Using the `prod` queue's minimum of 256 nodes would lead to severe performance degradation due to the small local problem size per rank.

### Resource Specification

*   **Nodes:** 4
*   **Ranks per node:** 104
*   **Total ranks:** 416 (4 nodes $\times$ 104 ranks/node)
*   **GPUs per node:** 0
*   **Walltime:** 1 hour
*   **Queue:** capacity
````
