# gemma-4-31b — vllm@frontier, base arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected Application:** vLLM (ROCm)

**Reasoning:** 
vLLM is specifically designed for high-throughput LLM inference and is the only application in the provided catalog optimized for serving large language models. It utilizes PagedAttention to manage KV cache memory efficiently, which is critical for scaling concurrency without running out of GPU memory. Furthermore, it is already validated on Frontier's AMD MI250X architecture and was used to achieve the baseline performance metrics (271.5 tok/s) mentioned in the workload.
````
