# nemotron-3-ultra — nwchem@polaris, rich arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected application: NWChem**

**Why it fits:**
- **Purpose-built for molecular quantum chemistry**: NWChem is a high-performance computational chemistry package explicitly supporting Hartree-Fock, DFT (including hybrid functionals like B3LYP), correlated methods (CCSD(T), MP2), and MCSCF — exactly the class of calculation described.
- **Native Gaussian basis set support**: The 6-31G* basis set is a standard Pople-style Gaussian-type orbital (GTO) basis; NWChem uses GTOs natively, unlike plane-wave codes (Quantum ESPRESSO, VASP) or mixed Gaussian-plane-wave codes (CP2K) where such bases are non-standard or require special handling.
- **MPI parallelization**: The workload uses 4 MPI ranks on 1 node (~5 s walltime), matching NWChem’s distributed-memory parallel model for SCF/DFT.
- **Input format**: NWChem reads a simple text input file specifying geometry, basis set, and DFT task — consistent with the collaborator’s input description.
- **Polaris deployment**: Listed in the Polaris software catalog as a CPU build for computational chemistry, ready to run via MPI.
````
