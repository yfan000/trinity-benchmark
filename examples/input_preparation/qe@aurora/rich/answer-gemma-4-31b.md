# gemma-4-31b — qe@aurora, rich arm

Input preparation. **FAIL** (correctness 1/2, completeness 0/2, usability 0/2, fatal; 4 of 17 requirements violated).

````
**3csic_64atom.scf.in**

```fortran
 &control
    calculation = 'scf'
    outdir = '/lus/flare/projects/PlasmaEdge/dokafor/qe_run'
    pseudo_dir = './'
 /
 &system
    ibrav = 2, 
    celldm(1) = 10.26,
    nat = 64, 
    ntyp = 2,
    ecutwfc = 60.0,
    ecutrho = 480.0,
 /
 &electrons
    conv_thr = 1.0d-8
 /
ATOMIC_SPECIES
 Si  28.085  Si.pbe-n-uspp.UPF
 C   12.011  C.pbe-n-uspp.UPF
ATOMIC_POSITIONS (alat)
 Si 0.00 0.00 0.00
 C   0.25 0.25 0.25
 Si 0.50 0.00 0.00
 C   0.75 0.25 0.25
 Si 0.00 0.50 0.00
 C   0.25 0.75 0.25
 Si 0.50 0.50 0.00
 C   0.75 0.75 0.25
 Si 0.00 0.00 0.50
 C   0.25 0.25 0.75
 Si 0.50 0.00 0.50
 C   0.75 0.25 0.75
 Si 0.00 0.50 0.50
 C   0.25 0.75 0.75
 Si 0.50 0.50 0.50
 C   0.75 0.75 0.75
 Si 1.00 0.00 0.00
 C   1.25 0.25 0.25
 Si 1.50 0.00 0.00
 C   1.75 0.25 0.25
 Si 1.00 0.50 0.00
 C   1.25 0.75 0.25
 Si 1.50 0.50 0.00
 C   1.75 0.75 0.25
 Si 1.00 0.00 0.50
 C   1.25 0.25 0.75
 Si 1.50 0.00 0.50
 C   1.75 0.25 0.75
 Si 1.00 0.50 0.50
 C   1.25 0.75 0.75
 Si 1.50 0.50 0.50
 C   1.75 0.75 0.75
 Si 0.00 1.00 0.00
 C   0.25 1.25 0.25
 Si 0.50 1.00 0.00
 C   0.75 1.25 0.25
 Si 0.00 1.50 0.00
 C   0.25 1.75 0.25
 Si 0.50 1.50 0.00
 C   0.75 1.75 0.25
 Si 0.00 1.00 0.50
 C   0.25 1.25 0.75
 Si 0.50 1.00 0.50
 C   0.75 1.25 0.75
 Si 0.00 1.50 0.50
 C   0.25 1.75 0.75
 Si 0.50 1.50 0.50
 C   0.75 1.75 0.75
 Si 1.00 1.00 0.00
 C   1.25 1.25 0.25
 Si 1.50 1.00 0.00
 C   1.75 1.25 0.25
 Si 1.00 1.50 0.00
 C   1.25 1.75 0.25
 Si 1.50 1.50 0.00
 C   1.75 1.75 0.25
 Si 1.00 1.00 0.50
 C   1.25 1.25 0.75
 Si 1.50 1.00 0.50
 C   1.75 1.25 0.75
 Si 1.00 1.50 0.50
 C   1.25 1.75 0.75
 Si 1.50 1.50 0.50
 C   1.75 1.75 0.75
K_POINTS
 automatic
 4 4 4 0 0 0
```

This file provides the necessary structural, electronic, and numerical parameters for `pw.x` to perform a self-consistent field (SCF) total energy calculation of a 2x2x2 3C-SiC supercell.
````
