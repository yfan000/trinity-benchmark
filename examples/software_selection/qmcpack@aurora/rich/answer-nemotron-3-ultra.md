# nemotron-3-ultra — qmcpack@aurora, rich arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected application: QMCPACK**

**Why it fits:**
- **Direct method match**: QMCPACK is a production Quantum Monte Carlo code that implements both Variational Monte Carlo (VMC) and Diffusion Monte Carlo (DMC) — exactly the methods specified.
- **Input compatibility**: It natively reads trial wavefunctions from HDF5 and uses XML for input drivers, matching the ready-to-use files described.
- **Architecture alignment**: The Aurora build includes SYCL/OpenMP offload for Intel GPU (PVC) acceleration, enabling efficient execution on Aurora's hardware.
- **Problem domain**: Designed for electron correlation in periodic systems such as silicon supercells.
- **Code-family continuity**: The prior context notes inputs were prepared on another facility using the same code family; QMCPACK is widely deployed across DOE leadership systems (Summit, Frontier, Perlmutter, Aurora), so HDF5/XML inputs are portable as-is.
````
