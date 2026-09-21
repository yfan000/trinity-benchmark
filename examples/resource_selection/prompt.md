# Prompt — lammps@polaris

Subtask: **Resource selection**. Base arm, exactly as the model received it.

````
Task: Determine the PBS Pro resource specification — nodes, GPUs per node, MPI ranks per node, total ranks, walltime, and queue — for the workload described below on Polaris.

Workload:
  Problem: Lennard-Jones argon, 500,000 atoms on an fcc lattice, reduced density 0.8442, reduced temperature 0.72, NVE, 100,000 timesteps, cutoff 2.5 sigma
  Software: LAMMPS
  System: Polaris (ALCF)
  Working directory: /eagle/QuantumMatX/lchen/lammps_run
  Prior runs on this machine: none (first run of this workload on this system)

Target system:
  Polaris (ALCF): 560 nodes, 4 x A100 per node, 32 CPU cores per node
    queue debug:         1-2 nodes,   max 1h
    queue debug-scaling: 1-10 nodes,  max 1h
    queue prod:          10-496 nodes, max 24h
    queue demand:        1-56 nodes,  max 1h
    queue preemptable:   1-10 nodes,  max 72h
    queue capacity:      1-4 nodes,   max 168h

Build defaults:
  ranks per node (build default): 4
  GPU notes: Via Kokkos backend (-k on g <ngpus> -sf kk -pk kokkos)
  scaling notes: Use Kokkos GPU backend for acceleration. 4 MPI ranks per node with 1 GPU each. Scale nodes for large systems (>1M atoms).

Instructions: Using the workload, the application's scaling behaviour, and the system's queue policy, determine nodes, GPUs per node, ranks per node, total ranks, walltime, and queue. Do NOT write a job script or scheduler directives — give the specification and the reasoning.

(a) CHOOSE A LEGAL QUEUE. Work in this order, and show each step:
  1. Size the work and derive the walltime you actually need;
  2. Go through the supplied queue table and eliminate every queue whose maximum walltime is below that figure, or whose node range excludes your node count, naming for each the limit that rules it out;
  3. Choose from what survives, and state the verdict against each of the three limits separately — node minimum, node maximum, maximum walltime — giving the requested value, the limit, and whether it passes. Any clear presentation will do; a table is fine.
  Every one of those three lines must read PASS. If any reads FAIL, the answer is not finished: change the node count, cut the walltime, or move to a queue that admits the request, then redo the check. A request that breaches any limit is rejected by the scheduler at submission and is worth nothing, however well reasoned — never present one as the answer, and never round a walltime up past the cap.

(b) Take ranks-per-node and GPUs-per-rank from the supplied build defaults — only the NODE COUNT is yours to choose.

(c) Do not claim a timing or throughput figure was measured or observed when none is supplied; state plainly what you assumed and what margin you added.

(d) Honour any scaling guidance supplied with the application, or say why it does not apply to this run.

(e) Close with a plain restatement of nodes, ranks per node, total ranks, GPUs per node, walltime, and queue, showing that total ranks = nodes × ranks per node.

Output: Provide the resource specification and the reasoning behind each choice.
````
