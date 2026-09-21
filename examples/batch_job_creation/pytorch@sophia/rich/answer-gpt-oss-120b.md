# gpt-oss-120b — pytorch@sophia, rich arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N ResNet50_Sophia
#PBS -l select=1:system=sophia:ngpus=4
#PBS -l place=scatter
#PBS -l walltime=01:00:00
#PBS -l filesystems=home:eagle
#PBS -q by-gpu
#PBS -A TrinityAgent
#PBS -o /eagle/AlloyDesign/bkowalski/pytorch_run/resnet50.out
#PBS -e /eagle/AlloyDesign/bkowalski/pytorch_run/resnet50.err

# ----------------------------------------------------------------------
# Create output directory (must exist before PBS reads -o / -e)
mkdir -p /eagle/AlloyDesign/bkowalski/pytorch_run

# Change to the directory where qsub was invoked
cd ${PBS_O_WORKDIR}

# ----------------------------------------------------------------------
# Load the software environment
source /home/hzheng/clearml/miniconda3/etc/profile.d/conda.sh
conda activate /eagle/datascience/hzheng/software/sophia/pytorch-mpi/conda_env
export LD_LIBRARY_PATH=/usr/lib64:/usr/local/cuda/lib64:${LD_LIBRARY_PATH}

# ----------------------------------------------------------------------
# Determine resource layout
NNODES=$(wc -l < $PBS_NODEFILE)          # (1) number of allocated nodes
NRANKS_PER_NODE=4                         # (2) GPUs (ranks) per node
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE )) # (3) total MPI ranks

echo "NNODES=${NNODES}  NRANKS_PER_NODE=${NRANKS_PER_NODE}  NTOTRANKS=${NTOTRANKS}"

# ----------------------------------------------------------------------
# Launch the distributed training
# Using the conda‑environment's python and torchrun (torch.distributed.run)
/eagle/datascience/hzheng/software/sophia/pytorch-2.11-mpi/conda_env/bin/python \
    -m torch.distributed.run \
    --nproc_per_node=${NRANKS_PER_NODE} \
    train.py
```
````
