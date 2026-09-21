# nemotron-3-ultra — vllm@frontier, base arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected application: vLLM (ROCm)**

**Why it fits:**
- **Directly validated on Frontier for this exact workload**: The software catalog explicitly notes vLLM (ROCm) was validated on Frontier's AMD MI250X GPUs with a measured throughput of **271.5 tok/s** — matching the user's prior single-node result (concurrency=16, TP=8) for LLaMA-3.1-8B.
- **Purpose-built for high-concurrency LLM inference**: vLLM implements PagedAttention, continuous batching, and optimized tensor parallelism — key for scaling throughput at higher concurrency.
- **Native ROCm support**: Tailored for AMD MI250X on Frontier, ensuring full GPU utilization without translation overhead.
- **Proven scalability path**: The existing validation at TP=8 provides a baseline for multi-node scaling via pipeline/data parallelism.
````
