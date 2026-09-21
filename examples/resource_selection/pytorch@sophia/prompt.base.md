# Prompt — pytorch@sophia

Subtask: **Resource selection**. Base arm, exactly as the model received it.

````
**Task:** Determine the PBS Pro resource specification — nodes, GPUs, ranks per node, total ranks, walltime, and queue — for a distributed deep-learning training job on Sophia.

**Workload:**
- Problem: ResNet-50 image classification on a 100,000-image subset, batch size 256 per GPU, mixed precision, 10 epochs
- Framework chosen: PyTorch (MPI)
- Working directory: /eagle/MatGenome/nsvensson/pytorch_run
- System: Sophia (ALCF)
- No prior timing measurements exist for this configuration on this system

**Target system:**
Sophia (ALCF): 24 nodes, 8 × A100 per node, ? CPU cores per node
  queue by-gpu:  1–1 nodes, max 24 h
  queue by-node: 1–8 nodes, max 24 h
  queue bigmem:  1–1 nodes, max 24 h

**Build defaults:**
GPU notes: CUDA 12.4, A100 (sm_80). MPI + NCCL + Gloo backends. Use NCCL for GPU collectives (conda OpenMPI is not CUDA-aware). LD_LIBRARY_PATH must include /usr/lib64 for libcuda.so on compute nodes.

**Instructions:** Using the workload, the application's scaling behaviour, and the system's queue policy, determine nodes, GPUs, ranks per node, walltime, and the queue to target. Do NOT write a job script or scheduler directives — give the specification and the reasoning.

You must:
(a) CHOOSE A LEGAL QUEUE. Work in this order, and show each step:
    1. Size the work and derive the walltime you actually need;
    2. Go through the supplied queue table and eliminate every queue whose maximum walltime is below that figure, or whose node range excludes your node count, naming for each the limit that rules it out;
    3. Choose from what survives, and state the verdict against each of the three limits separately — node minimum, node maximum, maximum walltime — giving the requested value, the limit, and whether it passes. Any clear presentation will do; a table is fine.
  Every one of those three lines must read PASS. If any reads FAIL, the answer is not finished: change the node count, cut the walltime, or move to a queue that admits the request, then redo the check. A request that breaches any limit is rejected by the scheduler at submission and is worth nothing, however well reasoned — never present one as the answer, and never round a walltime up past the cap;
(b) Take ranks-per-node and GPUs-per-rank from the supplied application defaults, which are a property of how the code was built — only the NODE COUNT is the agent's to choose;
(c) Do not claim a timing or throughput figure was measured or observed when the prompt supplies none; state plainly what you assumed and what margin you added;
(d) Honour any scaling guidance supplied with the application, or say why it does not apply to this run;
(e) Close with a plain restatement of nodes, ranks per node, total ranks, GPUs per node, walltime, and queue, showing that total ranks = nodes × ranks per node.

**Output:** Provide the resource specification and the reasoning behind each choice.
````
