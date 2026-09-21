# Prompt — nwchem@polaris

Subtask: **Resource selection**. Base arm, exactly as the model received it.

````
## Task
Determine the PBS Pro resource specification — nodes, GPUs per node, MPI ranks per node, total ranks, walltime, and queue — for a benchmarking run designed to establish scaling behaviour on Polaris.

## Workload
- Scientific problem: a single water molecule, B3LYP/6-31G* single-point energy, repeated across multiple node counts to characterise scaling
- Goal: scaling benchmark (not production); cover at least a small range of node counts
- Software: NWChem (already selected)
- Input file: run.nw in /eagle/FusionPIC/gpetrov/nwchem_run
- Prior timing: a single-node run of this exact calculation completed in 5 s wall time

## Target system
Polaris (ALCF): 560 nodes, 4 x A100 per node, 32 CPU cores per node
  queue debug: 1-2 nodes, max 1h
  queue debug-scaling: 1-10 nodes, max 1h
  queue prod: 10-496 nodes, max 24h
  queue demand: 1-56 nodes, max 1h
  queue preemptable: 1-10 nodes, max 72h
  queue capacity: 1-4 nodes, max 168h

## Build defaults
- ranks per node (build default): 4
- GPU notes: CPU-only build. GPU support is experimental and not standard in community releases.
- scaling notes: 4 MPI ranks per node. Scale nodes for larger molecular systems. GA (Global Arrays) library handles inter-node communication. Set memory stack/heap/global in input file to avoid OOM errors.

## Instructions
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

## Output
Provide the resource specification and the reasoning behind each choice.
````
