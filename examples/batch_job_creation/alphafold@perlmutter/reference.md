# Reference answer — alphafold@perlmutter

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
```bash
#!/bin/bash -l
#SBATCH --job-name=alphafold_ubiquitin
#SBATCH --qos=debug
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --constraint=gpu
#SBATCH --gpus-per-node=4
#SBATCH --time=02:00:00
#SBATCH -A m4553_g
#SBATCH --output=/pscratch/sd/b/bkowalski/alphafold_run/logs/%j.out
#SBATCH --error=/pscratch/sd/b/bkowalski/alphafold_run/logs/%j.err

mkdir -p /pscratch/sd/b/bkowalski/alphafold_run/logs

cd $SLURM_SUBMIT_DIR

module reset
module load conda
conda activate alphafold_env

mkdir -p ./output

srun -n 1 -G 1 python run_alphafold.py \
  --fasta_paths=run.fasta \
  --output_dir=./output \
  --model_preset=monomer \
  --data_dir=/global/cfs/cdirs/dasrepo/alphafold_data \
  --uniref90_database_path=/global/cfs/cdirs/dasrepo/alphafold_data/uniref90/uniref90.fasta \
  --mgnify_database_path=/global/cfs/cdirs/dasrepo/alphafold_data/mgnify/mgy_clusters_2022_05.fa \
  --template_mmcif_dir=/global/cfs/cdirs/dasrepo/alphafold_data/pdb_mmcif/mmcif_files \
  --obsolete_pdbs_path=/global/cfs/cdirs/dasrepo/alphafold_data/pdb_mmcif/obsolete.dat
```

Key decisions:
- `#SBATCH --qos=debug` selects the debug queue (not `--partition`).
- `#SBATCH -A m4553_g` applies the `_g` suffix for GPU allocation charging.
- `#SBATCH --constraint=gpu` is required for GPU nodes on Perlmutter.
- `--nodes=1`, `--ntasks-per-node=4`, `--time=02:00:00` match the decided resources.
- `--gpus-per-node=4` allocates the full node's GPUs (consistent with exclusive node allocation).
- `srun -n 1 -G 1` launches a single task using one GPU, matching AlphaFold's single-GPU-per-prediction model.
- `--fasta_paths=run.fasta` substitutes the actual input file for the catalog placeholder `input.fasta`.
- The `cd $SLURM_SUBMIT_DIR` uses Slurm's variable rather than a hardcoded path.
- `mkdir -p .../logs` is called before the `-o`/`-e` paths are written to.
- `mkdir -p ./output` ensures the AlphaFold output directory exists before the run.
````
