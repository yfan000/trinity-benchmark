# Prompt — nwchem@polaris

Subtask: **Batch job creation**. Base arm, exactly as the model received it.

````
## Task
Write a PBS Pro batch script that submits the described computational chemistry job on Polaris.

## Workload
- **Science:** Single water molecule, B3LYP/6-31G* single-point energy (reproducing a collaborator's earlier result)
- **System:** Polaris (ALCF) — uses PBS Pro scheduler
- **Working directory:** `/eagle/ProteinDesign/aschmidt/nwchem_run`
- **Input file:** `run.nw` (already present in working directory)
- **Software:** NWChem
- **Resources decided:** 1 node, 4 MPI ranks per node, walltime 00:30:00, queue debug
- **Project allocation:** `TrinityAgent`

## Software environment
```
module load PrgEnv-gnu
module swap gcc-native gcc-native/12.3
module load cray-mpich
export PATH=/eagle/datascience/hzheng/software/polaris/nwchem/bin:$PATH
export NWCHEM_BASIS_LIBRARY=/eagle/datascience/hzheng/software/polaris/nwchem/share/nwchem/libraries/
export NWCHEM_NWPW_LIBRARY=/eagle/datascience/hzheng/software/polaris/nwchem/share/nwchem/libraryps/
```
Launch command form (substitute correct input file and rank counts from resources decided above):
```
mpiexec -n 16 --ppn 4 nwchem input.nw
```
Binary: `/eagle/datascience/hzheng/software/polaris/nwchem/bin/nwchem`

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
This script is for a **different application** — do NOT copy its resource numbers. It demonstrates required form only:
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
Write a valid PBS Pro batch script for Polaris that:

(a) Requests resources in exactly the form the supplied site conventions and worked example demonstrate — including every directive element they show — and adds no per-chunk resource they omit, since nodes on Polaris are allocated exclusively.

(b) Includes the full boilerplate: a job-name directive; output and error directives pointing at concrete paths under the stated working directory (no shell variables in those paths); an explicit `cd` into the working directory using the scheduler's own variable; and creation of any directory those paths reference before the `cd`.

Set up the software environment using the exact module and export lines supplied, then launch NWChem with the correct total rank count and ranks-per-node derived from the resources decided above, using `run.nw` as the input file.

## Output
Return the complete batch script and nothing else.
````
