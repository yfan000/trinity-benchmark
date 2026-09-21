# Prompt — vllm@frontier

Subtask: **Batch job creation**. Base arm, exactly as the model received it.

````
Task: Write a valid Slurm batch script for Frontier that runs an LLM offline inference job and submits it to the scheduler.

Workload:
- Scientific problem: Llama-3.1-8B offline inference, 50 prompts, max_tokens=50, tensor parallel size 4
- System: Frontier (OLCF), scheduler: Slurm
- Working directory: /lustre/orion/NuclearMPX/scratch/jmartinez/vllm_run
- Project allocation to charge: CHM202
- Resources decided: 1 node, walltime 00:30:00, queue: debug
- Model path: /lustre/orion/csc708/scratch/hzheng/models/llama-3.1-8b

Software environment:
```
#!/bin/bash -l  # REQUIRED — module command unavailable without login shell
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
modules: PrgEnv-amd, rocm, miniforge3
```
launch command FORM (the filenames, prompt list, and parameters shown are catalog smoke-test placeholders — substitute the workload's model, 50 prompts, max_tokens=50, and tensor_parallel_size from the Workload above):
```
# Write to bench.py then: python bench.py
if __name__ == '__main__':
    from vllm import LLM, SamplingParams
    llm = LLM(
        model="/lustre/orion/csc708/scratch/hzheng/models/llama-3.1-8b",
        dtype="bfloat16",
        tensor_parallel_size=8,   # all 8 GCDs on one node
        enforce_eager=True,
        gpu_memory_utilization=0.85,
    )
    outputs = llm.generate(["Hello, HPC!"], SamplingParams(max_tokens=64))
    print(outputs[0].outputs[0].text)
```
binary: /lustre/orion/csc708/scratch/hzheng/vllm-rocm-env/bin/python

Scheduler conventions:
- Frontier (OLCF) uses Slurm. The debug queue is a QOS flag, not a partition: `#SBATCH -q debug`; pair it with `#SBATCH -p batch` as the partition.
- Account is specified as `#SBATCH -A <project>` (no suffix required on Frontier).
- Launch with `srun`, not mpiexec.
- Any output directory referenced by -o/-e must already exist; create it in the script before the launch step.
- Node allocation is exclusive; do not add per-GPU sub-node resource directives beyond what the worked example shows.

Worked example (DIFFERENT application — do NOT copy its resource numbers):
```
# source: https://docs.nersc.gov/jobs/examples/
#!/bin/bash
#SBATCH --qos=debug
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=32
#SBATCH --constraint=gpu
#SBATCH --gpus-per-node=4
#SBATCH -AmXXXX

#
# cray-mpich and cray-libsci conflict with openmpi so will automatically be unloaded.
#
module load openmpi

srun --mpi=pmix -n 64 ring_c
```

Instructions: Write a valid Slurm batch script for Frontier that (a) requests resources in exactly the form the supplied site conventions and worked example demonstrate, including every element they show, and adds no per-chunk resource they omit, since nodes on these systems are allocated exclusively; (b) includes the full boilerplate: a job-name directive, output and error directives pointing at concrete paths under the stated working directory, an explicit change into that working directory using the scheduler's own variable rather than a hardcoded path, and creation of any directory those paths reference; (c) sets up the software environment using the supplied module and environment lines verbatim; and (d) writes bench.py inline and launches it with the correct binary, substituting the workload's tensor_parallel_size, 50 prompts, and max_tokens=50 in place of the catalog's smoke-test values.

Output: Return the complete batch script.
````
