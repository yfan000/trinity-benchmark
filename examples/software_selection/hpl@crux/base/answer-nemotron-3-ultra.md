# nemotron-3-ultra — hpl@crux, base arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected Application: HPL**

**Why it fits:**
- **HPL (High Performance LINPACK)** is the canonical implementation of the Linpack benchmark used worldwide for dense linear algebra performance measurement (e.g., TOP500 rankings).
- The workload explicitly requests a "Linpack-style" dense linear algebra benchmark, which is exactly what HPL provides.
- The installed build is **CPU-only**, matching Crux's AMD EPYC CPU-only architecture.
- It is designed to run on a single node (or scale across nodes) and can be tuned for the node's memory and core count — consistent with the pre-existing, group-tuned input file in the working directory.
````
