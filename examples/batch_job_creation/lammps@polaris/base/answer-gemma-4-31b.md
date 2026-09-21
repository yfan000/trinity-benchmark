# gemma-4-31b — lammps@polaris, base arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N LJ_Argon_MD
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

# Ensure the working directory exists for the output/error files
# (Since directives are fixed paths, we ensure the path is available)
mkdir -p /eagle/CatalysisDFT/shaddad/lammps_run

# Software Environment
module load PrgEnv-gnu
module swap gcc-native gcc-native/12.3
module load cray-mpich
module load cudatoolkit-standalone
export PATH=/eagle/datascience/hzheng/software/lammps/bin:$PATH

# Resource calculation
NNODES=`wc -l < $PBS_NODEFILE`
NRANKS_PER_NODE=4
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))

echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE}"

# Launch command
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} lmp -in in.lammps -k on g 4 -sf kk -pk kokkos
```
````
