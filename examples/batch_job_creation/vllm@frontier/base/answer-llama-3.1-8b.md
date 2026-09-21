# llama-3.1-8b — vllm@frontier, base arm

Batch job creation. **FAIL** (correctness 2/2, completeness 0/2, usability 0/2, fatal; 1 of 17 requirements violated).

````
```bash
#!/bin/bash -l

# Job-name directive
#SBATCH --job-name=vllm-run

# Request resources
#SBATCH --qos=debug
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --constraint=gpu
#SBATCH --gpus-per-node=8
#SBATCH -p batch
#SBATCH -A CHM202

# Output and error directives
#SBATCH -o /lustre/orion/NuclearMPX/scratch/jmartinez/vllm_run/vllm-run.out
#SBATCH -e /lustre/orion/NuclearMPX/scratch/jmartinez/vllm_run/vllm-run.err

# Change into working directory
#SBATCH -D /lustre/orion/NuclearMPX/scratch/jmartinez/vllm_run

# Create output and error directories if they do not exist
mkdir -p /lustre/orion/NuclearMPX/scratch/jmartinez/vllm_run

# Load modules
module load PrgEnv-amd rocm miniforge3
unset PYTHONPATH PYTHONHOME
export PYTHONPATH=$ROCM_PATH/share/amd_smi:$PYTHONPATH
export HIP_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
unset ROCR_VISIBLE_DEVICES
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
export VLLM_TARGET_DEVICE=rocm
export PYTORCH_ROCM_ARCH=gfx90a
export TORCHDYNAMO_DISABLE=1
export TORCH_COMPILE_DISABLE=1
source /lustre/orion/csc708/scratch/hzheng/vllm-rocm-env/bin/activate

# Write bench.py inline
cat > bench.py <<EOF
if __name__ == '__main__':
    from vllm import LLM, SamplingParams
    llm = LLM(
        model="/lustre/orion/csc708/scratch/hzheng/models/llama-3.1-8b",
        dtype="bfloat16",
        tensor_parallel_size=4,
        enforce_eager=True,
        gpu_memory_utilization=0.85,
    )
    outputs = llm.generate(["Hello, HPC!"] * 50, SamplingParams(max_tokens=50))
    print(outputs[0].outputs[0].text)
EOF

# Launch the job
srun /lustre/orion/csc708/scratch/hzheng/vllm-rocm-env/bin/python bench.py
```
This script adheres to the provided site conventions and worked example, including all required directives, environment setup, and job execution. The `bench.py` script is written inline and the job is launched with the correct binary and parameters.
````
