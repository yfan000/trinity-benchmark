# gemma-4-31b — qmcpack@aurora, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
**Reasoning**

**1. Work Sizing and Walltime Estimation**
*   **Workload:** 64 atoms, 4096 walkers, 200 DMC blocks.
*   **Scaling Behavior:** DMC is embarrassingly parallel across walkers. With 4096 walkers, the job can be distributed across many ranks without losing efficiency.
*   **Assumption:** Since no prior timing is provided, I assume a typical throughput for a system of this size on Aurora GPU nodes. A conservative estimate for 200 blocks of DMC on a 64-atom system is roughly 2–4 hours of walltime when utilizing a moderate number of nodes.
*   **Margin:** I will request **4 hours** to provide a sufficient buffer for I/O, initialization, and potential fluctuations in node performance.

**2. Queue Elimination**
*   `debug`: Max walltime 1h < 4h (FAIL).
*   `debug-scaling`: Max walltime 1h < 4h (FAIL).
*   `prod`: Node minimum 256 nodes. To stay under 4 hours, 256 nodes (1536 GPUs) is excessive for 4096 walkers (only ~2.6 walkers per GPU), which would lead to poor efficiency. (FAIL).
*   `visualization`: While walltime fits, this queue is designated for visualization tasks, not production DMC. (FAIL).
*   `capacity`: Node range 1-16, Max walltime 168h. (PASS).

**3. Queue Validation (`capacity`)**
I will select **4 nodes** to ensure a healthy walker-to-GPU ratio (4096 walkers / 24 GPUs $\approx$ 170 walkers per GPU), which maintains high efficiency.

| Limit | Requested Value | Queue Limit | Result |
| :--- | :--- | :--- | :--- |
| Node Minimum | 4 | 1 | PASS |
| Node Maximum | 4 | 16 | PASS |
| Max Walltime | 4 hours | 168 hours | PASS |

**4. Application Configuration**
*   **Ranks per node:** Following build defaults, 6 ranks per node are used to map one MPI rank to each of the 6 Intel GPU tiles.
*   **GPUs per rank:** 1 (derived from 6 GPUs per node / 6 ranks per node).
*   **Scaling Guidance:** The use of 6 ranks per node honors the system architecture (6 tiles) and the SYCL build target.

***

**Final Specification**
*   **Nodes:** 4
*   **Ranks per node:** 6
*   **Total ranks:** 24 (4 nodes $\times$ 6 ranks per node)
*   **GPUs per node:** 6
*   **Walltime:** 4 hours
*   **Queue:** capacity
````
