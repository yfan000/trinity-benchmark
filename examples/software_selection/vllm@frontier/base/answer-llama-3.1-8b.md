# llama-3.1-8b — vllm@frontier, base arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
Based on the provided workload and system specifications, I recommend the installed application "vLLM (ROCm)" as the best fit for serving large language model inference at increased concurrency on the Frontier system.

Here's why:

1. **Architecture compatibility**: vLLM (ROCm) is specifically ported for the AMD MI250X on Frontier, ensuring native support for the system's architecture.
2. **Previous validation**: vLLM (ROCm) has been validated on Frontier, with a previous run achieving 271.5 tok/s at concurrency=16 and tensor parallelism=8. This suggests that the application has been optimized for the system and can handle high concurrency.
3. **Performance**: The previous validation run indicates that vLLM (ROCm) can handle high concurrency, making it a suitable choice for scaling LLM inference serving to higher concurrency levels.
4. **LLM inference**: vLLM (ROCm) is designed for inference tasks, which aligns with the workload of serving LLaMA-3.1-8B.

Considering these factors, vLLM (ROCm) appears to be the most suitable application for serving large language model inference at increased concurrency on the Frontier system.
````
