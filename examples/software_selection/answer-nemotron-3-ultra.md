# Answer — nemotron-3-ultra

nwchem@polaris, Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2).

````
**Selected application: NWChem**

**Why it fits:**
- NWChem is a high-performance computational chemistry package explicitly designed for *ab initio* electronic structure calculations, including Hartree–Fock, DFT (with hybrid functionals like B3LYP), and correlated methods, using Gaussian-type orbital basis sets such as 6-31G*.
- It is MPI-parallelized and optimized for HPC architectures, making it a natural match for the collaborator’s 4-rank, single-node run (~5 s walltime).
- The workload is a standard single-point DFT energy calculation on a small molecule (H₂O) with a Pople-style basis set—exactly the type of problem NWChem targets and excels at on CPU-based nodes (Polaris’ AMD EPYC processors).
````
