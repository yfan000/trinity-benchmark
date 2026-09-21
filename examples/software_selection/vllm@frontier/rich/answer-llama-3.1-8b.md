# llama-3.1-8b — vllm@frontier, rich arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
Based on the given workload and system specifications, I recommend using the "vLLM (ROCm)" application for serving large language model inference at increased concurrency on the Frontier system.

vLLM (ROCm) is specifically validated for the Frontier system and the AMD MI250X architecture, which aligns with the system's hardware. It has also been previously validated for serving LLaMA-3.1-8B inference on the same system, achieving 271.5 tok/s at concurrency=16 with tensor parallelism=8. This suggests that vLLM (ROCm) has been optimized for the Frontier system and is well-suited for large language model inference workloads.

Additionally, vLLM (ROCm) is designed to take advantage of the ROCm (Radeon Open Compute) platform, which is the open-source computing platform for AMD GPUs. This platform provides a set of tools and libraries that are optimized for AMD GPUs, including the MI250X.

Given the system's hardware and the workload's requirements, vLLM (ROCm) is the most suitable application for serving large language model inference at increased concurrency on the Frontier system.
````
