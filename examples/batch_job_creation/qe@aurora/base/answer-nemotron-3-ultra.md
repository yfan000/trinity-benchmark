# nemotron-3-ultra — qe@aurora, base arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
#!/bin/bash -l
#PBS -l select=1:system=aurora
#PBS -l place=scatter
#PBS -l walltime=00:30:00
#PBS -l filesystems=home:flare
#PBS -q debug
#PBS -A TrinityAgent
#PBS -N SiC_SCF_64atom
#PBS -o /lus/flare/projects/NuclearMPX/lchen/qe_run/logs/SiC_SCF_64atom.out
#PBS -e /lus/flare/projects/NuclearMPX/lchen/qe_run/logs/SiC_SCF_64atom.err

# Change to working directory
cd ${PBS_O_WORKDIR}

# Ensure log directory exists for PBS output/error
mkdir -p logs

# MPI settings
NNODES=`wc -l < $PBS_NODEFILE`
NRANKS_PER_NODE=104
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))

echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE}"

# Software environment
module use /soft/modulefiles
module load oneapi/release
module load intel_compute_runtime
module load cmake
unset PYTHONPATH
export PATH=/lus/flare/projects/datascience/hzheng/software/aurora/qe/7.4/bin:$PATH

PW_X=/lus/flare/projects/datascience/hzheng/software/aurora/qe/7.4/bin/pw.x

# Launch application
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} $PW_X -in scf.scf.in 2>&1 | tee output.scf.out
````
