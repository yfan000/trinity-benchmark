# llama-3.1-8b — nwchem@polaris, base arm

Input preparation. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 2 of 9 requirements violated).

````
### Directory Structure

```bash
/eagle/BioFoldX/nsvensson/nwchem_run
├── run_01
│   └── water.nw
├── run_02
│   └── water.nw
├── run_03
│   └── water.nw
├── run_04
│   └── water.nw
├── run_05
│   └── water.nw
├── run_06
│   └── water.nw
├── run_07
│   └── water.nw
├── run_08
│   └── water.nw
├── run_09
│   └── water.nw
├── run_10
│   └── water.nw
└── water.nw
```

### Input Files

#### water.nw (global file, used as a template)

```nw
echo

title "H2O B3LYP/6-31G* single-point energy"

start H2O

geometry units angstrom print
 O 0. 0. 0.
 H 0.9 0. 0.
 H 0. 0. 0.9
 symmetry c2v
end

basis "ao basis"
 O library 6-31G*
 H library 6-31G*
end

charge 0.0

b3lyp

task dft single-point

set o-h-bond-length 0.9
```

#### run_01/water.nw

```nw
echo

title "H2O B3LYP/6-31G* single-point energy"

start H2O

geometry units angstrom print
 O 0. 0. 0.
 H 0.9 0. 0.
 H 0. 0. 0.9
 symmetry c2v
end

basis "ao basis"
 O library 6-31G*
 H library 6-31G*
end

charge 0.0

b3lyp

task dft single-point

set o-h-bond-length 0.90
```

#### run_02/water.nw

```nw
echo

title "H2O B3LYP/6-31G* single-point energy"

start H2O

geometry units angstrom print
 O 0. 0. 0.
 H 0.91 0. 0.
 H 0. 0. 0.9
 symmetry c2v
end

basis "ao basis"
 O library 6-31G*
 H library 6-31G*
end

charge 0.0

b3lyp

task dft single-point

set o-h-bond-length 0.91
```

#### run_03/water.nw

```nw
echo

title "H2O B3LYP/6-31G* single-point energy"

start H2O

geometry units angstrom print
 O 0. 0. 0.
 H 0.92 0. 0.
 H 0. 0. 0.9
 symmetry c2v
end

basis "ao basis"
 O library 6-31G*
 H library 6-31G*
end

charge 0.0

b3lyp

task dft single-point

set o-h-bond-length 0.92
```

#### run_04/water.nw

```nw
echo

title "H2O B3LYP/6-31G* single-point energy"

start H2O

geometry units angstrom print
 O 0. 0. 0.
 H 0.93 0. 0.
 H 0. 0. 0.9
 symmetry c2v
end

basis "ao basis"
 O library 6-31G*
 H library 6-31G*
end

charge 0.0

b3lyp

task dft single-point

set o-h-bond-length 0.93
```

#### run_05/water.nw

```nw
echo

title "H2O B3LYP/6-31G* single-point energy"

start H2O

geometry units angstrom print
 O 0. 0. 0.
 H 0.94 0. 0.
 H 0. 0. 0.9
 symmetry c2v
end

basis "ao basis"
 O library 6-31G*
 H library 6-31G*
end

charge 0.0

b3lyp

task dft single-point

set o-h-bond-length 0.94
```

#### run_06/water.nw

```nw
echo

title "H2O B3LYP/6-31G* single-point energy"

start H2O

geometry units angstrom print
 O 0. 0. 0.
 H 0.95 0. 0.
 H 0. 0. 0.9
 symmetry c2v
end

basis "ao basis"
 O library 6-31G*
 H library 6-31G*
end

charge 0.0

b3lyp

task dft single-point

set o-h-bond-length 0.95
```

#### run_07/water.nw

```nw
echo

title "H2O B3LYP/6-31G* single-point energy"

start H2O

geometry units angstrom print
 O 0. 0. 0.
 H 0.96 0. 0.
 H 0. 0. 0.9
 symmetry c2v
end

basis "ao basis"
 O library 6-31G*
 H library 6-31G*
end

charge 0.0

b3lyp

task dft single-point

set o-h-bond-length 0.96
```

#### run_08/water.nw

```nw
echo

title "H2O B3LYP/6-31G* single-point energy"

start H2O

geometry units angstrom print
 O 0. 0. 0.
 H 0.97 0. 0.
 H 0. 0. 0.9
 symmetry c2v
end

basis "ao basis"
 O library 6-31G*
 H library 6-31G*
end

charge 0.0

b3lyp

task dft single-point

set o-h-bond-length 0.97
```

#### run_09/water.nw

```nw
echo

title "H2O B3LYP/6-31G* single-point energy"

start H2O

geometry units angstrom print
 O 0. 0. 0.
 H 0.98 0. 0.
 H 0. 0. 0.9
 symmetry c2v
end

basis "ao basis"
 O library 6-31G*
 H library 6-31G*
end

charge 0.0

b3lyp

task dft single-point

set o-h-bond-length 0.98
```

#### run_10/water.nw

```nw
echo

title "H2O B3LYP/6-31G* single-point energy"

start H2O

geometry units angstrom print
 O 0. 0. 0.
 H 0.99 0. 0.
 H 0. 0. 0.9
 symmetry c2v
end

basis "ao basis"
 O library 6-31G*
 H library 6-31G*
end

charge 0.0

b3lyp

task dft single-point

set o-h-bond-length 0.99
```

Each of these files is needed to run the specified workload on Polaris. They contain the input parameters and configuration required for the application to perform the task.
````
