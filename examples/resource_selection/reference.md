# Reference answer — lammps@polaris

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
Resource specification and reasoning:

(a) Queue selection — step by step

Step 1 — Walltime estimate.
This is the first run of this workload on Polaris, so no measured throughput is available. The system is 500,000 atoms — below the >1 M atom threshold cited in the scaling notes as the point where multi-node scaling becomes the primary driver. At 1 node / 4 A100 GPUs, LAMMPS Kokkos routinely sustains several hundred to a few thousand timesteps per second for a Lennard-Jones system of this size. A conservative assumption of ~500 ts/s gives 100,000 / 500 = 200 s of compute. Adding a generous safety margin (setup, I/O, uncertainty) brings the estimate to ~1,800 s (30 minutes). A 30-minute walltime is used as the target; it must not exceed any queue cap.

Step 2 — Eliminate queues.
Node count chosen (see reasoning below): 1 node.
  - debug:         1-2 nodes, max 1h (3600 s). Node range includes 1; walltime 1800 s ≤ 3600 s. NOT eliminated.
  - debug-scaling: 1-10 nodes, max 1h. Same — NOT eliminated, but max-1-job-per-user restriction noted.
  - prod:          min 10 nodes — ELIMINATES (node minimum 10 > requested 1).
  - demand:        by request only — functionally unavailable without prior approval. ELIMINATED on access grounds.
  - preemptable:   1-10 nodes, max 72h. NOT eliminated on limits alone, but jobs are killed without warning; unsuitable for a first diagnostic run.
  - capacity:      1-4 nodes, max 168h. NOT eliminated on limits.

Surviving candidates after hard-limit filtering: debug, debug-scaling, capacity.
For a first exploratory run the debug queue is the natural choice: designed for exactly this purpose, no special access required, no preemption risk, no per-user job-count squeeze (debug-scaling allows only 1 job queued/running).

Step 3 — Compliance check for debug queue with 1 node, 1800 s walltime.
  Node minimum  : requested 1, limit 1  → PASS
  Node maximum  : requested 1, limit 2  → PASS
  Max walltime  : requested 1800 s, limit 3600 s → PASS

All three lines read PASS. The selection is valid.

(b) Ranks per node and GPUs per rank — from build defaults.
The build defaults specify 4 MPI ranks per node with 1 GPU each, confirmed by the Kokkos flag pattern '-k on g <ngpus>'. These are fixed by how the code was built and installed; they are not the agent's to choose. Therefore: ranks per node = 4, GPUs per rank = 1, GPUs per node = 4 (all four A100s used).

(c) Timing assumption.
No measured throughput was available. The walltime was estimated from a conservative lower-bound performance figure (500 ts/s) plus a safety margin roughly 9× the raw compute time, totalling 1800 s. This is an assumption, not a measurement.

(d) Scaling guidance.
The scaling notes say to scale nodes for systems larger than 1 M atoms. This system has 500,000 atoms, which is below that threshold. Running on 1 node is consistent with the guidance. Multi-node scaling may be explored in follow-on runs once single-node performance is confirmed.

(e) Final specification.
  Nodes:          1
  Ranks per node: 4  (build default)
  Total ranks:    1 × 4 = 4
  GPUs per node:  4  (1 per rank, Kokkos backend)
  Walltime:       1800 s (30 minutes)
  Queue:          debug

Total ranks = nodes × ranks per node = 1 × 4 = 4. ✓
````
