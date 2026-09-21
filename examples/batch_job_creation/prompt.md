# Prompt — hpl@crux

Subtask: **Batch job creation**. Base arm, exactly as the model received it.

````
## Task
Write a valid PBS Pro batch script that submits the described workload on Crux.

## Workload
- Problem: HPL LINPACK, problem size N=50000, block size NB=232, 2x2 process grid
- System: Crux (ALCF, PBS Pro scheduler)
- Working directory: /eagle/NuclearMPX/aschmidt/hpl_run
- Input file HPL.dat is already present in the working directory
- Resources decided: 1 node, 128 ranks per node, walltime 00:30:00, queue debug
- Project allocation to charge: TrinityAgent

## Software environment
```
module swap PrgEnv-cray PrgEnv-gnu
module load cray-mpich
module load cray-libsci
export PATH=/eagle/datascience/hzheng/software/crux/hpl/bin:$PATH
launch command: mpiexec -n 128 --ppn 128 xhpl
binary: /eagle/datascience/hzheng/software/crux/hpl/bin/xhpl
```

## Scheduler conventions
- Directives are NOT shell-expanded: never use $VAR or ${VAR} in #PBS -o/-e paths.
- Never put a trailing comment on a #PBS line; PBS reads it as another directive.
- Job arrays use `#PBS -J 1-N` and the index variable `$PBS_ARRAY_INDEX` (NOT -t / $PBS_ARRAYID).
- Node list is `$PBS_NODEFILE`; node count is `wc -l < $PBS_NODEFILE` (there is no $PBS_NNODES).
- `cd ${PBS_O_WORKDIR}` in the script body, not in a directive.
- ALCF requires `#PBS -l filesystems=<list>` naming every filesystem the job touches (Polaris/Crux/Sophia: home:eagle — Aurora: home:flare) or the job is rejected or hangs.
- An account is required: `#PBS -A <project>`.
- Nodes are allocated exclusively; ncpus in select= describes the whole node.
- Any output directory referenced by -o/-e must already exist.

## Worked example
This script is for a **different application whose resources must NOT be copied** — it demonstrates required form only:
```
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
Write a valid batch script for this system's scheduler (PBS Pro) that:
(a) Requests resources in exactly the form the supplied site conventions and worked example demonstrate, including every element they show (select, place, walltime, filesystems, queue, account, job name, output path, error path), and adds no per-chunk resource they omit, since nodes are allocated exclusively.
(b) Includes full boilerplate: a job-name directive; output and error directives pointing at concrete paths under the stated working directory (no shell variables in those paths); an explicit `cd ${PBS_O_WORKDIR}`; and creates any directory those paths reference before writing to it.
(c) Sets up the software environment using the exact module lines supplied above.
(d) Launches the application with the supplied launch command using shell variables for node count and ranks per node derived at runtime.

## Output
Return the complete batch script.
````
