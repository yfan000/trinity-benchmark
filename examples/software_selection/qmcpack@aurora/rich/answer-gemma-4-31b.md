# gemma-4-31b — qmcpack@aurora, rich arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected Application:** QMCPACK

**Reasoning:**
QMCPACK is the only application in the provided list specifically designed for **Quantum Monte Carlo (QMC)** simulations. It directly supports the required methodologies (**Variational and Diffusion Monte Carlo**) and is optimized for the Aurora architecture via **SYCL/OpenMP offload** for Intel GPU acceleration. Additionally, QMCPACK natively utilizes **HDF5 and XML** for wavefunction and input driver files, matching the provided workload specifications.
````
