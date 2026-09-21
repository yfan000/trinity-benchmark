# gemma-4-31b — qmcpack@aurora, rich arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N silicon_dmc
#PBS -l select=1:system=aurora
#PBS -l place=scatter
#PBS -l walltime=01:00:00
#PBS -l filesystems=home:flare
#PBS -q debug
#PBS -A TrinityAgent
#PBS -o /lus/flare/projects/PlasmaEdge/rpatel/qmcpack_run/job.out
#PBS -e /lus/flare/projects/PlasmaEdge/rpatel/qmcpack_run/job.err

# Change to working directory
cd ${PBS_O_WORKDIR}

# Ensure the working directory exists for output files
mkdir -p /lus/flare/projects/PlasmaEdge/rpatel/qmcpack_run

# Software Environment
module use /soft/modulefiles
module load oneapi/release
module load intel_compute_runtime
module load cmake
unset PYTHONPATH
export PATH=/lus/flare/projects/datascience/hzheng/software/aurora/qmcpack/v4.0.0/bin:$PATH

# Resource calculation
NNODES=`wc -l < $PBS_NODEFILE`
NRANKS_PER_NODE=6
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))

echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE}"

# Launch application
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} qmcpack qmc.xml
```
````
