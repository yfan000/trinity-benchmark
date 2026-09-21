# nemotron-3-ultra — pytorch@sophia, base arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
#!/bin/bash -l
#PBS -l select=1:system=sophia
#PBS -l place=scatter
#PBS -l walltime=01:00:00
#PBS -l filesystems=home:eagle
#PBS -q by-gpu
#PBS -A TrinityAgent
#PBS -N resnet50_training
#PBS -o /eagle/AlloyDesign/bkowalski/pytorch_run/resnet50_training.out
#PBS -e /eagle/AlloyDesign/bkowalski/pytorch_run/resnet50_training.err

# Ensure output directory exists
mkdir -p /eagle/AlloyDesign/bkowalski/pytorch_run

# Change to working directory
cd ${PBS_O_WORKDIR}

# Software environment
source /home/hzheng/clearml/miniconda3/etc/profile.d/conda.sh
conda activate /eagle/datascience/hzheng/software/sophia/pytorch-mpi/conda_env
export LD_LIBRARY_PATH=/usr/lib64:/usr/local/cuda/lib64:${LD_LIBRARY_PATH}

# Node and rank configuration
NNODES=`wc -l < $PBS_NODEFILE`
NRANKS_PER_NODE=4
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))
echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE}"

# Launch distributed training
torchrun --nproc_per_node=${NRANKS_PER_NODE} train.py
````
