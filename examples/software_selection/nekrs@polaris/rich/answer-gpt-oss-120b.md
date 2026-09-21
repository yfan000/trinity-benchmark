# gpt-oss-120b — nekrs@polaris, rich arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected application:** **NekRS** – GPU‑accelerated spectral‑element CFD solver (Navier‑Stokes)

**Why it fits**

- **Spectral‑element method:** NekRS is built on the Nek5000 code base and uses the same high‑order spectral‑element discretization that your incompressible Navier‑Stokes simulation requires.  
- **GPU‑ready:** NekRS is specifically optimized for NVIDIA GPUs (including A100) using CUDA, HIP, and MPI, delivering the needed performance on Polaris.  
- **Checkpoint/restart support:** The solver writes binary field/restart files that can be read to resume a run exactly where it left off, matching the “restart from last written field” requirement.  
- **Installed on Polaris:** The software catalog lists NekRS as an available application, so you can launch it directly without building a custom GPU version.  

Thus, NekRS is the most appropriate installed package for your CFD workload on Polaris.
````
