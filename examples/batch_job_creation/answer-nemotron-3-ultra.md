# Answer — nemotron-3-ultra

hpl@crux, Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2).

````
#!/bin/bash -l
#PBS -l select=1:system=crux
#PBS -l place=scatter
#PBS -l walltime=00:30:00
#PBS -l filesystems=home:eagle
#PBS -q debug
#PBS -A TrinityAgent
#PBS -N hpl_N50000
#PBS -o /eagle/NuclearMPX/aschmidt/hpl_run/logs/hpl_N50000.out
#PBS -e /eagle/NuclearMPX/aschmidt/hpl_run/logs/hpl_N50000.err

# Change to working directory
cd ${PBS_O_WORKDIR}

# Create log directory if it doesn't exist
mkdir -p logs

# MPI settings
NNODES=`wc -l < $PBS_NODEFILE`
NRANKS_PER_NODE=128
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))

echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE}"

# Software environment
module swap PrgEnv-cray PrgEnv-gnu
module load cray-mpich
module load cray-libsci
export PATH=/eagle/datascience/hzheng/software/crux/hpl/bin:$PATH

# Launch HPL
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} xhpl
````
