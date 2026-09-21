# gemma-4-31b — nekrs@polaris, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
### Reasoning

**1. Sizing the Work and Walltime Derivation**
*   **Baseline Performance:** A 1-node run of 1,000 timesteps took 8 minutes.
*   **Production Workload:** 20,000 timesteps.
*   **Linear Scaling Calculation:** $\frac{20,000 \text{ steps}}{1,000 \text{ steps}} \times 8 \text{ minutes} = 160 \text{ minutes}$.
*   **Scaling Assumption:** I assume near-linear scaling for the time-to-solution as we increase node count, as the problem size (32k elements) is sufficient to distribute across a moderate number of nodes.
*   **Margin:** I add a 25% safety margin to account for I/O overhead during statistics collection (final 10,000 steps) and MPI communication overhead.
*   **Required Walltime:** $160 \text{ minutes} \times 1.25 = 200 \text{ minutes}$ (3 hours and 20 minutes).

**2. Queue Elimination**
*   **debug:** Max walltime 1h < 3h 20m (FAIL).
*   **debug-scaling:** Max walltime 1h < 3h 20m (FAIL).
*   **demand:** Max walltime 1h < 3h 20m (FAIL).
*   **preemptable:** Node range max 10. To keep the walltime low and ensure efficiency, I will target the `prod` queue, but for the sake of elimination, this is viable on time but limited in scale.
*   **capacity:** Node range max 4. This is too small for a production run of this scale.
*   **prod:** Node range 10-496, max walltime 24h. This fits the requirements.

**3. Final Queue Validation**
I will target **16 nodes** to ensure the workload is distributed efficiently across the GPUs while remaining well within the `prod` queue limits.

| Limit | Requested Value | Queue Limit | Status |
| :--- | :--- | :--- | :--- |
| Node Minimum | 16 | 10 | PASS |
| Node Maximum | 16 | 496 | PASS |
| Max Walltime | 3h 20m | 24h | PASS |

**4. Application Configuration**
*   **Ranks per Node:** Following the build defaults, 4 ranks per node are used.
*   **GPUs per Rank:** Following the build defaults, 1 GPU per rank is used (4 GPUs per node).
*   **Scaling Guidance:** The guidance specifies scaling by increasing node count while maintaining 4 ranks per node. This has been honored by selecting 16 nodes.

***

### Resource Specification

*   **Nodes:** 16
*   **Ranks per Node:** 4
*   **Total Ranks:** 64 (16 nodes $\times$ 4 ranks per node)
*   **GPUs per Node:** 4
*   **Walltime:** 3 hours 20 minutes
*   **Queue:** prod
````
