# Reference answer — qmcpack@aurora

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
Required file:

1. `si_dmc.xml` (or similar `.xml`) — QMCPACK's main input file. Must contain:
   - `<project>` block with a meaningful id and series="0"
   - `<qmcsystem>` containing:
     - `<simulationcell>` with lattice vectors for the 2x2x2 Si supercell (in bohr; conventional Si lattice a≈10.263 bohr for 2x2x2 giving a matrix of ~10.263 along diagonals scaled appropriately), periodic boundary conditions (`p p p`), and `LR_dim_cutoff`
     - `<particleset name="e">` with up-spin group size=128 and down-spin group size=128 (bulk Si: 64 atoms × 4 valence electrons each = 256 electrons total, 128 up + 128 down)
     - `<particleset name="ion0">` with group name="Si", size=64, correct Si mass (~51196.7 amu in atomic units), charge=4, valence=4, atomicnumber=14, and 64 positions consistent with the diamond-cubic 2x2x2 supercell
     - `<wavefunction>` containing a `<determinantset>` that reads from the `.h5` file produced by the DFT-to-QMCPACK converter (e.g., `<sposet_builder type="spline" href="FILE.h5" ...>`), plus a `<jastrow>` section for the Slater-Jastrow form (J1 one-body and J2 two-body terms)
     - `<hamiltonian>` with kinetic energy, electron-electron Coulomb (`coulomb`), electron-ion pseudopotential (`pseudopotential` referencing a Si pseudopotential `.xml` file), and ion-ion (`mpc` or `coulomb`) interactions
   - A VMC `<qmc method="vmc">` block (to optimize or for a warm-up step) and/or a DMC `<qmc method="dmc">` block with:
     - `<parameter name="walkers">4096</parameter>`
     - `<parameter name="timestep">0.005</parameter>`
     - `<parameter name="blocks">200</parameter>`

2. `.h5` wavefunction file — NOT written by hand. Produced by running `pw2qmcpack.x` (Quantum ESPRESSO converter) or `convertpw4qmc` against the prior DFT output. Command example:
   ```
   pw2qmcpack.x < pw2qmcpack.in
   ```
   This generates `*.pwscf.h5` which is referenced in the `.xml` via `href=`.

3. Si pseudopotential file (`.BFD.xml` or `.ccECP.xml`) — optional but standard practice; provides the pseudopotential for Si in QMCPACK's XML format. Required if a pseudopotential is used in the Hamiltonian block.

Key numerical checks the grader should apply:
- walkers = 4096
- timestep = 0.005
- blocks = 200
- ion0 group Si size = 64 (matches 2x2x2 supercell of diamond Si)
- electron up size = 128, down size = 128 (256 total = 64 × 4)
- method="dmc" present
- Slater-Jastrow wavefunction structure (determinantset + jastrow)
- href points to a `.h5` file (not fabricated inline)
- No job script or PBS directives present in output
- No invented XML keywords
````
