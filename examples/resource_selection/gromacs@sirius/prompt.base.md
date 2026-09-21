# Prompt — gromacs@sirius

Subtask: **Resource selection**. Base arm, exactly as the model received it.

````
**Task:** Determine the PBS Pro resource specification — nodes, GPUs, ranks per node, total ranks, walltime, and queue — for a GROMACS molecular dynamics restart job on Sirius.

**Workload:**
- Science: hen egg-white lysozyme solvated in TIP3P water with 0.15 M NaCl, ~34,000 atoms, NPT at 300 K, 2 fs timestep, PME, 5 ns production
- Software: GROMACS (already selected)
- Input: run.tpr in /lus/tegu/projects/BioFoldX/bkowalski/gromacs_run (restart from checkpoint; a previous run was interrupted and a checkpoint file is present)
- System: Sirius (ALCF)
- No prior throughput measurement is available for this system and system size

**Target system:**
Sirius (ALCF): 4 nodes, 4 x A100-SXM4-40GB per node, 64 CPU cores per node
  queue workq: 1–4 nodes, max 24h

**Build defaults:**
- ranks per node (build default): 8
- GPU notes: CUDA GPU offload for non-bonded, PME, and update kernels on A100. Pass -gpu_id to map MPI ranks to GPUs.
- scaling notes: One MPI rank per GPU is recommended (-ntmpi 8 for 8 GPUs per node). -gpu_id 01234567 maps ranks 0-7 to GPUs 0-7. For CPU-only PME: use -pme cpu -npme 1 with fewer GPU ranks. Multi-node: combine with thread-MPI or standard MPI; set -ntomp for OpenMP threading.

**Instructions:**
Using the workload, the application's scaling behaviour, and the system's queue policy, determine nodes, GPUs, ranks per node, walltime, and the queue to target. Do NOT write a job script or scheduler directives — give the specification and the reasoning.

You must:

(a) CHOOSE A LEGAL QUEUE. Work in this order, and show each step:
  1. Size the work and derive the walltime you actually need;
  2. Go through the supplied queue table and eliminate every queue whose maximum walltime is below that figure, or whose node range excludes your node count, naming for each the limit that rules it out;
  3. Choose from what survives, and state the verdict against each of the three limits separately — node minimum, node maximum, maximum walltime — giving the requested value, the limit, and whether it passes. Any clear presentation will do; a table is fine.
  Every one of those three lines must read PASS. If any reads FAIL, the answer is not finished: change the node count, cut the walltime, or move to a queue that admits the request, then redo the check. A request that breaches any limit is rejected by the scheduler at submission and is worth nothing, however well reasoned — never present one as the answer, and never round a walltime up past the cap.

(b) Take ranks-per-node and GPUs-per-rank from the supplied application defaults, which are a property of how the code was built — only the NODE COUNT is the agent's to choose.

(c) Do not claim a timing or throughput figure was measured or observed when the prompt supplies none; state plainly what you assumed and what margin you added.

(d) Honour any scaling guidance supplied with the application, or say why it does not apply to this run.

(e) Close with a plain restatement of nodes, ranks per node, total ranks, GPUs per node, walltime, and queue, showing that total ranks = nodes × ranks per node.

**Output:** Provide the resource specification and the reasoning behind each choice.
````
