# nemotron-3-ultra — gromacs@sirius, rich arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
#!/bin/bash -l
#PBS -N lysozyme_md
#PBS -l select=1:system=sirius
#PBS -l place=scatter
#PBS -l walltime=00:30:00
#PBS -l filesystems=home:tegu
#PBS -q workq
#PBS -A TrinityAgent
#PBS -o /lus/tegu/projects/MatGenome/shaddad/gromacs_run/logs/output.txt
#PBS -e /lus/tegu/projects/MatGenome/shaddad/gromacs_run/logs/error.txt

# Create log directory
mkdir -p /lus/tegu/projects/MatGenome/shaddad/gromacs_run/logs

# Change to working directory
cd ${PBS_O_WORKDIR}

# Load software environment
module load PrgEnv-gnu
module load cray-mpich
module load cray-fftw
module load cudatoolkit-standalone
export PATH=/lus/tegu/projects/PolarisAT/hzheng/software/gromacs/bin:$PATH

# MPI settings
NNODES=`wc -l < $PBS_NODEFILE`
NRANKS_PER_NODE=8
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))
echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE}"

# Launch simulation
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} gmx_mpi mdrun -v -deffnm run -gpu_id 01234567 -ntmpi 8
````
