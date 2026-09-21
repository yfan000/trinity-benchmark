# gpt-oss-120b — lammps@polaris, rich arm

Batch job creation. **FAIL** (correctness 2/2, completeness 2/2, usability 1/2; 1 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N lammps_500k                      # job name
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=00:30:00
#PBS -l filesystems=home:eagle
#PBS -q debug
#PBS -A TrinityAgent
#PBS -o /eagle/CatalysisDFT/shaddad/lammps_run/logs/%j.out   # stdout
#PBS -e /eagle/CatalysisDFT/shaddad/lammps_run/logs/%j.err   # stderr

# --------------------------------------------------------------------
# Change to the directory where the qsub command was issued
cd ${PBS_O_WORKDIR}

# Ensure the directory for PBS output/error exists before the job starts
mkdir -p /eagle/CatalysisDFT/shaddad/lammps_run/logs

# --------------------------------------------------------------------
# Load the software environment exactly as required
module load PrgEnv-gnu
module swap gcc-native gcc-native/12.3
module load cray-mpich
module load cudatoolkit-standalone
export PATH=/eagle/datascience/hzheng/software/lammps/bin:$PATH

# --------------------------------------------------------------------
# Resource bookkeeping (optional, useful for logging)
NNODES=$(wc -l < $PBS_NODEFILE)          # number of allocated nodes (should be 1)
NRANKS_PER_NODE=4
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))
echo "NUM_OF_NODES=${NNODES} TOTAL_NUM_RANKS=${NTOTRANKS} RANKS_PER_NODE=${NRANKS_PER_NODE}"

# --------------------------------------------------------------------
# Run LAMMPS
mpiexec -n 4 --ppn 4 lmp -in in.lammps -k on g 4 -sf kk -pk kokkos
```
````
