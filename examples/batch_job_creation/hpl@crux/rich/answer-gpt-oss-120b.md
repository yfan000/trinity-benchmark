# gpt-oss-120b — hpl@crux, rich arm

Batch job creation. **FAIL** (correctness 2/2, completeness 2/2, usability 1/2; 1 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N HPL_linpack                     # job name
#PBS -l select=1:system=crux            # 1 node, whole node allocated
#PBS -l place=scatter                   # placement (required form)
#PBS -l walltime=0:30:00                # 30 minutes
#PBS -l filesystems=home:eagle          # all filesystems touched
#PBS -q debug                           # queue
#PBS -A TrinityAgent                    # project allocation
#PBS -o /eagle/NuclearMPX/aschmidt/hpl_run/log/hpl.out   # stdout
#PBS -e /eagle/NuclearMPX/aschmidt/hpl_run/log/hpl.err   # stderr

# ----------------------------------------------------------------------
# Make sure the directory for PBS output/error exists before anything is
# written there (PBS opens the files when the job starts, so the directory
# must already be present).
mkdir -p /eagle/NuclearMPX/aschmidt/hpl_run/log

# ----------------------------------------------------------------------
# Move to the directory from which the job was submitted
cd ${PBS_O_WORKDIR}                     # (1)

# ----------------------------------------------------------------------
# Determine the node and rank layout at run time
NNODES=$(wc -l < "$PBS_NODEFILE")       # (2) number of allocated nodes
NRANKS_PER_NODE=128                     # (3) ranks per node as requested
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))   # (4) total MPI ranks

echo "NUM_OF_NODES=${NNODES}  TOTAL_NUM_RANKS=${NTOTRANKS}  RANKS_PER_NODE=${NRANKS_PER_NODE}"

# ----------------------------------------------------------------------
# Load the required software environment
module swap PrgEnv-cray PrgEnv-gnu
module load cray-mpich
module load cray-libsci
export PATH=/eagle/datascience/hzheng/software/crux/hpl/bin:$PATH

# ----------------------------------------------------------------------
# Execute the HPL benchmark
mpiexec -n "${NTOTRANKS}" --ppn "${NRANKS_PER_NODE}" xhpl
```
````
