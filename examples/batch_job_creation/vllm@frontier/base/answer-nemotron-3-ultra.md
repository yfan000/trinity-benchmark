# nemotron-3-ultra — vllm@frontier, base arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 17 requirements violated).

````
#!/bin/bash -l
#SBATCH -J llama31-8b-inference
#SBATCH -o logs/%x-%j.out
#SBATCH -e logs/%x-%j.err
#SBATCH -p batch
#SBATCH -q debug
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --constraint=gpu
#SBATCH --gpus-per-node=8
#SBATCH -A CHM202
#SBATCH -t 00:30:00

# Create log directory
mkdir -p logs

# Change to submission directory
cd $SLURM_SUBMIT_DIR

# Software environment (verbatim)
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

# Write bench.py with workload parameters
cat > bench.py << 'EOF'
if __name__ == '__main__':
    from vllm import LLM, SamplingParams
    llm = LLM(
        model="/lustre/orion/csc708/scratch/hzheng/models/llama-3.1-8b",
        dtype="bfloat16",
        tensor_parallel_size=4,
        enforce_eager=True,
        gpu_memory_utilization=0.85,
    )
    # 50 prompts
    prompts = [f"Prompt {i}: Hello, HPC!" for i in range(50)]
    outputs = llm.generate(prompts, SamplingParams(max_tokens=50))
    for output in outputs:
        print(output.outputs[0].text)
EOF

# Launch with srun
srun /lustre/orion/csc708/scratch/hzheng/vllm-rocm-env/bin/python bench.py
````
