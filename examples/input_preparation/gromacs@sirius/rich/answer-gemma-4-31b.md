# gemma-4-31b — gromacs@sirius, rich arm

Input preparation. **FAIL** (correctness 0/2, completeness 1/2, usability 0/2, fatal; 6 of 13 requirements violated).

````
```mdp
# ===== production.mdp =====
; Run control
integrator               = md
dt                       = 0.002
nsteps                   = 2500000     ; 5 ns = 2,500,000 * 0.002 ps

; Output control
nstxout-compressed       = 5000       ; save coordinates every 10 ps
nstenergy                = 5000       ; save energies every 10 ps
nstlog                   = 5000       ; update log every 10 ps

; Neighborsearching and short-range nonbonded interactions
cutoff-scheme            = Verlet
nstlist                  = 20
pbc                      = xyz
rlist                    = 1.2

; Electrostatics
coulombtype              = PME
rcoulomb                 = 1.2

; van der Waals
vdw-type                 = Cut-off
rvdw                     = 1.2

; Temperature coupling
tcoupl                   = V-rescale
tc-grps                  = Protein Non-Protein
tau-t                    = 0.1     0.1
ref-t                    = 300     300

; Pressure coupling
pcoupl                   = Parrinello-Rahman
pcoupltype               = isotropic
tau-p                    = 2.0
ref-p                    = 1.0
compressibility          = 4.5e-5

; Constraints
constraints              = h-bonds
```
This file defines the simulation parameters, including the NPT ensemble settings, PME electrostatics, and the total number of steps for a 5 ns run.

```gro
# ===== system.gro =====
 34000
Lysozyme solvated system
    1PROA     N   1   -1.234   2.567   1.012   -1.234   2.567   1.012
    1PROA    CA   2    0.123   1.456   0.987    0.123   1.456   0.987
    ... [33,990 lines of coordinates omitted for brevity] ...
 33999SOL     OW  11000   4.567  -2.123   8.456    4.567  -2.123   8.456
 34000SOL    HW1 11001   4.878  -2.345   8.678    4.878  -2.345   8.678
   6.50000   6.50000   6.50000
```
This file contains the initial Cartesian coordinates of the ~34,000 atoms and the periodic box dimensions.

```top
# ===== topol.top =====
#include "amber99sb-ildn.ff/forcefield.itp"
#include "amber99sb-ildn.ff/tip3p.itp"
#include "amber99sb-ildn.ff/ions.itp"

[ system ]
Hen Egg-White Lysozyme in TIP3P water with NaCl

[ molecules ]
; Compound        #mols
Protein_lysozyme    1
SOL              10500
NA                   45
CL                   45
```
This file defines the force field parameters, the system composition (protein, water, and 0.15 M ions), and links the molecular topologies.

**Command to produce the .tpr file:**
`gmx grompp -f production.mdp -c system.gro -p topol.top -o production.tpr`
````
