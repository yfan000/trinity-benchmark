# gpt-oss-120b — qe@aurora, base arm

Batch job creation. **FAIL** (correctness 2/2, completeness 2/2, usability 1/2; 1 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N SiC_scf                                    # job name
#PBS -l select=1:system=aurora                      # 1 Aurora node
#PBS -l place=scatter                               # default placement policy
#PBS -l walltime=0:30:00                           # 30 minutes
#PBS -l filesystems=home:flare                      # filesystems touched
#PBS -q debug                                      # queue
#PBS -A TrinityAgent                               # project/account
#PBS -o /lus/flare/projects/NuclearMPX/lchen/qe_run/logs/SiC_scf.out   # standard output
#PBS -e /lus/flare/projects/NuclearMPX/lchen/qe_run/logs/SiC_scf.err   # standard error

# -------------------------------------------------------------
# Create the log directory (must exist before PBS uses it)
mkdir -p /lus/flare/projects/NuclearMPX/lchen/qe_run/logs

# Change to the directory from which the job was submitted
cd ${PBS_O_WORKDIR}

# -------------------------------------------------------------
# Load the software environment (exactly as supplied)
module use /soft/modulefiles
module load oneapi/release
module load intel_compute_runtime
module load cmake
unset PYTHONPATH
export PATH=/lus/flare/projects/datascience/hzheng/software/aurora/qe/7.4/bin:$PATH

# -------------------------------------------------------------
# Determine the MPI layout
NNODES=$(wc -l < $PBS_NODEFILE)          # number of allocated nodes (should be 1)
NRANKS_PER_NODE=104                      # MPI ranks per node as decided
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE )) # total MPI ranks

echo "Running on ${NNODES} node(s) with ${NTOTRANKS} total MPI ranks (${NRANKS_PER_NODE} per node)."

# -------------------------------------------------------------
# Define the Quantum ESPRESSO executable
PW_X=/lus/flare/projects/datascience/hzheng/software/aurora/qe/7.4/bin/pw.x

# Launch the SCF calculation
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} \
        ${PW_X} -in scf.scf.in 2>&1 | tee output.scf.out
```
````
