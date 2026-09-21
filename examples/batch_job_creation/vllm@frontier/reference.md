# Reference answer — vllm@frontier

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
#!/bin/bash -l
#SBATCH -J llama31_8b_infer
#SBATCH -p batch
#SBATCH -q debug
#SBATCH -A CHM202
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH -t 00:30:00
#SBATCH -o /lustre/orion/NuclearMPX/scratch/jmartinez/vllm_run/logs/job_%j.out
#SBATCH -e /lustre/orion/NuclearMPX/scratch/jmartinez/vllm_run/logs/job_%j.err

# Create output directory if it does not exist
mkdir -p /lustre/orion/NuclearMPX/scratch/jmartinez/vllm_run/logs

# Change into working directory
cd $SLURM_SUBMIT_DIR

# Software environment setup
module load PrgEnv-amd rocm miniforge3
unset PYTHONPATH PYTHONHOME   # AFTER module load
export PYTHONPATH=$ROCM_PATH/share/amd_smi:$PYTHONPATH
export HIP_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
unset ROCR_VISIBLE_DEVICES
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY  # for internal node comms
export VLLM_TARGET_DEVICE=rocm
export PYTORCH_ROCM_ARCH=gfx90a
export TORCHDYNAMO_DISABLE=1
export TORCH_COMPILE_DISABLE=1
source /lustre/orion/csc708/scratch/hzheng/vllm-rocm-env/bin/activate

# Write inference script
cat > bench.py << 'EOF'
if __name__ == '__main__':
    from vllm import LLM, SamplingParams

    prompts = [f"Prompt number {i}: Describe a scientific application of HPC." for i in range(50)]

    llm = LLM(
        model="/lustre/orion/csc708/scratch/hzheng/models/llama-3.1-8b",
        dtype="bfloat16",
        tensor_parallel_size=4,
        enforce_eager=True,
        gpu_memory_utilization=0.85,
    )
    outputs = llm.generate(prompts, SamplingParams(max_tokens=50))
    for i, output in enumerate(outputs):
        print(f"[{i}] {output.outputs[0].text}")
EOF

# Launch
srun /lustre/orion/csc708/scratch/hzheng/vllm-rocm-env/bin/python bench.py
````
