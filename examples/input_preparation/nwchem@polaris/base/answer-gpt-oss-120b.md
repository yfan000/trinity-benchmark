# gpt-oss-120b — nwchem@polaris, base arm

Input preparation. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 1 of 9 requirements violated).

````
**/eagle/BioFoldX/nsvensson/nwchem_run/run_01/water.nw**  
```nw
title "Water B3LYP single‑point, O–H = 0.90 Å"

start water_01

geometry units angstrom print
 O  0.0000 0.0000 0.0000
 H  0.7092 0.5540 0.0000
 H -0.7092 0.5540 0.0000
 symmetry c2v
end

basis "ao basis"
 O library "6-31G*"
 H library "6-31G*"
end

dft
  xc b3lyp
  mult 1
  convergence energy 1d-8
  grid fine
end

task dft energy
```
*Needed to run the first geometry (O–H = 0.90 Å) on Polaris.*

---

**/eagle/BioFoldX/nsvensson/nwchem_run/run_02/water.nw**  
```nw
title "Water B3LYP single‑point, O–H = 0.91 Å"

start water_02

geometry units angstrom print
 O  0.0000 0.0000 0.0000
 H  0.7171 0.5602 0.0000
 H -0.7171 0.5602 0.0000
 symmetry c2v
end

basis "ao basis"
 O library "6-31G*"
 H library "6-31G*"
end

dft
  xc b3lyp
  mult 1
  convergence energy 1d-8
  grid fine
end

task dft energy
```
*Needed for the second geometry (O–H = 0.91 Å).*

---

**/eagle/BioFoldX/nsvensson/nwchem_run/run_03/water.nw**  
```nw
title "Water B3LYP single‑point, O–H = 0.92 Å"

start water_03

geometry units angstrom print
 O  0.0000 0.0000 0.0000
 H  0.7247 0.5663 0.0000
 H -0.7247 0.5663 0.0000
 symmetry c2v
end

basis "ao basis"
 O library "6-31G*"
 H library "6-31G*"
end

dft
  xc b3lyp
  mult 1
  convergence energy 1d-8
  grid fine
end

task dft energy
```
*Needed for the third geometry (O–H = 0.92 Å).*

---

**/eagle/BioFoldX/nsvensson/nwchem_run/run_04/water.nw**  
```nw
title "Water B3LYP single‑point, O–H = 0.93 Å"

start water_04

geometry units angstrom print
 O  0.0000 0.0000 0.0000
 H  0.7324 0.5725 0.0000
 H -0.7324 0.5725 0.0000
 symmetry c2v
end

basis "ao basis"
 O library "6-31G*"
 H library "6-31G*"
end

dft
  xc b3lyp
  mult 1
  convergence energy 1d-8
  grid fine
end

task dft energy
```
*Needed for the fourth geometry (O–H = 0.93 Å).*

---

**/eagle/BioFoldX/nsvensson/nwchem_run/run_05/water.nw**  
```nw
title "Water B3LYP single‑point, O–H = 0.94 Å"

start water_05

geometry units angstrom print
 O  0.0000 0.0000 0.0000
 H  0.7401 0.5787 0.0000
 H -0.7401 0.5787 0.0000
 symmetry c2v
end

basis "ao basis"
 O library "6-31G*"
 H library "6-31G*"
end

dft
  xc b3lyp
  mult 1
  convergence energy 1d-8
  grid fine
end

task dft energy
```
*Needed for the fifth geometry (O–H = 0.94 Å).*

---

**/eagle/BioFoldX/nsvensson/nwchem_run/run_06/water.nw**  
```nw
title "Water B3LYP single‑point, O–H = 0.95 Å"

start water_06

geometry units angstrom print
 O  0.0000 0.0000 0.0000
 H  0.7476 0.5848 0.0000
 H -0.7476 0.5848 0.0000
 symmetry c2v
end

basis "ao basis"
 O library "6-31G*"
 H library "6-31G*"
end

dft
  xc b3lyp
  mult 1
  convergence energy 1d-8
  grid fine
end

task dft energy
```
*Needed for the sixth geometry (O–H = 0.95 Å).*

---

**/eagle/BioFoldX/nsvensson/nwchem_run/run_07/water.nw**  
```nw
title "Water B3LYP single‑point, O–H = 0.96 Å"

start water_07

geometry units angstrom print
 O  0.0000 0.0000 0.0000
 H  0.7553 0.5910 0.0000
 H -0.7553 0.5910 0.0000
 symmetry c2v
end

basis "ao basis"
 O library "6-31G*"
 H library "6-31G*"
end

dft
  xc b3lyp
  mult 1
  convergence energy 1d-8
  grid fine
end

task dft energy
```
*Needed for the seventh geometry (O–H = 0.96 Å).*

---

**/eagle/BioFoldX/nsvensson/nwchem_run/run_08/water.nw**  
```nw
title "Water B3LYP single‑point, O–H = 0.97 Å"

start water_08

geometry units angstrom print
 O  0.0000 0.0000 0.0000
 H  0.7630 0.5971 0.0000
 H -0.7630 0.5971 0.0000
 symmetry c2v
end

basis "ao basis"
 O library "6-31G*"
 H library "6-31G*"
end

dft
  xc b3lyp
  mult 1
  convergence energy 1d-8
  grid fine
end

task dft energy
```
*Needed for the eighth geometry (O–H = 0.97 Å).*

---

**/eagle/BioFoldX/nsvensson/nwchem_run/run_09/water.nw**  
```nw
title "Water B3LYP single‑point, O–H = 0.98 Å"

start water_09

geometry units angstrom print
 O  0.0000 0.0000 0.0000
 H  0.7706 0.6033 0.0000
 H -0.7706 0.6033 0.0000
 symmetry c2v
end

basis "ao basis"
 O library "6-31G*"
 H library "6-31G*"
end

dft
  xc b3lyp
  mult 1
  convergence energy 1d-8
  grid fine
end

task dft energy
```
*Needed for the ninth geometry (O–H = 0.98 Å).*

---

**/eagle/BioFoldX/nsvensson/nwchem_run/run_10/water.nw**  
```nw
title "Water B3LYP single‑point, O–H = 0.99 Å"

start water_10

geometry units angstrom print
 O  0.0000 0.0000 0.0000
 H  0.7783 0.6095 0.0000
 H -0.7783 0.6095 0.0000
 symmetry c2v
end

basis "ao basis"
 O library "6-31G*"
 H library "6-31G*"
end

dft
  xc b3lyp
  mult 1
  convergence energy 1d-8
  grid fine
end

task dft energy
```
*Needed for the tenth geometry (O–H = 0.99 Å).*

---  

Each of these ten **`.nw`** input files tells NWChem how to build the water molecule with the specified O–H bond length, which basis set and functional to use (B3LYP/6‑31G*), and that a single‑point energy calculation (`task dft energy`) should be performed. Placing one file in each `run_XX` subdirectory satisfies the required directory layout for the Polaris workload.
````
