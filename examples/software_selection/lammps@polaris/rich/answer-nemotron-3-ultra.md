# nemotron-3-ultra — lammps@polaris, rich arm

Software selection. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 2 of 4 requirements violated).

````
**Selected application: GROMACS**

**Why it fits:**
- **Workload match:** GROMACS is purpose-built for high-performance classical force-field molecular dynamics of biomolecular systems (proteins, lipids, membranes). It directly consumes the described input files (force-field parameters, coordinate/topology files) and is the de facto standard for lipid–protein membrane simulations.
- **Hardware alignment:** The Polaris A100 GPUs are explicitly targeted by GROMACS’ highly optimized CUDA kernels, which deliver industry-leading throughput for systems of ~500k atoms. It achieves near-peak GPU utilization with minimal CPU overhead.
- **Turnaround priority:** GROMACS’ single-node and multi-GPU scaling on A100 provides the shortest time-to-solution for production MD runs. Its mature, battle-tested code path minimizes setup friction and queue wait (widely available, no exotic dependencies), ensuring the urgent result deadline is met.
````
