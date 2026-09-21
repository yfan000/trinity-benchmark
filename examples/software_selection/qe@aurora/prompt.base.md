# Prompt — qe@aurora

Subtask: **Software selection**. Base arm, exactly as the model received it.

````
Task: Identify the installed application on Aurora best suited to the described scientific workload.

Workload:
  Science: Plane-wave density functional theory (DFT) electronic structure calculations; a parameter sweep of many similar SCF runs across a range of crystal structures
  System: Aurora (ALCF)
  Working directory: /lus/flare/projects/BioFoldX/efaraday/run_current
  Inputs: files containing CONTROL, SYSTEM, and ELECTRONS namelists plus atomic species blocks

Installed software:
  chai-lab — Chai-1 protein structure prediction model (XPU-ported fork for Aurora In
  Python / Conda (frameworks) — Intel oneAPI ML stack via module load frameworks — PyTorch 2.8, vLLM 0.1
  CP2K — Quantum chemistry and molecular dynamics code with Intel oneAPI compiler
  DeepSpeed (XPU) — Microsoft DeepSpeed with Intel XPU support, built on top of PyTorch XPU 
  GROMACS — Molecular dynamics simulation with Intel GPU acceleration via SYCL backe
  HACC (HACCabana) — Hardware/Hybrid Accelerated Cosmology Code - HACCabana proxy with Kokkos
  HPL — High Performance Linpack benchmark using Intel MKL on Aurora
  LAMMPS — Classical molecular dynamics with Intel GPU acceleration via Kokkos SYCL
  Nek5000 — Spectral element CFD solver - CPU MPI build on Aurora with Intel oneAPI 
  NekRS — GPU-accelerated spectral element CFD solver with OCCA/SYCL backend for I
  NWChem — Computational chemistry software with Intel oneAPI compilers on Aurora
  OpenFold — AlphaFold2 PyTorch reimplementation — Intel XPU port for Aurora/Sunspot 
  OpenMM — GPU-accelerated molecular dynamics — XPU/PVC support via OpenCL platform
  PySCF — Python-based Simulations of Chemistry Framework (CPU-only; gpu4pyscf req
  PyTorch (XPU) — PyTorch with Intel XPU (GPU) support for Aurora Intel Data Center GPU Ma
  Quantum ESPRESSO — Plane-wave DFT code for electronic structure calculations on Aurora with
  QMCPACK — Quantum Monte Carlo code with SYCL/OpenMP offload for Intel GPU accelera
  TensorFlow (Intel Extension) — TensorFlow with Intel Extension for TensorFlow (itex) for XPU accelerati
  vLLM (Intel XPU, frameworks-shipped) — vLLM XPU inference on Aurora Intel PVC. The vllm bits ship inside the Au

Instructions: Consult the system's software catalog and identify the installed application best suited to this workload and architecture.

Output: Return the selected application and briefly explain why it fits.
````
