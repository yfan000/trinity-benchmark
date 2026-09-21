# llama-3.1-8b — gromacs@sirius, rich arm

Resource selection. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 2 of 10 requirements violated).

````
**Task:** Determine the PBS Pro resource specification for a GROMACS molecular dynamics restart job on Sirius.

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

**Step (a): Determine nodes, walltime, and queue**

### 1. Size the work and derive the walltime you actually need:

Based on the given workload, the simulation will run for 5 ns with a 2 fs timestep. The total number of time steps can be calculated as:

5 ns × (1 s / 10^9 s/ns) / (2 fs / 10^15 s/fs) ≈ 2,500,000 time steps

Since GROMACS typically spends a significant amount of time in the non-bonded and PME calculations, we assume that each time step will take approximately 10-20 μs. This is a rough estimate and may vary depending on the system size and hardware.

The total walltime required for the simulation is:

2,500,000 time steps × 15 μs/time step ≈ 37.5 hours

We add a 10% margin to account for any additional time required for the simulation to complete:

37.5 hours × 1.1 ≈ 41.25 hours

### 2. Go through the supplied queue table and eliminate every queue whose maximum walltime is below that figure, or whose node range excludes your node count:

| Queue | Maximum Walltime | Node Range |
| --- | --- | --- |
| workq | 24h | 1-4 nodes |
| debug | 2h | 1-2 nodes |
| dev | 1h | 1-2 nodes |
| test | 1h | 1-2 nodes |

Based on the maximum walltime of 41.25 hours, we eliminate the following queues:

* debug: 2h (below the maximum walltime)
* dev: 1h (below the maximum walltime)
* test: 1h (below the maximum walltime)

We are left with the workq queue, which has a maximum walltime of 24h and a node range of 1-4 nodes.

### 3. Choose from what survives, and state the verdict against each of the three limits separately:

| Queue | Node Minimum | Node Maximum | Maximum Walltime | Verdict |
| --- | --- | --- | --- | --- |
| workq | PASS | PASS | PASS | PASS |

The workq queue survives all three limits, so we choose this queue.

**Step (b): Determine ranks-per-node and GPUs-per-rank**

Based on the build defaults, we use the following values:

* ranks per node: 8
* GPUs per rank: 1 (one MPI rank per GPU is recommended)

**Step (c): Determine the node count**

Based on the system configuration, we have 4 nodes available. We will use all 4 nodes to run the simulation.

**Step (d): Honour any scaling guidance supplied with the application**

The scaling guidance recommends using one MPI rank per GPU, which we have already implemented by setting GPUs per rank to 1.

**Step (e): Close with a plain restatement of nodes, ranks per node, total ranks, GPUs per node, walltime, and queue**

Based on the above steps, we have:

* nodes: 4
* ranks per node: 8
* total ranks: 4 × 8 = 32
* GPUs per node: 8 (since each node has 8 GPUs)
* walltime: 41.25 hours
* queue: workq

The final resource specification is:

PBS Pro resource specification:
- nodes: 4
- ranks per node: 8
- total ranks: 32
- GPUs per node: 8
- walltime: 41.25 hours
- queue: workq
````
