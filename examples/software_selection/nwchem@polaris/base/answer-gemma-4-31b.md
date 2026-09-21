# gemma-4-31b — nwchem@polaris, base arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected Application:** NWChem

**Reasoning:** 
NWChem is specifically designed for high-performance computational chemistry and explicitly supports the required methods (DFT) and the B3LYP functional. Unlike the plane-wave DFT codes listed (such as Quantum ESPRESSO or VASP), NWChem uses Gaussian-type orbitals, which are necessary to utilize the specified 6-31G* basis set. It also supports the MPI parallelization required to match the collaborator's 4-rank execution.
````
