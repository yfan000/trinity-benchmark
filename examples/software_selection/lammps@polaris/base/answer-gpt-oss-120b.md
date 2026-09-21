# gpt-oss-120b — lammps@polaris, base arm

Software selection. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 2 of 4 requirements violated).

````
**Selected application:** **GROMACS**

**Why it fits the workload**

| Requirement | How GROMACS satisfies it |
|-------------|--------------------------|
| **Classical force‑field MD of a biomolecular system (lipid‑protein membrane, ~5 × 10⁵ atoms)** | GROMACS is purpose‑built for biomolecular simulations. It natively supports the common lipid and protein force fields (CHARMM, AMBER, OPLS, GROMOS, etc.) and has extensive tooling for membrane preparation and analysis. |
| **GPU‑accelerated performance on A100 GPUs** | The Polaris A100 nodes ship with a highly‑tuned GPU‑offload version of GROMACS. It exploits CUDA‑aware MPI, GPU direct memory access, and the “GPU‑resident” kernels that give >10 ns/day on systems of this size on a single A100. |
| **Minimal queue wait / fast turnaround** | GROMACS is one of the most frequently used MD codes on ALCF systems, so it is a standard, pre‑installed module with a well‑tested, low‑overhead job‑submission workflow. This typically results in the shortest queue times compared to less common packages. |
| **Ease of use for the given inputs** | The input files (force‑field parameters + topology/coordinates) can be used directly with GROMACS `gmx grompp`/`gmx mdrun` without needing additional conversion layers or custom scripting. |
| **Scalability for a single‐node, GPU‑only run** | For a 500 k‑atom system the optimal strategy on Polaris is to run a single‑node, 1‑A100 job. GROMACS scales efficiently in this regime, delivering the quickest “time‑to‑solution” without the overhead of multi‑node communication. |

**Conclusion:**  
Given the need for the fastest possible turnaround on the A100‑based Polaris cluster for a large biomolecular MD simulation, GROMACS is the best‑matched installed application. It provides state‑of‑the‑art GPU performance, seamless support for lipid‑protein force fields, and low queuing overhead, delivering the shortest time‑to‑result.
````
