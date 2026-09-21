# Prompt — gromacs@sirius

Subtask: **Batch job creation**. Base arm, exactly as the model received it.

````
## Task
Write a PBS Pro batch script for a molecular dynamics simulation on Sirius that can be submitted immediately to the scheduler.

## Workload
- **Science:** hen egg-white lysozyme solvated in TIP3P water with 0.15 M NaCl, ~34,000 atoms, NPT at 300 K, 2 fs timestep, PME, 5 ns production
- **System:** Sirius (ALCF staging cluster); scheduler: PBS Pro
- **Working directory:** `/lus/tegu/projects/MatGenome/shaddad/gromacs_run`
- **Input file:** `run.tpr` in the working directory
- **Project allocation:** `TrinityAgent`
- **Resources decided:** 1 node, 8 ranks per node, walltime 00:30:00, queue `workq`

## Software Environment
```
module load PrgEnv-gnu
module load cray-mpich
module load cray-fftw
module load cudatoolkit-standalone
export PATH=/lus/tegu/projects/PolarisAT/hzheng/software/gromacs/bin:$PATH
```
Binary: `/lus/tegu/projects/PolarisAT/hzheng/software/gromacs/bin/gmx_mpi`

Launch command form (rank counts and filenames are catalog placeholders — substitute the actual input and decided resources):
```
mpiexec -n 8 --ppn 8 gmx_mpi mdrun -v -deffnm md -gpu_id 01234567 -ntmpi 8
```

## Scheduler Conventions
- Directives are NOT shell-expanded: never use `$VAR` or `${VAR}` in `#PBS -o`/`-e` paths.
- Never put a trailing comment on a `#PBS` line; PBS reads it as another directive.
- Job arrays use `#PBS -J 1-N` and the index variable `$PBS_ARRAY_INDEX` (NOT `-t` / `$PBS_ARRAYID`).
- Node list is `$PBS_NODEFILE`; node count is `wc -l < $PBS_NODEFILE` (there is no `$PBS_NNODES`).
- `cd ${PBS_O_WORKDIR}` in the script body, not in a directive.
- ALCF requires `#PBS -l filesystems=<list>` naming every filesystem the job touches; for Sirius the required value is `home:tegu`.
- An account is required: `#PBS -A <project>`.
- Nodes are allocated exclusively; do not add per-CPU or per-GPU sub-selectors beyond what the worked example shows.
- Any output directory referenced by `-o`/`-e` must already exist; create it in the script body if needed.

## Worked Example
*This script is for a DIFFERENT application. Do NOT copy its resource numbers. It shows required form only.*
```bash
#!/bin/bash -l
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=0:30:00
#PBS -l filesystems=home:eagle
#PBS -q debug
#PBS -A Catalyst

# Change to working directory
cd ${PBS_O_WORKDIR}  # (1)!

# MPI and OpenMP settings
NNODES=`wc -l < $PBS_NODEFILE` # (2)!
NRANKS_PER_NODE=16 # (3)!
NDEPTH=2 # (4)!
NTHREADS=2 # (5)!

NTOTRANKS=$(( NNODES * NRANKS_PER_NODE )) # (6)!
echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE} THREADS_PER_RANK= ${NTHREADS}"

mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} --depth=${NDEPTH} --cpu-bind depth --env OMP_NUM_THREADS=${NTHREADS} -env OMP_PLACES=threads ./hello_affinity
```

## Instructions
Write a valid PBS Pro batch script that:

(a) Requests resources in exactly the form the scheduler conventions and worked example demonstrate — including `select=`, `place=`, `walltime=`, `filesystems=`, queue, and account directives — and adds no per-chunk resource specifiers they omit, since nodes on Sirius are allocated exclusively.

(b) Includes full boilerplate: a job-name directive; output and error directives pointing at concrete literal paths under the stated working directory (no shell variables in those paths); explicit `cd` into the working directory using the scheduler's own variable; and creation of any log or output directory those paths reference before the application runs.

(c) Loads the supplied modules and sets the PATH export before invoking the application.

(d) Launches the application with the correct MPI wrapper and flags, substituting the actual input file and decided resource counts for the placeholders in the launch command form.

## Output
Return the complete, ready-to-submit batch script.
````
