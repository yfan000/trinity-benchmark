# gemma-4-31b — nekrs@polaris, rich arm

Batch job creation. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 1 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N nekrs_restart
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=00:30:00
#PBS -l filesystems=home:eagle
#PBS -q debug
#PBS -A TrinityAgent
#PBS -o /eagle/BioFoldX/tnakamura/nekrs_run/logs/std.out
#PBS -e /eagle/BioFoldX/tnakamura/nekrs_run/logs/std.err

# Change to working directory
cd ${PBS_O_WORKDIR}

# Ensure log directory exists for the -o and -e directives
mkdir -p logs

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

# Resource calculations
NNODES=$(wc -l < $PBS_NODEFILE)
NRANKS_PER_NODE=4
NTASKS=$(( NNODES * NRANKS_PER_NODE ))

echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTASKS} RANKS_PER_NODE= ${NRANKS_PER_NODE}"

# Launch command
# For restarts in nekRS, the --setup flag is omitted and the binary is called directly
# Using the provided affinity helper and resource specifications
mpiexec -n ${NTASKS} -ppn ${NRANKS_PER_NODE} -d 8 --cpu-bind depth ./.lhelper nekrs --backend CUDA --device-id 0
```
````
