# gemma-4-31b — nwchem@polaris, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
### Reasoning

**1. Sizing and Walltime**
*   **Workload:** A single water molecule is an extremely small system. A single-node run took 5 seconds.
*   **Scaling Goal:** To characterize scaling, I will test a range of node counts: 1, 2, 4, and 8 nodes.
*   **Estimated Walltime:** Since the problem is tiny, the computation time will remain negligible. However, MPI overhead and job startup will dominate. I assume a maximum of 5 seconds per run plus overhead. For a series of benchmark runs (or a single run at the highest node count), 15 minutes (0.25h) provides a generous margin (3x the original runtime plus overhead).

**2. Queue Selection**
*   **Target Node Count:** 8 nodes (to cover the range 1–8).
*   **Required Walltime:** 0.25 hours.
*   **Queue Elimination:**
    *   `debug`: Eliminated (Max nodes 2 < Requested 8).
    *   `prod`: Eliminated (Min nodes 10 > Requested 8).
    *   `capacity`: Eliminated (Max nodes 4 < Requested 8).
    *   `demand`: Potential candidate.
    *   `preemptable`: Potential candidate.
    *   `debug-scaling`: Potential candidate.

**3. Final Queue Verification (`debug-scaling`)**
I choose `debug-scaling` as it is specifically designed for this workload type.

| Limit | Requested Value | Queue Limit | Result |
| :--- | :--- | :--- | :--- |
| Node Minimum | 8 nodes | 1 node | PASS |
| Node Maximum | 8 nodes | 10 nodes | PASS |
| Max Walltime | 0.25 hours | 1 hour | PASS |

**4. Application Defaults & Scaling Guidance**
*   **Ranks per Node:** The build default is 4 MPI ranks per node.
*   **GPUs:** The build is CPU-only; therefore, 0 GPUs per node.
*   **Scaling Guidance:** The guidance suggests 4 MPI ranks per node and scaling nodes for larger systems. While a water molecule is not a "larger system," I am following the build default of 4 ranks per node to establish the baseline scaling behavior as requested.

---

### Resource Specification

*   **Nodes:** 8
*   **Ranks per node:** 4
*   **Total ranks:** 32 (8 nodes × 4 ranks per node)
*   **GPUs per node:** 0
*   **Walltime:** 0:15:00 (15 minutes)
*   **Queue:** debug-scaling
````
