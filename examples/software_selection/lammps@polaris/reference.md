# Reference answer — lammps@polaris

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
Selected application: LAMMPS

Reason: LAMMPS is the catalog's classical molecular dynamics code with GPU acceleration via the Kokkos backend, making it the direct match for a classical force-field simulation of a ~500,000-atom lipid-protein membrane system on Polaris's A100 GPUs. For a deadline run where turnaround matters most, a single-node job (1 node, 4 A100 GPUs) is sufficient for this atom count and fits in the debug queue (max 2 nodes, up to 1-hour walltime), which has no queue wait compared to the prod queue. The Kokkos GPU backend offloads the dominant force-evaluation work to the GPUs, maximising ns/day and minimising wall-clock time. Launch uses mpiexec with 4 MPI ranks (one per GPU), invoking the binary at /eagle/datascience/hzheng/software/lammps/bin/lmp with the Kokkos flags enabled. Setup requires loading PrgEnv-gnu, gcc-native/12.3, cray-mpich, and cudatoolkit-standalone modules and adding the install bin directory to PATH.
````
