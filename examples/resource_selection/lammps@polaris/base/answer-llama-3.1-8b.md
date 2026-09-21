# llama-3.1-8b — lammps@polaris, base arm

Resource selection. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 4 of 10 requirements violated).

````
Based on the provided workload and system specifications, we can determine the PBS Pro resource specification as follows:

**Step 1: Derive the walltime**

The workload involves 500,000 atoms, and we are given that the simulation will run for 100,000 timesteps. Assuming a constant simulation time per timestep, we can estimate the total walltime required.

The Lennard-Jones potential is typically calculated using a Verlet algorithm, which requires 2-3 timesteps per time unit (e.g., fs). Assuming 2.5 timesteps per time unit, the total simulation time would be approximately 100,000 / 2.5 = 40,000 time units.

A typical Lennard-Jones simulation on a modern GPU cluster might require around 1-2 nanoseconds (ns) per time unit, depending on the specific implementation and hardware. Assuming an average of 1.5 ns per time unit, the total simulation time would be approximately 40,000 × 1.5 = 60,000 ns.

Converting this to seconds, we get 60,000 ns / 1,000,000,000 ns/s = 0.06 seconds. However, this is a highly optimistic estimate, and the actual walltime required might be significantly longer. To account for this, we will add a 10x margin to the estimated walltime.

Walltime = 0.06 s × 10 = 0.6 s

However, this walltime is far too short for a typical simulation. Let's assume that each timestep takes around 1-10 microseconds (μs) per atom, depending on the specific implementation and hardware. For 500,000 atoms, this would be around 500,000 × 1-10 μs = 500,000-5,000,000 μs or 0.5-5 seconds.

To account for the actual walltime required, let's assume an average of 2.5 seconds per timestep for 500,000 atoms. With 100,000 timesteps, the total walltime would be approximately 100,000 × 2.5 = 25,000 seconds.

Adding a 10x margin to this estimated walltime, we get:

Walltime = 25,000 s × 10 = 250,000 s

Converting this to hours, we get 250,000 s / 3600 s/h = 69.44 hours.

**Step 2: Eliminate queues with insufficient walltime or node range**

| Queue | Node Minimum | Node Maximum | Maximum Walltime | Passes |
| --- | --- | --- | --- | --- |
| debug | 1 | 2 | 1h | FAIL |
| debug-scaling | 1 | 10 | 1h | FAIL |
| prod | 10 | 496 | 24h | PASS |
| demand | 1 | 56 | 1h | FAIL |
| preemptable | 1 | 10 | 72h | PASS |
| capacity | 1 | 4 | 168h | PASS |

**Step 3: Choose a queue**

Based on the available queues, we can choose either the prod or preemptable queue. Both queues have sufficient walltime and node range to accommodate our simulation.

**Queue selection**

We will choose the prod queue, as it has a higher node maximum and a longer maximum walltime.

**Node count**

Based on the system specifications, we can choose a node count that is within the prod queue's node range. We will choose 256 nodes, which is within the prod queue's node range of 10-496 nodes.

**Ranks per node and GPUs per rank**

Based on the build defaults, we will use 4 ranks per node and 1 GPU per rank.

**Total ranks**

Total ranks = nodes × ranks per node = 256 × 4 = 1024

**Resource specification**

Based on the above calculations, the PBS Pro resource specification for the simulation is:

* Nodes: 256
* Ranks per node: 4
* Total ranks: 1024
* GPUs per node: 1
* Walltime: 250,000 s (or 69.44 hours)
* Queue: prod

**Scaling guidance**

The scaling guidance suggests using Kokkos GPU backend for acceleration and 4 MPI ranks per node with 1 GPU each. This is consistent with our chosen resource specification.

**Assumptions and margins**

We assumed an average simulation time per timestep of 2.5 seconds for 500,000 atoms and added a 10x margin to the estimated walltime. We also assumed an average of 2.5 seconds per timestep for 500,000 atoms and added a 10x margin to the estimated walltime.

**Plain restatement of resource specification**

Nodes: 256
Ranks per node: 4
Total ranks: 1024
GPUs per node: 1
Walltime: 250,000 s (or 69.44 hours)
Queue: prod
````
