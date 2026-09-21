# nemotron-3-ultra — qe@aurora, rich arm

Input preparation. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 2 of 17 requirements violated).

````
3csic_64atom.scf.in
```fortran
&control
    calculation = 'scf'
    prefix = '3csic_64atom'
    outdir = './tmp'
    pseudo_dir = '.'
    tstress = .true.
    tprnfor = .true.
    verbosity = 'high'
 /
&system
    ibrav = 2
    celldm(1) = 16.48
    nat = 64
    ntyp = 2
    ecutwfc = 60.0
    ecutrho = 480.0
    input_dft = 'PBE'
    occupations = 'smearing'
    smearing = 'gaussian'
    degauss = 0.01
 /
&electrons
    diagonalization = 'david'
    mixing_beta = 0.7
    conv_thr = 1.0d-8
 /
ATOMIC_SPECIES
 Si  28.085  Si.pbe-us.UPF
 C   12.011  C.pbe-us.UPF
ATOMIC_POSITIONS (alat)
 Si  0.000000  0.000000  0.000000
 Si  0.500000  0.000000  0.000000
 Si  0.000000  0.500000  0.000000
 Si  0.000000  0.000000  0.500000
 Si  0.500000  0.500000  0.000000
 Si  0.500000  0.000000  0.500000
 Si  0.000000  0.500000  0.500000
 Si  0.500000  0.500000  0.500000
 Si  0.000000  0.250000  0.250000
 Si  0.500000  0.250000  0.250000
 Si  0.000000  0.750000  0.250000
 Si  0.000000  0.250000  0.750000
 Si  0.500000  0.750000  0.250000
 Si  0.500000  0.250000  0.750000
 Si  0.000000  0.750000  0.750000
 Si  0.500000  0.750000  0.750000
 Si  0.250000  0.000000  0.250000
 Si  0.750000  0.000000  0.250000
 Si  0.250000  0.500000  0.250000
 Si  0.250000  0.000000  0.750000
 Si  0.750000  0.500000  0.250000
 Si  0.750000  0.000000  0.750000
 Si  0.250000  0.500000  0.750000
 Si  0.750000  0.500000  0.750000
 Si  0.250000  0.250000  0.000000
 Si  0.750000  0.250000  0.000000
 Si  0.250000  0.750000  0.000000
 Si  0.250000  0.250000  0.500000
 Si  0.750000  0.750000  0.000000
 Si  0.750000  0.250000  0.500000
 Si  0.250000  0.750000  0.500000
 Si  0.750000  0.750000  0.500000
 C   0.125000  0.125000  0.125000
 C   0.625000  0.125000  0.125000
 C   0.125000  0.625000  0.125000
 C   0.125000  0.125000  0.625000
 C   0.625000  0.625000  0.125000
 C   0.625000  0.125000  0.625000
 C   0.125000  0.625000  0.625000
 C   0.625000  0.625000  0.625000
 C   0.125000  0.375000  0.375000
 C   0.625000  0.375000  0.375000
 C   0.125000  0.875000  0.375000
 C   0.125000  0.375000  0.875000
 C   0.625000  0.875000  0.375000
 C   0.625000  0.375000  0.875000
 C   0.125000  0.875000  0.875000
 C   0.625000  0.875000  0.875000
 C   0.375000  0.125000  0.375000
 C   0.875000  0.125000  0.375000
 C   0.375000  0.625000  0.375000
 C   0.375000  0.125000  0.875000
 C   0.875000  0.625000  0.375000
 C   0.875000  0.125000  0.875000
 C   0.375000  0.625000  0.875000
 C   0.875000  0.625000  0.875000
 C   0.375000  0.375000  0.125000
 C   0.875000  0.375000  0.125000
 C   0.375000  0.875000  0.125000
 C   0.375000  0.375000  0.625000
 C   0.875000  0.875000  0.125000
 C   0.875000  0.375000  0.625000
 C   0.375000  0.875000  0.625000
 C   0.875000  0.875000  0.625000
K_POINTS automatic
  4 4 4 1 1 1
```

This input file defines a 64-atom 2×2×2 supercell of 3C-SiC (zinc-blende) for an SCF total-energy calculation with the specified cutoffs (60 Ry wavefunction, 480 Ry charge density), a 4×4×4 Monkhorst-Pack k-grid, PBE ultrasoft pseudopotentials, and convergence settings appropriate for a scaling benchmark on Aurora. The lattice constant (16.48 bohr) corresponds to a 2× conventional cell parameter of ~4.36 Å. All 64 atomic positions are listed explicitly in alat units matching the supercell.
````
