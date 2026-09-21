# nemotron-3-ultra — lammps@polaris, base arm

Input preparation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 9 requirements violated).

````
```
in.lj_argon
# Lennard-Jones argon, 500,000 atoms, fcc lattice, reduced density 0.8442
# fcc has 4 atoms/conventional cell → 500,000/4 = 125,000 cells = 50×50×50
# region block 0 50 0 50 0 50 with lattice fcc 0.8442 yields exactly 500,000 atoms

units           lj
atom_style      atomic

lattice         fcc 0.8442
region          box block 0 50 0 50 0 50
create_box      1 box
create_atoms    1 box
mass            1 1.0

velocity        all create 0.72 12345 loop geom

pair_style      lj/cut 2.5
pair_coeff      1 1 1.0 1.0 2.5

neighbor        0.3 bin
neigh_modify    every 20 delay 0 check no

fix             1 all nve

#dump           1 all atom 1000 dump.lj_argon

thermo          1000
run             100000
```

This input file defines the complete LAMMPS simulation for 500,000 Lennard-Jones argon atoms on an fcc lattice at reduced density 0.8442 and temperature 0.72, using NVE integration for 100,000 timesteps with a 2.5σ cutoff. The box dimensions (50×50×50 conventional fcc cells) are chosen to produce exactly 500,000 atoms.
````
