# Prompt — pytorch@sophia

Subtask: **Batch job creation**. Base arm, exactly as the model received it.

````
**Task:** Write a PBS Pro batch script for Sophia that requests the correct allocation, sets up the software environment, and launches a distributed deep learning training run.

**Workload:**
- Problem: ResNet-50 image classification on a 100,000-image subset, batch size 256 per GPU, mixed precision, 10 epochs
- System: Sophia (ALCF), scheduler: PBS Pro
- Working directory: /eagle/AlloyDesign/bkowalski/pytorch_run
- Training script: train.py (already in working directory)
- Project allocation: TrinityAgent
- Resources decided: 1 node, 4 ranks per node, walltime 01:00:00, queue by-gpu

**Software environment:**
```
source /home/hzheng/clearml/miniconda3/etc/profile.d/conda.sh

conda activate /eagle/datascience/hzheng/software/sophia/pytorch-mpi/conda_env

export LD_LIBRARY_PATH=/usr/lib64:/usr/local/cuda/lib64:${LD_LIBRARY_PATH}
```
launched with (catalog placeholders — substitute actual input file and decided resources):
```
# For GPU distributed training (recommended): torchrun --nproc_per_node=8 train.py
# Or with MPI for CPU collectives: mpirun -n 4 python train.py
```
binary: `/eagle/datascience/hzheng/software/sophia/pytorch-2.11-mpi/conda_env/bin/python`

**Scheduler conventions:**
- Directives are NOT shell-expanded: never use $VAR or ${VAR} in #PBS -o/-e paths.
- Never put a trailing comment on a #PBS line; PBS reads it as another directive.
- Job arrays use `#PBS -J 1-N` and the index variable `$PBS_ARRAY_INDEX` (NOT -t / $PBS_ARRAYID).
- Node list is `$PBS_NODEFILE`; node count is `wc -l < $PBS_NODEFILE` (there is no $PBS_NNODES).
- `cd ${PBS_O_WORKDIR}` in the script body, not in a directive.
- ALCF requires `#PBS -l filesystems=<list>` naming every filesystem the job touches (Sophia: home:eagle) or the job is rejected or hangs.
- An account is required: `#PBS -A <project>`.
- Nodes are allocated exclusively; ncpus in select= describes the whole node.
- Any output directory referenced by -o/-e must already exist.

**Worked example** (for a DIFFERENT application on a different system — demonstrates required form only, do NOT copy its resource numbers, queue, or launch command):
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

**Instructions:** Write a valid PBS Pro batch script for Sophia that:
(a) Requests resources in exactly the form the supplied site conventions and worked example demonstrate, including every element they show (select, place, walltime, filesystems, queue, account, job name, output path, error path), and adds no per-chunk resource they omit, since nodes on Sophia are allocated exclusively.
(b) Includes the full boilerplate: a job-name directive, output and error directives pointing at concrete paths under the stated working directory (no shell variables in those directive values), an explicit `mkdir -p` for any directory those paths reference, and an explicit change into the working directory using `cd ${PBS_O_WORKDIR}`.
(c) Sources the software environment exactly as given above.
(d) Launches the training run using the GPU distributed training form of the launch command, substituting the correct number of GPUs per node for this job and the correct training script name.

**Output:** Return the complete batch script.
````
