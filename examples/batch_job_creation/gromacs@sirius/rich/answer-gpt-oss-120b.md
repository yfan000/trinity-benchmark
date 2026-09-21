# gpt-oss-120b — gromacs@sirius, rich arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N lysozyme_md
#PBS -l select=1:system=sirius
#PBS -l place=scatter
#PBS -l walltime=0:30:00
#PBS -l filesystems=home:tegu
#PBS -q workq
#PBS -A TrinityAgent
#PBS -o /lus/tegu/projects/MatGenome/shaddad/gromacs_run/logs/md.out
#PBS -e /lus/tegu/projects/MatGenome/shaddad/gromacs_run/logs/md.err

# ----------------------------------------------------------------------
# Move to the directory from which the job was submitted
cd ${PBS_O_WORKDIR}

# Create the directory that will hold the stdout / stderr files
mkdir -p /lus/tegu/projects/MatGenome/shaddad/gromacs_run/logs

# ----------------------------------------------------------------------
# Load the required software modules
module load PrgEnv-gnu
module load cray-mpich
module load cray-fftw
module load cudatoolkit-standalone

# Add GROMACS to the PATH
export PATH=/lus/tegu/projects/PolarisAT/hzheng/software/gromacs/bin:$PATH

# ----------------------------------------------------------------------
# Determine resources allocated by the scheduler
NNODES=$(wc -l < $PBS_NODEFILE)          # number of allocated nodes
NRANKS_PER_NODE=8                         # 8 MPI ranks per node
NTHREADS=1                                # one OpenMP thread per rank (GPU‑only)

NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))
echo "NNODES=${NNODES}  TOTAL_RANKS=${NTOTRANKS}  RANKS_PER_NODE=${NRANKS_PER_NODE}  THREADS_PER_RANK=${NTHREADS}"

# ----------------------------------------------------------------------
# Run GROMACS mdrun with MPI and GPU support
mpiexec -n ${NTOTRANKS} \
        --ppn ${NRANKS_PER_NODE} \
        --env OMP_NUM_THREADS=${NTHREADS} \
        --env OMP_PLACES=threads \
        gmx_mpi mdrun -v \
                       -s run.tpr \
                       -deffnm md \
                       -gpu_id 01234567 \
                       -ntmpi ${NRANKS_PER_NODE}
```
````
