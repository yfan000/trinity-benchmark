# Prompt — hpl@crux

Subtask: **Software selection**. Base arm, exactly as the model received it.

````
Task: Identify which installed application on Crux should be used to run a dense linear algebra benchmark workload.

Workload:
  Problem: High-performance dense linear algebra benchmark (Linpack-style) on a single Crux node
  System: Crux (ALCF, 256-node AMD EPYC CPU-only cluster)
  Working directory: /eagle/PlasmaEdge/aschmidt/run_current
  Input: A pre-existing benchmark input file is present in the working directory, authored by the group and tuned for the node's memory and core count

Installed software:
  Conda Environment (ML) — Python 3.11 conda environment for ML and scientific computing on Crux (C
  CP2K — CP2K quantum chemistry and condensed matter physics package (CPU-only bu
  Globus Compute Endpoint Environment — Python 3.11 conda environment for running Globus Compute endpoints on Cr
  GROMACS — GROMACS molecular dynamics simulation package (CPU-only build)
  HACC — Hardware/Hybrid Accelerated Cosmology Code (HACC) N-body cosmology simul
  HPL — High Performance LINPACK benchmark (CPU-only build)
  LAMMPS — Classical molecular dynamics with OpenMP acceleration (CPU-only, no GPU)
  NAMD — NAMD molecular dynamics simulation (CPU-only build)
  Nek5000 — Nek5000 spectral element CFD solver (CPU-only build)
  NekRS — NekRS high-order spectral element CFD solver (CPU-only build)
  NWChem — NWChem high-performance computational chemistry package (CPU-only build)
  OpenFOAM — OpenFOAM open source CFD toolbox (CPU-only build)
  Quantum ESPRESSO — Quantum ESPRESSO plane-wave DFT package (CPU-only build)
  QMCPACK — QMCPACK quantum Monte Carlo code (CPU-only build)
  VASP — Vienna Ab initio Simulation Package (VASP) plane-wave DFT (CPU-only buil
  WRF — Weather Research and Forecasting (WRF) model (CPU-only build)

Instructions: Consult the system's software catalog and identify the installed application best suited to this workload and architecture.

Output: Return the selected application and briefly explain why it fits.
````
