# gpt-oss-120b — vllm@frontier, base arm

Software selection. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 1 of 4 requirements violated).

````
**Selected application:** **vLLM (ROCm)**  

**Why it fits the workload**

- **Purpose‑built for LLM serving:** vLLM is an inference engine specifically optimized for high‑throughput, low‑latency serving of large language models.  
- **ROCm‑native on Frontier:** The ROCm‑compiled version runs directly on Frontier’s AMD MI250X GPUs, leveraging the full GPU capabilities (HIP, async copy, tensor cores) available on the system.  
- **Proven performance:** The software catalog notes a validated run on Frontier achieving **271.5 tokens / s at concurrency = 16 with TP = 8**, exactly the benchmark you already have. This demonstrates that vLLM can already scale to the concurrency level you need and provides a solid baseline for further scaling (higher concurrency, multi‑node, larger TP).  
- **Scalability features:** vLLM supports dynamic batching, speculative decoding, and distributed tensor‑parallel execution, all of which are essential for increasing concurrency without sacrificing per‑token latency.  
- **Integration with your environment:** The application is already installed and accessible in the default module system, making it straightforward to load and launch (e.g., `module load vllm/rocm`), and it works with the PyTorch and ROCm stack already present on Frontier.

**Conclusion:** For scaling LLaMA‑3.1‑8B inference to higher concurrency on Frontier, the **vLLM (ROCm)** package is the most appropriate choice— it is purpose‑built, GPU‑optimized for the MI250X architecture, and has already demonstrated the required baseline performance on this machine.
````
