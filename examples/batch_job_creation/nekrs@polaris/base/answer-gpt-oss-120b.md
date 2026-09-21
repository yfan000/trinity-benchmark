# gpt-oss-120b — nekrs@polaris, base arm

Batch job creation. **FAIL** (correctness 2/2, completeness 2/2, usability 1/2; 1 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N nekrs_restart
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=00:30:00
#PBS -l filesystems=home:eagle
#PBS -q debug
#PBS -A TrinityAgent
#PBS -o /eagle/BioFoldX/tnakamura/nekrs_run/logs/nekrs_restart.out
#PBS -e /eagle/BioFoldX/tnakamura/nekrs_run/logs/nekrs_restart.err
#PBS -V          # export all environment variables to the job

# ----------------------------------------------------------------------
# Create directories for PBS output/error (must exist before the job starts)
mkdir -p /eagle/BioFoldX/tnakamura/nekrs_run/logs

# ----------------------------------------------------------------------
# Move to the directory from which the job was submitted
cd ${PBS_O_WORKDIR}

# ----------------------------------------------------------------------
# Load the software environment
module restore
module use /soft/modulefiles
module swap PrgEnv-nvidia PrgEnv-gnu
module load cudatoolkit-standalone/12.9
module load cuda/12.9
module load gcc-native/13.2
module load craype-x86-milan craype-accel-nvidia80
module load spack-pe-base cmake

# ----------------------------------------------------------------------
# Set NEKRS environment variables
export NEKRS_HOME=/eagle/datascience/hzheng/software/nekrs
export PATH=$NEKRS_HOME/bin:$PATH
export MPICH_GPU_SUPPORT_ENABLED=1
export NEKRS_GPU_MPI=1
export MPIR_CVAR_CH4_OFI_ENABLE_RMA=0

# ----------------------------------------------------------------------
# Determine the allocation size
NNODES=$(wc -l < "$PBS_NODEFILE")
NRANKS_PER_NODE=4            # 4 GPUs per Polaris node
NTASKS=$(( NNODES * NRANKS_PER_NODE ))

echo "NNODES=$NNODES  NRANKS_PER_NODE=$NRANKS_PER_NODE  NTASKS=$NTASKS"

# ----------------------------------------------------------------------
# Launch NekRS in restart mode
#   - The case name is "case" (files case.par, case.re2, case.udf are present)
#   - The GPU‑affinity helper .lhelper is used to bind GPUs inversely to MPI rank
mpiexec -n $NTASKS -ppn $NRANKS_PER_NODE -d 8 --cpu-bind depth ./.lhelper nekrs \
       --setup case \
       --backend CUDA \
       --device-id 0 \
       --restart
```
````
