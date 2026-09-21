# gemma-4-31b — hpl@crux, base arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N HPL_LINPACK
#PBS -l select=1:ncpus=128
#PBS -l place=scatter
#PBS -l walltime=00:30:00
#PBS -l filesystems=home:eagle
#PBS -q debug
#PBS -A TrinityAgent
#PBS -o /eagle/NuclearMPX/aschmidt/hpl_run/hpl.out
#PBS -e /eagle/NuclearMPX/aschmidt/hpl_run/hpl.err

# Change to working directory
cd ${PBS_O_WORKDIR}

# Ensure output directory exists (redundant here as it is the working dir, but required by convention)
mkdir -p /eagle/NuclearMPX/aschmidt/hpl_run

# MPI and Resource settings
NNODES=`wc -l < $PBS_NODEFILE`
NRANKS_PER_NODE=128
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))

echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE}"

# Software environment
module swap PrgEnv-cray PrgEnv-gnu
module load cray-mpich
module load cray-libsci
export PATH=/eagle/datascience/hzheng/software/crux/hpl/bin:$PATH

# Launch command
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} xhpl
```
````
