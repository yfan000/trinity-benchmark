# Prompt — vllm@frontier

Subtask: **Software selection**. Base arm, exactly as the model received it.

````
Task: Identify the installed application on Frontier best suited to serving large language model inference at increased concurrency.

Workload:
- Problem: Scale LLM inference serving for LLaMA-3.1-8B from a validated single-node run (271.5 tok/s at concurrency=16, TP=8) to higher concurrency
- System: Frontier (OLCF)
- Working directory: /lustre/orion/BioFoldX/scratch/tnakamura/sim_run
- Prior measurement: single-node run achieved 38.9 tok/s (c=1), 102.5 tok/s (c=4), 271.5 tok/s (c=16) with tensor parallelism=8

Installed software:
  alphafold — 
  chai-lab — Chai-1 protein structure prediction model (ROCm port for Frontier MI250X
  cp2k — 
  deepspeed — 
  gromacs — 
  GROMACS (HIP/ROCm) — GPU-accelerated GROMACS via HIP/ROCm for AMD MI250X on Frontier
  hacc — 
  hpl — 
  lammps — 
  nek5000 — 
  nekrs — 
  OpenFold — AlphaFold2 PyTorch reimplementation — AMD MI250X ROCm port for Frontier 
  openmm — 
  PySCF — Python-based Simulations of Chemistry Framework (CPU-only; gpu4pyscf req
  pytorch — 
  qe — 
  qmcpack — 
  tensorflow — 
  vLLM (ROCm) — vLLM ROCm inference on Frontier AMD MI250X. Validated 2026-05-11: 271.5 

Instructions: Consult the system's software catalog and identify the installed application best suited to this workload and architecture.

Output: Return the selected application and briefly explain why it fits.
````
