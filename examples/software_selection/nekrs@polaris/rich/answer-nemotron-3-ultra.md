# nemotron-3-ultra — nekrs@polaris, rich arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected Application: NekRS**

**Why it fits:**
- **Spectral element method for incompressible Navier‑Stokes:** NekRS is a GPU‑accelerated spectral element CFD solver explicitly designed for incompressible/low‑Mach Navier‑Stokes flows, matching the problem’s numerical method and physics.
- **GPU‑native on A100:** Built for NVIDIA GPUs (including A100) via CUDA/hipSYCL, it leverages the Polaris A100 hardware directly.
- **Checkpoint/restart capability:** NekRS writes binary field/restart files (e.g., `.fld`, `.chk`) that allow exact recovery of the solution state, enabling resumption from the interrupted run in `/eagle/CosmoSurvey/kwong/job_dir`.
- **Provenance:** Derived from the Nek5000/NekCEM lineage, it inherits robust restart I/O and spectral‑element discretization tailored for this class of CFD problems.
````
