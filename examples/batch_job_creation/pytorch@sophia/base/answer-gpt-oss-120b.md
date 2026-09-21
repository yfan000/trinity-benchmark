# gpt-oss-120b — pytorch@sophia, base arm

Batch job creation. **FAIL** (correctness 2/2, completeness 2/2, usability 1/2; 1 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N ResNet50_train                           # job name
#PBS -l select=1:system=sophia:ngpus=4           # 1 exclusive node with 4 GPUs
#PBS -l place=scatter                            # placement (required syntax)
#PBS -l walltime=01:00:00                        # max run time
#PBS -l filesystems=home:eagle                   # all filesystems used
#PBS -q by-gpu                                   # queue
#PBS -A TrinityAgent                             # project allocation
#PBS -o /eagle/AlloyDesign/bkowalski/pytorch_run/logs/stdout.log   # stdout
#PBS -e /eagle/AlloyDesign/bkowalski/pytorch_run/logs/stderr.log   # stderr

# ----------------------------------------------------------------------
# Create directories for PBS output files (must exist before PBS reads them)
mkdir -p /eagle/AlloyDesign/bkowalski/pytorch_run/logs

# Move to the directory where the job was submitted
cd ${PBS_O_WORKDIR}

# ----------------------------------------------------------------------
# Determine node and rank layout
NNODES=$(wc -l < "$PBS_NODEFILE")      # number of allocated nodes
NRANKS_PER_NODE=4                      # GPU‑rank per node (as decided)
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))

echo "NUM_OF_NODES=${NNODES}  TOTAL_NUM_RANKS=${NTOTRANKS}  RANKS_PER_NODE=${NRANKS_PER_NODE}"

# ----------------------------------------------------------------------
# Load the software environment
source /home/hzheng/clearml/miniconda3/etc/profile.d/conda.sh
conda activate /eagle/datascience/hzheng/software/sophia/pytorch-mpi/conda_env
export LD_LIBRARY_PATH=/usr/lib64:/usr/local/cuda/lib64:${LD_LIBRARY_PATH}

# ----------------------------------------------------------------------
# Launch the distributed PyTorch training
# (GPU‑distributed training with torchrun)
torchrun --nproc_per_node=${NRANKS_PER_NODE} train.py
```
````
