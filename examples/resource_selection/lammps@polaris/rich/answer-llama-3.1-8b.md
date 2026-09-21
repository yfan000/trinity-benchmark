# llama-3.1-8b — lammps@polaris, rich arm

Resource selection. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 4 of 10 requirements violated).

````
**Resource specification and reasoning:**

**Workload details:**
- Problem: Lennard-Jones argon, 500,000 atoms on an fcc lattice
- Software: LAMMPS
- System: Polaris (ALCF)
- Working directory: /eagle/QuantumMatX/lchen/lammps_run

**Scaling behaviour:**
- The workload is a large system (>1M atoms), so we should scale nodes for acceleration.

**System queue policy:**
- Queue debug: 1-2 nodes, max 1h
- Queue debug-scaling: 1-10 nodes, max 1h
- Queue prod: 10-496 nodes, max 24h
- Queue demand: 1-56 nodes, max 1h
- Queue preemptable: 1-10 nodes, max 72h
- Queue capacity: 1-4 nodes, max 168h

**Step 1: Size the work and derive the walltime you actually need**
- We assume 100,000 timesteps and 1 timestep per second (a reasonable assumption, but no measurement is provided).
- Total walltime: 100,000 timesteps × 1 second/timestep = 100,000 seconds
- Convert to hours: 100,000 seconds ÷ 3600 = 27.78 hours
- We add a 10% margin for safety: 27.78 hours × 1.1 = 30.57 hours

**Step 2: Eliminate queues with maximum walltime below the figure or node range excluding the node count**
- Queue debug: max 1h (FAIL, walltime)
- Queue debug-scaling: max 1h (FAIL, walltime)
- Queue demand: max 1h (FAIL, walltime)
- Queue preemptable: max 72h (PASS, walltime)
- Queue capacity: max 168h (PASS, walltime)
- Queue prod: max 24h (FAIL, walltime)

**Step 3: Choose from what survives**
- We choose the queue capacity as it has the largest node range and meets the walltime requirement.

**Node count:**
- We have 560 nodes available.

**Queue verdict:**
- Queue: capacity
- Node minimum: 1 (PASS, 1 ≤ 560)
- Node maximum: 4 (PASS, 1 ≤ 560)
- Maximum walltime: 168h (PASS, 30.57h ≤ 168h)

**Ranks per node and GPUs per node:**
- Ranks per node: 4 (build default)
- GPUs per node: 1 (build default, 1 GPU per rank)

**Total ranks:**
- Total ranks = nodes × ranks per node = 560 × 4 = 2240

**Walltime:**
- Walltime: 30.57 hours

**Resource specification:**
- Nodes: 560
- Ranks per node: 4
- Total ranks: 2240
- GPUs per node: 1
- Walltime: 30.57 hours
- Queue: capacity
````
