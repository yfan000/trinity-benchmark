# gpt-oss-120b — nwchem@polaris, base arm

Software selection. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 4 requirements violated).

````
**Selected application:** **NWChem**

**Why it fits**

- **DFT capability:** NWChem provides full‑feature Hartree‑Fock and Kohn‑Sham DFT, including the hybrid B3LYP functional.
- **Gaussian‑type basis support:** It natively handles atom‑centered Gaussian basis sets such as 6‑31G*, exactly the specification of the test case.
- **CPU‑only MPI scaling:** The Polaris nodes are CPU‑focused; NWChem’s MPI implementation scales efficiently with a small number of ranks (the collaborator used 4 MPI ranks on a single node).
- **Performance for tiny systems:** For a water molecule with a modest basis, NWChem can complete a B3LYP single‑point in a few seconds, matching the ~5 s wall‑time reported.
- **Installed and maintained:** It appears in the Polaris software catalog as “High‑performance computational chemistry: HF, DFT, CCSD(T), MCSCF, MD,” indicating it is the intended quantum‑chemistry tool for such workloads.

Thus, NWChem is the most appropriate installed application to reproduce the collaborator’s B3LYP/6‑31G* single‑point energy calculation on Polaris.
````
