# gemma-4-31b — lammps@polaris, base arm

Input preparation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 9 requirements violated).

````
`in.lj_argon`
```
# LJ Argon simulation on Polaris
# System: 500,000 atoms, fcc lattice, reduced density 0.8442, T=0.72, NVE

units           lj
atom_style      atomic

# Calculation for box size:
# fcc lattice has 4 atoms per unit cell. 
# To get 500,000 atoms: 500,000 / 4 = 125,000 unit cells.
# A cube of 50^3 = 125,000 unit cells.
# Lattice constant is determined by the reduced density 0.8442.
lattice         fcc 0.8442
region          simbox block 0 50 0 50 0 50
create_box      1 simbox
create_atoms    1 box
mass            1 1.0

# Initialize temperature to 0.72
velocity        all create 0.72 12345 mom yes rot yes dist gaussian

pair_style      lj/cut 2.5
pair_coeff      1 1 1.0 1.0 2.5

neighbor        0.3 bin
neigh_modify    every 1 delay 0 check yes

fix             1 all nve

thermo          1000
run             100000
```
This file is the main LAMMPS input script that defines the system geometry, force field parameters, ensemble, and runtime execution.
````
