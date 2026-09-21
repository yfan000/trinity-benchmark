# gemma-4-31b — nwchem@polaris, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
### Reasoning

**1. Workload Sizing and Walltime**
*   **Baseline:** A single-node run takes 5 seconds.
*   **Scaling Goal:** This is a benchmarking run to characterize scaling. Even with the overhead of increasing node counts and the inefficiency of running a tiny system (single water molecule) across multiple nodes, the compute time will remain negligible.
*   **Estimated Walltime:** Assuming a 10x overhead for communication and initialization on the largest node count, the actual compute time is still under a minute. I will request **10 minutes (00:10:00)** to provide a generous margin for job startup and file I/O.

**2. Queue Selection**
To characterize scaling, a range of node counts is required. I will target a run of **8 nodes** to test the transition from small-scale to medium-scale.

*   **Queue Elimination:**
    *   `debug`: Ruled out (Max 2 nodes; requested 8).
    *   `prod`: Ruled out (Min 10 nodes; requested 8).
    *   `capacity`: Ruled out (Max 4 nodes; requested 8).
    *   `preemptable`: Eligible, but `debug-scaling` is more appropriate for this specific goal.
    *   `demand`: Eligible.
    *   `debug-scaling`: Eligible.

*   **Verdict for `debug-scaling`:**

| Limit | Requested Value | Queue Limit | Result |
| :--- | :--- | :--- | :--- |
| Node Minimum | 8 nodes | 1 node | **PASS** |
| Node Maximum | 8 nodes | 10 nodes | **PASS** |
| Max Walltime | 10 minutes | 1 hour | **PASS** |

**3. Application Defaults and Scaling Guidance**
*   **Ranks per Node:** The build default is 4 ranks per node.
*   **GPUs per Node:** The build is CPU-only; therefore, 0 GPUs are requested.
*   **Scaling Guidance:** The guidance suggests scaling nodes for larger systems. While a single water molecule is not a "large system," this run is specifically a benchmark to characterize the scaling behavior of the software/interconnect on Polaris, so the guidance to use 4 MPI ranks per node is followed.

### Resource Specification
*   **Nodes:** 8
*   **Ranks per node:** 4
*   **Total ranks:** 32 (8 nodes $\times$ 4 ranks per node)
*   **GPUs per node:** 0
*   **Walltime:** 00:10:00
*   **Queue:** debug-scaling
````
