# nemotron-3-ultra — vllm@frontier, rich arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 17 requirements violated).

````
#!/bin/bash -l
#SBATCH -J llama31_8b_offline_inference
#SBATCH -A CHM202
#SBATCH -p batch
#SBATCH -q debug
#SBATCH -N 1
#SBATCH -t 00:30:00
#SBATCH -o /lustre/orion/NuclearMPX/scratch/jmartinez/vllm_run/slurm_out/%x-%j.out
#SBATCH -e /lustre/orion/NuclearMPX/scratch/jmartinez/vllm_run/slurm_out/%x-%j.err

mkdir -p /lustre/orion/NuclearMPX/scratch/jmartinez/vllm_run/slurm_out
cd ${SLURM_SUBMIT_DIR}

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
    prompts = [f"Prompt {i}: Hello, HPC!" for i in range(50)]
    outputs = llm.generate(prompts, SamplingParams(max_tokens=50))
    for out in outputs:
        print(out.outputs[0].text)
EOF

srun /lustre/orion/csc708/scratch/hzheng/vllm-rocm-env/bin/python bench.py
````
