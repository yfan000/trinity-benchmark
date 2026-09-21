# llama-3.1-8b — qe@aurora, base arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -l select=1:system=aurora
#PBS -l walltime=00:30:00
#PBS -l filesystems=home:flare
#PBS -q debug
#PBS -A TrinityAgent
#PBS -N 3C-SiC_SCF

# Create output and error directories
mkdir -p output
mkdir -p error

# Change to working directory
cd ${PBS_O_WORKDIR}

# Software environment setup
module use /soft/modulefiles
module load oneapi/release
module load intel_compute_runtime
module load cmake
unset PYTHONPATH
export PATH=/lus/flare/projects/datascience/hzheng/software/aurora/qe/7.4/bin:$PATH

# Set up the launch command
PW_X=/lus/flare/projects/datascience/hzheng/software/aurora/qe/7.4/bin/pw.x
NTOTRANKS=416
NRANKS_PER_NODE=104
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} $PW_X -in scf.scf.in 2>&1 | tee output/scf.out
```

This script follows the provided site conventions and worked example structure. It requests the required resources, sets up the software environment, and launches the application with the correct input filename and rank counts. The output and error directories are created before the job runs, and the working directory is changed using the scheduler's own variable.
````
