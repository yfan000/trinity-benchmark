# gemma-4-31b — gromacs@sirius, base arm

Software selection. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 1 of 4 requirements violated).

````
**Selected Application:** NAMD

**Reasoning:** While GROMACS and LAMMPS are also molecular dynamics tools, NAMD is specifically engineered for high scalability on large biomolecular systems across multiple GPU nodes. Given the workload's objective to establish "scaling behaviour across available GPU nodes" for a "biomolecular" simulation, NAMD is the most appropriate choice due to its superior parallel efficiency and optimization for large-scale GPU clusters.
````
