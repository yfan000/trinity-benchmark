# Reference answer — qmcpack@aurora

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
Selected application: QMCPACK

Reason: QMCPACK is the only installed application explicitly implementing Quantum Monte Carlo (variational and diffusion Monte Carlo) methods. It accepts HDF5 wavefunction files and XML input drivers natively, matching the inputs prepared at the prior facility. Its Aurora build uses SYCL/OpenMP offload targeting the Intel Data Center GPU Max Series (spir64), making it the correct match for Aurora's GPU architecture.

Key details from the catalog entry:
  - Binary: /lus/flare/projects/datascience/hzheng/software/aurora/qmcpack/v4.0.0/bin/qmcpack
  - Required modules: oneapi/release, intel_compute_runtime, cmake
  - Setup also requires: module use /soft/modulefiles, unset PYTHONPATH, export PATH to install bin
  - Launch command: mpiexec -n 6 --ppn 6 qmcpack input.xml
  - Default queue: debug; default walltime: 3600 s; default nodes: 1; ppn: 6
  - GPU support: Intel Data Center GPU Max Series via SYCL offload (ENABLE_SYCL=ON, OFFLOAD_TARGET=spir64)
  - Output files: *.scalar.dat, *.stat.h5, *.s*.config.h5
````
