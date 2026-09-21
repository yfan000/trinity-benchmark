# nemotron-3-ultra — lammps@polaris, base arm

Software selection. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 2 of 4 requirements violated).

````
**Selected Application: GROMACS**

**Reasoning:**  
GROMACS is purpose-built for high-performance classical molecular dynamics of biomolecular systems (proteins, lipids, membranes) and features heavily optimized, GPU-native kernels that excel on NVIDIA A100 GPUs. For a ~500,000-atom lipid–protein membrane system using standard force fields (CHARMM, AMBER, etc.), GROMACS consistently delivers the fastest time-to-solution on Polaris, especially at modest scale (1–few GPUs), minimizing both queue wait and wall-clock time. It is the de facto standard for urgent, production biomolecular MD on GPU clusters.
````
