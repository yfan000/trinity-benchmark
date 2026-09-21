# gpt-oss-120b — qmcpack@aurora, base arm

Batch job creation. **FAIL** (correctness 2/2, completeness 2/2, usability 1/2; 1 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N Si_bulk_DMC                     # job name
#PBS -l select=1:system=aurora          # 1 exclusive Aurora node
#PBS -l place=scatter                  # placement policy (as in example)
#PBS -l walltime=01:00:00              # 1 hour wall‑time
#PBS -l filesystems=home:flare         # filesystems accessed
#PBS -q debug                          # queue
#PBS -A TrinityAgent                   # project allocation
#PBS -o /lus/flare/projects/PlasmaEdge/rpatel/qmcpack_run/logs/qmc.out   # stdout file
#PBS -e /lus/flare/projects/PlasmaEdge/rpatel/qmcpack_run/logs/qmc.err   # stderr file

# ----------------------------------------------------------------------
# Create the directory that will hold the output/error files
mkdir -p /lus/flare/projects/PlasmaEdge/rpatel/qmcpack_run/logs

# Change to the directory from which the job was submitted
cd ${PBS_O_WORKDIR}                     # (1)

# ----------------------------------------------------------------------
# Load the software environment
module use /soft/modulefiles
module load oneapi/release
module load intel_compute_runtime
module load cmake
unset PYTHONPATH
export PATH=/lus/flare/projects/datascience/hzheng/software/aurora/qmcpack/v4.0.0/bin:$PATH

# ----------------------------------------------------------------------
# Determine run‑time layout (information useful for logging)
NNODES=`wc -l < $PBS_NODEFILE`          # (2)
NRANKS_PER_NODE=6                       # (3) – as decided by the pipeline
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))   # (4)

echo "NUM_OF_NODES=${NNODES}  TOTAL_NUM_RANKS=${NTOTRANKS}  RANKS_PER_NODE=${NRANKS_PER_NODE}"

# ----------------------------------------------------------------------
# Execute the QMCpack job
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} qmcpack qmc.xml
```
````
