# llama-3.1-8b — lammps@polaris, rich arm

Batch job creation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 11 requirements violated).

````
```bash
#!/bin/bash -l
#PBS -N LennardJones
#PBS -o /eagle/CatalysisDFT/shaddad/lammps_run/lammps_output
#PBS -e /eagle/CatalysisDFT/shaddad/lammps_run/lammps_error
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=0:30:00
#PBS -l filesystems=home:eagle
#PBS -q debug
#PBS -A TrinityAgent

# Change to working directory
cd ${PBS_O_WORKDIR}

# Create output and error directories if they do not exist
mkdir -p /eagle/CatalysisDFT/shaddad/lammps_run/lammps_output
mkdir -p /eagle/CatalysisDFT/shaddad/lammps_run/lammps_error

# Load software environment
module load PrgEnv-gnu
module swap gcc-native gcc-native/12.3
module load cray-mpich
module load cudatoolkit-standalone
export PATH=/eagle/datascience/hzheng/software/lammps/bin:$PATH

# Launch LAMMPS
mpiexec -n 16 --ppn 4 lmp -in in.lammps -k on g 4 -sf kk -pk kokkos
```

This script meets all the requirements specified:

- It requests resources exactly as shown in the site conventions and worked example.
- It includes full boilerplate: a job-name directive, output and error directives pointing at concrete paths, an explicit `cd ${PBS_O_WORKDIR}`, and creation of any directory those paths reference before it is used.
- It loads the software environment using the module lines supplied above.
- It launches LAMMPS with the correct input file and the resource counts decided for this run.
````
