# nemotron-3-ultra — nekrs@polaris, base arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected application: NekRS**

**Why it fits:**
- **Spectral element method**: NekRS is explicitly a "GPU-accelerated spectral element CFD solver (Navier-Stokes) based on Nek" — directly matching the spectral element discretization requirement.
- **Incompressible Navier-Stokes**: Designed for incompressible/low-Mach Navier-Stokes flows, exactly the problem described.
- **A100 GPU acceleration**: Built for GPU execution (via OCCA/hipSYCL) and deployed on Polaris A100s; the workload mandates A100 GPUs.
- **Checkpoint/restart from binary field files**: Inherits Nek5000's restart capability — it reads/writes binary field/restart files (`.fld`, `.chk`, etc.) so an interrupted run can resume from the last written checkpoint in `/eagle/CosmoSurvey/kwong/job_dir`.
- **Polaris-native**: Listed in the Polaris software catalog as an installed, supported application.
````
