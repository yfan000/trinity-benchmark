# llama-3.1-8b — qmcpack@aurora, rich arm

Resource selection. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 1 of 10 requirements violated).

````
**Resource Specification**

- Nodes: 1024
- Ranks per node: 6
- Total Ranks: 6144
- GPUs per node: 6
- Walltime: 12h
- Queue: prod

**Reasoning**

**(a) Choosing a legal queue**

1. **Size the work and derive the walltime you actually need**:

- Number of atoms: 64
- Number of walkers: 4096
- Number of DMC blocks: 200
- Timestep: 0.005 Ha^-1
- Assuming 1 hour of walltime per 100 DMC blocks (a rough estimate for diffusion Monte Carlo), the walltime needed is approximately:
  200 blocks / 100 blocks/hour = 2 hours
  However, we also need to account for the time it takes to load the Slater-Jastrow trial wavefunction from a prior DFT run, which is not specified. To be safe, we'll add a 50% margin to the walltime:
  2 hours * 1.5 = 3 hours

However, this walltime is too short to complete the job. We need to increase the walltime to 12 hours to account for the time it takes to complete the diffusion Monte Carlo simulation.

2. **Go through the supplied queue table and eliminate every queue whose maximum walltime is below that figure, or whose node range excludes your node count**:

| Queue | Node Range | Max Walltime |
| --- | --- | --- |
| debug | 1-2 nodes | 1h |
| debug-scaling | 2-256 nodes | 1h |
| prod | 256-10624 nodes | 24h |
| capacity | 1-16 nodes | 168h |
| visualization | 1-32 nodes | 8h |

Eliminating queues with maximum walltime below 12 hours or node range excluding our node count:

- Eliminate debug, debug-scaling, visualization, and capacity queues
- Keep prod queue

3. **Choose from what survives**:

| Queue | Node Minimum | Node Maximum | Max Walltime | Verdict |
| --- | --- | --- | --- | --- |
| prod | 256 nodes | 10624 nodes | 24h | PASS (node minimum), PASS (node maximum), FAIL (walltime) |
| prod | 256 nodes | 10624 nodes | 24h |  | PASS (node minimum), PASS (node maximum), PASS (walltime) with 12h |

We need to choose a queue that allows for 256 nodes (our required node count) and has a maximum walltime of at least 12 hours. The prod queue meets these requirements.

**(b) Ranks per node and GPUs per rank**

- Ranks per node: 6 (build default)
- GPUs per rank: 1 (since we're using Intel Data Center GPU Max Series via SYCL offload)

**(c) Walltime assumption**

We assumed 1 hour of walltime per 100 DMC blocks for the diffusion Monte Carlo simulation and added a 50% margin to the walltime.

**(d) Scaling guidance**

No scaling guidance was provided for this run.

**(e) Resource specification**

- Nodes: 1024
- Ranks per node: 6
- Total Ranks: 6144
- GPUs per node: 6
- Walltime: 12h
- Queue: prod
````
