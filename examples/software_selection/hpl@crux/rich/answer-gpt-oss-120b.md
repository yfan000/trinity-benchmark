# gpt-oss-120b — hpl@crux, rich arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected application:** **HPL – High‑Performance LINPACK benchmark (CPU‑only build)**  

**Why it fits:**  
- HPL is specifically the reference implementation of the LINPACK benchmark, designed to measure the performance of dense linear‑algebra (DGEMM) on a single node.  
- It runs entirely on CPUs, matching Crux’s AMD EPYC CPU‑only architecture.  
- The workload you described (a Linpack‑style dense linear algebra benchmark using a tuned input file) aligns exactly with what HPL expects, so it will use the provided input to configure the problem size for the node’s cores and memory.  

Thus, HPL is the appropriate installed application to execute this benchmark on Crux.
````
