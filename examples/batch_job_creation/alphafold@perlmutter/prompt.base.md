# Prompt — alphafold@perlmutter

Subtask: **Batch job creation**. Base arm, exactly as the model received it.

````
## Task
Write a Slurm batch script for Perlmutter that runs a protein structure prediction job and can be submitted immediately with `sbatch`.

## Workload
- **Problem:** Predict the structure of human ubiquitin (UniProt P0CG48), 76-residue monomer, full database search, 5 models with relaxation
- **System:** Perlmutter (NERSC) — scheduler is Slurm
- **Working directory:** `/pscratch/sd/b/bkowalski/alphafold_run`
- **Input file:** `run.fasta` (already present in the working directory)
- **Project allocation:** `m4553`
- **Resources decided:** 1 node, 4 ranks per node, walltime 02:00:00, queue `debug`

## Software environment
```
module reset
module load conda
conda activate alphafold_env
modules: conda

launch command form:
srun -n 1 -G 1 python run_alphafold.py \
  --fasta_paths=input.fasta \
  --output_dir=./output \
  --model_preset=monomer \
  --data_dir=/global/cfs/cdirs/dasrepo/alphafold_data \
  --uniref90_database_path=/global/cfs/cdirs/dasrepo/alphafold_data/uniref90/uniref90.fasta \
  --mgnify_database_path=/global/cfs/cdirs/dasrepo/alphafold_data/mgnify/mgy_clusters_2022_05.fa \
  --template_mmcif_dir=/global/cfs/cdirs/dasrepo/alphafold_data/pdb_mmcif/mmcif_files \
  --obsolete_pdbs_path=/global/cfs/cdirs/dasrepo/alphafold_data/pdb_mmcif/obsolete.dat

binary: /global/cfs/cdirs/dasrepo/hzheng/software/perlmutter/alphafold_venv_v3/bin/python
```
Substitute `run.fasta` for `input.fasta` and apply the decided resources (not the smoke-test placeholders).

## Scheduler conventions
- Perlmutter selects the queue by QOS: `#SBATCH -q debug` (there is no `--partition=debug`).
- GPU jobs require the architecture constraint `#SBATCH -C gpu`.
- The account carries a `_g` suffix for GPU allocations: `#SBATCH -A <project>_g`.
- Job arrays use `#SBATCH --array=1-N` with `$SLURM_ARRAY_TASK_ID`.
- Launch with `srun`, not mpiexec.
- Any output directory referenced by `-o`/`-e` must already exist.

## Worked example
This example is for a **different application** — its node count, task count, and modules must NOT be copied. It demonstrates required script form only.
```bash
# source: https://docs.nersc.gov/jobs/examples/
#!/bin/bash
#SBATCH --qos=debug
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=32
#SBATCH --constraint=gpu
#SBATCH --gpus-per-node=4
#SBATCH -A mXXXX_g

#
# cray-mpich and cray-libsci conflict with openmpi so will automatically be unloaded.
#
module load openmpi

srun --mpi=pmix -n 64 ring_c
```

## Instructions
Write a valid Slurm batch script that:
(a) Requests resources in exactly the form the site conventions and worked example demonstrate — including every directive element they show — and adds no per-chunk resource they omit, since nodes on Perlmutter are allocated exclusively.
(b) Includes full boilerplate: a job-name directive; output and error directives pointing at concrete paths under the stated working directory; an explicit `cd` into the working directory using Slurm's own variable (not a hardcoded path); and creation of any directory those `-o`/`-e` paths reference before they are used.
(c) Sets up the software environment using the supplied module lines.
(d) Launches the application with the correct command, substituting the actual input filename and decided resources.

## Output
Return the complete, ready-to-submit batch script.
````
