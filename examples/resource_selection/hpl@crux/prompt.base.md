# Prompt — hpl@crux

Subtask: **Resource selection**. Base arm, exactly as the model received it.

````
Task: Determine the PBS Pro resource specification — nodes, GPUs per node, ranks per node, total ranks, walltime, and queue — for a deadline-sensitive HPL LINPACK run on Crux.

Workload:
- Problem: HPL LINPACK, problem size N=50000, block size NB=232, 2x2 process grid
- System: Crux (ALCF)
- Working directory: /eagle/CosmoSurvey/dokafor/hpl_run
- Turnaround is the priority; the run must complete as quickly as possible
- Software selected: HPL; input file HPL.dat is present in the working directory

Target system:
  Crux (ALCF): 256 nodes, 0 x  per node, 128 CPU cores per node
    queue debug:       1-8 nodes,   max 1h
    queue workq-route: 1-184 nodes, max 24h
    queue preemptable: 1-10 nodes,  max 72h
    queue demand:      1-64 nodes,  max 1h

Build defaults:
  ranks per node (build default): 128
  scaling notes: CPU-only benchmark. Maximize performance by using all 128 cores per node. Tune N, NB, P, Q parameters in HPL.dat for Crux node memory (512 GB/node).

Instructions: Using the workload, the application's scaling behaviour, and the system's queue policy, determine nodes, GPUs, ranks per node, walltime and the queue to target. Do NOT write a job script or scheduler directives — give the specification and the reasoning.

(a) CHOOSE A LEGAL QUEUE. Work in this order, and show each step:
  1. Size the work and derive the walltime you actually need;
  2. Go through the supplied queue table and eliminate every queue whose maximum walltime is below that figure, or whose node range excludes your node count, naming for each the limit that rules it out;
  3. Choose from what survives, and state the verdict against each of the three limits separately — node minimum, node maximum, maximum walltime — giving the requested value, the limit, and whether it passes. Any clear presentation will do; a table is fine.
  Every one of those three lines must read PASS. If any reads FAIL, the answer is not finished: change the node count, cut the walltime, or move to a queue that admits the request, then redo the check. A request that breaches any limit is rejected by the scheduler at submission and is worth nothing, however well reasoned — never present one as the answer, and never round a walltime up past the cap.

(b) Take ranks-per-node and GPUs-per-rank from the supplied application defaults, which are a property of how the code was built — only the NODE COUNT is the agent's to choose.

(c) Do not claim a timing or throughput figure was measured or observed when the prompt supplies none; state plainly what you assumed and what margin you added.

(d) Honour any scaling guidance supplied with the application, or say why it does not apply to this run.

(e) Close with a plain restatement of nodes, ranks per node, total ranks, GPUs per node, walltime and queue, showing that total ranks = nodes × ranks per node.

Output: Provide the resource specification and the reasoning behind each choice.
````
