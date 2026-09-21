# Reference answer — qmcpack@aurora

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
```bash
#!/bin/bash -l
#PBS -N qmcpack_dmc_si
#PBS -l select=1:system=aurora
#PBS -l place=scatter
#PBS -l walltime=1:00:00
#PBS -l filesystems=home:flare
#PBS -q debug
#PBS -A TrinityAgent
#PBS -o /lus/flare/projects/PlasmaEdge/rpatel/qmcpack_run/logs/qmcpack_dmc_si.out
#PBS -e /lus/flare/projects/PlasmaEdge/rpatel/qmcpack_run/logs/qmcpack_dmc_si.err

# Change to working directory
cd ${PBS_O_WORKDIR}

# Create log directory if it does not exist
mkdir -p /lus/flare/projects/PlasmaEdge/rpatel/qmcpack_run/logs

# Software environment
module use /soft/modulefiles
module load oneapi/release
module load intel_compute_runtime
module load cmake
unset PYTHONPATH
export PATH=/lus/flare/projects/datascience/hzheng/software/aurora/qmcpack/v4.0.0/bin:$PATH

# MPI settings
NNODES=`wc -l < $PBS_NODEFILE`
NRANKS_PER_NODE=6
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))
echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE}"

# Launch QMCPACK
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} qmcpack qmc.xml
```
````
