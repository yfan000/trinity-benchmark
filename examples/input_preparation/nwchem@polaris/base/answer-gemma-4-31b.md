# gemma-4-31b — nwchem@polaris, base arm

Input preparation. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 1 of 9 requirements violated).

````
To maintain the fixed $\text{H--O--H}$ angle of $104.5^\circ$ while varying the $\text{O--H}$ bond length ($d$), the coordinates are calculated as:
$\text{O}$ at $(0, 0, 0)$, $\text{H}_1$ at $(d, 0, 0)$, and $\text{H}_2$ at $(d \cos(104.5^\circ), d \sin(104.5^\circ), 0)$.

`run_01/h2o.nw`
```nwchem
echo

title "Water single point B3LYP 6-31G* bond 0.90"

geometry units angstrom
  o 0.000000 0.000000 0.000000
  h 0.900000 0.000000 0.000000
  h -0.234145 0.869331 0.000000
end

basis
  * library 6-31G*
end

dft
  xc b3lyp
  grid medium
end

task dft
```
Needed for the first data point in the sweep (O-H = 0.90 Å).

`run_02/h2o.nw`
```nwchem
echo

title "Water single point B3LYP 6-31G* bond 0.91"

geometry units angstrom
  o 0.000000 0.000000 0.000000
  h 0.910000 0.000000 0.000000
  h -0.236751 0.879024 0.000000
end

basis
  * library 6-31G*
end

dft
  xc b3lyp
  grid medium
end

task dft
```
Needed for the second data point in the sweep (O-H = 0.91 Å).

`run_03/h2o.nw`
```nwchem
echo

title "Water single point B3LYP 6-31G* bond 0.92"

geometry units angstrom
  o 0.000000 0.000000 0.000000
  h 0.920000 0.000000 0.000000
  h -0.239358 0.888718 0.000000
end

basis
  * library 6-31G*
end

dft
  xc b3lyp
  grid medium
end

task dft
```
Needed for the third data point in the sweep (O-H = 0.92 Å).

`run_04/h2o.nw`
```nwchem
echo

title "Water single point B3LYP 6-31G* bond 0.93"

geometry units angstrom
  o 0.000000 0.000000 0.000000
  h 0.930000 0.000000 0.000000
  h -0.241964 0.898411 0.000000
end

basis
  * library 6-31G*
end

dft
  xc b3lyp
  grid medium
end

task dft
```
Needed for the fourth data point in the sweep (O-H = 0.93 Å).

`run_05/h2o.nw`
```nwchem
echo

title "Water single point B3LYP 6-31G* bond 0.94"

geometry units angstrom
  o 0.000000 0.000000 0.000000
  h 0.940000 0.000000 0.000000
  h -0.244571 0.908105 0.000000
end

basis
  * library 6-31G*
end

dft
  xc b3lyp
  grid medium
end

task dft
```
Needed for the fifth data point in the sweep (O-H = 0.94 Å).

`run_06/h2o.nw`
```nwchem
echo

title "Water single point B3LYP 6-31G* bond 0.95"

geometry units angstrom
  o 0.000000 0.000000 0.000000
  h 0.950000 0.000000 0.000000
  h -0.247177 0.917798 0.000000
end

basis
  * library 6-31G*
end

dft
  xc b3lyp
  grid medium
end

task dft
```
Needed for the sixth data point in the sweep (O-H = 0.95 Å).

`run_07/h2o.nw`
```nwchem
echo

title "Water single point B3LYP 6-31G* bond 0.96"

geometry units angstrom
  o 0.000000 0.000000 0.000000
  h 0.960000 0.000000 0.000000
  h -0.249784 0.927492 0.000000
end

basis
  * library 6-31G*
end

dft
  xc b3lyp
  grid medium
end

task dft
```
Needed for the seventh data point in the sweep (O-H = 0.96 Å).

`run_08/h2o.nw`
```nwchem
echo

title "Water single point B3LYP 6-31G* bond 0.97"

geometry units angstrom
  o 0.000000 0.000000 0.000000
  h 0.970000 0.000000 0.000000
  h -0.252390 0.937185 0.000000
end

basis
  * library 6-31G*
end

dft
  xc b3lyp
  grid medium
end

task dft
```
Needed for the eighth data point in the sweep (O-H = 0.97 Å).

`run_09/h2o.nw`
```nwchem
echo

title "Water single point B3LYP 6-31G* bond 0.98"

geometry units angstrom
  o 0.000000 0.000000 0.000000
  h 0.980000 0.000000 0.000000
  h -0.254997 0.946879 0.000000
end

basis
  * library 6-31G*
end

dft
  xc b3lyp
  grid medium
end

task dft
```
Needed for the ninth data point in the sweep (O-H = 0.98 Å).

`run_10/h2o.nw`
```nwchem
echo

title "Water single point B3LYP 6-31G* bond 0.99"

geometry units angstrom
  o 0.000000 0.000000 0.000000
  h 0.990000 0.000000 0.000000
  h -0.257603 0.956572 0.000000
end

basis
  * library 6-31G*
end

dft
  xc b3lyp
  grid medium
end

task dft
```
Needed for the tenth data point in the sweep (O-H = 0.99 Å).
````
