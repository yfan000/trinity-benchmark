# Reference answer — nwchem@polaris

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
Selected application: NWChem

Why it fits: NWChem is the only installed application that directly supports Hartree-Fock, DFT (including hybrid functionals such as B3LYP), and Gaussian-type basis sets (such as 6-31G*) for molecular single-point energy calculations. CP2K also does DFT but is oriented toward periodic/solid-state systems; Quantum ESPRESSO uses plane waves and pseudopotentials rather than Gaussian basis sets; PySCF supports similar methods but is a Python framework less suited to reproducing an MPI-parallel production run. NWChem is the standard high-performance quantum chemistry code installed on Polaris that matches this exact workload.

Key details from the catalog entry:
  - Binary: /eagle/datascience/hzheng/software/polaris/nwchem/bin/nwchem
  - Input file type: .nw (text file specifying geometry, basis, DFT functional, and task)
  - Run command: mpiexec -n 16 --ppn 4 nwchem input.nw (scale ranks to match desired node count)
  - Required environment setup: module load PrgEnv-gnu; module swap gcc-native gcc-native/12.3; module load cray-mpich; export PATH and NWCHEM_BASIS_LIBRARY
  - Defaults: 1 node, debug queue, 1800 s walltime, 4 MPI ranks per node
  - GPU support: none (CPU-only build); the collaborator's 4-rank, ~5 s result is consistent with a small single-point DFT job on 1 node
````
