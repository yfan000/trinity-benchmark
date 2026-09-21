# Prompt — nwchem@polaris, enriched arm

Subtask: **Input preparation**. The base prompt with catalog material inserted — format contract, setup and run commands, scaling notes. Derived from the base arm by verified-reversible text insertion, never regenerated, so the two arms are paired.

````
## Task
Create all input files required to run NWChem for the specified workload on Polaris.

## Workload
- **Scientific problem:** a single water molecule, B3LYP/6-31G* single-point energy
- **Sweep:** 10 runs varying the O–H bond length from 0.90 Å to 0.99 Å in 0.01 Å steps (H–O–H angle fixed at 104.5°); one input file per run
- **Target system:** Polaris (ALCF)
- **Working directory:** `/eagle/BioFoldX/nsvensson/nwchem_run`; place each input file in its own subdirectory named `run_01` through `run_10`
- **Measured reference:** a single-node, 4-rank smoke test for this system completed in ~5 s wall time

## Required input files
WRITE these files (one per subdirectory), in fenced code blocks, filename is yours to choose: `.nw`

DO NOT write contents for: `*.out`, `*.log`, `*.db`, `*.movecs` — the run produces these.

## Worked example
```
# source: https://raw.githubusercontent.com/nwchemgit/nwchem/master/QA/tests/dft_he2%2B/dft_he2%2B.nw
# He2+ cation, DFT — different molecule and functional from our H2O/B3LYP task

echo

title "he2+ hcth functional"

start he2+

geometry units angstrom print
 he 0.   0.58 0.
 symmetry c2v
end

basis "ao basis"
 he library "DZVP (DFT Orbital)"
 he p
  0.183 1.
end

basis "cd basis"
 he library DGauss_A2_DFT_Coulomb_Fitting
end

charge +1.0

dft
 mult 2
 #grid lebedev 100 8
 grid medium
 convergence energy 1d-10
 XC hcth
end

task dft gradient

title "he2+ hcth147 functional"
set dft:use_hcth147 t
dft
 XC hcth147
end

task dft gradient

[... 63 more lines of this file omitted — the form above is what matters]
```

## Input file format
Every .nw you write must contain: geometry, task
Usually present, not required: start, basis

## System context
per node: 32 CPU cores per node, 4 x A100 per node
filesystems available: /eagle, /home
Set memory stack/heap/global in input file to avoid OOM errors.

## Instructions
Determine the parameters and configuration the application requires for this workload, then write out each input file in full.

(a) Use only directives and keywords you are certain exist in this application's input format — omit a feature rather than invent a keyword for it.

(b) Never fabricate the contents of binary or runtime-generated files (databases, wavefunction or checkpoint files, restart files, outputs) — list those as produced at runtime instead of writing text into them.

(c) Treat the worked example as a demonstration of FORM ONLY: block names, keyword spellings, card ordering. Its numerical values, chemical species, pseudopotential filenames and comment headers describe a DIFFERENT system and must not be carried over.

(d) Make sure any count you declare matches the entries you actually write out (a declared atom count against the positions listed, for example).

Do NOT write a job script or scheduler directives — input files only.

Every file you write must contain the sections named under Input file format above. That section says what must appear inside each file; it does not give the values, which are yours to determine.

## Output
For each required file (all 10), give its path relative to the working directory and its complete contents in a fenced code block, then one line on why each is needed.
````
