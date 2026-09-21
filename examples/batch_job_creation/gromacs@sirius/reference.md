# Reference answer — gromacs@sirius

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
```bash
#!/bin/bash -l
#PBS -N lysozyme_md
#PBS -o /lus/tegu/projects/MatGenome/shaddad/gromacs_run/logs/job.out
#PBS -e /lus/tegu/projects/MatGenome/shaddad/gromacs_run/logs/job.err
#PBS -l select=1:system=sirius
#PBS -l place=scatter
#PBS -l walltime=0:30:00
#PBS -l filesystems=home:tegu
#PBS -q workq
#PBS -A TrinityAgent

# Change to working directory
cd ${PBS_O_WORKDIR}

# Create log directory if it does not exist
mkdir -p /lus/tegu/projects/MatGenome/shaddad/gromacs_run/logs

# Node/rank accounting
NNODES=`wc -l < $PBS_NODEFILE`
NRANKS_PER_NODE=8
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))
echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE}"

# Software environment
module load PrgEnv-gnu
module load cray-mpich
module load cray-fftw
module load cudatoolkit-standalone
export PATH=/lus/tegu/projects/PolarisAT/hzheng/software/gromacs/bin:$PATH

# Launch GROMACS
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} gmx_mpi mdrun -v -deffnm md -gpu_id 01234567 -ntmpi 8 -s run.tpr
```

**Key decisions reflected:**
- `select=1:system=sirius` — 1 node on Sirius; no extra per-CPU/GPU sub-selectors (exclusive allocation).
- `walltime=0:30:00` — 30-minute limit as decided by resource selection.
- `filesystems=home:tegu` — Sirius-specific value from the system catalog (not `home:eagle`).
- `queue workq` — only queue on Sirius.
- `#PBS -A TrinityAgent` — required account directive.
- `-o`/`-e` use hardcoded literal paths (no `$VAR` expansion in directives); `mkdir -p` ensures the `logs/` directory exists before PBS tries to open those files.
- `cd ${PBS_O_WORKDIR}` in the script body, not in a directive.
- `NRANKS_PER_NODE=8`, `NTOTRANKS=8` matching the decided 8 ranks per node on 1 node.
- `-gpu_id 01234567` maps 8 MPI ranks to 8 GPUs (Sirius has 4 GPUs per node × 1 node = 4 GPUs; adjust to `0123` if the site exposes only 4 IDs, but the catalog placeholder uses 8 digits for an 8-rank-per-node layout).
- `-s run.tpr` points to the prepared input file in the working directory.
````
