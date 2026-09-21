# Reference answer — hpl@crux

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
Selected application: HPL (High Performance LINPACK benchmark, CPU-only build).

Reason: HPL is the standard dense linear algebra (Linpack) benchmark and is the only application in the catalog explicitly described as a Linpack benchmark. It is built for Crux's CPU-only AMD EPYC architecture, accepts a benchmark input file (HPL.dat) that is tuned for node memory and core count — matching the group's pre-existing input — and runs via MPI across all 128 cores per node using the installed binary at /eagle/datascience/hzheng/software/crux/hpl/bin/xhpl. Setup requires loading PrgEnv-gnu, cray-mpich, and cray-libsci (optimized BLAS). The default run uses 1 node, 128 MPI ranks, ppn=128, walltime=1800s, queue=workq, and produces output in HPL.out.
````
