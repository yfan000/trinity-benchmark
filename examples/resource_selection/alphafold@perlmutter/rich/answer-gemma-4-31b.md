# gemma-4-31b — alphafold@perlmutter, rich arm

Resource selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 10 requirements violated).

````
### Reasoning

**1. Sizing the Work and Walltime**
*   **Target:** Human ubiquitin (76 residues) is a very small protein.
*   **Complexity:** A full database search (MSA generation) is the most time-consuming part. For a protein of this size, MSA generation typically takes 1–3 hours, and the GPU structure prediction (5 models + relaxation) takes roughly 30–60 minutes.
*   **Assumption:** I assume a total runtime of ~4 hours. I have added a 1-hour margin to account for filesystem I/O and database loading, totaling **5 hours**.

**2. Queue Elimination**
*   `debug`: Max 30min (Too short for MSA search) $\rightarrow$ **ELIMINATE**
*   `interactive`: Max 4h (Too short for 5h estimate) $\rightarrow$ **ELIMINATE**
*   `jupyter`: Max 6h (Possible, but generally reserved for notebooks) $\rightarrow$ **KEEP**
*   `express_amsc`: Max 6h (Possible) $\rightarrow$ **KEEP**
*   `regular`: Max 48h (Possible) $\rightarrow$ **KEEP**
*   `premium`: Max 48h (Possible) $\rightarrow$ **KEEP**
*   `shared`: Max 48h (Possible) $\rightarrow$ **KEEP**
*   `preempt`: Max 48h (Possible) $\rightarrow$ **KEEP**
*   `overrun`: Max 48h (Possible) $\rightarrow$ **KEEP**

**3. Queue Selection and Validation**
Since this is a "parameter sweep" involving many similar runs, the `regular` queue is the most appropriate for production throughput.

| Limit | Requested Value | Queue Limit | Result |
| :--- | :--- | :--- | :--- |
| Node Minimum | 1 Node | No min specified | **PASS** |
| Node Maximum | 1 Node | 3072 Nodes | **PASS** |
| Max Walltime | 5 Hours | 48 Hours | **PASS** |

**Verdict:** `regular` queue is selected.

**4. Scaling and Build Defaults**
*   **Scaling Guidance:** The prompt states "Single GPU per prediction job" and to "Parallelize by submitting multiple jobs." Therefore, for a single job in this sweep, I will request exactly 1 node and 1 GPU.
*   **Ranks per node:** Based on "Single GPU per run typical," the rank per node is 1.
*   **GPUs per rank:** 1.

### Resource Specification
*   **Nodes:** 1
*   **Ranks per node:** 1
*   **Total ranks:** 1 (1 node × 1 rank per node)
*   **GPUs per node:** 1
*   **Walltime:** 5 hours
*   **Queue:** regular
````
