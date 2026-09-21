# nemotron-3-ultra — qe@aurora, rich arm

Software selection. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 2 of 4 requirements violated).

````
**Selected Application: Quantum ESPRESSO**

**Why it fits:**
- **Workload Match:** The workload explicitly describes "Plane-wave density functional theory (DFT) electronic structure calculations" and a "parameter sweep of many similar SCF runs." Quantum ESPRESSO is the canonical plane-wave DFT code in the catalog, listed specifically as a "Plane-wave DFT code for electronic structure calculations on Aurora with Intel oneAPI."
- **Input Format Match:** The input description—"files containing CONTROL, SYSTEM, and ELECTRONS namelists plus atomic species blocks"—is the exact native input structure for Quantum ESPRESSO's `pw.x` executable (e.g., `&CONTROL`, `&SYSTEM`, `&ELECTRONS`, `ATOMIC_SPECIES`, `ATOMIC_POSITIONS`, `K_POINTS`).
- **Architecture Suitability:** The installed version is built with the Intel oneAPI compiler toolchain for Aurora, ensuring optimized performance on Intel Xe GPU (XPU) accelerators via SYCL/DPC++ offload, which is critical for the high-throughput parameter sweep.
- **Directory Context:** The working directory `/lus/flare/projects/BioFoldX/efaraday/run_current` resides on the Aurora Lustre filesystem (`/lus/flare`), which is the intended high-performance storage for such simulation campaigns.
````
