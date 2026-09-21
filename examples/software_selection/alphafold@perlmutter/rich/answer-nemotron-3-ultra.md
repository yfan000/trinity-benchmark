# nemotron-3-ultra — alphafold@perlmutter, rich arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected Application: AlphaFold**

**Why it fits:**
- **Purpose-built for the task:** AlphaFold2 is specifically designed for *ab initio* protein structure prediction from a single amino acid sequence, which matches the workload exactly.
- **Architecture alignment:** The installation is provided as a conda environment on Perlmutter, making it readily accessible on the A100 GPUs (via the `gpu` partition) without additional compilation.
- **Proven accuracy:** As the CASP14/15-winning method, it is the community standard for high-accuracy monomer structure prediction.
- **Input compatibility:** It directly accepts a FASTA sequence as input, requiring no prior structural templates or complex setup for a first run.
````
