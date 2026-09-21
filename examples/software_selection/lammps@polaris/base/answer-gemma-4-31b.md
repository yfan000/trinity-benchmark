# gemma-4-31b — lammps@polaris, base arm

Software selection. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 1 of 4 requirements violated).

````
**Selected Application:** NAMD

**Reasoning:** 
For a classical force-field simulation of a biomolecular system (lipid-protein membrane) with ~500,000 atoms on the Polaris A100 GPU cluster, NAMD is the best choice. Unlike general MD codes, NAMD is specifically designed as a "GPU-resident" engine, meaning it offloads the vast majority of the computation to the GPU to minimize CPU-GPU communication bottlenecks. For a system of this size where "shortest time-to-result" is the priority, NAMD's architecture is optimized for maximum throughput and scalability on A100 nodes.
````
