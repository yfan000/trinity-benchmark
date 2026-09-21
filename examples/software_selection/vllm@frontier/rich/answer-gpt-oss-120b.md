# gpt-oss-120b — vllm@frontier, rich arm

Software selection. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 2 of 4 requirements violated).

````
**Selected application:** **vLLM (ROCm)**  

**Why it fits the workload**

| Reason | Detail |
|--------|--------|
| **Purpose‑built for LLM serving** | vLLM is a high‑performance inference engine designed specifically for large language models, handling dynamic batching, speculative decoding, and multi‑GPU tensor parallelism out of the box. |
| **ROCm‑native on Frontier** | The Frontier nodes use AMD MI250X GPUs and the ROCm stack. The installed *vLLM (ROCm)* build runs natively on this hardware, taking full advantage of the GPUs’ compute and memory bandwidth. |
| **Validated performance** | A recent validation on Frontier (2026‑05‑11) showed vLLM achieving **271.5 tokens / s** with **TP=8** and **concurrency = 16** for the LLaMA‑3.1‑8B model—the same configuration you are scaling from. |
| **Scalable concurrency** | vLLM’s dynamic request scheduler automatically aggregates many concurrent inference requests into larger batched kernels, which is exactly what is needed to push beyond the current concurrency = 16 while keeping latency low. |
| **Tensor‑parallel support** | It natively supports tensor‑parallelism (TP=8) across the two MI250X GPUs per node, enabling you to keep the same model partitioning when expanding to multi‑node deployments. |
| **Ease of integration** | vLLM provides a simple Python API / OpenAI‑compatible server, so you can ramp up additional client processes or a multi‑node endpoint without rewriting your inference code. |
| **Community and OLCF support** | Being part of the Frontier software catalog, vLLM receives regular updates and has documented guidance for scaling on OLCF systems, making troubleshooting and performance tuning easier. |

**Conclusion**  
For scaling LLaMA‑3.1‑8B inference to higher concurrency on Frontier, the *vLLM (ROCm)* package is the best‑matched, production‑ready tool already proven on the exact hardware and model you are using. Use its dynamic batching and tensor‑parallel capabilities to increase throughput while maintaining low latency.
````
