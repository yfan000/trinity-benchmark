# nemotron-3-ultra — hpl@crux, rich arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected Application: HPL**

**Why it fits:**  
HPL (High Performance LINPACK) is the standard benchmark for dense linear algebra performance (Linpack-style) and is explicitly listed as a "CPU-only build" — matching Crux’s AMD EPYC CPU-only architecture. The workload describes a pre‑existing, node‑tuned input file, which aligns with HPL’s typical `HPL.dat` configuration for problem size, block size, and process grid. No other installed code is designed for this specific benchmark purpose.
````
