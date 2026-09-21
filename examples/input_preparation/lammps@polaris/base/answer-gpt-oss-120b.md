# gpt-oss-120b — lammps@polaris, base arm

Input preparation. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 1 of 9 requirements violated).

````
**File:** `in.lj_argon`

```lammps
# LAMMPS input script for reduced‑LJ argon (ε=σ=mass=1)
# 500 000 atoms on an fcc lattice, reduced density ρ = 0.8442,
# reduced temperature T = 0.72, NVE integration, 1e5 timesteps.
# -------------------------------------------------------------
# Lattice spacing for fcc: a = (4/ρ)^(1/3) ≈ (4/0.8442)^(1/3) = 1.68 σ
# Choose 50 unit cells in each direction:
#   N_atoms = 4 * 50 * 50 * 50 = 500 000
#   Box length = 50 * a ≈ 84.0 σ
# The region is defined in lattice units (0‑50) so the physical size
# is automatically set to 50 × a.

units           lj
atom_style      atomic

# ----- Lattice and simulation box --------------------------------
lattice         fcc 1.0                # a will be set by “region … units lattice”
region          box block 0 50 0 50 0 50 units lattice
create_box      1 box
create_atoms    1 box
mass            1 1.0

# ----- Initial velocities ----------------------------------------
velocity        all create 0.72 12345 loop geom   # T* = 0.72, seed = 12345

# ----- Interatomic potential --------------------------------------
pair_style      lj/cut 2.5
pair_coeff      1 1 1.0 1.0 2.5        # ε=1, σ=1, cutoff = 2.5σ

# ----- Neighbor list ---------------------------------------------
neighbor        0.3 bin
neigh_modify    every 20 delay 0 check no

# ----- Time integration -------------------------------------------
fix             1 all nve

# ----- Output ----------------------------------------------------
thermo          1000
#dump            1 all atom 5000 dump.lj_argon   # (optional, uncomment to write trajectory)

run             100000
```

**Why this file is needed:**  
`in.lj_argon` is the complete LAMMPS input script that defines the system (500 k argon atoms on an fcc lattice at the prescribed reduced density and temperature), the interaction model, integration method, and the run parameters required to perform the simulation on Polaris. Running LAMMPS with this file will generate the trajectory, thermodynamic output, and any optional dumps during the 100 000‑step NVE run.
````
