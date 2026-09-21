# Prompt — qe@aurora

Subtask: **Resource selection**. Base arm, exactly as the model received it.

````
Task: Determine the node count, ranks per node, total ranks, GPUs per node, walltime, and queue for a production DFT campaign on Aurora.

Workload:
- Science: 3C-SiC in the zinc-blende structure, 2x2x2 conventional supercell (64 atoms), SCF total-energy calculation, plane-wave cutoff 60 Ry, charge-density cutoff 480 Ry, 4x4x4 Monkhorst-Pack k-grid, PBE functional, ultrasoft pseudopotentials
- Software: Quantum ESPRESSO (already selected)
- Input file: scf.scf.in in /lus/flare/projects/BioFoldX/yamamoto/qe_run
- System: Aurora (ALCF)
- Campaign requirement: must fit within Aurora queue limits for a production run

Target system:
Aurora (ALCF): 10624 nodes, 6 x Intel Data Center GPU Max Series per node, 104 CPU cores per node
  queue debug: 1-2 nodes, max 1h
  queue debug-scaling: 2-256 nodes, max 1h
  queue prod: 256-10624 nodes, max 24h
  queue capacity: 1-16 nodes, max 168h
  queue visualization: 1-32 nodes, max 8h

Build defaults:
  ranks per node (build default): 104
  GPU notes: CPU-only MPI build (Intel MKL FFT). GPU offload via pw_gpu requires NVIDIA; Aurora uses Intel GPUs.
  scaling notes: 104 CPU cores per node. CPU-only build with Intel MKL + ScaLAPACK.

Instructions: Using the workload, the application's scaling behaviour and the system's queue policy, determine nodes, GPUs, ranks per node, walltime and the queue to target. Do NOT write a job script or scheduler directives — give the specification and the reasoning.

(a) CHOOSE A LEGAL QUEUE. Work in this order, and show each step:
    1. Size the work and derive the walltime you actually need;
    2. Go through the supplied queue table and eliminate every queue whose maximum walltime is below that figure, or whose node range excludes your node count, naming for each the limit that rules it out;
    3. Choose from what survives, and state the verdict against each of the three limits separately — node minimum, node maximum, maximum walltime — giving the requested value, the limit and whether it passes. Any clear presentation will do; a table is fine.
  Every one of those three lines must read PASS. If any reads FAIL, the answer is not finished: change the node count, cut the walltime, or move to a queue that admits the request, then redo the check. A request that breaches any limit is rejected by the scheduler at submission and is worth nothing, however well reasoned — never present one as the answer, and never round a walltime up past the cap;
(b) Take ranks-per-node and GPUs-per-rank from the supplied application defaults, which are a property of how the code was built — only the NODE COUNT is the agent's to choose;
(c) Do not claim a timing or throughput figure was measured or observed when the prompt supplies none; state plainly what you assumed and what margin you added;
(d) Honour any scaling guidance supplied with the application, or say why it does not apply to this run;
(e) Close with a plain restatement of nodes, ranks per node, total ranks, GPUs per node, walltime and queue, showing that total ranks = nodes x ranks per node.

Output: Provide the resource specification and the reasoning behind each choice.
````
