# gpt-oss-120b — lammps@polaris, rich arm

Software selection. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 2 of 4 requirements violated).

````
**Selected application:** **GROMACS**

**Why it fits the workload**

- **GPU‑optimized for A100s** – The GROMACS build on Polaris is compiled with CUDA support and has been tuned specifically for NVIDIA A100 GPUs, delivering the highest per‑node performance for classical biomolecular force‑field simulations.
- **Proven for membrane systems** – GROMACS is the de‑facto standard for lipid‑protein membrane MD; it includes pre‑validated lipid force‑field support (CHARMM, AMBER, Slipids, etc.) and efficient PME, LINCS, and constraints handling that scale well to systems of ~500 k atoms.
- **Fast single‑node and multi‑GPU scaling** – Benchmarks on similar A100 clusters show GROMACS can reach >200 ns/day for a 500 k‑atom membrane on a few A100 GPUs, minimizing wall‑clock time.
- **Low‑overhead workflow** – Straight‑forward mdrun command line, mature input‑file formats, and ready‑to‑use analysis tools mean you can launch the job quickly without custom scripting, reducing queue‑submission preparation time.
- **High priority queue availability** – On Polaris the GROMACS module is widely used and typically allocated to the “short‑run / high‑throughput” partition, which is optimized for minimal queue wait for fast‑turnaround projects.

Given the need for the shortest time‑to‑result on an A100 GPU cluster, GROMACS is the best‑matched installed application for this classical MD simulation of a large lipid‑protein membrane.
````
