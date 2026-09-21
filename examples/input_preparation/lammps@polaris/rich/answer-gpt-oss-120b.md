# gpt-oss-120b — lammps@polaris, rich arm

Input preparation. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 1 of 9 requirements violated).

````
**File:** `in.lj_argon`

```lammps
# LAMMPS input script for reduced‑unit Lennard‑Jones argon
# ------------------------------------------------------
# Target: 500 000 atoms on an FCC lattice
# Reduced density ρ* = 0.8442, temperature T* = 0.72
# LJ reduced units (ε = σ = m = 1)
#
# For an FCC lattice the number density is ρ* = 4 / a³
# => a = (4/ρ*)^(1/3) = (4/0.8442)^(1/3) ≈ 1.6788 σ
# Choose an integer number of unit cells per side:
#   Ncells = 50 → 50³ = 125 000 cells → 4 × 125 000 = 500 000 atoms
# Box length = Ncells × a = 50 × 1.6788 ≈ 83.94 σ
# The region is defined in lattice units (0–50) for convenience.

units           lj
atom_style      atomic

# ----- Lattice and geometry ---------------------------------
lattice         fcc 1.6788
region          box block 0 50 0 50 0 50 units lattice
create_box      1 box
create_atoms    1 box

mass            1 1.0

# ----- Initial velocities ------------------------------------
velocity        all create 0.72 274839 loop geom

# ----- Interatomic potential ---------------------------------
pair_style      lj/cut 2.5
pair_coeff      1 1 1.0 1.0 2.5

# ----- Neighbor list -----------------------------------------
neighbor        0.3 bin
neigh_modify    every 1 delay 0 check yes

# ----- Time integration ---------------------------------------
fix             1 all nve

# ----- Output ------------------------------------------------
thermo          100
#dump           1 all atom 1000 dump.lj_argon
#dump_modify    1 sort id

run             100000
```

*Why this file is needed:*  
`in.lj_argon` contains all LAMMPS commands that define the system (500 k argon atoms on an FCC lattice at the required reduced density), the simulation settings (units, potentials, NVE integration), and the run parameters (100 000 timesteps). It is the sole input script LAMMPS will read to perform the requested Lennard‑Jones argon simulation on the Polaris system.
````
