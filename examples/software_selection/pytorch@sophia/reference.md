# Reference answer — pytorch@sophia

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
Selected application: PyTorch (MPI)

Why it fits:
- PyTorch (MPI) is built from source on Sophia with CUDA 12.4 targeting A100 GPUs (sm_80), matching the node hardware exactly. GROMACS, LAMMPS, NekRS, and Quantum ESPRESSO all target V100 (SM_70) and are for molecular dynamics or CFD/DFT, not deep learning. vLLM is an inference server, not a training framework. DeepSpeed is installed on top of PyTorch (MPI) and targets LLM-scale training, not a standard ResNet-50 data-parallel campaign. TensorFlow is available but PyTorch (MPI) is the native, source-built framework with MPI+NCCL backends specifically suited for distributed GPU training on Sophia's A100 nodes.
- For a single-node, all-GPU data-parallel job the appropriate queue is by-gpu (default), requesting up to 8 GPUs. The recommended launcher is torchrun with --nproc_per_node set to the number of GPUs requested, using NCCL for GPU collectives.
- Setup requires activating the conda environment at /eagle/datascience/hzheng/software/sophia/pytorch-mpi/conda_env and setting LD_LIBRARY_PATH to include /usr/lib64 and /usr/local/cuda/lib64 so that libcuda.so is found on compute nodes.
- Default sizing: 1 node, queue by-gpu, walltime 3600 s (adjustable up to the queue ceiling for a production campaign).
````
