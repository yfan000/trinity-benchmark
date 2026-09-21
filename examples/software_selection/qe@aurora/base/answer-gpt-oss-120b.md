# gpt-oss-120b — qe@aurora, base arm

Software selection. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 2 of 4 requirements violated).

````
**Selected application:** **Quantum ESPRESSO**  

**Why it fits**

- **Plane‑wave DFT focus:** Quantum ESPRESSO is a dedicated plane‑wave density‑functional theory package; its input format (namelists for `&CONTROL`, `&SYSTEM`, `&ELECTRONS`, plus atomic species blocks) matches exactly the files you already have.  
- **Aurora‑optimized build:** The installed version is compiled with the Intel oneAPI compiler and uses SYCL/OpenMP off‑loading, providing native acceleration on Aurora’s Intel Data Center GPUs (PVC/XPU).  
- **Scalable for many independent SCF jobs:** The code scales efficiently with MPI+SYCL, so a parameter sweep of many similar self‑consistent‑field calculations across a set of crystal structures can be run in parallel (e.g., one MPI rank per structure) while fully exploiting the GPU resources.  
- **Supported workflow:** Quantum ESPRESSO integrates well with typical batch‑system scripts on Aurora and can be launched from the working directory `/lus/flare/projects/BioFoldX/efaraday/run_current` without additional conversion of input files.  

Therefore, Quantum ESPRESSO is the best‑matched installed application for your plane‑wave DFT workload on Aurora.
````
