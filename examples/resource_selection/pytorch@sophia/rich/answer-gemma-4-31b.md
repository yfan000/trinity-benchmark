# gemma-4-31b — pytorch@sophia, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
### Reasoning

**1. Sizing the Work and Walltime**
*   **Workload:** ResNet-50, 100,000 images, 10 epochs = 1,000,000 total images to process.
*   **Throughput Assumption:** On an A100, ResNet-50 mixed-precision throughput typically reaches ~2,000–3,000 images per second per GPU. I will assume a conservative 2,000 images/sec/GPU.
*   **Compute Calculation:**
    *   Using 4 nodes (32 GPUs total): $\text{Total Throughput} = 32 \times 2,000 = 64,000 \text{ images/sec}$.
    *   $\text{Time per epoch} = 100,000 / 64,000 \approx 1.56 \text{ seconds}$. 
    *   *Correction:* The above is an overestimation of throughput per GPU. A more realistic throughput for ResNet-50 on A100 (batch 256) is roughly 300–500 images/sec/GPU.
    *   **Revised Calculation (400 images/sec/GPU):**
        *   Total throughput (32 GPUs) = $32 \times 400 = 12,800 \text{ images/sec}$.
        *   Time for 1M images = $1,000,000 / 12,800 \approx 78 \text{ seconds}$.
*   **Walltime Estimation:** Even with significant overhead for MPI/NCCL initialization, data loading, and validation, the actual compute time is very low. However, to account for filesystem latency on `/eagle` and potential scaling inefficiencies, I will assume a total runtime of 1 hour.
*   **Margin:** I add a 2x safety margin to account for the lack of prior timing measurements on Sophia, bringing the requested walltime to **2 hours**.

**2. Queue Elimination**
*   **Queue `by-gpu`:** Node range is 1–1. My requirement is 4 nodes. $\rightarrow$ **ELIMINATED** (Node range).
*   **Queue `bigmem`:** Node range is 1–1. My requirement is 4 nodes. $\rightarrow$ **ELIMINATED** (Node range).
*   **Queue `by-node`:** Node range 1–8, Max walltime 24h. $\rightarrow$ **SURVIVES**.

**3. Final Queue Validation (`by-node`)**

| Limit | Requested Value | Queue Limit | Result |
| :--- | :--- | :--- | :--- |
| Node Minimum | 4 nodes | 1 node | **PASS** |
| Node Maximum | 4 nodes | 8 nodes | **PASS** |
| Max Walltime | 2 hours | 24 hours | **PASS** |

**4. Ranks and GPUs**
*   **Ranks per node:** Following the build defaults for distributed PyTorch on Sophia (where one rank is typically mapped to one GPU for NCCL efficiency), I use **8 ranks per node**.
*   **GPUs per rank:** 1.
*   **Scaling:** ResNet-50 scales well across small-to-medium node counts (1–8 nodes). 4 nodes is chosen to balance throughput and queue availability.

***

### Resource Specification

*   **Nodes:** 4
*   **Ranks per node:** 8
*   **Total ranks:** 32 (4 nodes $\times$ 8 ranks per node)
*   **GPUs per node:** 8
*   **Walltime:** 02:00:00
*   **Queue:** by-node
````
