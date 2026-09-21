# gpt-oss-120b — qe@aurora, rich arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N scf_3C_SiC
#PBS -l select=1:system=aurora
#PBS -l place=scatter
#PBS -l walltime=00:30:00
#PBS -l filesystems=home:flare
#PBS -q debug
#PBS -A TrinityAgent
#PBS -o /lus/flare/projects/NuclearMPX/lchen/qe_run/outputs/scf.out
#PBS -e /lus/flare/projects/NuclearMPX/lchen/qe_run/errors/scf.err

# ----------------------------------------------------------------------
#  Change to the directory from which the job was submitted
# ----------------------------------------------------------------------
cd ${PBS_O_WORKDIR}

# ----------------------------------------------------------------------
#  Create directories for stdout / stderr (must exist before PBS uses them)
# ----------------------------------------------------------------------
mkdir -p /lus/flare/projects/NuclearMPX/lchen/qe_run/outputs
mkdir -p /lus/flare/projects/NuclearMPX/lchen/qe_run/errors

# ----------------------------------------------------------------------
#  Load the software environment (exactly as supplied)
# ----------------------------------------------------------------------
module use /soft/modulefiles
module load oneapi/release
module load intel_compute_runtime
module load cmake
unset PYTHONPATH
export PATH=/lus/flare/projects/datascience/hzheng/software/aurora/qe/7.4/bin:$PATH

# ----------------------------------------------------------------------
#  Define the Quantum ESPRESSO executable
# ----------------------------------------------------------------------
PW_X=/lus/flare/projects/datascience/hzheng/software/aurora/qe/7.4/bin/pw.x

# ----------------------------------------------------------------------
#  Determine the MPI layout
# ----------------------------------------------------------------------
NNODES=$(wc -l < $PBS_NODEFILE)          # number of allocated nodes
NRANKS_PER_NODE=104                      # 104 MPI ranks per node (as decided)
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE )) # total MPI ranks

echo "NUM_OF_NODES=${NNODES}  TOTAL_NUM_RANKS=${NTOTRANKS}  RANKS_PER_NODE=${NRANKS_PER_NODE}"

# ----------------------------------------------------------------------
#  Run the SCF calculation
# ----------------------------------------------------------------------
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} \
    $PW_X -in scf.scf.in 2>&1 | tee output.scf.out
```
````
