# Prompt — lammps@polaris

Subtask: **Batch job creation**. Base arm, exactly as the model received it.

````
## Task
Write a PBS Pro batch script that submits the described molecular dynamics workload on Polaris.

## Workload
- **Problem:** Lennard-Jones argon, 500,000 atoms on an fcc lattice, reduced density 0.8442, reduced temperature 0.72, NVE, 100,000 timesteps, cutoff 2.5 sigma
- **System:** Polaris (ALCF), PBS Pro scheduler
- **Working directory:** /eagle/CatalysisDFT/shaddad/lammps_run
- **Input file:** in.lammps (already present in the working directory)
- **Software:** LAMMPS
- **Resources decided:** 1 node, 4 MPI ranks per node, walltime 00:30:00, queue debug
- **Project allocation:** TrinityAgent

## Software Environment
Apply these module lines and launch command exactly:
```
module load PrgEnv-gnu
module swap gcc-native gcc-native/12.3
module load cray-mpich
module load cudatoolkit-standalone
export PATH=/eagle/datascience/hzheng/software/lammps/bin:$PATH
```
Launch command form (substitute the correct input file and resource counts decided above):
```
mpiexec -n 4 --ppn 4 lmp -in input.lammps -k on g 4 -sf kk -pk kokkos
```
Binary: `/eagle/datascience/hzheng/software/lammps/bin/lmp`

## Scheduler Conventions
- Directives are NOT shell-expanded: never use $VAR or ${VAR} in #PBS -o/-e paths.
- Never put a trailing comment on a #PBS line; PBS reads it as another directive.
- Job arrays use `#PBS -J 1-N` and the index variable `$PBS_ARRAY_INDEX` (NOT -t / $PBS_ARRAYID).
- Node list is `$PBS_NODEFILE`; node count is `wc -l < $PBS_NODEFILE` (there is no $PBS_NNODES).
- `cd ${PBS_O_WORKDIR}` in the script body, not in a directive.
- ALCF requires `#PBS -l filesystems=<list>` naming every filesystem the job touches (Polaris/Crux/Sophia: home:eagle) or the job is rejected or hangs.
- An account is required: `#PBS -A <project>`.
- Nodes are allocated exclusively; ncpus in select= describes the whole node.
- Any output directory referenced by -o/-e must already exist.

### Worked Example (different application — do NOT copy its resource numbers)
```bash
#!/bin/bash -l
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=0:30:00
#PBS -l filesystems=home:eagle
#PBS -q debug
#PBS -A Catalyst

# Change to working directory
cd ${PBS_O_WORKDIR}

# MPI and OpenMP settings
NNODES=`wc -l < $PBS_NODEFILE`
NRANKS_PER_NODE=16
NDEPTH=2
NTHREADS=2

NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))
echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE} THREADS_PER_RANK= ${NTHREADS}"

mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} --depth=${NDEPTH} --cpu-bind depth --env OMP_NUM_THREADS=${NTHREADS} -env OMP_PLACES=threads ./hello_affinity
```

## Instructions
Write a valid PBS Pro batch script that:
(a) Requests resources in exactly the form the supplied site conventions and worked example demonstrate — including every directive element they show — and adds no per-chunk resource they omit, since nodes on Polaris are allocated exclusively.
(b) Includes full boilerplate: a job-name directive; output and error directives pointing at concrete paths under the stated working directory (no shell variables in those paths); an explicit `cd ${PBS_O_WORKDIR}` using the scheduler variable; and creation of any directory those paths reference before it is used.
(c) Loads the software environment using the module lines supplied above.
(d) Launches LAMMPS with the correct input file and the resource counts decided for this run.

## Output
Return the complete batch script.
````
