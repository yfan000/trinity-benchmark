# nemotron-3-ultra — lammps@polaris, rich arm

Input preparation. **PASS** (correctness 2/2, completeness 2/2, usability 2/2; 0 of 9 requirements violated).

````
**File: in.lj_argon**

```
# LAMMPS input for Lennard-Jones argon
# 500,000 atoms on FCC lattice at reduced density 0.8442, T* = 0.72, NVE
# FCC has 4 atoms/conventional cell; 500,000/4 = 125,000 cells = 50^3
# lattice fcc 0.8442 sets lattice constant a = (4/0.8442)^(1/3) ≈ 1.678
# region 0 50 in each direction → 50×50×50 cells → exactly 500,000 atoms

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

thermo          1000
run             100000
```

**Why this file is needed:** This is the sole LAMMPS input deck defining the 500,000-atom Lennard-Jones argon system at the specified thermodynamic state (ρ*=0.8442, T*=0.72), ensemble (NVE), and simulation length (100,000 steps). It sets up the FCC lattice with correct box dimensions to yield exactly the target atom count, assigns initial velocities at the target temperature, and configures the truncated LJ potential with a 2.5σ cutoff.
````
