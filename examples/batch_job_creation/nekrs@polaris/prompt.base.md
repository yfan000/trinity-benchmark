# Prompt — nekrs@polaris

Subtask: **Batch job creation**. Base arm, exactly as the model received it.

````
Task: Write a valid PBS Pro batch script that restarts a NekRS simulation from a checkpoint on Polaris.

Workload:
- Problem: turbulent pipe flow at friction Reynolds number 550, 32,000 spectral elements at polynomial order 7, 20,000 timesteps, statistics collected over the final 10,000
- System: Polaris (ALCF), PBS Pro scheduler
- Working directory: /eagle/BioFoldX/tnakamura/nekrs_run
- Input case files already present: case.par, case.re2, case.udf
- Checkpoint files are present in the working directory; the run must restart from them
- Resources decided: 1 node, 4 ranks per node, walltime 00:30:00, queue debug
- Project allocation to charge: TrinityAgent

Software environment:
  module restore
  module use /soft/modulefiles
  module swap PrgEnv-nvidia PrgEnv-gnu
  module load cudatoolkit-standalone/12.9
  module load cuda/12.9
  module load gcc-native/13.2
  module load craype-x86-milan craype-accel-nvidia80
  module load spack-pe-base cmake
  export NEKRS_HOME=/eagle/datascience/hzheng/software/nekrs
  export PATH=$NEKRS_HOME/bin:$PATH
  export MPICH_GPU_SUPPORT_ENABLED=1
  export NEKRS_GPU_MPI=1
  export MPIR_CVAR_CH4_OFI_ENABLE_RMA=0
  modules: cudatoolkit-standalone/12.9, cuda/12.9, gcc-native/13.2
  launch command FORM (substitute the input case name and resources decided above):
    # nekRS uses 1 MPI rank per GPU (4 GPUs/node on Polaris) # GPU affinity helper assigns GPUs inversely to MPI local rank mpiexec -n $NTASKS -ppn 4 -d 8 --cpu-bind depth ./.lhelper nekrs --setup <casename> --backend CUDA --device-id 0
  binary: /eagle/datascience/hzheng/software/nekrs/bin/nekrs

Scheduler conventions:
  - Directives are NOT shell-expanded: never use $VAR or ${VAR} in #PBS -o/-e paths.
  - Never put a trailing comment on a #PBS line; PBS reads it as another directive.
  - Job arrays use `#PBS -J 1-N` and the index variable `$PBS_ARRAY_INDEX` (NOT -t / $PBS_ARRAYID).
  - Node list is `$PBS_NODEFILE`; node count is `wc -l < $PBS_NODEFILE` (there is no $PBS_NNODES).
  - `cd ${PBS_O_WORKDIR}` in the script body, not in a directive.
  - ALCF requires `#PBS -l filesystems=<list>` naming every filesystem the job touches (Polaris/Crux/Sophia: home:eagle - Aurora: home:flare) or the job is rejected or hangs.
  - An account is required: `#PBS -A <project>`.
  - Nodes are allocated exclusively; ncpus in select= describes the whole node.
  - Any output directory referenced by -o/-e must already exist.

Worked example (DIFFERENT application — do NOT copy its rank counts or resources):
  #!/bin/bash -l
  #PBS -l select=1:system=polaris
  #PBS -l place=scatter
  #PBS -l walltime=0:30:00
  #PBS -l filesystems=home:eagle
  #PBS -q debug
  #PBS -A Catalyst
  
  # Change to working directory
  cd ${PBS_O_WORKDIR}  # (1)!
  
  # MPI and OpenMP settings
  NNODES=`wc -l < $PBS_NODEFILE` # (2)!
  NRANKS_PER_NODE=16 # (3)!
  NDEPTH=2 # (4)!
  NTHREADS=2 # (5)!
  
  NTOTRANKS=$(( NNODES * NRANKS_PER_NODE )) # (6)!
  echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE} THREADS_PER_RANK= ${NTHREADS}"
  
  mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} --depth=${NDEPTH} --cpu-bind depth --env OMP_NUM_THREADS=${NTHREADS} -env OMP_PLACES=threads ./hello_affinity

Instructions: Write a valid PBS Pro batch script that:
  (a) requests resources in exactly the form the supplied site conventions and worked example demonstrate, including every element they show, and adds no per-chunk resource they omit, since nodes on these systems are allocated exclusively;
  (b) includes the full boilerplate: a job-name directive, output and error directives pointing at concrete paths under the stated working directory, an explicit change into that directory using the scheduler's own variable rather than a hardcoded path, and creation of any directory those paths reference;
  (c) loads the software environment exactly as listed above;
  (d) computes NNODES and NTASKS from the scheduler environment and launches the solver in restart mode against the case files in the working directory, using the launch command form provided.

Output: Return the complete batch script.
````
