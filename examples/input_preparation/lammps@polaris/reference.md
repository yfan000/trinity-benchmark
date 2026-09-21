# Reference answer — lammps@polaris

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
The agent must produce one input file, `in.lj_argon`, placed in `/eagle/NuclearMPX/jmartinez/lammps_run`, with the following correct properties:

**Physics / keywords that must appear:**
- `units lj`
- `atom_style atomic`
- `lattice fcc 0.8442` — reduced density 0.8442
- A `region` and `create_box` / `create_atoms` sequence whose box dimensions yield exactly 500,000 atoms on an fcc lattice. fcc places 4 atoms per unit cell, so 500,000 / 4 = 125,000 unit cells; a 50×50×50 supercell of fcc unit cells gives 4×125,000 = 500,000 atoms. The region block should therefore span 0 to 50 in each dimension (e.g. `region box block 0 50 0 50 0 50`).
- `mass 1 1.0`
- `velocity all create 0.72 <any_integer_seed> loop geom` — reduced temperature 0.72
- `pair_style lj/cut 2.5` — cutoff 2.5 sigma
- `pair_coeff 1 1 1.0 1.0 2.5` — LJ epsilon=1, sigma=1
- `neighbor 0.3 bin` (or similar skin distance)
- `neigh_modify` with reasonable settings
- `fix 1 all nve` — NVE ensemble
- `thermo <N>` — some thermodynamic output interval
- `run 100000` — exactly 100,000 timesteps

**Files NOT written by the agent (produced at runtime):**
- `log.lammps`
- Any `*.dump` or `*.lammpstrj` files

**No scheduler content** (no `#PBS` directives, no `mpiexec` line) should appear in the input file.

**Runtime setup (for reference; not part of the input file):**
```
module load PrgEnv-gnu
module swap gcc-native gcc-native/12.3
module load cray-mpich
module load cudatoolkit-standalone
export PATH=/eagle/datascience/hzheng/software/lammps/bin:$PATH
```

**Launch command:**
```
mpiexec -n 4 --ppn 4 lmp -in in.lj_argon -k on g 4 -sf kk -pk kokkos
```

**Queue/sizing defaults:** debug queue, 1 node, walltime 1800 s, ppn 4 (4 MPI ranks × 1 GPU each via Kokkos backend).
````
