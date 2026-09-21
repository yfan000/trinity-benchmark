# gpt-oss-120b — qmcpack@aurora, rich arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected application:** **QMCPACK**

**Why it fits**

- **Purpose‑built for QMC:** QMCPACK is a state‑of‑the‑art Quantum Monte Carlo package that implements variational and diffusion Monte Carlo (VMC/DMC) methods, exactly the workflow described.
- **Native Aurora support:** It is compiled with SYCL/OpenMP offload, allowing direct execution on Aurora’s Intel Data Center GPU (PVC) hardware with high performance.
- **Input compatibility:** QMCPACK reads trial‑wavefunction data from HDF5 files and uses XML driver files for simulation control, matching the prepared inputs you already have.
- **Scalable on large systems:** Designed for strong‑scaling on many‑node GPU clusters, it can exploit the full compute power of the Aurora system for a silicon supercell calculation.
````
