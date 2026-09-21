# Reference answer — alphafold@perlmutter

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
Selected application: AlphaFold

Reason: AlphaFold (DeepMind AlphaFold2) is purpose-built for predicting three-dimensional protein structure from an amino acid sequence. It is the canonical tool for this task and is installed on Perlmutter as a conda environment with CUDA GPU support (required for the neural-network structure-prediction step). chai-lab (Chai-1) is also a protein structure predictor on this system, but AlphaFold2 is the established, well-validated choice for a first run on a single protein chain. The other catalog entries address molecular dynamics (GROMACS, NAMD, LAMMPS, OpenMM), quantum chemistry (CP2K, NWChem, VASP, Quantum ESPRESSO, QMCPACK, PySCF), CFD (Nek5000, NekRS, OpenFOAM, WRF), cosmology (HACC), general deep learning (PyTorch, TensorFlow, DeepSpeed), LLM inference (vLLM), or benchmarking (HPL) — none of which perform protein structure prediction.

Key operational details:
- Environment setup: module reset; module load conda; conda activate alphafold_env
- Binary: Python interpreter inside the AlphaFold conda environment at /global/cfs/cdirs/dasrepo/hzheng/software/perlmutter/alphafold_venv_v3/bin/python
- Launch: srun -n 1 -G 1 python run_alphafold.py with --fasta_paths, --output_dir, --model_preset=monomer, and paths to genetic databases under /global/cfs/cdirs/dasrepo/alphafold_data/
- Requires one GPU; runs as a single-node job
- Default queue: debug; default walltime: 7200 s
- Outputs ranked PDB structure files and result pickle files under output/*/ranked_*.pdb and output/*/result_model_*.pkl
````
