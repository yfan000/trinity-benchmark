# nemotron-3-ultra — qmcpack@aurora, base arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected application: QMCPACK**

**Why it fits:**  
QMCPACK is a dedicated Quantum Monte Carlo code that natively supports Variational Monte Carlo (VMC) and Diffusion Monte Carlo (DMC) methods for electron‑correlation problems. It reads trial wavefunctions from HDF5 files and uses XML input drivers—exactly the file formats described in the workload. The Aurora installation is built with SYCL/OpenMP offload for Intel Data Center GPU (PVC) acceleration, matching the target architecture. The prior context (inputs prepared on another system with the same code family) further confirms QMCPACK as the intended application.
````
