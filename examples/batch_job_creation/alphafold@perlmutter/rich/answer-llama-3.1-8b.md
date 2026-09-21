# llama-3.1-8b — alphafold@perlmutter, rich arm

Batch job creation. **FAIL** (correctness 0/2, completeness 0/2, usability 0/2, fatal; 2 of 17 requirements violated).

````
```bash
#!/bin/bash
#SBATCH --qos=debug
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --constraint=gpu
#SBATCH -A m4553_g
#SBATCH -o /pscratch/sd/b/bkowalski/alphafold_run/output-%A_%a.out
#SBATCH -e /pscratch/sd/b/bkowalski/alphafold_run/error-%A_%a.err
#SBATCH -J alphafold_job
#SBATCH --mail-type=ALL

# source: https://docs.nersc.gov/jobs/examples/
# Create the output directory before launching the job
mkdir -p /pscratch/sd/b/bkowalski/alphafold_run/output

# Change into the working directory
cd /pscratch/sd/b/bkowalski/alphafold_run

# source: https://docs.nersc.gov/jobs/examples/
# reset modules and load conda environment
module reset
module load conda
conda activate alphafold_env

# Launch the application
srun -n 1 -G 1 python /global/cfs/cdirs/dasrepo/hzheng/software/perlmutter/alphafold_venv_v3/bin/python run_alphafold.py \
  --fasta_paths=run.fasta \
  --output_dir=./output \
  --model_preset=monomer \
  --data_dir=/global/cfs/cdirs/dasrepo/alphafold_data \
  --uniref90_database_path=/global/cfs/cdirs/dasrepo/alphafold_data/uniref90/uniref90.fasta \
  --mgnify_database_path=/global/cfs/cdirs/dasrepo/alphafold_data/mgnify/mgy_clusters_2022_05.fa \
  --template_mmcif_dir=/global/cfs/cdirs/dasrepo/alphafold_data/pdb_mmcif/mmcif_files \
  --obsolete_pdbs_path=/global/cfs/cdirs/dasrepo/alphafold_data/pdb_mmcif/obsolete.dat
```

This script should be saved to a file (e.g., `alphafold_script.sh`), and then submitted with `sbatch alphafold_script.sh`.
````
