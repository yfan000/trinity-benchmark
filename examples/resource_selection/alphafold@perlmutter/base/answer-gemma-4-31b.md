# gemma-4-31b — alphafold@perlmutter, base arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
### Reasoning

**(a) Queue Selection**

1.  **Size the work and derive walltime:**
    *   The target is a small protein (76 residues). AlphaFold's execution time is dominated by the MSA (Multiple Sequence Alignment) generation and the structure prediction/relaxation.
    *   For a small monomer (<100 residues), MSA search and prediction typically take between 1 to 3 hours.
    *   **Assumption:** I assume 2 hours for completion and add a 100% margin to account for database I/O overhead on `/pscratch` and relaxation steps.
    *   **Required Walltime:** 4 hours.

2.  **Eliminate ineligible queues:**
    *   `debug`: Max 30min (Limit: 4h > 30min) $\rightarrow$ **ELIMINATED**
    *   `express_amsc`: Max 6h (Passes walltime, but usually reserved for specific high-throughput workloads; however, strictly by limits, it stays).
    *   `interactive`: Max 4h (Limit: 4h $\le$ 4h) $\rightarrow$ **STAYS**
    *   `jupyter`: Max 6h (Passes walltime, but intended for notebooks) $\rightarrow$ **STAYS**
    *   `regular`, `premium`, `shared`, `preempt`, `overrun`: Max 48h $\rightarrow$ **STAY**

3.  **Final Queue Selection:**
    The workload is a "parameter sweep" of "many similar runs." The `regular` queue is the standard choice for production sweeps on Perlmutter to avoid the constraints of interactive or short-term queues.

    **Verification for `regular` queue (Node count: 1):**
    | Limit | Requested | Limit | Result |
    | :--- | :--- | :--- | :--- |
    | Node Minimum | 1 | $\ge 1$ | **PASS** |
    | Node Maximum | 1 | 3072 | **PASS** |
    | Max Walltime | 4h | 48h | **PASS** |

**(b) Ranks and GPUs**
Following the Build Defaults:
*   Structure prediction requires a CUDA GPU.
*   Single GPU per run is typical.
*   Ranks per node: 1 (as it is a single-GPU process per job).

**(c) Timing Assumptions**
As no specific timing was provided, I assumed a baseline of 2 hours for a 76-residue protein based on standard AlphaFold performance for small proteins, adding a 2-hour safety margin for a total of 4 hours.

**(d) Scaling Guidance**
The scaling notes state: "Single GPU per prediction job. Parallelize by submitting multiple jobs with different FASTA inputs." I have followed this by specifying 1 node and 1 GPU for a single job in the sweep, intending for the user to submit many such jobs to the scheduler.

### Final Resource Specification
*   **Nodes:** 1
*   **Ranks per node:** 1
*   **Total ranks:** 1 (1 node $\times$ 1 rank per node)
*   **GPUs per node:** 1
*   **Walltime:** 4 hours
*   **Queue:** regular
````
