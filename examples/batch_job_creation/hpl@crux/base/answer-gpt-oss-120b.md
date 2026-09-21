# gpt-oss-120b — hpl@crux, base arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N HPL_50000
#PBS -l select=1:ncpus=128:system=crux
#PBS -l place=scatter
#PBS -l walltime=0:30:00
#PBS -l filesystems=home:eagle
#PBS -q debug
#PBS -A TrinityAgent
#PBS -o /eagle/NuclearMPX/aschmidt/hpl_run/logs/hpl.out
#PBS -e /eagle/NuclearMPX/aschmidt/hpl_run/logs/hpl.err

# ----------------------------------------------------------------------
#  Change to the directory from which the job was submitted
# ----------------------------------------------------------------------
cd ${PBS_O_WORKDIR}

# ----------------------------------------------------------------------
#  Create the directory for PBS output/error files (if it does not exist)
# ----------------------------------------------------------------------
mkdir -p /eagle/NuclearMPX/aschmidt/hpl_run/logs

# ----------------------------------------------------------------------
#  Load the software environment
# ----------------------------------------------------------------------
module swap PrgEnv-cray PrgEnv-gnu
module load cray-mpich
module load cray-libsci
export PATH=/eagle/datascience/hzheng/software/crux/hpl/bin:$PATH

# ----------------------------------------------------------------------
#  Determine runtime parameters
# ----------------------------------------------------------------------
NNODES=$(wc -l < "$PBS_NODEFILE")          # number of allocated nodes
NRANKS_PER_NODE=128                         # ranks per node (as requested)
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))   # total number of MPI ranks

echo "NNODES=${NNODES}  NRANKS_PER_NODE=${NRANKS_PER_NODE}  NTOTRANKS=${NTOTRANKS}"
echo "Running HPL with input file HPL.dat in ${PBS_O_WORKDIR}"

# ----------------------------------------------------------------------
#  Launch the application
# ----------------------------------------------------------------------
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} xhpl
```
````
