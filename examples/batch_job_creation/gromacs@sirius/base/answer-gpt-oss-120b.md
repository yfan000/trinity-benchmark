# gpt-oss-120b — gromacs@sirius, base arm

Batch job creation. **FAIL** (correctness 2/2, completeness 2/2, usability 1/2; 1 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N gromacs_mdrun                     # job name
#PBS -l select=1:system=sirius            # 1 exclusive node on Sirius
#PBS -l place=scatter                     # any placement is fine for a single node
#PBS -l walltime=00:30:00                 # 30 min wall‑clock limit
#PBS -l filesystems=home:tegu             # all file‑systems touched by the job
#PBS -q workq                             # queue to use
#PBS -A TrinityAgent                      # project allocation
#PBS -o /lus/tegu/projects/MatGenome/shaddad/gromacs_run/logs/stdout.txt
#PBS -e /lus/tegu/projects/MatGenome/shaddad/gromacs_run/logs/stderr.txt

# ----------------------------------------------------------------------
# Change to the directory from which the job was submitted
cd ${PBS_O_WORKDIR}

# Create the log directory (must exist before PBS writes into it)
mkdir -p /lus/tegu/projects/MatGenome/shaddad/gromacs_run/logs

# ----------------------------------------------------------------------
# Load the software environment
module load PrgEnv-gnu
module load cray-mpich
module load cray-fftw
module load cudatoolkit-standalone

# Add GROMACS to PATH
export PATH=/lus/tegu/projects/PolarisAT/hzheng/software/gromacs/bin:$PATH

# ----------------------------------------------------------------------
# Determine the actual allocation size
NNODES=$(wc -l < $PBS_NODEFILE)          # number of allocated nodes
NRANKS_PER_NODE=8                         # ranks per node as requested
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE )) # total MPI ranks

echo "Nodes allocated : $NNODES"
echo "Ranks per node   : $NRANKS_PER_NODE"
echo "Total ranks      : $NTOTRANKS"

# ----------------------------------------------------------------------
# Run GROMACS mdrun
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} \
    gmx_mpi mdrun -v -s run.tpr -deffnm md \
    -gpu_id 01234567 -ntmpi ${NRANKS_PER_NODE}
```

Save the file (e.g., `gmx_job.pbs`) and submit it with  

```bash
qsub gmx_job.pbs
```  

The script requests exactly the resources you specified, loads the required modules, points all output to concrete log files, and launches the production MD run on 1 node with 8 MPI ranks.
````
