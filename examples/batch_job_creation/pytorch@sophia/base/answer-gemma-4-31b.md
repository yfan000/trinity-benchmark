# gemma-4-31b — pytorch@sophia, base arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N resnet50_training
#PBS -l select=1:ncpus=128:ngpus=4
#PBS -l place=scatter
#PBS -l walltime=01:00:00
#PBS -l filesystems=home:eagle
#PBS -q by-gpu
#PBS -A TrinityAgent
#PBS -o /eagle/AlloyDesign/bkowalski/pytorch_run/logs/output.log
#PBS -e /eagle/AlloyDesign/bkowalski/pytorch_run/logs/error.log

# Ensure the output directory exists before the job starts executing
mkdir -p /eagle/AlloyDesign/bkowalski/pytorch_run/logs

# Change to working directory
cd ${PBS_O_WORKDIR}

# Software environment setup
source /home/hzheng/clearml/miniconda3/etc/profile.d/conda.sh
conda activate /eagle/datascience/hzheng/software/sophia/pytorch-mpi/conda_env

export LD_LIBRARY_PATH=/usr/lib64:/usr/local/cuda/lib64:${LD_LIBRARY_PATH}

# Resource calculation
NNODES=`wc -l < $PBS_NODEFILE`
GPUS_PER_NODE=4

echo "NUM_OF_NODES= ${NNODES} GPUS_PER_NODE= ${GPUS_PER_NODE}"

# Launch distributed deep learning training
# Using torchrun for GPU distributed training as recommended
torchrun --nproc_per_node=${GPUS_PER_NODE} train.py
```
````
