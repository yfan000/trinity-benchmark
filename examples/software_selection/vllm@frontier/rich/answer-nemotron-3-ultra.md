# nemotron-3-ultra — vllm@frontier, rich arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected application: vLLM (ROCm)**

**Why it fits:**
- **Purpose-built for LLM inference**: vLLM is specifically designed for high-throughput, low-latency serving of large language models with features like PagedAttention, continuous batching, and optimized CUDA/ROCm kernels.
- **Validated on Frontier**: The software catalog explicitly notes it is validated on Frontier's AMD MI250X GPUs (ROCm) with a measured throughput of **271.5 tok/s** — matching exactly the prior single-node result (concurrency=16, TP=8) for LLaMA-3.1-8B.
- **Scalable concurrency**: vLLM’s continuous batching and efficient memory management are engineered to scale throughput at higher concurrency levels, making it the ideal choice for the stated goal of scaling beyond the validated single-node run.
- **Native ROCm support**: The installed version is ported for AMD MI250X via ROCm, ensuring full hardware utilization on Frontier without additional porting effort.
````
