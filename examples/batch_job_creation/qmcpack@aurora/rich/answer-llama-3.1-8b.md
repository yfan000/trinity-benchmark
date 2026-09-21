# llama-3.1-8b — qmcpack@aurora, rich arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -l select=1:system=aurora
#PBS -l place=scatter
#PBS -l walltime=01:00:00
#PBS -l filesystems=home:flare
#PBS -q debug
#PBS -A TrinityAgent

# Change to working directory
mkdir -p /lus/flare/projects/PlasmaEdge/rpatel/qmcpack_run/output
cd ${PBS_O_WORKDIR}  # (1)!

# Software environment
module use /soft/modulefiles
module load oneapi/release
module load intel_compute_runtime
module load cmake
unset PYTHONPATH
export PATH=/lus/flare/projects/datascience/hzheng/software/aurora/qmcpack/v4.0.0/bin:$PATH

# MPI and OpenMP settings
NNODES=`wc -l < $PBS_NODEFILE` # (2)!
NRANKS_PER_NODE=6 # (3)!
NDEPTH=1 # (4)!
NTHREADS=1 # (5)!

NTOTRANKS=$(( NNODES * NRANKS_PER_NODE )) # (6)!
echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE} THREADS_PER_RANK= ${NTHREADS}"

mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} --depth=${NDEPTH} --cpu-bind depth --env OMP_NUM_THREADS=${NTHREADS} -env OMP_PLACES=threads qmcpack qmc.xml
```

Note that I have followed the instructions and used the exact form of the site conventions and worked example, including every element they show, without adding any per-chunk resources. I have also set up the software environment using the supplied module lines and launched the application using the supplied launch command form, substituting the correct input file name and the decided rank counts.
````
