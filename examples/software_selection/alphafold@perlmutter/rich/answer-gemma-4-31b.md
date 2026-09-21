# gemma-4-31b — alphafold@perlmutter, rich arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Application:** AlphaFold

**Reasoning:** AlphaFold is specifically designed for the task of predicting a protein's three-dimensional structure directly from its amino acid sequence. While `chai-lab` is also a structure prediction model, AlphaFold is the industry standard for *ab initio* protein folding and is provided on Perlmutter via a dedicated conda environment tailored for this specific workload. Other listed software (like GROMACS, NAMD, or OpenMM) are intended for molecular dynamics simulations of existing structures rather than initial structure prediction from a sequence.
````
