# gpt-oss-120b — nekrs@polaris, rich arm

Batch job creation. **FAIL** (correctness 1/2, completeness 2/2, usability 1/2; 2 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N nekrs_restart                                   # job name
#PBS -l select=1:system=polaris                         # 1 exclusive node
#PBS -l place=scatter                                   # placement policy
#PBS -l walltime=00:30:00                               # max run time
#PBS -l filesystems=home:eagle                          # filesystems used
#PBS -q debug                                           # queue
#PBS -A TrinityAgent                                    # project allocation
#PBS -o /eagle/BioFoldX/tnakamura/nekrs_run/nekrs_restart.out   # stdout
#PBS -e /eagle/BioFoldX/tnakamura/nekrs_run/nekrs_restart.err   # stderr

# ----------------------------------------------------------------------
# Change to the directory where the job was submitted
cd ${PBS_O_WORKDIR}

# ----------------------------------------------------------------------
# Load the software environment exactly as required
module restore
module use /soft/modulefiles
module swap PrgEnv-nvidia PrgEnv-gnu
module load cudatoolkit-standalone/12.9
module load cuda/12.9
module load gcc-native/13.2
module load craype-x86-milan craype-accel-nvidia80
module load spack-pe-base cmake

export NEKRS_HOME=/eagle/datascience/hzheng/software/nekrs
export PATH=$NEKRS_HOME/bin:$PATH
export MPICH_GPU_SUPPORT_ENABLED=1
export NEKRS_GPU_MPI=1
export MPIR_CVAR_CH4_OFI_ENABLE_RMA=0

# ----------------------------------------------------------------------
# Determine the MPI layout
NNODES=$(wc -l < $PBS_NODEFILE)          # number of allocated nodes
NRANKS_PER_NODE=4                        # 4 GPUs per Polaris node
NTASKS=$(( NNODES * NRANKS_PER_NODE ))   # total MPI ranks

echo "===== nekRS restart job ====="
echo "  Nodes allocated       : $NNODES"
echo "  Ranks per node        : $NRANKS_PER_NODE"
echo "  Total MPI ranks       : $NTASKS"
echo "  Working directory     : ${PBS_O_WORKDIR}"
echo "================================"

# ----------------------------------------------------------------------
# Launch nekRS in restart mode.
# The helper .lhelper sets GPU affinity (inverse to MPI local rank).
# The case name (base name of the .par file) is “case”.
mpiexec -n ${NTASKS} \
        -ppn ${NRANKS_PER_NODE} \
        -d 8 \
        --cpu-bind depth \
        ./.lhelper \
        $NEKRS_HOME/bin/nekrs \
        --restart case \
        --backend CUDA \
        --device-id 0
```
````
