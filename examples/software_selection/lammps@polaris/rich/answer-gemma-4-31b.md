# gemma-4-31b — lammps@polaris, rich arm

Software selection. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 2 of 4 requirements violated).

````
**Selected Application:** NAMD

**Reasoning:**
For a classical force-field simulation of a large biomolecular system (~500,000 atoms) on the Polaris A100 GPU cluster, NAMD is the best fit because it is specifically described as a "**GPU-resident** molecular dynamics engine." Unlike some other MD codes that may offload only specific calculations to the GPU, a GPU-resident engine minimizes CPU-GPU data transfer overhead, which is critical for maximizing throughput and achieving the shortest time-to-result for urgent production runs on A100 architecture. While GROMACS, LAMMPS, and OpenMM are also capable, NAMD is highly optimized for large-scale biomolecular membrane systems on ALCF infrastructure.
````
