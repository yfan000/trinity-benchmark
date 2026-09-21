# Reference answer — pytorch@sophia

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
#!/bin/bash -l
#PBS -N resnet50_repro
#PBS -l select=1:system=sophia
#PBS -l place=scatter
#PBS -l walltime=1:00:00
#PBS -l filesystems=home:eagle
#PBS -q by-gpu
#PBS -A TrinityAgent
#PBS -o /eagle/AlloyDesign/bkowalski/pytorch_run/logs/resnet50_repro.out
#PBS -e /eagle/AlloyDesign/bkowalski/pytorch_run/logs/resnet50_repro.err

# Create log directory if it does not exist
mkdir -p /eagle/AlloyDesign/bkowalski/pytorch_run/logs

# Change to working directory
cd ${PBS_O_WORKDIR}

# Software environment setup
source /home/hzheng/clearml/miniconda3/etc/profile.d/conda.sh
conda activate /eagle/datascience/hzheng/software/sophia/pytorch-mpi/conda_env
export LD_LIBRARY_PATH=/usr/lib64:/usr/local/cuda/lib64:${LD_LIBRARY_PATH}

# Node and rank configuration
NNODES=`wc -l < $PBS_NODEFILE`
NRANKS_PER_NODE=4
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))
echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE}"

# Launch distributed training
torchrun --nproc_per_node=4 train.py
````
