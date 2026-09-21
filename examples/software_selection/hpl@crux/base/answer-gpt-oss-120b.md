# gpt-oss-120b — hpl@crux, base arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected application:** **HPL — High Performance LINPACK benchmark (CPU‑only build)**  

**Why it fits**

- **Purpose‑aligned:** HPL implements the Linpack algorithm, the canonical benchmark for dense linear‑algebra performance on CPUs.  
- **Architecture match:** Crux is an AMD EPYC‑CPU‑only cluster; the HPL build is compiled for CPU‑only execution, making full use of the node’s many cores and memory bandwidth.  
- **Scope:** The workload targets a *single* node, which is exactly how HPL is typically run for per‑node performance measurements.  
- **Input ready:** The working directory already contains a tuned HPL input file (problem size, block size, etc.) customized for the node’s core count and memory, so no additional configuration is needed.  

Therefore, the HPL application is the appropriate choice to run the dense linear‑algebra benchmark on Crux.
````
