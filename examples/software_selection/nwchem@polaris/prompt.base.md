# Prompt — nwchem@polaris

Subtask: **Software selection**. Base arm, exactly as the model received it.

````
Task: Identify the installed application on Polaris best suited to reproduce a collaborator's B3LYP DFT single-point energy calculation on a water molecule using the 6-31G* basis set.

Workload:
  Problem: H2O B3LYP/6-31G* single-point energy, 4 MPI ranks
  System: Polaris (ALCF)
  Working directory: /eagle/ProteinDesign/mrossi/run_current
  Prior result: collaborator ran this on 1 node in ~5 s walltime using 4 MPI ranks
  Input: a text input file describing the geometry, basis, and DFT task

Installed software:
  AlphaFold2 — DeepMind AlphaFold2 protein structure prediction from amino acid sequenc
  chai-lab — Chai-1 protein structure prediction model (CUDA port for Polaris A100)
  Python / Conda — Default ALCF Polaris scientific Python stack (PyTorch + TensorFlow + com
  CP2K — Quantum chemistry and solid-state physics DFT/MP2/CCSD code (CPU build)
  DeepSpeed — Microsoft DeepSpeed distributed deep learning training with ZeRO optimiz
  ESMFold — Single-sequence protein structure prediction using Meta's ESMFold (esmfo
  FLASH — Adaptive mesh refinement astrophysics simulation code for reactive flows
  GAMESS RI-MP2 mini-app — DOE quantum-chemistry RI-MP2 correlation-energy kernel; cross-vendor ben
  Globus Compute Endpoint Environment — Python 3.11 conda environment for running Globus Compute endpoints on Po
  GROMACS — High-performance molecular dynamics for biomolecular simulations
  HACCabana — GPU-accelerated cosmological N-body proxy app (HACC short-range force so
  HPL — HPL/LINPACK benchmark measuring floating-point performance via LU decomp
  LAMMPS — Classical molecular dynamics with GPU acceleration via Kokkos
  Megatron-LM — NVIDIA Megatron-LM / Megatron-Core LLM training with tensor, pipeline, a
  MOOSE — Multiphysics Object-Oriented Simulation Environment - finite-element fra
  NAMD — GPU-resident molecular dynamics engine for biomolecular simulations
  Nek5000 — Spectral element CFD solver for incompressible/low-Mach flows
  NekRS — GPU-accelerated spectral element CFD solver (Navier-Stokes) based on Nek
  NIXL — NVIDIA Inference Xfer Library — high-perf point-to-point transfers for A
  NWChem — High-performance computational chemistry: HF, DFT, CCSD(T), MCSCF, MD
  OpenFOAM — Open-source CFD toolbox for fluid dynamics, heat transfer, and combustio
  OpenMM — High-performance molecular dynamics simulation toolkit with GPU accelera
  PySCF — Python-based Simulations of Chemistry Framework with GPU acceleration (g
  PyTorch — Deep learning framework with GPU acceleration via CUDA, NCCL, and cuDNN
  Quantum ESPRESSO — Plane-wave DFT code for electronic structure calculations
  QMCPack — Open-source production-level many-body ab initio Quantum Monte Carlo cod
  TensorFlow — Open-source deep learning framework with GPU acceleration via CUDA
  VASP — Vienna Ab initio Simulation Package for electronic structure calculation
  vLLM — High-throughput LLM inference server with PagedAttention and tensor para
  WRF — Weather Research and Forecasting model for mesoscale numerical weather p

Instructions: Consult the system's software catalog and identify the installed application best suited to this workload and architecture.

Output: Return the selected application and briefly explain why it fits.
````
