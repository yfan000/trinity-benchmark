# Reference answer — vllm@frontier

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
Selected application: vLLM (ROCm)

Reason: vLLM (ROCm) is the only installed application purpose-built for LLM inference serving on Frontier's AMD MI250X GPUs. It has been validated on this exact system with LLaMA-3.1-8B using tensor parallelism across 8 GCDs (TP=8), producing the throughput numbers cited in the workload (38.9/102.5/271.5 tok/s at c=1/4/16). Scaling to higher concurrency is a direct extension of this validated configuration. No other catalog entry addresses LLM inference serving; alternatives such as pytorch or deepspeed are general frameworks without the batched inference scheduling that vLLM provides. The ROCm build is confirmed working on Frontier (build_status: built, version 0.9.2rc2.dev1802+rocm).
````
