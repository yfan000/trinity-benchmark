# nemotron-3-ultra — pytorch@sophia, rich arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
#!/bin/bash -l
#PBS -l select=1:system=sophia
#PBS -l place=scatter
#PBS -l walltime=01:00:00
#PBS -l filesystems=home:eagle
#PBS -q by-gpu
#PBS -A TrinityAgent
#PBS -N resnet50_train
#PBS -o /eagle/AlloyDesign/bkowalski/pytorch_run/logs/train.out
#PBS -e /eagle/AlloyDesign/bkowalski/pytorch_run/logs/train.err

# Create output directory
mkdir -p /eagle/AlloyDesign/bkowalski/pytorch_run/logs

# Change to working directory
cd ${PBS_O_WORKDIR}

# Software environment
source /home/hzheng/clearml/miniconda3/etc/profile.d/conda.sh
conda activate /eagle/datascience/hzheng/software/sophia/pytorch-mpi/conda_env
export LD_LIBRARY_PATH=/usr/lib64:/usr/local/cuda/lib64:${LD_LIBRARY_PATH}

# Launch distributed training (4 GPUs per node)
torchrun --nproc_per_node=4 train.py
````
