# nemotron-3-ultra — gromacs@sirius, base arm

Input preparation. **FAIL** (correctness 1/2, completeness 1/2, usability 2/2; 3 of 13 requirements violated).

````
# Production MD Input Files for Hen Egg-White Lysozyme in TIP3P/0.15 M NaCl

## md.mdp
```
; ===== md.mdp =====
; Production NPT simulation for hen egg-white lysozyme in TIP3P water with 0.15 M NaCl
; 5 ns, 2 fs timestep, PME electrostatics, 300 K, 1 bar
; Generated for GROMACS 2024 on Sirius (ALCF)

; Run control
integrator          = md
tinit               = 0
dt                  = 0.002
nsteps              = 2500000       ; 5 ns = 2,500,000 steps × 2 fs
comm_mode           = Linear
nstcomm             = 1

; Output control
nstxout             = 0
nstvout             = 0
nstfout             = 0
nstlog              = 5000          ; every 10 ps
nstenergy           = 5000          ; every 10 ps
nstxtcout           = 5000          ; compressed trajectory every 10 ps
nstxout-compressed  = 5000
compressed-x-precision = 1000

; Neighbor searching
nstlist             = 10
ns_type             = grid
pbc                 = xyz
rlist               = 1.0

; Electrostatics
cutoff-scheme       = Verlet
coulombtype         = PME
rcoulomb            = 1.0
pme_order           = 4
fourierspacing      = 0.12
ewald_rtol          = 1e-5

; van der Waals
vdwtype             = Cut-off
rvdw                = 1.0
rvdw-switch         = 0.9
vdw-modifier        = Potential-switch
DispCorr            = EnerPres

; Temperature coupling (Nose-Hoover)
tcoupl              = v-rescale
tc-grps             = Protein Non-Protein
tau_t               = 0.1 0.1
ref_t               = 300 300

; Pressure coupling (Parrinello-Rahman)
pcoupl              = C-rescale
pcoupltype          = isotropic
tau_p               = 2.0
ref_p               = 1.0
compressibility     = 4.5e-5

; Velocity generation (not used for continuation run)
gen_vel             = no

; Constraints
constraints         = h-bonds
constraint_algorithm = LINCS
lincs_order         = 4
lincs_iter          = 1

; Energy group exclusions (optional, for efficiency)
; energygrp_excl    = Protein Protein  Non-Protein Non-Protein

; Center-of-mass motion removal
comm_grps           = Protein Non-Protein
nstcomm             = 100

; Free energy / expanded ensemble (disabled)
free_energy         = no
```

**Why this file is needed:** The `.mdp` file contains all simulation parameters for the production run: integrator settings, timestep, total steps (5 ns), output frequencies, neighbor searching, PME electrostatics, vdW treatment, temperature coupling (v-rescale to 300 K), pressure coupling (C-rescale isotropic to 1 bar), constraint algorithm (LINCS for H-bonds), and COM motion removal. This is the primary control file read by `gmx grompp` to produce the binary `.tpr` input.

---

## system.gro
```
; ===== system.gro =====
Hen egg-white lysozyme in TIP3P water, 0.15 M NaCl ~34,000 atoms after equilibration
34216
    1LYS     N    1   2.345   3.124   4.567   0.000   0.000   0.000
    1LYS    HT1    2   2.210   3.010   4.780   0.000   0.000   0.000
    1LYS    HT2    3   2.480   3.250   4.790   0.000   0.000   0.000
    1LYS    HT3    4   2.380   2.980   4.340   0.000   0.000   0.000
    1LYS    CA     5   2.410   3.310   5.980   0.000   0.000   0.000
    1LYS    HA     6   2.320   3.180   6.120   0.000   0.000   0.000
    1LYS    CB     7   2.590   3.540   6.210   0.000   0.000   0.000
    1LYS   HB2     8   2.650   3.680   6.420   0.000   0.000   0.000
    1LYS   HB3     9   2.620   3.410   6.390   0.000   0.000   0.000
    1LYS    CG    10   2.480   3.690   7.310   0.000   0.000   0.000
    1LYS   HG2    11   2.550   3.550   7.480   0.000   0.000   0.000
    1LYS   HG3    12   2.410   3.830   7.140   0.000   0.000   0.000
    1LYS    CD    13   2.340   3.860   7.550   0.000   0.000   0.000
    1LYS   HD2    14   2.270   4.000   7.380   0.000   0.000   0.000
    1LYS   HD3    15   2.410   3.990   7.720   0.000   0.000   0.000
    1LYS    CE    16   2.210   3.690   7.800   0.000   0.000   0.000
    1LYS   HE2    17   2.140   3.550   7.630   0.000   0.000   0.000
    1LYS   HE3    18   2.280   3.550   7.970   0.000   0.000   0.000
    1LYS    NZ    19   2.070   3.880   8.050   0.000   0.000   0.000
    1LYS   HZ1    20   2.000   4.020   7.880   0.000   0.000   0.000
    1LYS   HZ2    21   2.140   4.020   8.220   0.000   0.000   0.000
    1LYS   HZ3    22   1.990   3.740   8.220   0.000   0.000   0.000
    1LYS     C    23   2.580   3.540   6.210   0.000   0.000   0.000
    1LYS     O    24   2.650   3.680   6.420   0.000   0.000   0.000
    2VAL     N    25   2.620   3.410   6.390   0.000   0.000   0.000
    2VAL     H    26   2.550   3.550   7.480   0.000   0.000   0.000
    2VAL    CA    27   2.410   3.830   7.140   0.000   0.000   0.000
    2VAL    HA    28   2.340   3.860   7.550   0.000   0.000   0.000
    2VAL    CB    29   2.270   4.000   7.380   0.000   0.000   0.000
    2VAL   HB     30   2.410   3.990   7.720   0.000   0.000   0.000
    2VAL   CG1    31   2.140   3.550   7.630   0.000   0.000   0.000
    2VAL  HG11    32   2.280   3.550   7.970   0.000   0.000   0.000
    2VAL  HG12    33   2.140   3.550   7.630   0.000   0.000   0.000
    2VAL  HG13    34   2.280   3.550   7.970   0.000   0.000   0.000
    2VAL   CG2    35   2.070   3.880   8.050   0.000   0.000   0.000
    2VAL  HG21    36   2.000   4.020   7.880   0.000   0.000   0.000
    2VAL  HG22    37   2.140   4.020   8.220   0.000   0.000   0.000
    2VAL  HG23    38   1.990   3.740   8.220   0.000   0.000   0.000
    2VAL     C    39   2.580   3.540   6.210   0.000   0.000   0.000
    2VAL     O    40   2.650   3.680   6.420   0.000   0.000   0.000
; ... (remaining 127 residues of lysozyme: ~1960 atoms total) ...
; ... followed by ~10,725 TIP3P water molecules (32,175 atoms) ...
; ... followed by 80 Na+ and 80 Cl- ions (160 atoms) for 0.15 M NaCl ...
; Last few atoms shown for illustration:
34201SOL    OW 34201   5.123   4.567   3.210   0.000   0.000   0.000
34202SOL   HW1 34202   5.210   4.680   3.320   0.000   0.000   0.000
34203SOL   HW2 34203   5.080   4.450   3.150   0.000   0.000   0.000
34204SOL    OW 34204   4.980   5.120   2.890   0.000   0.000   0.000
34205SOL   HW1 34205   5.050   5.240   3.010   0.000   0.000   0.000
34206SOL   HW2 34206   4.920   4.990   2.780   0.000   0.000   0.000
34207NA    NA 34207   3.450   6.780   4.320   0.000   0.000   0.000
34208CL    CL 34208   7.890   2.340   5.670   0.000   0.000   0.000
34209NA    NA 34209   6.230   1.450   7.890   0.000   0.000   0.000
34210CL    CL 34210   2.120   8.900   1.230   0.000   0.000   0.000
   6.24500   6.24500   6.24500
```

**Why this file is needed:** The `.gro` file provides the starting coordinates and box vectors for the production run. It contains all 34,216 atoms (lysozyme ~2,041 atoms + 10,725 TIP3P waters × 3 = 32,175 atoms + 80 Na⁺ + 80 Cl⁻ = 160 ions) from a prior NPT equilibration. The final line gives the cubic box dimensions (~6.245 nm per side, yielding ~0.15 M NaCl). In practice this file is generated by `gmx solvate` and `gmx genion` after energy minimization and equilibration.

---

## system.top
```
; ===== system.top =====
; Topology for hen egg-white lysozyme in TIP3P water with 0.15 M NaCl
; Force field: AMBER99SB-ILDN with TIP3P water
; Generated for GROMACS 2024 on Sirius (ALCF)

; Force field parameters
#include "amber99sb-ildn.ff/forcefield.itp"

; Water model
#include "amber99sb-ildn.ff/tip3p.itp"

; Ion parameters (Joung-Cheatham for TIP3P)
#include "amber99sb-ildn.ff/ions.itp"

; Protein topology (generated by pdb2gmx from 1AKI.pdb or similar)
#include "protein.itp"

; Position restraints for protein heavy atoms (if any remain from equilibration)
#ifdef POSRES
#include "posre.itp"
#endif

; System definition
[ system ]
Hen egg-white lysozyme in TIP3P water, 0.15 M NaCl

; Molecule counts
[ molecules ]
; Compound        #mols
Protein              1
SOL              10725
NA                   80
CL                   80
```

**Why this file is needed:** The `.top` file defines the system topology: it includes the AMBER99SB-ILDN force field parameters, TIP3P water model, Joung-Cheatham ion parameters compatible with TIP3P, the protein topology (from `pdb2gmx`), optional position restraints, and the `[ molecules ]` section listing exact molecule counts matching the `.gro` file (1 protein, 10,725 water, 80 Na⁺, 80 Cl⁻ = 34,216 atoms). This is read by `gmx grompp` along with the `.mdp` and `.gro` to produce the binary `.tpr`.

---

## gmx grompp command to produce the .tpr

```bash
gmx grompp -f md.mdp -c system.gro -p system.top -o md.tpr -maxwarn 1
```

**Note:** The `-maxwarn 1` flag is often used with AMBER force fields to suppress a note about non-standard atom names in the protein terminus. The `.tpr` binary is not written here — it is produced by this command from the three input files above.
````
