# gpt-oss-120b — qe@aurora, rich arm

Software selection. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 1 of 4 requirements violated).

````
**Selected application:** **Quantum ESPRESSO**

**Why it fits**

- **Domain‑specific:** Quantum ESPRESSO is a dedicated plane‑wave DFT package, exactly matching the scientific workload (SCF electronic‑structure calculations on crystalline systems).  
- **Aurora‑ready:** The installed build is compiled for the ALCF Aurora system with Intel oneAPI SYCL off‑loading, allowing the code to exploit the Intel Data Center GPU (PVC) accelerators.  
- **High‑throughput friendly:** Quantum ESPRESSO’s input format (namelists for `CONTROL`, `SYSTEM`, `ELECTRONS`, etc.) matches the files already present in the working directory, enabling straightforward parameter sweeps across many crystal structures.  
- **Performance & scaling:** The SYCL‑GPU version delivers strong performance on Aurora’s heterogeneous nodes and scales well across MPI ranks, ideal for running large batches of independent SCF jobs.  

Thus, Quantum ESPRESSO is the most appropriate installed application for the described plane‑wave DFT workload on Aurora.
````
