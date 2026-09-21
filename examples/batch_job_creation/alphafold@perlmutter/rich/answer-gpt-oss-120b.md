# gpt-oss-120b — alphafold@perlmutter, rich arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 1 of 17 requirements violated).

````
```bash
#!/bin/bash
#
# SBATCH directives – Perlmutter conventions
#
#SBATCH --job-name=alphafold_ubiquitin                 # descriptive name
#SBATCH --output=output/alphafold.%j.out               # STDOUT  (must exist)
#SBATCH --error=output/alphafold.%j.err                # STDERR  (must exist)
#SBATCH --qos=debug                                    # queue selection
#SBATCH --nodes=1                                      # 1 node
#SBATCH --ntasks-per-node=4                            # 4 MPI ranks / tasks per node
#SBATCH --constraint=gpu                              # GPU nodes only
#SBATCH --gpus-per-node=4                              # 4 GPUs on the node
#SBATCH --time=02:00:00                                # wall‑clock limit
#SBATCH -A m4553_g                                      # project allocation (GPU suffix)

# ----------------------------------------------------------------------
#  Set up the run environment
# ----------------------------------------------------------------------
# Move to the directory from which the job was submitted
cd "${SLURM_SUBMIT_DIR}"

# Create the directory that will hold the Slurm output / error files
mkdir -p output

# Load the software stack
module reset
module load conda
conda activate alphafold_env

# ----------------------------------------------------------------------
#  Run AlphaFold
# ----------------------------------------------------------------------
srun -n 4 -G 4 python run_alphafold.py \
  --fasta_paths=run.fasta \
  --output_dir=./output \
  --model_preset=monomer \
  --data_dir=/global/cfs/cdirs/dasrepo/alphafold_data \
  --uniref90_database_path=/global/cfs/cdirs/dasrepo/alphafold_data/uniref90/uniref90.fasta \
  --mgnify_database_path=/global/cfs/cdirs/dasrepo/alphafold_data/mgnify/mgy_clusters_2022_05.fa \
  --template_mmcif_dir=/global/cfs/cdirs/dasrepo/alphafold_data/pdb_mmcif/mmcif_files \
  --obsolete_pdbs_path=/global/cfs/cdirs/dasrepo/alphafold_data/pdb_mmcif/obsolete.dat
```

Save the script (e.g., `run_alphafold.sbatch`) in the working directory  
`/pscratch/sd/b/bkowalski/alphafold_run` and submit it with  

```bash
sbatch run_alphafold.sbatch
```
````
