# llama-3.1-8b — qe@aurora, base arm

Resource selection. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 1 of 10 requirements violated).

````
**Workload and System Details**

- Science: 3C-SiC in the zinc-blende structure, 2x2x2 conventional supercell (64 atoms), SCF total-energy calculation
- Software: Quantum ESPRESSO (already selected)
- Input file: scf.scf.in in /lus/flare/projects/BioFoldX/yamamoto/qe_run
- System: Aurora (ALCF)
- Application defaults:
  - Ranks per node: 104
  - GPU notes: CPU-only MPI build (Intel MKL FFT). GPU offload via pw_gpu requires NVIDIA; Aurora uses Intel GPUs.
  - Scaling notes: 104 CPU cores per node. CPU-only build with Intel MKL + ScaLAPACK.

**Step 1: Derive the walltime needed**

Assuming a typical SCF calculation for a 64-atom system, we can estimate the walltime needed. Let's assume 10 minutes per SCF iteration, and 5 iterations for convergence. This gives us a total walltime of:

10 minutes/iteration * 5 iterations = 50 minutes

However, to be safe, let's add a 10% margin:

50 minutes * 1.1 = 55 minutes

Converting this to hours, we get:

55 minutes / 60 = 0.917 hours

Rounding down to the nearest hour (since we can't use a fraction of an hour), we get:

0.917 hours ≈ 1 hour

However, this is below the minimum walltime required for a production run (24 hours). Let's assume a more complex calculation that requires 10 hours of walltime.

**Step 2: Eliminate queues that don't meet the walltime or node requirements**

| Queue | Node Range | Max Walltime | Eliminated |
| --- | --- | --- | --- |
| debug | 1-2 nodes | 1h | FAIL (walltime) |
| debug-scaling | 2-256 nodes | 1h | FAIL (walltime) |
| capacity | 1-16 nodes | 168h | FAIL (node range) |
| visualization | 1-32 nodes | 8h | FAIL (walltime) |
| prod | 256-10624 nodes | 24h | PASS |

**Step 3: Choose the queue**

We are left with the prod queue, which meets all the requirements.

**Queue Verdict**

- Node minimum: 256 nodes (PASS)
- Node maximum: 10624 nodes (PASS)
- Maximum walltime: 24 hours (PASS)

**Step 4: Determine ranks per node and GPUs per node**

We will use the application defaults:

- Ranks per node: 104
- GPUs per node: 0 (CPU-only build)

**Resource Specification**

- Nodes: 256
- Ranks per node: 104
- Total ranks: 256 x 104 = 26624
- GPUs per node: 0
- Walltime: 24 hours
- Queue: prod

**Reasoning**

We chose the prod queue because it meets all the requirements: node range, walltime, and maximum walltime. We used the application defaults for ranks per node and GPUs per node. We assumed a more complex calculation that requires 10 hours of walltime, but rounded down to the nearest hour (24 hours) to meet the queue requirements.
````
