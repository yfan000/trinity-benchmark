# gemma-4-31b — gromacs@sirius, rich arm

Software selection. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 1 of 4 requirements violated).

````
**Selected Application:** NAMD

**Reasoning:** While GROMACS and LAMMPS are also molecular dynamics packages, NAMD is specifically optimized for high scalability across large numbers of GPU nodes for biomolecular systems. Given that the primary goal of this workload is to establish "scaling behaviour across available GPU nodes" for a biomolecular simulation, NAMD’s architecture is the best fit for high-performance, large-scale GPU distribution on Sirius.
````
