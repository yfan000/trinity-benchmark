# nemotron-3-ultra — lammps@polaris, rich arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
#!/bin/bash -l
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=00:30:00
#PBS -l filesystems=home:eagle
#PBS -q debug
#PBS -A TrinityAgent
#PBS -N lj_argon_500k
#PBS -o /eagle/CatalysisDFT/shaddad/lammps_run/logs/lj_argon_500k.out
#PBS -e /eagle/CatalysisDFT/shaddad/lammps_run/logs/lj_argon_500k.err

# Change to working directory
cd ${PBS_O_WORKDIR}

# Ensure log directory exists
mkdir -p logs

# Load software environment
module load PrgEnv-gnu
module swap gcc-native gcc-native/12.3
module load cray-mpich
module load cudatoolkit-standalone
export PATH=/eagle/datascience/hzheng/software/lammps/bin:$PATH

# MPI rank configuration
NNODES=$(wc -l < $PBS_NODEFILE)
NRANKS_PER_NODE=4
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))

echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE}"

# Launch LAMMPS
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} lmp -in in.lammps -k on g 4 -sf kk -pk kokkos
````
