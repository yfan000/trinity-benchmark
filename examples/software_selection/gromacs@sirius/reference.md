# Reference answer — gromacs@sirius

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
Selected application: GROMACS

Reason: GROMACS is the purpose-built high-performance molecular dynamics package for biomolecular simulations installed on Sirius. It supports CUDA GPU offload on the A100 GPUs present on Sirius, making it well-suited for a scaling benchmark across GPU nodes. While NAMD is also a biomolecular MD code with GPU support, GROMACS is specifically catalogued on Sirius with a built binary at /lus/tegu/projects/PolarisAT/hzheng/software/gromacs/bin/gmx_mpi and documented scaling guidance (one MPI rank per GPU, -ntmpi and -gpu_id flags), making it the correct choice for establishing scaling behaviour. LAMMPS handles classical MD but is not biomolecular-focused. All other installed packages address machine learning, electronic structure, or quantum chemistry workloads unrelated to biomolecular MD.
````
