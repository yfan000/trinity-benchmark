# nemotron-3-ultra — qe@aurora, base arm

Software selection. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 1 of 4 requirements violated).

````
**Selected Application: Quantum ESPRESSO**

**Why it fits:**
- **Workload Match:** The workload explicitly describes *plane-wave DFT electronic structure calculations* with *SCF runs* across *crystal structures*. Quantum ESPRESSO is the canonical plane-wave DFT code (specifically its `pw.x` executable) for exactly this purpose.
- **Input Format:** The described input files containing `CONTROL`, `SYSTEM`, `ELECTRONS` namelists plus atomic species blocks are the **exact native input format for Quantum ESPRESSO** (PWscf).
- **Architecture Support:** The software catalog lists Quantum ESPRESSO as installed on Aurora with Intel oneAPI/GPU support, making it ready for the Intel PVC (XPU) architecture.
- **Parameter Sweep Suitability:** As a standard MPI-parallelized plane-wave code, it is well-suited for high-throughput parameter sweeps of similar SCF calculations on Aurora's GPU nodes.
````
