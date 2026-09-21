# gemma-4-31b — qmcpack@aurora, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
### Reasoning

**1. Sizing the Work and Walltime**
*   **Workload:** 4,096 walkers $\times$ 200 DMC blocks = 819,200 total walker-blocks.
*   **System Scale:** Silicon (64 atoms) is a relatively small system for Aurora. In DMC, the primary computational cost is the evaluation of the Slater determinant and Jastrow factor.
*   **Throughput Assumption:** For a 64-atom system on Intel GPU Max series, I assume a conservative throughput of approximately 2 blocks per GPU per hour (accounting for the 4,096 walkers and timestep).
*   **Calculation:** 
    *   Total GPU-hours needed $\approx$ 200 blocks / (2 blocks/hour) = 100 GPU-hours (for one walker).
    *   However, since walkers are distributed across ranks, the "blocks" are the primary unit of time. 200 blocks at $\sim$30 seconds per block per GPU $\approx$ 1.6 hours.
*   **Margin:** I will add a 100% safety margin to account for I/O, initialization, and potential fluctuations in block time.
*   **Estimated Walltime:** 3.2 hours.

**2. Queue Elimination**
*   `debug`: Max walltime 1h < 3.2h (**FAIL**)
*   `debug-scaling`: Max walltime 1h < 3.2h (**FAIL**)
*   `prod`: Min nodes 256. To use this, I would need to request 256 nodes, which is overkill for 64 atoms and 200 blocks, leading to extreme inefficiency. (**FAIL** - node minimum)
*   `visualization`: Max nodes 32, Max walltime 8h. (Candidate)
*   `capacity`: Max nodes 16, Max walltime 168h. (Candidate)

**3. Queue Selection and Verification**
I will target the `capacity` queue. To balance throughput and efficiency for a 64-atom system, I will request 4 nodes.

| Limit | Requested Value | Queue Limit | Result |
| :--- | :--- | :--- | :--- |
| Node Minimum | 4 nodes | 1 node | **PASS** |
| Node Maximum | 4 nodes | 16 nodes | **PASS** |
| Max Walltime | 3.2 hours | 168 hours | **PASS** |

**4. Application Scaling and Build Defaults**
*   **Ranks per node:** The build default is 6.
*   **GPUs per rank:** With 6 GPUs per node and 6 ranks per node, the mapping is 1 GPU per rank.
*   **Scaling:** QMCPACK scales linearly with the number of walkers. 4,096 walkers across 24 total ranks (4 nodes $\times$ 6 ranks) provides $\sim$170 walkers per rank, which is a healthy load for efficient GPU utilization.

### Resource Specification

*   **Nodes:** 4
*   **Ranks per node:** 6
*   **Total ranks:** 24 (4 nodes $\times$ 6 ranks/node)
*   **GPUs per node:** 6
*   **Walltime:** 3.2 hours
*   **Queue:** capacity
````
