# gemma-4-31b — qe@aurora, rich arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected Application:** Quantum ESPRESSO

**Reasoning:**
Quantum ESPRESSO is explicitly designed for plane-wave density functional theory (DFT) electronic structure calculations, which directly matches the science workload. Furthermore, the input requirements (CONTROL, SYSTEM, and ELECTRONS namelists) are the standard input format for Quantum ESPRESSO. While other chemistry codes like NWChem or CP2K are installed, Quantum ESPRESSO is the primary tool for plane-wave basis set DFT calculations on Aurora.
````
