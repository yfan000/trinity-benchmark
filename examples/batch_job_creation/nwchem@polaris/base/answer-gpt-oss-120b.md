# gpt-oss-120b — nwchem@polaris, base arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N water_energy
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=0:30:00
#PBS -l filesystems=home:eagle
#PBS -q debug
#PBS -A TrinityAgent
#PBS -o /eagle/ProteinDesign/aschmidt/nwchem_run/pbs_logs/water_energy.out
#PBS -e /eagle/ProteinDesign/aschmidt/nwchem_run/pbs_logs/water_energy.err

# Create directory for PBS output/error files (must exist before the job starts)
mkdir -p /eagle/ProteinDesign/aschmidt/nwchem_run/pbs_logs

# Change to the directory from which the job was submitted
cd ${PBS_O_WORKDIR}

# ----------------------------------------------------------------------
# Software environment
module load PrgEnv-gnu
module swap gcc-native gcc-native/12.3
module load cray-mpich
export PATH=/eagle/datascience/hzheng/software/polaris/nwchem/bin:$PATH
export NWCHEM_BASIS_LIBRARY=/eagle/datascience/hzheng/software/polaris/nwchem/share/nwchem/libraries/
export NWCHEM_NWPW_LIBRARY=/eagle/datascience/hzheng/software/polaris/nwchem/share/nwchem/libraryps/
# ----------------------------------------------------------------------

# Determine MPI layout
NNODES=$(wc -l < "$PBS_NODEFILE")          # number of allocated nodes
NRANKS_PER_NODE=4                           # MPI ranks per node (as requested)
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))   # total number of MPI ranks

echo "NUM_OF_NODES= ${NNODES}  TOTAL_NUM_RANKS= ${NTOTRANKS}  RANKS_PER_NODE= ${NRANKS_PER_NODE}"

# Run NWChem
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} nwchem run.nw
```
````
