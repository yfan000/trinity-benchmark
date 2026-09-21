# gpt-oss-120b — nwchem@polaris, rich arm

Input preparation. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 1 of 9 requirements violated).

````
**run_01/h2o.nw** – O–H distance = 0.90 Å  
```nw
title "H2O single‑point B3LYP/6‑31G* (r_OH = 0.90 Å)"

start h2o_r090

geometry units angstrom print
 O  0.0000  0.0000 0.0000
 H  0.9000  0.0000 0.0000
 H -0.2250  0.8712 0.0000
end

basis "ao basis"
 O library "6-31G*"
 H library "6-31G*"
end

# modest memory limit for a tiny system
set int:mx_memory 2000 mb

dft
  xc b3lyp
  mult 1
  convergence energy 1d-8
  grid medium
end

task dft energy
```
*Needed to run the first geometry (0.90 Å).*

---

**run_02/h2o.nw** – O–H distance = 0.91 Å  
```nw
title "H2O single‑point B3LYP/6‑31G* (r_OH = 0.91 Å)"

start h2o_r091

geometry units angstrom print
 O  0.0000  0.0000 0.0000
 H  0.9100  0.0000 0.0000
 H -0.2275  0.8809 0.0000
end

basis "ao basis"
 O library "6-31G*"
 H library "6-31G*"
end

set int:mx_memory 2000 mb

dft
  xc b3lyp
  mult 1
  convergence energy 1d-8
  grid medium
end

task dft energy
```
*Needed to run the second geometry (0.91 Å).*

---

**run_03/h2o.nw** – O–H distance = 0.92 Å  
```nw
title "H2O single‑point B3LYP/6‑31G* (r_OH = 0.92 Å)"

start h2o_r092

geometry units angstrom print
 O  0.0000  0.0000 0.0000
 H  0.9200  0.0000 0.0000
 H -0.2300  0.8910 0.0000
end

basis "ao basis"
 O library "6-31G*"
 H library "6-31G*"
end

set int:mx_memory 2000 mb

dft
  xc b3lyp
  mult 1
  convergence energy 1d-8
  grid medium
end

task dft energy
```
*Needed to run the third geometry (0.92 Å).*

---

**run_04/h2o.nw** – O–H distance = 0.93 Å  
```nw
title "H2O single‑point B3LYP/6‑31G* (r_OH = 0.93 Å)"

start h2o_r093

geometry units angstrom print
 O  0.0000  0.0000 0.0000
 H  0.9300  0.0000 0.0000
 H -0.2325  0.9012 0.0000
end

basis "ao basis"
 O library "6-31G*"
 H library "6-31G*"
end

set int:mx_memory 2000 mb

dft
  xc b3lyp
  mult 1
  convergence energy 1d-8
  grid medium
end

task dft energy
```
*Needed to run the fourth geometry (0.93 Å).*

---

**run_05/h2o.nw** – O–H distance = 0.94 Å  
```nw
title "H2O single‑point B3LYP/6‑31G* (r_OH = 0.94 Å)"

start h2o_r094

geometry units angstrom print
 O  0.0000  0.0000 0.0000
 H  0.9400  0.0000 0.0000
 H -0.2350  0.9119 0.0000
end

basis "ao basis"
 O library "6-31G*"
 H library "6-31G*"
end

set int:mx_memory 2000 mb

dft
  xc b3lyp
  mult 1
  convergence energy 1d-8
  grid medium
end

task dft energy
```
*Needed to run the fifth geometry (0.94 Å).*

---

**run_06/h2o.nw** – O–H distance = 0.95 Å  
```nw
title "H2O single‑point B3LYP/6‑31G* (r_OH = 0.95 Å)"

start h2o_r095

geometry units angstrom print
 O  0.0000  0.0000 0.0000
 H  0.9500  0.0000 0.0000
 H -0.2375  0.9196 0.0000
end

basis "ao basis"
 O library "6-31G*"
 H library "6-31G*"
end

set int:mx_memory 2000 mb

dft
  xc b3lyp
  mult 1
  convergence energy 1d-8
  grid medium
end

task dft energy
```
*Needed to run the sixth geometry (0.95 Å).*

---

**run_07/h2o.nw** – O–H distance = 0.96 Å  
```nw
title "H2O single‑point B3LYP/6‑31G* (r_OH = 0.96 Å)"

start h2o_r096

geometry units angstrom print
 O  0.0000  0.0000 0.0000
 H  0.9600  0.0000 0.0000
 H -0.2400  0.9293 0.0000
end

basis "ao basis"
 O library "6-31G*"
 H library "6-31G*"
end

set int:mx_memory 2000 mb

dft
  xc b3lyp
  mult 1
  convergence energy 1d-8
  grid medium
end

task dft energy
```
*Needed to run the seventh geometry (0.96 Å).*

---

**run_08/h2o.nw** – O–H distance = 0.97 Å  
```nw
title "H2O single‑point B3LYP/6‑31G* (r_OH = 0.97 Å)"

start h2o_r097

geometry units angstrom print
 O  0.0000  0.0000 0.0000
 H  0.9700  0.0000 0.0000
 H -0.2425  0.9390 0.0000
end

basis "ao basis"
 O library "6-31G*"
 H library "6-31G*"
end

set int:mx_memory 2000 mb

dft
  xc b3lyp
  mult 1
  convergence energy 1d-8
  grid medium
end

task dft energy
```
*Needed to run the eighth geometry (0.97 Å).*

---

**run_09/h2o.nw** – O–H distance = 0.98 Å  
```nw
title "H2O single‑point B3LYP/6‑31G* (r_OH = 0.98 Å)"

start h2o_r098

geometry units angstrom print
 O  0.0000  0.0000 0.0000
 H  0.9800  0.0000 0.0000
 H -0.2450  0.9486 0.0000
end

basis "ao basis"
 O library "6-31G*"
 H library "6-31G*"
end

set int:mx_memory 2000 mb

dft
  xc b3lyp
  mult 1
  convergence energy 1d-8
  grid medium
end

task dft energy
```
*Needed to run the ninth geometry (0.98 Å).*

---

**run_10/h2o.nw** – O–H distance = 0.99 Å  
```nw
title "H2O single‑point B3LYP/6‑31G* (r_OH = 0.99 Å)"

start h2o_r099

geometry units angstrom print
 O  0.0000  0.0000 0.0000
 H  0.9900  0.0000 0.0000
 H -0.2475  0.9583 0.0000
end

basis "ao basis"
 O library "6-31G*"
 H library "6-31G*"
end

set int:mx_memory 2000 mb

dft
  xc b3lyp
  mult 1
  convergence energy 1d-8
  grid medium
end

task dft energy
```
*Needed to run the tenth geometry (0.99 Å).*
````
