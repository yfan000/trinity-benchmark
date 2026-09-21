# Prompt — qmcpack@aurora

Subtask: **Batch job creation**. Base arm, exactly as the model received it.

````
## Task
Write a PBS Pro batch script that can be submitted to the Aurora supercomputer at ALCF for the workload described below.

## Workload
- **Scientific problem:** Bulk silicon in the diamond structure, 2x2x2 supercell (64 atoms), diffusion Monte Carlo with a Slater-Jastrow trial wavefunction from a prior DFT run, 4096 walkers, timestep 0.005 Ha^-1, 200 DMC blocks
- **System:** Aurora (ALCF) — PBS Pro scheduler
- **Working directory:** /lus/flare/projects/PlasmaEdge/rpatel/qmcpack_run
- **Input files present in working directory:** qmc.xml, qmc.h5
- **Project allocation to charge:** TrinityAgent
- **Resources decided by earlier pipeline stages:** 1 node, 6 ranks per node, walltime 01:00:00, queue debug

## Software Environment
```
module use /soft/modulefiles
module load oneapi/release
module load intel_compute_runtime
module load cmake
unset PYTHONPATH
export PATH=/lus/flare/projects/datascience/hzheng/software/aurora/qmcpack/v4.0.0/bin:$PATH
```
modules: oneapi/release, intel_compute_runtime, cmake

Launch command form (substitute the actual input file and decided rank counts):
```
mpiexec -n 6 --ppn 6 qmcpack input.xml
```
binary: /lus/flare/projects/datascience/hzheng/software/aurora/qmcpack/v4.0.0/bin/qmcpack

## Scheduler Conventions
- Directives are NOT shell-expanded: never use $VAR or ${VAR} in #PBS -o/-e paths.
- Never put a trailing comment on a #PBS line; PBS reads it as another directive.
- Job arrays use `#PBS -J 1-N` and the index variable `$PBS_ARRAY_INDEX` (NOT -t / $PBS_ARRAYID).
- Node list is `$PBS_NODEFILE`; node count is `wc -l < $PBS_NODEFILE` (there is no $PBS_NNODES).
- `cd ${PBS_O_WORKDIR}` in the script body, not in a directive.
- ALCF requires `#PBS -l filesystems=<list>` naming every filesystem the job touches (Aurora: home:flare) or the job is rejected or hangs.
- An account is required: `#PBS -A <project>`.
- Nodes are allocated exclusively; ncpus in select= describes the whole node.
- Any output directory referenced by -o/-e must already exist.

## Worked Example
The following script is for a **different application on a different system** and uses resources that must NOT be copied. It demonstrates required form only:
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
Write a valid PBS Pro batch script for Aurora that:

(a) Requests resources in exactly the form the supplied site conventions and worked example demonstrate, including every element they show (select, place, walltime, filesystems, queue, account), and adds no per-chunk resource (such as ncpus or ngpus) that they omit, since nodes on these systems are allocated exclusively.

(b) Includes the full boilerplate: a job-name directive; output and error directives pointing at concrete paths under the stated working directory (no shell variables in those paths); an explicit change into the working directory using the scheduler's own variable; and creation of any directory those paths reference before they are written to.

(c) Sets up the software environment using exactly the module lines supplied above.

(d) Launches the application using the supplied launch command form, substituting the correct input file name and the decided rank counts.

## Output
Return the complete batch script.
````
