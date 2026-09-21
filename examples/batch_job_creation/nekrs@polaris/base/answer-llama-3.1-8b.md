# llama-3.1-8b — nekrs@polaris, base arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
Here is the complete batch script that meets the requirements:

```bash
#!/bin/bash -l

#PBS -N restart_nekrs
#PBS -o /eagle/BioFoldX/tnakamura/nekrs_run/output
#PBS -e /eagle/BioFoldX/tnakamura/nekrs_run/error
#PBS -d ${PBS_O_WORKDIR}
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=0:30:00
#PBS -l filesystems=home:eagle
#PBS -q debug
#PBS -A TrinityAgent

# Change to working directory
cd ${PBS_O_WORKDIR}

# MPI and OpenMP settings
NNODES=`wc -l < $PBS_NODEFILE`
NRANKS_PER_NODE=4
NTASKS=$(( NNODES * NRANKS_PER_NODE ))

# Software environment
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

# Launch the solver in restart mode
mkdir -p output
mkdir -p error
mpiexec -n ${NTASKS} -ppn ${NRANKS_PER_NODE} -d 8 --cpu-bind depth ./.lhelper nekrs --setup case --backend CUDA --device-id 0 --restart
```

This script meets all the requirements specified, including:

*   Requesting resources in the exact form specified by the site conventions and worked example.
*   Including the full boilerplate, including a job-name directive, output and error directives, and creation of any directories those paths reference.
*   Loading the software environment exactly as listed above.
*   Computing NNODES and NTASKS from the scheduler environment and launching the solver in restart mode against the case files in the working directory, using the launch command form provided.
````
