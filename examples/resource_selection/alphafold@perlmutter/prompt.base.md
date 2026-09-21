# Prompt — alphafold@perlmutter

Subtask: **Resource selection**. Base arm, exactly as the model received it.

````
## Task
Determine the Slurm resource specification — nodes, GPUs, ranks per node, walltime, and queue — for the workload described below on Perlmutter. Do NOT write a job script or scheduler directives; give the specification and the reasoning.

## Workload
Problem: human ubiquitin (UniProt P0CG48), 76-residue monomer, full database search, 5 models with relaxation
Scope: parameter sweep — many similar runs, each predicting the same target independently
Software selected: AlphaFold
Input: run.fasta in working directory /pscratch/sd/j/jmartinez/alphafold_run
System: Perlmutter (NERSC)

## Target System
Perlmutter (NERSC): 3072 nodes, 4 x A100 per node, 64 CPU cores per node
  queue express_amsc: max 6h
  queue debug: 1-8 nodes, max 30min
  queue regular: max 48h
  queue premium: max 48h
  queue shared: max 48h
  queue preempt: 1-128 nodes, max 48h
  queue interactive: 1-4 nodes, max 4h
  queue jupyter: 1-4 nodes, max 6h
  queue overrun: max 48h

## Build Defaults
GPU notes: CUDA GPU required for structure prediction. Single GPU per run typical.
Scaling notes: Single GPU per prediction job. Parallelize by submitting multiple jobs with different FASTA inputs. MSA computation is CPU-intensive before GPU structure prediction.

## Instructions
Using the workload, the application's scaling behaviour, and the system's queue policy, determine nodes, GPUs, ranks per node, walltime, and the queue to target for a single job in this sweep.

(a) CHOOSE A LEGAL QUEUE. Work in this order, and show each step:
  1. Size the work and derive the walltime you actually need;
  2. Go through the supplied queue table and eliminate every queue whose maximum walltime is below that figure, or whose node range excludes your node count, naming for each the limit that rules it out;
  3. Choose from what survives, and state the verdict against each of the three limits separately — node minimum, node maximum, maximum walltime — giving the requested value, the limit, and whether it passes. Any clear presentation will do; a table is fine.
  Every one of those three lines must read PASS. If any reads FAIL, the answer is not finished: change the node count, cut the walltime, or move to a queue that admits the request, then redo the check. A request that breaches any limit is rejected by the scheduler at submission and is worth nothing, however well reasoned — never present one as the answer, and never round a walltime up past the cap.

(b) Take ranks-per-node and GPUs-per-rank from the supplied Build Defaults, which are a property of how the code was built — only the NODE COUNT is yours to choose.

(c) Do not claim a timing or throughput figure was measured or observed when the prompt supplies none; state plainly what you assumed and what margin you added.

(d) Honour any scaling guidance supplied with the application, or say why it does not apply to this run.

(e) Close with a plain restatement of nodes, ranks per node, total ranks, GPUs per node, walltime, and queue, showing that total ranks = nodes × ranks per node.

## Output
Provide the resource specification and the reasoning behind each choice.
````
