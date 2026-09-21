# gemma-4-31b — nwchem@polaris, rich arm

Input preparation. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 1 of 9 requirements violated).

````
To perform a sweep of the O–H bond length for a water molecule using B3LYP/6-31G*, we vary the distance $r$ from 0.90 Å to 0.99 Å. Using the H–O–H angle of 104.5°, the Cartesian coordinates are calculated as:
Oxygen at $(0, 0, 0)$, Hydrogen 1 at $(r, 0, 0)$, and Hydrogen 2 at $(r \cos(104.5^\circ), r \sin(104.5^\circ), 0)$.

`run_01/water.nw`
```nwchem
echo

title "Water B3LYP/6-31G* Single Point - OH=0.90"

memory 512 MB

geometry units angstrom
 o 0.000000 0.000000 0.000000
 h 0.900000 0.000000 0.000000
 h -0.234000 0.867500 0.000000
end

basis
 * library 6-31G*
end

dft
  XC B3LYP
  grid medium
end

task dft
```
Needed to calculate the single-point energy for O–H bond length 0.90 Å.

`run_02/water.nw`
```nwchem
echo

title "Water B3LYP/6-31G* Single Point - OH=0.91"

memory 512 MB

geometry units angstrom
 o 0.000000 0.000000 0.000000
 h 0.910000 0.000000 0.000000
 h -0.236600 0.877200 0.000000
end

basis
 * library 6-31G*
end

dft
  XC B3LYP
  grid medium
end

task dft
```
Needed to calculate the single-point energy for O–H bond length 0.91 Å.

`run_03/water.nw`
```nwchem
echo

title "Water B3LYP/6-31G* Single Point - OH=0.92"

memory 512 MB

geometry units angstrom
 o 0.000000 0.000000 0.000000
 h 0.920000 0.000000 0.000000
 h -0.239200 0.886800 0.000000
end

basis
 * library 6-31G*
end

dft
  XC B3LYP
  grid medium
end

task dft
```
Needed to calculate the single-point energy for O–H bond length 0.92 Å.

`run_04/water.nw`
```nwchem
echo

title "Water B3LYP/6-31G* Single Point - OH=0.93"

memory 512 MB

geometry units angstrom
 o 0.000000 0.000000 0.000000
 h 0.930000 0.000000 0.000000
 h -0.241800 0.896500 0.000000
end

basis
 * library 6-31G*
end

dft
  XC B3LYP
  grid medium
end

task dft
```
Needed to calculate the single-point energy for O–H bond length 0.93 Å.

`run_05/water.nw`
```nwchem
echo

title "Water B3LYP/6-31G* Single Point - OH=0.94"

memory 512 MB

geometry units angstrom
 o 0.000000 0.000000 0.000000
 h 0.940000 0.000000 0.000000
 h -0.244400 0.906100 0.000000
end

basis
 * library 6-31G*
end

dft
  XC B3LYP
  grid medium
end

task dft
```
Needed to calculate the single-point energy for O–H bond length 0.94 Å.

`run_06/water.nw`
```nwchem
echo

title "Water B3LYP/6-31G* Single Point - OH=0.95"

memory 512 MB

geometry units angstrom
 o 0.000000 0.000000 0.000000
 h 0.950000 0.000000 0.000000
 h -0.247000 0.915800 0.000000
end

basis
 * library 6-31G*
end

dft
  XC B3LYP
  grid medium
end

task dft
```
Needed to calculate the single-point energy for O–H bond length 0.95 Å.

`run_07/water.nw`
```nwchem
echo

title "Water B3LYP/6-31G* Single Point - OH=0.96"

memory 512 MB

geometry units angstrom
 o 0.000000 0.000000 0.000000
 h 0.960000 0.000000 0.000000
 h -0.249600 0.925400 0.000000
end

basis
 * library 6-31G*
end

dft
  XC B3LYP
  grid medium
end

task dft
```
Needed to calculate the single-point energy for O–H bond length 0.96 Å.

`run_08/water.nw`
```nwchem
echo

title "Water B3LYP/6-31G* Single Point - OH=0.97"

memory 512 MB

geometry units angstrom
 o 0.000000 0.000000 0.000000
 h 0.970000 0.000000 0.000000
 h -0.252200 0.935100 0.000000
end

basis
 * library 6-31G*
end

dft
  XC B3LYP
  grid medium
end

task dft
```
Needed to calculate the single-point energy for O–H bond length 0.97 Å.

`run_09/water.nw`
```nwchem
echo

title "Water B3LYP/6-31G* Single Point - OH=0.98"

memory 512 MB

geometry units angstrom
 o 0.000000 0.000000 0.000000
 h 0.980000 0.000000 0.000000
 h -0.254800 0.944700 0.000000
end

basis
 * library 6-31G*
end

dft
  XC B3LYP
  grid medium
end

task dft
```
Needed to calculate the single-point energy for O–H bond length 0.98 Å.

`run_10/water.nw`
```nwchem
echo

title "Water B3LYP/6-31G* Single Point - OH=0.99"

memory 512 MB

geometry units angstrom
 o 0.000000 0.000000 0.000000
 h 0.990000 0.000000 0.000000
 h -0.257400 0.954400 0.000000
end

basis
 * library 6-31G*
end

dft
  XC B3LYP
  grid medium
end

task dft
```
Needed to calculate the single-point energy for O–H bond length 0.99 Å.
````
