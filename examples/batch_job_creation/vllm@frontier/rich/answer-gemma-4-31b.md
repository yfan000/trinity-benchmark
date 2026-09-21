# gemma-4-31b — vllm@frontier, rich arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 17 requirements violated).

````
```bash
#!/bin/bash -l
#SBATCH -J llama_inference
#SBATCH -p batch
#SBATCH -q debug
#SBATCH -A CHM202
#SBATCH --nodes=1
#SBATCH --constraint=gpu
#SBATCH --time=00:30:00
#SBATCH -o %x_%j.out
#SBATCH -e %x_%j.err

# Change to the working directory provided in the workload
cd /lustre/orion/NuclearMPX/scratch/jmartinez/vllm_run

# Ensure the current directory exists (for output files)
mkdir -p .

# Software environment setup
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

# Write the inference script inline
cat <<EOF > bench.py
if __name__ == '__main__':
    from vllm import LLM, SamplingParams
    
    # Workload: Llama-3.1-8B, tensor parallel size 4
    llm = LLM(
        model="/lustre/orion/csc708/scratch/hzheng/models/llama-3.1-8b",
        dtype="bfloat16",
        tensor_parallel_size=4,
        enforce_eager=True,
        gpu_memory_utilization=0.85,
    )
    
    # Workload: 50 prompts, max_tokens=50
    prompts = ["Prompt " + str(i) for i in range(50)]
    sampling_params = SamplingParams(max_tokens=50)
    
    outputs = llm.generate(prompts, sampling_params)
    
    for output in outputs:
        print(f"Generated text: {output.outputs[0].text}")
EOF

# Launch the job using srun and the specified binary
srun /lustre/orion/csc708/scratch/hzheng/vllm-rocm-env/bin/python bench.py
```
````
