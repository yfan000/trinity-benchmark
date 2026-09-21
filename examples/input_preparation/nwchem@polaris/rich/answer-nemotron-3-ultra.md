# nemotron-3-ultra — nwchem@polaris, rich arm

Input preparation. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 1 of 9 requirements violated).

````
For this workload, I need to create 10 NWChem input files (`.nw`), one per subdirectory `run_01` through `run_10`, each with a different O–H bond length (0.90–0.99 Å in 0.01 Å steps) while keeping the H–O–H angle fixed at 104.5°. Each file performs a B3LYP/6-31G* single-point energy calculation. Memory directives are included to avoid OOM errors on Polaris.

### run_01/h2o.nw
```nw
start h2o_run01

memory stack 200 mb
memory heap 200 mb
memory global 100 mb

geometry units angstrom
 O     0.000000    0.000000    0.000000
 H     0.711180    0.000000    0.551520
 H    -0.711180    0.000000    0.551520
end

basis
 * library 6-31G*
end

dft
 xc b3lyp
 grid fine
 convergence energy 1e-8
end

task dft energy
```
**Needed for:** First sweep point (O–H = 0.90 Å) B3LYP/6-31G* single-point energy.

### run_02/h2o.nw
```nw
start h2o_run02

memory stack 200 mb
memory heap 200 mb
memory global 100 mb

geometry units angstrom
 O     0.000000    0.000000    0.000000
 H     0.719082    0.000000    0.557648
 H    -0.719082    0.000000    0.557648
end

basis
 * library 6-31G*
end

dft
 xc b3lyp
 grid fine
 convergence energy 1e-8
end

task dft energy
```
**Needed for:** Second sweep point (O–H = 0.91 Å) B3LYP/6-31G* single-point energy.

### run_03/h2o.nw
```nw
start h2o_run03

memory stack 200 mb
memory heap 200 mb
memory global 100 mb

geometry units angstrom
 O     0.000000    0.000000    0.000000
 H     0.726984    0.000000    0.563776
 H    -0.726984    0.000000    0.563776
end

basis
 * library 6-31G*
end

dft
 xc b3lyp
 grid fine
 convergence energy 1e-8
end

task dft energy
```
**Needed for:** Third sweep point (O–H = 0.92 Å) B3LYP/6-31G* single-point energy.

### run_04/h2o.nw
```nw
start h2o_run04

memory stack 200 mb
memory heap 200 mb
memory global 100 mb

geometry units angstrom
 O     0.000000    0.000000    0.000000
 H     0.734886    0.000000    0.569904
 H    -0.734886    0.000000    0.569904
end

basis
 * library 6-31G*
end

dft
 xc b3lyp
 grid fine
 convergence energy 1e-8
end

task dft energy
```
**Needed for:** Fourth sweep point (O–H = 0.93 Å) B3LYP/6-31G* single-point energy.

### run_05/h2o.nw
```nw
start h2o_run05

memory stack 200 mb
memory heap 200 mb
memory global 100 mb

geometry units angstrom
 O     0.000000    0.000000    0.000000
 H     0.742788    0.000000    0.576032
 H    -0.742788    0.000000    0.576032
end

basis
 * library 6-31G*
end

dft
 xc b3lyp
 grid fine
 convergence energy 1e-8
end

task dft energy
```
**Needed for:** Fifth sweep point (O–H = 0.94 Å) B3LYP/6-31G* single-point energy.

### run_06/h2o.nw
```nw
start h2o_run06

memory stack 200 mb
memory heap 200 mb
memory global 100 mb

geometry units angstrom
 O     0.000000    0.000000    0.000000
 H     0.750690    0.000000    0.582160
 H    -0.750690    0.000000    0.582160
end

basis
 * library 6-31G*
end

dft
 xc b3lyp
 grid fine
 convergence energy 1e-8
end

task dft energy
```
**Needed for:** Sixth sweep point (O–H = 0.95 Å) B3LYP/6-31G* single-point energy.

### run_07/h2o.nw
```nw
start h2o_run07

memory stack 200 mb
memory heap 200 mb
memory global 100 mb

geometry units angstrom
 O     0.000000    0.000000    0.000000
 H     0.758592    0.000000    0.588288
 H    -0.758592    0.000000    0.588288
end

basis
 * library 6-31G*
end

dft
 xc b3lyp
 grid fine
 convergence energy 1e-8
end

task dft energy
```
**Needed for:** Seventh sweep point (O–H = 0.96 Å) B3LYP/6-31G* single-point energy.

### run_08/h2o.nw
```nw
start h2o_run08

memory stack 200 mb
memory heap 200 mb
memory global 100 mb

geometry units angstrom
 O     0.000000    0.000000    0.000000
 H     0.766494    0.000000    0.594416
 H    -0.766494    0.000000    0.594416
end

basis
 * library 6-31G*
end

dft
 xc b3lyp
 grid fine
 convergence energy 1e-8
end

task dft energy
```
**Needed for:** Eighth sweep point (O–H = 0.97 Å) B3LYP/6-31G* single-point energy.

### run_09/h2o.nw
```nw
start h2o_run09

memory stack 200 mb
memory heap 200 mb
memory global 100 mb

geometry units angstrom
 O     0.000000    0.000000    0.000000
 H     0.774396    0.000000    0.600544
 H    -0.774396    0.000000    0.600544
end

basis
 * library 6-31G*
end

dft
 xc b3lyp
 grid fine
 convergence energy 1e-8
end

task dft energy
```
**Needed for:** Ninth sweep point (O–H = 0.98 Å) B3LYP/6-31G* single-point energy.

### run_10/h2o.nw
```nw
start h2o_run10

memory stack 200 mb
memory heap 200 mb
memory global 100 mb

geometry units angstrom
 O     0.000000    0.000000    0.000000
 H     0.782298    0.000000    0.606672
 H    -0.782298    0.000000    0.606672
end

basis
 * library 6-31G*
end

dft
 xc b3lyp
 grid fine
 convergence energy 1e-8
end

task dft energy
```
**Needed for:** Tenth sweep point (O–H = 0.99 Å) B3LYP/6-31G* single-point energy.

---

**Coordinate derivation:** O at origin; H positions computed as (±r·sin(52.25°), 0, r·cos(52.25°)) with sin(52.25°)=0.7902, cos(52.25°)=0.6128. Each file uses `task dft energy` for single-point, B3LYP via `xc b3lyp`, 6-31G* basis from library, and memory guards for Polaris.
````
