# gemma-4-31b — nekrs@polaris, base arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected Application:** NekRS

**Reasoning:**
NekRS is the best fit because it is specifically designed as a **GPU-accelerated** solver (targeting the A100s on Polaris) for the **incompressible Navier-Stokes** equations using the **spectral element method**. While Nek5000 also uses spectral elements, NekRS is the optimized version for GPU architectures. Furthermore, as a production-grade CFD solver, it supports the required capability to resume simulations from binary restart/field files.
````
