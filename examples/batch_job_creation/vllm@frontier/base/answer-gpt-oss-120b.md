# gpt-oss-120b — vllm@frontier, base arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 1 of 17 requirements violated).

````
```bash
#!/bin/bash -l
# -------------------------------------------------
# Frontier (OLCF) Slurm batch script for Llama‑3.1‑8B offline inference
# -------------------------------------------------
#SBATCH --job-name=llama3_inference
#SBATCH --output=%x-%j.out               # stdout  → $SLURM_SUBMIT_DIR/%x-%j.out
#SBATCH --error=%x-%j.err                # stderr  → $SLURM_SUBMIT_DIR/%x-%j.err
#SBATCH --time=00:30:00                  # wall‑clock limit
#SBATCH --qos=debug                      # QoS (debug queue)
#SBATCH --partition=batch                # partition
#SBATCH --nodes=1                        # exclusive node allocation
#SBATCH --ntasks-per-node=1              # one Slurm task (we launch with srun)
#SBATCH --constraint=gpu                 # request GPU nodes
#SBATCH --gpus-per-node=4                # four GPUs for tensor‑parallelism=4
#SBATCH -A CHM202                        # project allocation
# -------------------------------------------------

# ------------------------------------------------------------------
# Create a directory for the output files (must exist before they are used)
# ------------------------------------------------------------------
mkdir -p "$SLURM_SUBMIT_DIR/logs"

# ------------------------------------------------------------------
# Load software modules and set up the environment (exactly as supplied)
# ------------------------------------------------------------------
module load PrgEnv-amd rocm miniforge3
unset PYTHONPATH PYTHONHOME               # AFTER module load
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

# ------------------------------------------------------------------
# Write the inference benchmark script (bench.py)
# ------------------------------------------------------------------
cat > bench.py << 'EOF'
#!/usr/bin/env python
"""
Offline inference benchmark for Llama‑3.1‑8B with vLLM on Frontier.
Generates 50 short prompts, each limited to 50 output tokens.
"""

from vllm import LLM, SamplingParams

# 50 dummy prompts – replace with real data if desired
prompts = [f"Prompt #{i+1}: Explain the significance of quantum entanglement in 1 sentence."
           for i in range(50)]

llm = LLM(
    model="/lustre/orion/csc708/scratch/hzheng/models/llama-3.1-8b",
    dtype="bfloat16",
    tensor_parallel_size=4,          # 4 GPUs on the node
    enforce_eager=True,
    gpu_memory_utilization=0.85,
)

sampling_params = SamplingParams(max_tokens=50)

outputs = llm.generate(prompts, sampling_params)

# Print each generated text on its own line
for i, out in enumerate(outputs):
    print(f"[Prompt {i+1}] {out.outputs[0].text}")
EOF

# ------------------------------------------------------------------
# Launch the benchmark with srun
# ------------------------------------------------------------------
srun /lustre/orion/csc708/scratch/hzheng/vllm-rocm-env/bin/python bench.py
```
````
