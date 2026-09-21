# gemma-4-31b — lammps@polaris, rich arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N LJ_Argon_500k
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=00:30:00
#PBS -l filesystems=home:eagle
#PBS -q debug
#PBS -A TrinityAgent
#PBS -o /eagle/CatalysisDFT/shaddad/lammps_run/job.out
#PBS -e /eagle/CatalysisDFT/shaddad/lammps_run/job.err

# Change to working directory
cd ${PBS_O_WORKDIR}

# Ensure output directory exists (redundant here as it is the O_WORKDIR, 
# but included per instructions for paths referenced in -o/-e)
mkdir -p /eagle/CatalysisDFT/shaddad/lammps_run

# Software Environment
module load PrgEnv-gnu
module swap gcc-native gcc-native/12.3
module load cray-mpich
module load cudatoolkit-standalone
export PATH=/eagle/datascience/hzheng/software/lammps/bin:$PATH

# Resource calculations
NNODES=`wc -l < $PBS_NODEFILE`
NRANKS_PER_NODE=4
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))

echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE}"

# Launch LAMMPS
# -n 4: total ranks
# --ppn 4: ranks per node
# -k on g 4: Kokkos on GPUs, 4 GPU cores/streams
# -sf kk: Kokkos suffix
# -pk kokkos: Kokkos package
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} lmp -in in.lammps -k on g 4 -sf kk -pk kokkos
```
````
