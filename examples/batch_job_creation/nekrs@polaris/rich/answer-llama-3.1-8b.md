# llama-3.1-8b — nekrs@polaris, rich arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
```bash
#!/bin/bash -l

#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=00:30:00
#PBS -l filesystems=home:eagle
#PBS -q debug
#PBS -A TrinityAgent
#PBS -N restart_nekrs_simulation

# Change to working directory
cd ${PBS_O_WORKDIR}

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

# MPI settings
NNODES=`wc -l < $PBS_NODEFILE`
NTASKS_PER_NODE=4
NTASKS=$(( NNODES * NTASKS_PER_NODE ))

# Launch the solver
echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTASKS} RANKS_PER_NODE= ${NTASKS_PER_NODE}"
mpiexec -n ${NTASKS} -ppn ${NTASKS_PER_NODE} -d 8 --cpu-bind depth ./.lhelper nekrs --setup case --backend CUDA --device-id 0 --restart
```

Note that I have used the exact form of the directives as provided in the site conventions and worked example, and have not added any additional per-chunk resources. I have also included the full boilerplate, loaded the software environment exactly as listed, computed NNODES and NTASKS from the scheduler environment, and launched the solver in restart mode against the case files in the working directory using the launch command form provided.
````
