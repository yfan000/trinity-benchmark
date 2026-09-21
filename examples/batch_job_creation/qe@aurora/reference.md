# Reference answer — qe@aurora

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
#!/bin/bash -l
#PBS -N qe_scf_3csic
#PBS -l select=1:system=aurora
#PBS -l place=scatter
#PBS -l walltime=0:30:00
#PBS -l filesystems=home:flare
#PBS -q debug
#PBS -A TrinityAgent
#PBS -o /lus/flare/projects/NuclearMPX/lchen/qe_run/logs/qe_scf_3csic.out
#PBS -e /lus/flare/projects/NuclearMPX/lchen/qe_run/logs/qe_scf_3csic.err

# Create log directory if it does not exist
mkdir -p /lus/flare/projects/NuclearMPX/lchen/qe_run/logs

# Change to working directory
cd ${PBS_O_WORKDIR}

# Software environment
module use /soft/modulefiles
module load oneapi/release
module load intel_compute_runtime
module load cmake
unset PYTHONPATH
export PATH=/lus/flare/projects/datascience/hzheng/software/aurora/qe/7.4/bin:$PATH

# MPI settings
NNODES=`wc -l < $PBS_NODEFILE`
NRANKS_PER_NODE=104
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))
echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE}"

# Launch Quantum ESPRESSO pw.x
PW_X=/lus/flare/projects/datascience/hzheng/software/aurora/qe/7.4/bin/pw.x
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} $PW_X -in scf.scf.in 2>&1 | tee output.scf.out
````
