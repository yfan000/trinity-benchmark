# nemotron-3-ultra — alphafold@perlmutter, base arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected Application: AlphaFold**

**Reasoning:**
AlphaFold (specifically AlphaFold2 via the provided conda environment) is the industry-standard tool for *ab initio* protein structure prediction from a single amino acid sequence. It was designed explicitly for this workload—taking a raw sequence as input and predicting the 3D structure using deep learning (attention-based architecture) trained on known structures and sequences. It is optimized for GPU acceleration (Perlmutter’s A100s) and is the most validated application for this specific task among the installed software. While `chai-lab` (Chai-1) is also a capable structure prediction model, AlphaFold remains the canonical, most widely benchmarked choice for single-chain prediction on HPC systems.
````
