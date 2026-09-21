# gpt-oss-120b — alphafold@perlmutter, base arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 1 of 4 requirements violated).

````
**Selected application:** **AlphaFold (DeepMind AlphaFold2)**  

**Why it fits**

- **Purpose‑built**: AlphaFold2 is explicitly designed for *ab initio* prediction of a protein’s three‑dimensional structure directly from its amino‑acid sequence, matching the workload description.
- **Proven accuracy**: It delivers near‑experimental accuracy for single‑chain predictions, which is ideal for a first‑run, single‑protein case.
- **GPU‑ready on Perlmutter**: The installation includes a dedicated Conda environment with CUDA support, allowing the model to take full advantage of Perlmutter’s GPU nodes (A100/A10) for fast inference.
- **Ease of use**: The provided environment already contains all required dependencies (TensorFlow, MMseqs2, OpenMM, etc.), so no additional software stack needs to be built.
- **Resource‑appropriate**: For a single protein chain the memory and compute demand comfortably fit within a single GPU allocation on Perlmutter, avoiding the need for large‑scale distributed training frameworks such as DeepSpeed.

Thus, AlphaFold is the most appropriate installed tool for predicting the 3‑D structure of the target protein on Perlmutter.
````
