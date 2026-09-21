# gpt-oss-120b — gromacs@sirius, rich arm

Input preparation. **FAIL** (correctness 1/2, completeness 1/2, usability 2/2; 3 of 13 requirements violated).

````
**File 1 – md.mdp**  
*Production run parameters (NPT, 5 ns, 2 fs timestep, PME, TIP3P water, 0.15 M NaCl)*  

```mdp
; ================================
; MD production run (NPT, 5 ns)
; ================================

; Run control
integrator               = md
dt                       = 0.002        ; 2 fs
nsteps                   = 2500000      ; 5 ns = 2 500 000 steps
comm_mode                = Linear
nstcomm                  = 1

; Output control
nstlog                    = 1000        ; write to log file every 2 ps
nstenergy                 = 1000        ; write energies every 2 ps
nstxout_compressed        = 1000        ; write coordinates to .xtc every 2 ps
nstvout                  = 0
nstfout                  = 0

; Neighbor searching
nstlist                   = 10
ns_type                   = grid
pbc                       = xyz

; Long‑range electrostatics
cutoff-scheme             = Verlet
coulombtype               = PME
rcoulomb                  = 1.0
rcoulomb-switch           = 0.0          ; no switching
coulomb_modifier          = Potential‑shift‑Verlet

; Van der Waals
vdwtype                   = Cut-off
rvdw                      = 1.0
rvdw-switch               = 0.0
vdw_modifier              = Potential‑shift‑Verlet

; Dispersion correction
DispCorr                  = EnerPres

; Temperature coupling
tcoupl                    = V-rescale
tc_grps                   = Protein Non‑Protein
tau_t                     = 0.1   0.1
ref_t                     = 300   300

; Pressure coupling
pcoupl                    = Parrinello-Rahman
pcoupltype                = isotropic
tau_p                     = 2.0
ref_p                     = 1.0
compressibility           = 4.5e-5

; Constraints
constraints               = h-bonds
continuation              = yes          ; use velocities from previous run
constraint_algorithm      = Lincs
lincs_iter                = 2
lincs_order               = 4

; Velocity generation (not needed for production)
gen_vel                   = no
```

*Why this file?*  
`md.mdp` tells GROMACS how the dynamics should be performed – integrator, time step, total length, thermostats, barostats, cut‑offs, PME, and what output to write. It is read by **gmx grompp** to build the binary run‑input file (`prod.tpr`).

---

**File 2 – conf.gro**  
*Coordinates of lysozyme, TIP3P water and 0.15 M Na⁺/Cl⁻.*  
(Only the header, a few illustrative lines, and the box vector are shown; the full file must contain **34 000** atom entries that match the numbers in the topology.)

```gro
Lysozyme in TIP3P water with 0.15 M NaCl
34000
   1LYS    N    1   1.234   2.345   3.456
   1LYS   H1    2   1.300   2.400   3.500
   1LYS   CA    3   1.500   2.600   3.700
   ... (remaining protein atoms) ...
 1001WAT    OW  34001  12.345  13.456  14.567
 1001WAT   HW1  34002  12.400  13.500  14.600
 1001WAT   HW2  34003  12.300  13.400  14.500
  ... (remaining water atoms) ...
 20001  NA    NA   15.000  16.000  17.000
 20002  CL    CL   15.500  16.500  17.500
  ... (remaining ion atoms) ...
   3.00000   3.00000   3.00000   ; box vectors (nm)
```

*Why this file?*  
`conf.gro` supplies the initial positions (and optionally velocities) of every atom in the system. The atom count on the second line **must** equal the number of coordinate records that follow; GROMACS reads this file when generating the run‑input (`.tpr`).

---

**File 3 – topol.top**  
*Topology that pulls together the protein force‑field, TIP3P water model, and the ion parameters.*

```top
; =============================================================================
; Topology for lysozyme in TIP3P water, 0.15 M NaCl
; =============================================================================

; -------------------- Force‑field --------------------
#include "amber99sb-ildn.ff/forcefield.itp"
#include "amber99sb-ildn.ff/tip3p.itp"
#include "amber99sb-ildn.ff/ions.itp"

; -------------------- System definition --------------------
[ defaults ]
; nbfunc    comb-rule   gen-pairs   fudgeLJ   fudgeQQ
1           2           yes         1.0       1.0

[ system ]
; Name
Lysozyme‑TIP3P‑0.15M‑NaCl

; -------------------- Molecule list --------------------
[ molecules ]
; Compound        #mol
Protein          1          ; lysozyme (single molecule)
SOL              15000      ; water molecules (~33 000 atoms)
NA               220        ; Na⁺ ions to reach 0.15 M
CL               220        ; Cl⁻ ions to neutralise charge and reach 0.15 M
```

*Why this file?*  
`topol.top` tells GROMACS which force‑field files to use, defines atom‑type defaults, and lists how many molecules of each species are present. It is required by **gmx grompp** together with the coordinate file to build the run‑input.

---

**Command to generate the binary run file (`prod.tpr`)**

```bash
gmx grompp -f md.mdp -c conf.gro -p topol.top -o prod.tpr -maxwarn 1
```

*Explanation*: `gmx grompp` reads the three input files (`md.mdp`, `conf.gro`, `topol.top`), checks consistency, and writes the portable binary run‑input file `prod.tpr`, which is what the subsequent `gmx mdrun` command will use to perform the 5 ns production MD on the Sirius system.
````
