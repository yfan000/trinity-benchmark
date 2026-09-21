# gpt-oss-120b — alphafold@perlmutter, base arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 1 of 17 requirements violated).

````
```bash
#!/bin/bash
#
#  AlphaFold run for human ubiquitin (P0CG48) on Perlmutter
#
#SBATCH --job-name=alphafold_ubiquitin          # descriptive name
#SBATCH --qos=debug                             # debug queue (QOS, not partition)
#SBATCH --nodes=1                               # number of nodes
#SBATCH --ntasks-per-node=4                     # 4 MPI ranks (tasks) per node
#SBATCH --constraint=gpu                       # request GPU‑enabled nodes
#SBATCH --gpus-per-node=4                       # one GPU per rank
#SBATCH -t 02:00:00                             # wall‑clock time
#SBATCH -A m4553_g                              # project account (GPU suffix)
#SBATCH -o $SLURM_SUBMIT_DIR/alphafold_%j.out   # standard output
#SBATCH -e $SLURM_SUBMIT_DIR/alphafold_%j.err   # standard error

#--------------------------------------------------------------------
#  Load the software environment
#--------------------------------------------------------------------
module reset
module load conda
conda activate alphafold_env

#--------------------------------------------------------------------
#  Work in the directory from which the job was submitted
#--------------------------------------------------------------------
cd "$SLURM_SUBMIT_DIR"

#--------------------------------------------------------------------
#  Run AlphaFold
#--------------------------------------------------------------------
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

Save the script (e.g. `run_alphafold.sbatch`) in the directory  

`/pscratch/sd/b/bkowalski/alphafold_run`  

and submit it with:

```bash
cd /pscratch/sd/b/bkowalski/alphafold_run
sbatch run_alphafold.sbatch
```

The job will run on one node with four GPU‑enabled ranks, predict the structure of ubiquitin using the full AlphaFold databases, generate five models, and write its log files to `alphafold_<jobID>.out` and `alphafold_<jobID>.err` in the same directory.
````
