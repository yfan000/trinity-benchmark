# gpt-oss-120b — qmcpack@aurora, rich arm

Batch job creation. **FAIL** (correctness 2/2, completeness 2/2, usability 1/2; 1 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N silicon_dmc                     # (a) job name
#PBS -l select=1:system=aurora          # (a) one exclusive Aurora node
#PBS -l place=scatter                   # (a) placement (required by convention)
#PBS -l walltime=01:00:00               # (a) wall‐clock limit
#PBS -l filesystems=home:flare          # (a) all filesystems touched
#PBS -q debug                           # (a) queue
#PBS -A TrinityAgent                    # (a) project/account
#PBS -o /lus/flare/projects/PlasmaEdge/rpatel/qmcpack_run/logs/qmc.out   # (b) stdout
#PBS -e /lus/flare/projects/PlasmaEdge/rpatel/qmcpack_run/logs/qmc.err   # (b) stderr

# ----------------------------------------------------------------------
# (b)  Ensure the output directory exists and move to the job’s start dir
mkdir -p /lus/flare/projects/PlasmaEdge/rpatel/qmcpack_run/logs
cd ${PBS_O_WORKDIR}                     # (b) change to the directory where qsub was issued

# ----------------------------------------------------------------------
# (c)  Load the software environment exactly as prescribed
module use /soft/modulefiles
module load oneapi/release
module load intel_compute_runtime
module load cmake
unset PYTHONPATH
export PATH=/lus/flare/projects/datascience/hzheng/software/aurora/qmcpack/v4.0.0/bin:$PATH

# ----------------------------------------------------------------------
# (d)  Run QMCpack
#     – 64‑atom Si (2×2×2) supercell, Slater‑Jastrow trial from prior DFT
#     – 4096 walkers, timestep 0.005 Ha⁻¹, 200 DMC blocks
#     – 6 MPI ranks (one per core) on the single allocated node
mpiexec -n 6 --ppn 6 qmcpack qmc.xml
```
````
