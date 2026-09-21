# Prompt — alphafold@perlmutter

Subtask: **Software selection**. Base arm, exactly as the model received it.

````
Task: Identify the installed application on Perlmutter best suited to predict the three-dimensional structure of a protein from its amino acid sequence.

Workload:
  Problem: ab initio protein structure prediction for a single protein chain
  Input: amino acid sequence of the target protein (first run on this machine)
  System: Perlmutter (NERSC)
  Working directory: /pscratch/sd/a/aschmidt/case01

Installed software:
  AlphaFold — DeepMind AlphaFold2 protein structure prediction via conda environment
  chai-lab — Chai-1 protein structure prediction model (CUDA build for Perlmutter A10
  Python / Conda — Default scientific Python stack via NERSC module, with conda environment
  CP2K — Quantum chemistry and solid state physics software with DBCSR GPU offloa
  DeepSpeed — Microsoft distributed training library for large-scale deep learning wit
  GROMACS — High-performance molecular dynamics for biomolecular simulations
  HACC — Hardware/Hybrid Accelerated Cosmology Code for N-body cosmological simul
  HPL — High Performance Linpack benchmark for measuring peak floating-point per
  LAMMPS — Classical molecular dynamics with GPU acceleration via Kokkos
  NAMD — Scalable molecular dynamics for large biomolecular systems
  Nek5000 — Spectral element solver for incompressible Navier-Stokes and related PDE
  NekRS — GPU-native spectral element CFD solver based on Nek5000
  NWChem — High-performance computational chemistry code for molecular and periodic
  OpenFOAM — Open-source finite volume CFD toolbox for continuum mechanics simulation
  OpenMM — GPU-accelerated molecular dynamics simulation toolkit via conda environm
  PySCF — Python-based Simulations of Chemistry Framework with GPU acceleration (g
  PyTorch — Deep learning framework with CUDA+NCCL GPU support via NERSC system modu
  Quantum ESPRESSO — DFT electronic structure with GPU acceleration (OpenACC/CUDA) via NERSC
  QMCPACK — Quantum Monte Carlo ab initio electronic structure code (CPU + CUDA GPU
  TensorFlow — Deep learning framework with GPU support via NERSC system module
  VASP — Vienna Ab initio Simulation Package for DFT electronic structure (licens
  vLLM — High-throughput LLM inference server with PagedAttention and tensor para
  WRF — Weather Research and Forecasting mesoscale atmospheric simulation model

Instructions: Consult the system's software catalog and identify the installed application best suited to this workload and architecture.

Output: Return the selected application and briefly explain why it fits.
````
