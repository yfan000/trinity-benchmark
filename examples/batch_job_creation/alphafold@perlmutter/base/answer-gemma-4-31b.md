# gemma-4-31b — alphafold@perlmutter, base arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 17 requirements violated).

````
```bash
#!/bin/bash
#SBATCH -J AF_ubiquitin
#SBATCH -q debug
#SBATCH -A m4553_g
#SBATCH -C gpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --gpus-per-node=4
#SBATCH -t 02:00:00
#SBATCH -o %j.out
#SBATCH -e %j.err

# Change to the working directory using Slurm's variable
cd $SLURM_SUBMIT_DIR

# Ensure output directory for the application exists
mkdir -p ./output

# Software environment setup
module reset
module load conda
conda activate alphafold_env

# Launch application
# Note: Using the provided binary path to ensure the correct venv is used
srun -n 1 -G 1 /global/cfs/cdirs/dasrepo/hzheng/software/perlmutter/alphafold_venv_v3/bin/python run_alphafold.py \
  --fasta_paths=run.fasta \
  --output_dir=./output \
  --model_preset=monomer \
  --data_dir=/global/cfs/cdirs/dasrepo/alphafold_data \
  --uniref90_database_path=/global/cfs/cdirs/dasrepo/alphafold_data/uniref90/uniref90.fasta \
  --mgnify_database_path=/global/cfs/cdirs/dasrepo/alphafold_data/mgnify/mgy_clusters_2022_05.fa \
  --template_mmcif_dir=/global/cfs/cdirs/dasrepo/alphafold_data/pdb_mmcif/mmcif_files \
  --obsolete_pdbs_path=/global/cfs/cdirs/dasrepo/alphafold_data/pdb_mmcif/obsolete.dat
```
````
