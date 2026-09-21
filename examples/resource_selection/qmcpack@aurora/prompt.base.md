# Prompt — qmcpack@aurora

Subtask: **Resource selection**. Base arm, exactly as the model received it.

````
Task: Determine the node count, GPU count, MPI rank count, walltime and queue needed to submit a QMCPACK job on Aurora that reproduces a collaborator's earlier result.

Workload:
- Science: bulk silicon in the diamond structure, 2x2x2 supercell (64 atoms), diffusion Monte Carlo with a Slater-Jastrow trial wavefunction from a prior DFT run, 4096 walkers, timestep 0.005 Ha^-1, 200 DMC blocks
- System: Aurora (ALCF)
- Working directory: /lus/flare/projects/MatGenome/tnakamura/qmcpack_run
- Input files present: qmc.xml, qmc.h5
- Goal: reproduce a collaborator's earlier result on the same system; no prior timing measurement is available

Target system:
Aurora (ALCF): 10624 nodes, 6 x Intel Data Center GPU Max Series per node, 104 CPU cores per node
  queue debug: 1-2 nodes, max 1h
  queue debug-scaling: 2-256 nodes, max 1h
  queue prod: 256-10624 nodes, max 24h
  queue capacity: 1-16 nodes, max 168h
  queue visualization: 1-32 nodes, max 8h

Build defaults:
  ranks per node (build default): 6
  GPU notes: Intel Data Center GPU Max Series via SYCL offload (ENABLE_SYCL=ON, OFFLOAD_TARGET=spir64)
  scaling notes: 6 Intel GPU tiles per node. QMCPACK SYCL build targets spir64 for Intel GPUs.

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
