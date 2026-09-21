# Prompt — vllm@frontier

Subtask: **Resource selection**. Base arm, exactly as the model received it.

````
Task: Determine the node count, GPU count, ranks per node, total ranks, walltime, and queue for a batch job on Frontier.

Workload:
- Problem: Llama-3.1-8B offline inference, 50 prompts, max_tokens=50, tensor parallel size 4
- System: Frontier (OLCF)
- Working directory: /lustre/orion/AstroLENS/scratch/kwong/vllm_run
- Prior measurement: server startup ~165 s; validated throughput at TP=8 on 1 node

Target system:
  Frontier (OLCF): 9408 nodes, 8 x MI250X per node, 64 CPU cores per node
    queue batch: 1-9280 nodes, max 24h
    queue debug: max 2h
    queue extended: 1-64 nodes, max 24h
    queue g1: 1-2 nodes, max 2h
    queue service: 1-1 nodes, max 24h

Build defaults:
  GPU notes: AMD MI250X via ROCm 6.2.4. Each node has 4x MI250X = 8 GCD devices. torch.hip = 6.1.40091 (torch+rocm6.1 against ROCm 6.2.4 runtime — compatible). VALIDATED 2026-05-11 (Slurm job 4567519, node frontier10177/10178): - vLL
  sizing defaults: nodes=1, partition=g1, ranks-per-node=8 (one per GCD)

Instructions: Using the workload, the application's scaling behaviour and the system's queue policy, determine nodes, GPUs, ranks per node, walltime and the queue to target. Do NOT write a job script or scheduler directives — give the specification and the reasoning.

(a) CHOOSE A LEGAL QUEUE. Work in this order, and show each step:
      1. Size the work and derive the walltime you actually need;
      2. Go through the supplied queue table and eliminate every queue whose maximum walltime is below that figure, or whose node range excludes your node count, naming for each the limit that rules it out;
      3. Choose from what survives, and state the verdict against each of the three limits separately — node minimum, node maximum, maximum walltime — giving the requested value, the limit and whether it passes. Any clear presentation will do; a table is fine.
    Every one of those three lines must read PASS. If any reads FAIL, the answer is not finished: change the node count, cut the walltime, or move to a queue that admits the request, then redo the check. A request that breaches any limit is rejected by the scheduler at submission and is worth nothing, however well reasoned — never present one as the answer, and never round a walltime up past the cap.

(b) Take ranks-per-node and GPUs-per-rank from the supplied application defaults, which are a property of how the code was built — only the NODE COUNT is the agent's to choose.

(c) Do not claim a timing or throughput figure was measured or observed when the prompt supplies none; state plainly what you assumed and what margin you added.

(d) Honour any scaling guidance supplied with the application, or say why it does not apply to this run.

(e) Close with a plain restatement of nodes, ranks per node, total ranks, GPUs per node, walltime and queue, showing that total ranks = nodes x ranks per node.

Note: this workload is being ported from an ALCF system running PBS Pro. Frontier runs Slurm; use Slurm directives and launcher conventions throughout — never PBS.

Output: Provide the resource specification and the reasoning behind each choice.
````
