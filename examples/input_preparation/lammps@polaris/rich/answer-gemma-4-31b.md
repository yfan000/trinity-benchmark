# gemma-4-31b — lammps@polaris, rich arm

Input preparation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 9 requirements violated).

````
`in.lj_argon`
```
# LJ Argon simulation on Polaris
# Physics: 500k atoms, FCC lattice, rho=0.8442, T=0.72, NVE ensemble

units           lj
atom_style      atomic

# Reasoning for box dimensions:
# FCC lattice has 4 atoms per unit cell.
# To get 500,000 atoms: 500,000 / 4 = 125,000 unit cells.
# 125,000^(1/3) = 50. 
# A 50x50x50 grid of unit cells creates exactly 500,000 atoms.

lattice         fcc 0.8442
region          simbox block 0 50 0 50 0 50
create_box      1 simbox
create_atoms    1 simbox
mass            1 1.0

# Set temperature to 0.72 (reduced units)
velocity        all create 0.72 12345 loop geom

pair_style      lj/cut 2.5
pair_coeff      1 1 1.0 1.0 2.5

neighbor        0.3 bin
neigh_modify    every 1 delay 0 check yes

fix             1 all nve

thermo          1000
run             100000
```
This file contains the complete LAMMPS physics and simulation control parameters required to initialize the argon system, set the ensemble, and execute the specified number of timesteps.
````
