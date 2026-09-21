# gemma-4-31b — nekrs@polaris, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
### Reasoning

**1. Sizing the work and deriving walltime**
*   **Baseline Performance:** A 1-node run of 1,000 timesteps took 8 minutes.
*   **Production Workload:** 20,000 total timesteps.
*   **Scaling Strategy:** Based on the provided scaling notes, NekRS scales by increasing the node count. To optimize throughput for a production run, I will scale to **16 nodes**. Assuming near-linear scaling for this problem size (32k elements), the time per 1,000 steps decreases by a factor of 16: $8 \text{ min} / 16 = 0.5 \text{ min}$ per 1,000 steps.
*   **Calculation:** $20 \text{ (units of 1,000 steps)} \times 0.5 \text{ min/unit} = 10 \text{ minutes}$.
*   **Margin:** I will add a 100% safety margin to account for I/O (statistics collection over 10k steps), MPI overhead, and system jitter.
*   **Estimated Walltime:** 20 minutes (0.33 hours).

**2. Queue Elimination**
*   `debug`: Node limit (1-2) excludes 16 nodes.
*   `debug-scaling`: Node limit (1-10) excludes 16 nodes.
*   `demand`: Node limit (1-56) is OK, but usually reserved for short interactive tests.
*   `preemptable`: Node limit (1-10) excludes 16 nodes.
*   `capacity`: Node limit (1-4) excludes 16 nodes.
*   `prod`: Node range (10-496) and Walltime (24h) both accommodate the request.

**3. Final Queue Verification (`prod`)**

| Limit | Requested Value | Queue Limit | Result |
| :--- | :--- | :--- | :--- |
| Node Minimum | 16 | 10 | **PASS** |
| Node Maximum | 16 | 496 | **PASS** |
| Max Walltime | 20 min | 24h | **PASS** |

**4. Application Configuration**
*   **Ranks per node:** 4 (as per build default).
*   **GPUs per node:** 4 (matching ranks per node, 1 MPI rank per GPU).
*   **Scaling Guidance:** The scaling guidance to use 1 rank per GPU is honored by selecting 4 ranks per node on Polaris. Kernel precompilation is already done (cached), so no `--build-only` run is required.

---

### Resource Specification

*   **Nodes:** 16
*   **Ranks per node:** 4
*   **Total ranks:** 64 (16 nodes $\times$ 4 ranks/node)
*   **GPUs per node:** 4
*   **Walltime:** 20 minutes
*   **Queue:** prod
````
