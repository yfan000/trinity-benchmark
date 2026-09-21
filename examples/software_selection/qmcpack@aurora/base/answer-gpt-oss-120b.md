# gpt-oss-120b — qmcpack@aurora, base arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected application:** **QMCPACK**

**Why it fits**

- **Purpose‑built for Quantum Monte Carlo:** QMCPACK implements Variational Monte Carlo (VMC) and Diffusion Monte Carlo (DMC) methods, exactly the techniques required for high‑accuracy electron‑correlation studies of solid‑state systems such as a silicon supercell.  
- **Native input formats:** The code’s standard driver uses XML files for the simulation specification and can read trial‑wavefunction data from HDF5 (the `.h5` format used by many QMCPACK workflows). Your existing input files can therefore be used without conversion.  
- **Optimized for Aurora:** QMCPACK on ALCF Aurora is compiled with SYCL/OpenMP off‑load, leveraging the Intel Data Center GPU (PVC) architecture for massive parallel performance. This matches the hardware where the job will run.  
- **Proven scaling on large supercomputers:** QMCPACK has demonstrated strong scaling on thousands of nodes on Aurora, making it the most performant and reliable choice among the installed packages for this workload.  

Hence, QMCPACK is the best‑suited installed application to run your variational and diffusion Monte Carlo simulations on Aurora.
````
