# gemma-4-31b — hpl@crux, rich arm

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
#PBS -o /eagle/NuclearMPX/aschmidt/hpl_run/hpl_out.log
#PBS -e /eagle/NuclearMPX/aschmidt/hpl_run/hpl_err.log

# Change to working directory
cd ${PBS_O_WORKDIR}

# Ensure the output directory exists (as per instructions for -o/-e paths)
mkdir -p /eagle/NuclearMPX/aschmidt/hpl_run

# Software environment setup
module swap PrgEnv-cray PrgEnv-gnu
module load cray-mpich
module load cray-libsci
export PATH=/eagle/datascience/hzheng/software/crux/hpl/bin:$PATH

# MPI and Resource settings
NNODES=`wc -l < $PBS_NODEFILE`
NRANKS_PER_NODE=128
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))

echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE}"

# Launch command
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} xhpl
```
````
