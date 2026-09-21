# gpt-oss-120b — vllm@frontier, rich arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 1 of 17 requirements violated).

````
```bash
#!/bin/bash -l

# -------------------  Slurm directives  -------------------
#SBATCH --job-name=vllm_infer                     # a short job name
#SBATCH --output=logs/%x-%j.out                    # STDOUT  (under $SLURM_SUBMIT_DIR)
#SBATCH --error=logs/%x-%j.err                     # STDERR  (under $SLURM_SUBMIT_DIR)
#SBATCH --nodes=1                                 # one full node
#SBATCH --ntasks-per-node=8                       # one task per GPU (8 GPUs per node)
#SBATCH --constraint=gpu                         # request GPU‑equipped nodes
#SBATCH --gpus-per-node=8                         # use all GPUs on the node
#SBATCH -A CHM202                                 # project allocation
#SBATCH --qos=debug                               # debug QoS
#SBATCH -p batch                                  # partition
#SBATCH --time=00:30:00                           # wall‑clock limit

# -------------------  Environment setup  -------------------
# Change to the directory where the job was submitted
cd "$SLURM_SUBMIT_DIR"

# Create the directory for the log files (must exist before the job starts)
mkdir -p logs

# Load the software stack exactly as supplied
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

# -------------------  Write the benchmark script  -------------------
cat > bench.py << 'PYEOF'
#!/usr/bin/env python
"""
Simple offline‑inference benchmark for Llama‑3.1‑8B using vLLM.
Generates 50 prompts, each limited to 50 tokens.
"""
from vllm import LLM, SamplingParams

# 50 dummy prompts – replace with real prompts if desired
prompts = [f"Prompt {i}" for i in range(1, 51)]

llm = LLM(
    model="/lustre/orion/csc708/scratch/hzheng/models/llama-3.1-8b",
    dtype="bfloat16",
    tensor_parallel_size=4,          # as required by the workload
    enforce_eager=True,
    gpu_memory_utilization=0.85,
)

sampling_params = SamplingParams(max_tokens=50)

outputs = llm.generate(prompts, sampling_params)

# Print each generated completion
for i, out in enumerate(outputs):
    print(f"--- Prompt {i+1} ---")
    print(out.outputs[0].text)
    print()
PYEOF

# -------------------  Launch the job  -------------------
srun /lustre/orion/csc708/scratch/hzheng/vllm-rocm-env/bin/python bench.py
```
````
