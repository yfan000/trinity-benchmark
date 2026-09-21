# nemotron-3-ultra — nekrs@polaris, rich arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
#!/bin/bash -l
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=00:30:00
#PBS -l filesystems=home:eagle
#PBS -q debug
#PBS -A TrinityAgent
#PBS -N nekrs_pipe_Re550_restart
#PBS -o /eagle/BioFoldX/tnakamura/nekrs_run/logs/nekrs.out
#PBS -e /eagle/BioFoldX/tnakamura/nekrs_run/logs/nekrs.err

# Change to working directory
cd ${PBS_O_WORKDIR}

# Ensure output directory exists for PBS -o/-e (must exist at job start; created here for safety)
mkdir -p logs

# MPI and GPU affinity settings
NNODES=`wc -l < $PBS_NODEFILE`
NRANKS_PER_NODE=4
NDEPTH=8
NTHREADS=1

NTASKS=$(( NNODES * NRANKS_PER_NODE ))
echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTASKS} RANKS_PER_NODE= ${NRANKS_PER_NODE} THREADS_PER_RANK= ${NTHREADS}"

# Load software environment
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

# Launch NekRS restart from checkpoint (checkpoint files in working directory)
mpiexec -n ${NTASKS} -ppn ${NRANKS_PER_NODE} -d ${NDEPTH} --cpu-bind depth ./.lhelper nekrs --setup case --backend CUDA --device-id 0
````
