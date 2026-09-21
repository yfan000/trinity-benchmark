# Reference answer — qe@aurora

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
The agent must produce one pw.x SCF input file (e.g., `3csic_64atom.scf.in`) placed in `/lus/flare/projects/PlasmaEdge/dokafor/qe_run`.

Required file: `3csic_64atom.scf.in`

Key parameters that must be present and correct:
- `&CONTROL`: `calculation = 'scf'`
- `&SYSTEM`:
  - `ibrav = 0` (or appropriate ibrav for zinc-blende supercell; ibrav=0 with explicit CELL_PARAMETERS is most portable for a 2x2x2 supercell)
  - `nat = 64` (2x2x2 supercell of zinc-blende SiC = 8 unit cells × 2 atoms = 16 atoms per conventional cell... wait: zinc-blende conventional cell has 8 atoms (4 formula units); 2x2x2 supercell = 8×8 = 64 atoms. Correct.)
  - `ntyp = 2` (Si and C)
  - `ecutwfc = 60.0` (plane-wave cutoff in Ry)
  - `ecutrho = 480.0` (charge-density cutoff in Ry)
  - `input_dft = 'PBE'` (or rely on pseudopotential; explicitly stating is acceptable)
- `&ELECTRONS`: convergence settings (defaults acceptable)
- `ATOMIC_SPECIES`: two entries — Si (28.086 amu, a PBE ultrasoft UPF) and C (12.011 amu, a PBE ultrasoft UPF)
- `ATOMIC_POSITIONS`: exactly 64 lines covering the 2x2x2 zinc-blende supercell positions (crystal or angstrom or bohr)
- `CELL_PARAMETERS` (if ibrav=0): lattice vectors for 2x2x2 supercell of 3C-SiC (a ≈ 4.358 Å per unit cell, so supercell edge ≈ 8.716 Å)
- `K_POINTS automatic`: `4 4 4 0 0 0` (4x4x4 Monkhorst-Pack; shift 0 0 0 or 1 1 1 both acceptable)

UPF pseudopotential files needed at runtime (NOT written by agent — located or referenced by name):
- Si PBE ultrasoft UPF (e.g., `Si.pbe-n-rrkjus_psl.1.0.0.UPF`)
- C PBE ultrasoft UPF (e.g., `C.pbe-n-rrkjus_psl.1.0.0.UPF`)

Runtime-generated files (agent must NOT write these):
- `output.scf.out` (stdout redirect)
- `*.xml`, `*.save/` (produced by pw.x during run)

Launch context (for reference, not part of input files):
- Binary: `/lus/flare/projects/datascience/hzheng/software/aurora/qe/7.4/bin/pw.x`
- Modules: `oneapi/release`, `intel_compute_runtime`, `cmake`
- CPU-only MPI build; ppn=104 CPU cores per node
- Queue for scaling: `debug-scaling` (2–256 nodes) or `prod` (256+ nodes)
- Run command form: `mpiexec -n <nprocs> --ppn <ppn> $PW_X -in 3csic_64atom.scf.in 2>&1 | tee output.scf.out`
````
