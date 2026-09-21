# gemma-4-31b — gromacs@sirius, base arm

Batch job creation. **FAIL** (correctness 2/2, completeness 1/2, usability 2/2; 1 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N lysozyme_md
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=00:30:00
#PBS -l filesystems=home:tegu
#PBS -q workq
#PBS -A TrinityAgent
#PBS -o /lus/tegu/projects/MatGenome/shaddad/gromacs_run/md.out
#PBS -e /lus/tegu/projects/MatGenome/shaddad/gromacs_run/md.err

# Change to working directory
cd ${PBS_O_WORKDIR}

# Ensure the working directory exists (though PBS_O_WORKDIR implies it does)
# and explicitly prepare for output files as per conventions.
mkdir -p /lus/tegu/projects/MatGenome/shaddad/gromacs_run

# Software Environment
module load PrgEnv-gnu
module load cray-mpich
module load cray-fftw
module load cudatoolkit-standalone
export PATH=/lus/tegu/projects/PolarisAT/hzheng/software/gromacs/bin:$PATH

# Resource calculations
NNODES=`wc -l < $PBS_NODEFILE`
NRANKS_PER_NODE=8
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))

echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE}"

# Launch GROMACS
# Input file: run.tpr, Output prefix: md
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} /lus/tegu/projects/PolarisAT/hzheng/software/gromacs/bin/gmx_mpi mdrun -v -s run.tpr -deffnm md -gpu_id 01234567 -ntmpi 8
```
````
