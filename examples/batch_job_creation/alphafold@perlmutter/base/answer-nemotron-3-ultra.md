# nemotron-3-ultra — alphafold@perlmutter, base arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 17 requirements violated).

````
#!/bin/bash
#SBATCH --job-name=alphafold_ubiquitin
#SBATCH --output=/pscratch/sd/b/bkowalski/alphafold_run/logs/alphafold_%j.out
#SBATCH --error=/pscratch/sd/b/bkowalski/alphafold_run/logs/alphafold_%j.err
#SBATCH -q debug
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --gpus-per-node=4
#SBATCH --constraint=gpu
#SBATCH -A m4553_g
#SBATCH --time=02:00:00

# Ensure log directory exists for Slurm output/error files
mkdir -p /pscratch/sd/b/bkowalski/alphafold_run/logs

# Change to the submission directory (working directory)
cd $SLURM_SUBMIT_DIR

# Set up the software environment
module reset
module load conda
conda activate alphafold_env

# Launch AlphaFold prediction
srun -n 1 -G 1 python run_alphafold.py \
  --fasta_paths=run.fasta \
  --output_dir=./output \
  --model_preset=monomer \
  --data_dir=/global/cfs/cdirs/dasrepo/alphafold_data \
  --uniref90_database_path=/global/cfs/cdirs/dasrepo/alphafold_data/uniref90/uniref90.fasta \
  --mgnify_database_path=/global/cfs/cdirs/dasrepo/alphafold_data/mgnify/mgy_clusters_2022_05.fa \
  --template_mmcif_dir=/global/cfs/cdirs/dasrepo/alphafold_data/pdb_mmcif/mmcif_files \
  --obsolete_pdbs_path=/global/cfs/cdirs/dasrepo/alphafold_data/pdb_mmcif/obsolete.dat
````
