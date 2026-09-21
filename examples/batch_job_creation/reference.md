# Reference answer — hpl@crux

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
#!/bin/bash -l
#PBS -N hpl_scaling
#PBS -l select=1:system=crux
#PBS -l place=scatter
#PBS -l walltime=0:30:00
#PBS -l filesystems=home:eagle
#PBS -q debug
#PBS -A TrinityAgent
#PBS -o /eagle/NuclearMPX/aschmidt/hpl_run/logs/hpl_scaling.out
#PBS -e /eagle/NuclearMPX/aschmidt/hpl_run/logs/hpl_scaling.err

# Create log directory if it does not exist
mkdir -p /eagle/NuclearMPX/aschmidt/hpl_run/logs

# Change to working directory
cd ${PBS_O_WORKDIR}

# Set up software environment
module swap PrgEnv-cray PrgEnv-gnu
module load cray-mpich
module load cray-libsci
export PATH=/eagle/datascience/hzheng/software/crux/hpl/bin:$PATH

# Runtime resource counts
NNODES=`wc -l < $PBS_NODEFILE`
NRANKS_PER_NODE=128
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))
echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE}"

# Launch HPL
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} xhpl
````
