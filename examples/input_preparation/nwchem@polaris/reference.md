# Reference answer — nwchem@polaris

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
Ten NWChem input files (`.nw`), one per subdirectory `run_01/` through `run_10/`, placed under `/eagle/BioFoldX/nsvensson/nwchem_run/`. Each file is a standard NWChem text input deck containing:

1. `echo` directive (echoes input to output for reproducibility)
2. `title` string identifying the run and bond length
3. `start` directive giving a unique scratch/restart prefix (e.g. `h2o_sweep_01`)
4. `memory` block — e.g. `memory stack 1000 mb heap 200 mb global 1000 mb` (CPU-only build; avoids OOM on single node)
5. `geometry units angstrom` block with exactly 3 atoms: one O at the origin and two H atoms placed using the specified O–H bond length for that run (0.90 Å for run_01, 0.91 Å for run_02, … 0.99 Å for run_10) and the fixed 104.5° H–O–H angle; no symmetry keyword required
6. `basis` block assigning the `6-31G*` basis set to all elements (O and H) via `* library 6-31G*`
7. `dft` block specifying `XC b3lyp` and optionally `mult 1` (closed-shell singlet) and `convergence energy 1d-8`
8. `task dft energy` as the final directive

The ten files differ only in the O–H bond length and in the `start` prefix / `title` string. No `.db` or `.movecs` files are written by the agent — these are runtime outputs. The run command for each subdirectory is `mpiexec -n 16 --ppn 4 nwchem input.nw` (from the catalog), requiring modules `PrgEnv-gnu`, `gcc-native/12.3`, `cray-mpich` and the environment variables `NWCHEM_BASIS_LIBRARY` and `NWCHEM_NWPW_LIBRARY` set to the install-tree paths. Default queue is `debug`, 1 node, walltime 1800 s, on Polaris (CPU-only NWChem build; no GPU directives).
````
