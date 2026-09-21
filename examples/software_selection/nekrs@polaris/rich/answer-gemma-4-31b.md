# gemma-4-31b — nekrs@polaris, rich arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected Application:** NekRS

**Reasoning:** 
NekRS is the best fit because it is specifically designed as a GPU-accelerated spectral element CFD solver for the Navier-Stokes equations. While other CFD tools like OpenFOAM or Nek5000 are available, NekRS is optimized for the A100 GPU architecture on Polaris and directly matches the "spectral element method" and "incompressible flow" requirements of the workload. Additionally, as a production CFD solver, it supports the necessary binary field output/restart functionality required to resume the interrupted simulation.
````
