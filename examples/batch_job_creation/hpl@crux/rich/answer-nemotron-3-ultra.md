# nemotron-3-ultra — hpl@crux, rich arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
#!/bin/bash -l
#PBS -l select=1:system=crux
#PBS -l place=scatter
#PBS -l walltime=0:30:00
#PBS -l filesystems=home:eagle
#PBS -q debug
#PBS -A TrinityAgent
#PBS -N hpl_N50000
#PBS -o /eagle/NuclearMPX/aschmidt/hpl_run/logs/hpl.out
#PBS -e /eagle/NuclearMPX/aschmidt/hpl_run/logs/hpl.err

# Ensure output directory exists (for any script-generated output; PBS -o/-e paths must exist at submit time)
mkdir -p /eagle/NuclearMPX/aschmidt/hpl_run/logs

# Change to working directory
cd ${PBS_O_WORKDIR}

# Software environment
module swap PrgEnv-cray PrgEnv-gnu
module load cray-mpich
module load cray-libsci
export PATH=/eagle/datascience/hzheng/software/crux/hpl/bin:$PATH

# MPI settings derived at runtime
NNODES=`wc -l < $PBS_NODEFILE`
NRANKS_PER_NODE=128
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))

echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE}"

# Launch HPL
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} xhpl
````
