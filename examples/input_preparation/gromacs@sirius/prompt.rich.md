# Prompt — gromacs@sirius, enriched arm

Subtask: **Input preparation**. The base prompt with catalog material inserted — format contract, setup and run commands, scaling notes. Derived from the base arm by verified-reversible text insertion, never regenerated, so the two arms are paired.

````
## Task
Determine and construct all input files that GROMACS requires to run the specified production molecular dynamics workload.

## Workload
- **System:** hen egg-white lysozyme solvated in TIP3P water with 0.15 M NaCl, ~34,000 atoms, NPT at 300 K, 2 fs timestep, PME, 5 ns production
- **Software:** GROMACS (already selected)
- **Target machine:** Sirius (ALCF)
- **Working directory:** `/lus/tegu/projects/QuantumMatX/dokafor/gromacs_run`

## Required input files
WRITE these 3 files, one fenced code block each, filenames are yours to choose: `.mdp`, `.gro`, `.top`

DO NOT write contents for:
- `.tpr` — built by the toolchain from the files above; give the `gmx grompp` command that produces it
- `md.log`, `md.edr`, `md.xtc`, `md.trr`, `*.cpt` — produced at runtime, do not write these

Include `.itp` and/or `.ndx` only if this workload genuinely requires them.

## Worked example
Below is a real input deck for a **DIFFERENT** physical system, taken from public GROMACS repositories. It demonstrates block names, keyword spellings, and card ordering **only**. Its numerical values, chemical species, and comment headers describe a different system and must **not** be carried over.

```
# ===== md.mdp =====
# source: https://raw.githubusercontent.com/wehs7661/ensemble_md/master/ensemble_md/tests/data/expanded.mdp
# a real input for a DIFFERENT system — form only

; Run control
integrator = md-vv
tinit = 0
dt = 0.002
nsteps = 500
comm_mode = Linear
nstcomm = 1
nstfout = 0

; Output control
nstlog = 100
nstcalcenergy = 1
nstenergy = 1000
nstxout_compressed = 100

; Neighborsearching and short-range nonbonded interactions
nstlist = 10
ns_type = grid
pbc = xyz
rlist = 1.0

; Electrostatics
cutoff_scheme = verlet
coulombtype = PME
coulomb_modifier = Potential-shift-Verlet
rcoulomb_switch = 0.89
rcoulomb = 0.9

; van der Waals
vdw_type = Cut-off
vdw_modifier = Potential-switch
rvdw_switch = 0.85
rvdw = 0.9

; Apply long range dispersion corrections for Energy and Pressure
DispCorr = AllEnerPres
[... 75 more lines of this file omitted — the form above is what matters]

# ===== conf.gro =====
# source: https://raw.githubusercontent.com/gromacs/gromacs/main/src/testutils/simulationdatabase/spc2.gro
# a real input for a DIFFERENT system — form only

6
    1SOL     OW    1   0.569   1.275   1.165   0.569   1.215   1.965
    1SOL    HW1    2   0.476   1.268   1.128   0.669   1.225   1.865
    1SOL    HW2    3   0.580   1.364   1.209   0.769   1.235   1.765
    2SOL     OW    4   1.555   1.511   0.703   0.869   1.245   1.665
    2SOL    HW1    5   1.498   1.495   0.784   0.169   0.275   1.565
    2SOL    HW2    6   1.496   1.521   0.623   0.269   2.275   1.465
   3.01000   3.01000   3.01000

# ===== topol.top =====
# source: https://raw.githubusercontent.com/gromacs/gromacs/main/src/testutils/simulationdatabase/spc2.top
# a real input for a DIFFERENT system — form only

; Prepare only the subset of OPLS/AA needed for tip3p
#define _FF_OPLS
#define _FF_OPLSAA

[ defaults ]
; nbfunc	comb-rule	gen-pairs	fudgeLJ	fudgeQQ
1		3		yes		0.5	0.5

[ atomtypes ]
; full atom descriptions are available in ffoplsaa.atp
; name  bond_type    mass    charge   ptype          sigma      epsilon
#ifdef HEAVY_H
 opls_111   OW	8      9.95140    -0.834       A    3.15061e-01  6.36386e-01
 opls_112   HW	1      4.03200     0.417       A    0.00000e+00  0.00000e+00
#else
 opls_111   OW	8     15.99940    -0.834       A    3.15061e-01  6.36386e-01
 opls_112   HW	1      1.00800     0.417       A    0.00000e+00  0.00000e+00
#endif

; Include water topology
#include "oplsaa.ff/tip3p.itp"

[ system ]
; Name
spc2

[ molecules ]
; Compound        #mols
SOL              2
```

## Input file format
Every .mdp you write must contain: integrator, nsteps
Usually present, not required: coulombtype, cutoff-scheme

## System context
per node: 64 CPU cores per node, 4 x A100-SXM4-40GB per node, 512 GB memory per node
filesystems available: /tegu, /home

## Instructions
Determine the parameters and configuration GROMACS requires for this workload, then write out each input file in full.

**(a)** Use only directives and keywords you are certain exist in this application's input format — omit a feature rather than invent a keyword for it.

**(b)** Never fabricate the contents of binary or runtime-generated files (databases, wavefunction or checkpoint files, restart files, outputs) — list those as produced at runtime instead of writing text into them.

**(c)** Treat the worked example above as a demonstration of **form only**: block names, keyword spellings, card ordering. Its numerical values, chemical species, and comment headers describe a different system and must not be carried over.

**(d)** Make sure any count you declare matches the entries you actually write out — for example, a declared atom count must match the number of position lines in the coordinate file.

Do **not** write a job script or scheduler directives — input files only.

Every file you write must contain the sections named under Input file format above. That section says what must appear inside each file; it does not give the values, which are yours to determine.

## Output
For each required file, give its filename and its complete contents in a fenced code block, then one line explaining why each file is needed. You are writing file contents as text; you have no filesystem access and are not expected to create anything on disk.
````
