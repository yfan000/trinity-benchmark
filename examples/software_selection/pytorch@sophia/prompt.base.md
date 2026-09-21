# Prompt — pytorch@sophia

Subtask: **Software selection**. Base arm, exactly as the model received it.

````
Task: Identify the installed application on Sophia best suited to the described deep learning training workload.

Workload:
  Problem: Distributed training of a ResNet-50 image classification model across all GPUs on a single node using data parallelism
  System: Sophia (ALCF)
  Working directory: /eagle/CombustionSim/jmartinez/run_current
  Framework requirement: Must support multi-GPU collective communication via NCCL for gradient synchronization
  Campaign: Production run that must respect queue limits

Installed software:
  Python / Conda — Default scientific Python stack via conda on Sophia A100 nodes
  DeepSpeed — DeepSpeed distributed LLM/model training, installed into the PyTorch MPI
  GROMACS — GROMACS molecular dynamics with CUDA GPU offload (V100, SM_70) and MPI
  LAMMPS (Kokkos/GPU) — LAMMPS molecular dynamics with GPU acceleration via Kokkos (V100, SM_70)
  NekRS — GPU-accelerated spectral element CFD solver on Sophia (V100)
  PyTorch (MPI) — PyTorch 2.5.0a0 with MPI+NCCL distributed backends, built from source on
  Quantum ESPRESSO — Plane-wave DFT code — GPU-accelerated build on Sophia (V100)
  QMCPACK — Quantum Monte Carlo ab initio electronic structure code (CPU build on So
  TensorFlow — TensorFlow 2.x with CUDA 12.4 GPU support, installed via conda on Sophia
  vLLM — High-throughput LLM inference server with PagedAttention on Sophia A100 

Instructions: Consult the system's software catalog and identify the installed application best suited to this workload and architecture.

Output: Return the selected application and briefly explain why it fits.
````
