# gpt-oss-120b — nwchem@polaris, rich arm

Batch job creation. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 1 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N water_b3lyp
#PBS -o /eagle/ProteinDesign/aschmidt/nwchem_run/water_b3lyp.out
#PBS -e /eagle/ProteinDesign/aschmidt/nwchem_run/water_b3lyp.err
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=0:30:00
#PBS -l filesystems=home:eagle
#PBS -q debug
#PBS -A TrinityAgent

# Create output directory (already exists but safe)
mkdir -p /eagle/ProteinDesign/aschmidt/nwchem_run

# Change to the directory from which the job was submitted
cd ${PBS_O_WORKDIR}

# Load the software environment
module load PrgEnv-gnu
module swap gcc-native gcc-native/12.3
module load cray-mpich
export PATH=/eagle/datascience/hzhheng/software/polaris/nwchem/bin:$PATH
export NWCHEM_BASIS_LIBRARY=/eagle/datascience/hzhheng/software/polaris/nwchem/share/nwchem/libraries/
export NWCHEM_NWPW_LIBRARY=/eagle/datascience/hzhheng/software/polaris/nwchem/share/nwchem/libraryps/

# Determine the number of allocated nodes and set rank layout
NNODES=$(wc -l < $PBS_NODEFILE)
NRANKS_PER_NODE=4
NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))

echo "NNODES=${NNODES} TOTAL_RANKS=${NTOTRANKS} RANKS_PER_NODE=${NRANKS_PER_NODE}"

# Run NWChem
mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} nwchem run.nw
```
````
