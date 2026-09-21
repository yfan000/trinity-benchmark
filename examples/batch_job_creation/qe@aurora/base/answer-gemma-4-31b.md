# gemma-4-31b — qe@aurora, base arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N SiC_SCF
#PBS -l select=1
#PBS -l walltime=00:30:00
#PBS -l filesystems=home:flare
#PBS -q debug
#PBS -A TrinityAgent
#PBS -o /lus/flare/projects/NuclearMPX/lchen/qe_run/scf.scf.out
#PBS -e /lus/flare/projects/NuclearMPX/lchen/qe_run/scf.scf.err

# Change to working directory
cd ${PBS_O_WORKDIR}

# Software environment setup
module use /soft/modulefiles
module load oneapi/release
module load intel_compute_runtime
module load cmake
unset PYTHONPATH
export PATH=/lus/flare/projects/datascience/hzheng/software/aurora/qe/7.4/bin:$PATH

# MPI Resource Calculation
NNODES=`wc -l < $PBS_NODEFILE`
NRANKS_PER_NODE=104
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))

# Binary path
PW_X=/lus/flare/projects/datascience/hzheng/software/aurora/qe/7.4/bin/pw.x

# Launch command
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} $PW_X -in scf.scf.in 2>&1 | tee scf.scf.out
```
````
