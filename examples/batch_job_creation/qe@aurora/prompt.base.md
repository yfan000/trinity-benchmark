# Prompt — qe@aurora

Subtask: **Batch job creation**. Base arm, exactly as the model received it.

````
**Task:** Write a valid PBS Pro batch script that submits the described DFT workload on Aurora.

**Workload:**
- Science: 3C-SiC in the zinc-blende structure, 2x2x2 conventional supercell (64 atoms), SCF total-energy calculation, plane-wave cutoff 60 Ry, charge-density cutoff 480 Ry, 4x4x4 Monkhorst-Pack k-grid, PBE functional, ultrasoft pseudopotentials
- System: Aurora (ALCF); scheduler is PBS Pro
- Working directory: /lus/flare/projects/NuclearMPX/lchen/qe_run
- Input file already present: scf.scf.in
- Resources decided: 1 node, 104 MPI ranks per node, walltime 00:30:00, queue debug
- Project allocation to charge: TrinityAgent

**Software environment:**
```
module use /soft/modulefiles
module load oneapi/release
module load intel_compute_runtime
module load cmake
unset PYTHONPATH
export PATH=/lus/flare/projects/datascience/hzheng/software/aurora/qe/7.4/bin:$PATH
```
Binary: `/lus/flare/projects/datascience/hzheng/software/aurora/qe/7.4/bin/pw.x`

Launch command form (substitute actual input file and rank counts for the placeholders):
```
PW_X=/lus/flare/projects/datascience/hzheng/software/aurora/qe/7.4/bin/pw.x
mpiexec -n <nprocs> --ppn <ppn> $PW_X -in input.scf.in 2>&1 | tee output.scf.out
```

**Scheduler conventions:**
- Directives are NOT shell-expanded: never use $VAR or ${VAR} in directive lines (e.g. -o/-e paths).
- Never put a trailing comment on a directive line; the scheduler reads it as part of the directive.
- Job arrays use `#PBS -J 1-N` and index variable `$PBS_ARRAY_INDEX` (NOT -t / $PBS_ARRAYID).
- Node list is `$PBS_NODEFILE`; node count is `wc -l < $PBS_NODEFILE` (there is no $PBS_NNODES).
- Change directory with `cd ${PBS_O_WORKDIR}` in the script body, not in a directive.
- ALCF requires `#PBS -l filesystems=<list>` naming every filesystem the job touches (Aurora: home:flare).
- An account directive is required: `#PBS -A <project>`.
- Nodes are allocated exclusively; do not add per-core or per-GPU sub-selects that the example omits.
- Any output directory referenced by -o/-e must already exist before the job runs; create it in the script if needed.

**Worked example** (for a DIFFERENT application on a DIFFERENT system — do NOT copy its resource values; use it only to understand the required script structure and directive form):
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

**Instructions:** Write a valid PBS Pro batch script for Aurora that:
(a) Requests resources in exactly the form the supplied site conventions and worked example demonstrate, including every element they show (select, walltime, filesystems, queue, account, job name, output and error paths), and adds no per-chunk resource specifiers they omit, since nodes are allocated exclusively.
(b) Includes the full boilerplate: a job-name directive, output and error directives pointing at concrete paths under the stated working directory (no shell variables in those directive lines), an explicit change into the working directory using the scheduler's own variable, and creation of any directory those paths reference before they are used.
(c) Sets up the software environment using the supplied module lines verbatim.
(d) Launches the application using the supplied launch command form, substituting the correct input filename and the decided rank counts for all placeholders.

**Output:** Return the complete batch script.
````
