# Reference answer — nekrs@polaris

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
#!/bin/bash -l
#PBS -N nekrs_restart
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=0:30:00
#PBS -l filesystems=home:eagle
#PBS -q debug
#PBS -A TrinityAgent
#PBS -o /eagle/BioFoldX/tnakamura/nekrs_run/logs/nekrs_restart.out
#PBS -e /eagle/BioFoldX/tnakamura/nekrs_run/logs/nekrs_restart.err

# Create log directory if it does not exist
mkdir -p /eagle/BioFoldX/tnakamura/nekrs_run/logs

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
NNODES=$(wc -l < $PBS_NODEFILE)
NRANKS_PER_NODE=4
NTASKS=$(( NNODES * NRANKS_PER_NODE ))
echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTASKS} RANKS_PER_NODE= ${NRANKS_PER_NODE}"

# Launch NekRS restarting from checkpoint
# nekRS uses 1 MPI rank per GPU (4 GPUs/node on Polaris)
# GPU affinity helper assigns GPUs inversely to MPI local rank
mpiexec -n $NTASKS -ppn 4 -d 8 --cpu-bind depth ./.lhelper nekrs --setup case --backend CUDA --device-id 0
````
