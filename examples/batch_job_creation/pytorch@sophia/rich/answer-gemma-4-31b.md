# gemma-4-31b — pytorch@sophia, rich arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N ResNet50_Training
#PBS -l select=1:ncpus=48:mpiprocs=4:ngpus=4
#PBS -l place=scatter
#PBS -l walltime=01:00:00
#PBS -l filesystems=home:eagle
#PBS -q by-gpu
#PBS -A TrinityAgent
#PBS -o /eagle/AlloyDesign/bkowalski/pytorch_run/logs/resnet.out
#PBS -e /eagle/AlloyDesign/bkowalski/pytorch_run/logs/resnet.err

# Ensure output directory exists
mkdir -p /eagle/AlloyDesign/bkowalski/pytorch_run/logs

# Change to working directory
cd ${PBS_O_WORKDIR}

# Software environment setup
source /home/hzheng/clearml/miniconda3/etc/profile.d/conda.sh
conda activate /eagle/datascience/hzheng/software/sophia/pytorch-mpi/conda_env

export LD_LIBRARY_PATH=/usr/lib64:/usr/local/cuda/lib64:${LD_LIBRARY_PATH}

# Resource calculation for logging
NNODES=`wc -l < $PBS_NODEFILE`
GPUS_PER_NODE=4
echo "NUM_OF_NODES= ${NNODES} GPUS_PER_NODE= ${GPUS_PER_NODE}"

# Launch distributed deep learning training
# Using torchrun for GPU distributed training as requested
torchrun --nproc_per_node=${GPUS_PER_NODE} train.py
```
````
