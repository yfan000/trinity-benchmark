# Prompt — gromacs@sirius

Subtask: **Software selection**. Base arm, exactly as the model received it.

````
Task: Identify the installed application on Sirius best suited to the described scientific workload.

Workload:
  Problem: Biomolecular molecular dynamics benchmarking run to establish scaling behaviour across available GPU nodes
  System: Sirius (ALCF)
  Working directory: /lus/tegu/projects/FusionPIC/efaraday/campaign_a
  Input: A pre-compiled binary run-input file encoding the full simulation topology and parameters

Installed software:
  Python / Conda — Default scientific Python stack via conda on Sirius A100 nodes
  DeepSpeed — Microsoft DeepSpeed ZeRO optimizer for large-scale distributed model tra
  GROMACS — High-performance molecular dynamics package for biomolecular simulations
  LAMMPS — Large-scale Atomic/Molecular Massively Parallel Simulator for classical 
  NAMD — Scalable molecular dynamics code for large biomolecular systems with GPU
  OpenFold — AlphaFold2 PyTorch reimplementation on Sirius A100 (CUDA)
  PySCF — Python-based Simulations of Chemistry Framework with GPU acceleration (g
  PyTorch — Deep learning framework for GPU-accelerated model training and inference
  Quantum ESPRESSO — Plane-wave DFT code for electronic structure calculations
  QMCPack — Open-source production-level many-body ab initio Quantum Monte Carlo cod
  Unsloth — 2x faster LoRA/QLoRA fine-tuning of Llama/Qwen/Mistral via fused Triton 
  vLLM — High-throughput LLM inference server with PagedAttention and tensor para

Instructions: Consult the system's software catalog and identify the installed application best suited to this workload and architecture.

Output: Return the selected application and briefly explain why it fits.
````
