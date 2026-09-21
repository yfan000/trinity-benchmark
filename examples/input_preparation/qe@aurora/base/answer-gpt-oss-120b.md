# gpt-oss-120b — qe@aurora, base arm

Input preparation. **FAIL** (correctness 0/2, completeness 0/2, usability 0/2, fatal; 6 of 17 requirements violated).

````
**File:** `3csic_64atom.scf.in`

```fortran
&control
   calculation = 'scf'
   prefix      = '3cSiC_64'
   pseudo_dir  = './pseudo'
   outdir      = './tmp'
   tstress     = .true.
   tprnfor     = .true.
/
&system
   ibrav   = 1,
   celldm(1) = 16.4840,      ! 2 × lattice constant of 3C‑SiC (a ≈ 4.359 Å) in Bohr
   nat     = 64,
   ntyp    = 2,
   ecutwfc = 60.0,
   ecutrho = 480.0,
   occupations = 'fixed'
/
&electrons
   conv_thr = 1.0d-8
/
ATOMIC_SPECIES
 Si  28.0855  Si.pbe-rrkj.UPF
 C    12.0107  C.pbe-rrkj.UPF

ATOMIC_POSITIONS (crystal)
 Si 0.000000 0.000000 0.000000
 Si 0.000000 0.000000 0.500000
 Si 0.000000 0.500000 0.000000
 Si 0.000000 0.500000 0.500000
 Si 0.500000 0.000000 0.000000
 Si 0.500000 0.000000 0.500000
 Si 0.500000 0.500000 0.000000
 Si 0.500000 0.500000 0.500000
 Si 0.000000 0.250000 0
````
