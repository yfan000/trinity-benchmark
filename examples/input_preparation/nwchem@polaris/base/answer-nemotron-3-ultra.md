# nemotron-3-ultra — nwchem@polaris, base arm

Input preparation. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 1 of 9 requirements violated).

````
### run_01/input.nw
```nw
echo

title "water B3LYP/6-31G* single point O-H=0.90 Å"

start water

geometry units angstrom
 O     0.000000    0.000000    0.000000
 H     0.710900    0.000000    0.551900
 H    -0.710900    0.000000    0.551900
 symmetry c2v
end

basis
 * library 6-31G*
end

charge 0

dft
 mult 1
 xc b3lyp
 grid fine
 convergence energy 1d-8
end

task dft energy
```
This input file defines the B3LYP/6-31G* single-point energy calculation for water with O–H bond length 0.90 Å (H–O–H angle 104.5°).

### run_02/input.nw
```nw
echo

title "water B3LYP/6-31G* single point O-H=0.91 Å"

start water

geometry units angstrom
 O     0.000000    0.000000    0.000000
 H     0.718800    0.000000    0.558000
 H    -0.718800    0.000000    0.558000
 symmetry c2v
end

basis
 * library 6-31G*
end

charge 0

dft
 mult 1
 xc b3lyp
 grid fine
 convergence energy 1d-8
end

task dft energy
```
This input file defines the B3LYP/6-31G* single-point energy calculation for water with O–H bond length 0.91 Å (H–O–H angle 104.5°).

### run_03/input.nw
```nw
echo

title "water B3LYP/6-31G* single point O-H=0.92 Å"

start water

geometry units angstrom
 O     0.000000    0.000000    0.000000
 H     0.726700    0.000000    0.564100
 H    -0.726700    0.000000    0.564100
 symmetry c2v
end

basis
 * library 6-31G*
end

charge 0

dft
 mult 1
 xc b3lyp
 grid fine
 convergence energy 1d-8
end

task dft energy
```
This input file defines the B3LYP/6-31G* single-point energy calculation for water with O–H bond length 0.92 Å (H–O–H angle 104.5°).

### run_04/input.nw
```nw
echo

title "water B3LYP/6-31G* single point O-H=0.93 Å"

start water

geometry units angstrom
 O     0.000000    0.000000    0.000000
 H     0.734600    0.000000    0.570300
 H    -0.734600    0.000000    0.570300
 symmetry c2v
end

basis
 * library 6-31G*
end

charge 0

dft
 mult 1
 xc b3lyp
 grid fine
 convergence energy 1d-8
end

task dft energy
```
This input file defines the B3LYP/6-31G* single-point energy calculation for water with O–H bond length 0.93 Å (H–O–H angle 104.5°).

### run_05/input.nw
```nw
echo

title "water B3LYP/6-31G* single point O-H=0.94 Å"

start water

geometry units angstrom
 O     0.000000    0.000000    0.000000
 H     0.742500    0.000000    0.576400
 H    -0.742500    0.000000    0.576400
 symmetry c2v
end

basis
 * library 6-31G*
end

charge 0

dft
 mult 1
 xc b3lyp
 grid fine
 convergence energy 1d-8
end

task dft energy
```
This input file defines the B3LYP/6-31G* single-point energy calculation for water with O–H bond length 0.94 Å (H–O–H angle 104.5°).

### run_06/input.nw
```nw
echo

title "water B3LYP/6-31G* single point O-H=0.95 Å"

start water

geometry units angstrom
 O     0.000000    0.000000    0.000000
 H     0.750400    0.000000    0.582500
 H    -0.750400    0.000000    0.582500
 symmetry c2v
end

basis
 * library 6-31G*
end

charge 0

dft
 mult 1
 xc b3lyp
 grid fine
 convergence energy 1d-8
end

task dft energy
```
This input file defines the B3LYP/6-31G* single-point energy calculation for water with O–H bond length 0.95 Å (H–O–H angle 104.5°).

### run_07/input.nw
```nw
echo

title "water B3LYP/6-31G* single point O-H=0.96 Å"

start water

geometry units angstrom
 O     0.000000    0.000000    0.000000
 H     0.758300    0.000000    0.588700
 H    -0.758300    0.000000    0.588700
 symmetry c2v
end

basis
 * library 6-31G*
end

charge 0

dft
 mult 1
 xc b3lyp
 grid fine
 convergence energy 1d-8
end

task dft energy
```
This input file defines the B3LYP/6-31G* single-point energy calculation for water with O–H bond length 0.96 Å (H–O–H angle 104.5°).

### run_08/input.nw
```nw
echo

title "water B3LYP/6-31G* single point O-H=0.97 Å"

start water

geometry units angstrom
 O     0.000000    0.000000    0.000000
 H     0.766200    0.000000    0.594800
 H    -0.766200    0.000000    0.594800
 symmetry c2v
end

basis
 * library 6-31G*
end

charge 0

dft
 mult 1
 xc b3lyp
 grid fine
 convergence energy 1d-8
end

task dft energy
```
This input file defines the B3LYP/6-31G* single-point energy calculation for water with O–H bond length 0.97 Å (H–O–H angle 104.5°).

### run_09/input.nw
```nw
echo

title "water B3LYP/6-31G* single point O-H=0.98 Å"

start water

geometry units angstrom
 O     0.000000    0.000000    0.000000
 H     0.774100    0.000000    0.600900
 H    -0.774100    0.000000    0.600900
 symmetry c2v
end

basis
 * library 6-31G*
end

charge 0

dft
 mult 1
 xc b3lyp
 grid fine
 convergence energy 1d-8
end

task dft energy
```
This input file defines the B3LYP/6-31G* single-point energy calculation for water with O–H bond length 0.98 Å (H–O–H angle 104.5°).

### run_10/input.nw
```nw
echo

title "water B3LYP/6-31G* single point O-H=0.99 Å"

start water

geometry units angstrom
 O     0.000000    0.000000    0.000000
 H     0.782000    0.000000    0.607100
 H    -0.782000    0.000000    0.607100
 symmetry c2v
end

basis
 * library 6-31G*
end

charge 0

dft
 mult 1
 xc b3lyp
 grid fine
 convergence energy 1d-8
end

task dft energy
```
This input file defines the B3LYP/6-31G* single-point energy calculation for water with O–H bond length 0.99 Å (H–O–H angle 104.5°).
````
