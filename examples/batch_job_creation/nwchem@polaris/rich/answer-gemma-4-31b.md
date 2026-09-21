# gemma-4-31b — nwchem@polaris, rich arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N NWChem_Water
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=00:30:00
#PBS -l filesystems=home:eagle
#PBS -q debug
#PBS -A TrinityAgent
#PBS -o /eagle/ProteinDesign/aschmidt/nwchem_run/job.out
#PBS -e /eagle/ProteinDesign/aschmidt/nwchem_run/job.err

# Ensure output directory exists
mkdir -p /eagle/ProteinDesign/aschmidt/nwchem_run

# Change to working directory
cd ${PBS_O_WORKDIR}

# Software environment
module load PrgEnv-gnu
module swap gcc-native gcc-native/12.3
module load cray-mpich
export PATH=/eagle/datascience/hzheng/software/polaris/nwchem/bin:$PATH
export NWCHEM_BASIS_LIBRARY=/eagle/datascience/hzheng/software/polaris/nwchem/share/nwchem/libraries/
export NWCHEM_NWPW_LIBRARY=/eagle/datascience/hzheng/software/polaris/nwchem/share/nwchem/libraryps/

# MPI Resource Calculation
NNODES=`wc -l < $PBS_NODEFILE`
NRANKS_PER_NODE=4
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))

echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE}"

# Launch NWChem
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} nwchem run.nw
```
````
