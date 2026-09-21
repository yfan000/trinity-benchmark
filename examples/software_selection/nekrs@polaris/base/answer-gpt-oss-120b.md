# gpt-oss-120b — nekrs@polaris, base arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected application:** **NekRS** (GPU‑accelerated spectral‑element CFD solver)

**Why it fits**

- **Problem match:** NekRS is the GPU‑enabled counterpart of Nek5000 and is designed specifically for incompressible/low‑Mach Navier‑Stokes simulations using the spectral‑element method – exactly the type of flow solver described.
- **GPU requirement:** It is built for NVIDIA GPUs and runs efficiently on A100s, leveraging CUDA, NCCL and the GPU‑aware MPI stack available on Polaris.
- **Checkpoint/restart support:** NekRS (like Nek5000) provides native checkpoint/restart functionality; it can read the binary field/restart files written by a previous run and resume the simulation from that state.
- **Installed on Polaris:** The software catalog lists “NekRS – GPU‑accelerated spectral element CFD solver (Navier‑Stokes) based on Nek”, confirming it is available on the system.
- **Performance & scalability:** NekRS is optimized for the large‑scale GPU nodes of Polaris, making it the most appropriate choice over CPU‑only Nek5000 or other unrelated packages (e.g., molecular‑dynamics, quantum‑chemistry, deep‑learning tools).

Thus, **NekRS** is the best‑suited installed application for the described CFD workload on Polaris.
````
