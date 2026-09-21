# Reference answer — qe@aurora

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
Selected application: Quantum ESPRESSO

Reason: Quantum ESPRESSO is the only installed plane-wave DFT code on Aurora, built with Intel oneAPI (ifx/MKL/ScaLAPACK) and explicitly designed for electronic structure calculations — matching the workload's plane-wave DFT SCF runs and the Fortran namelist input format (&CONTROL, &SYSTEM, &ELECTRONS, ATOMIC_SPECIES) described. For a parameter sweep of many similar runs, individual jobs are launched via:
  mpiexec -n <nprocs> --ppn <ppn> /lus/flare/projects/datascience/hzheng/software/aurora/qe/7.4/bin/pw.x -in input.scf.in 2>&1 | tee output.scf.out
Required modules:
  module use /soft/modulefiles
  module load oneapi/release
  module load intel_compute_runtime
  module load cmake
Default sizing: 1 node, 104 MPI ranks per node (CPU-only MPI build using Intel MKL FFT), walltime 1800 s, debug queue. The sweep of similar runs maps naturally to multiple independent jobs or a job array, each consuming one node.
````
