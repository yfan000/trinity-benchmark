# Prompt — hpl@crux, enriched arm

Subtask: **Input preparation**. The base prompt with catalog material inserted — format contract, setup and run commands, scaling notes. Derived from the base arm by verified-reversible text insertion, never regenerated, so the two arms are paired.

````
## Task
Write the complete set of input files required to run HPL for the workload described below.

## Workload
- Application: HPL (selected by prior pipeline stage)
- Problem: HPL LINPACK, problem size N=50000, block size NB=232, 2x2 process grid
- System: Crux (ALCF, AMD EPYC CPU-only cluster)
- Working directory: /eagle/CatalysisDFT/gpetrov/hpl_run
- Prior run: a small-scale test passed; this is a scale-up run using the same algorithmic choices

## Required input files
WRITE this file, in a fenced code block, under exactly this name (the application opens no other): HPL.dat

DO NOT write contents for:
- HPL.out, *.log — the run produces these

## Worked example
```
# source: https://raw.githubusercontent.com/NVIDIA/deepops/master/workloads/bit/hpl/hplfiles/HPL.dat_2N_dgx2
# a real input for a DIFFERENT system — form only

HPLinpack benchmark input file
Innovative Computing Laboratory, University of Tennessee
HPL.out      output file name (if any)
6            device out (6=stdout,7=stderr,file)
1            # of problems sizes (N)
376832 335872 344064 352256 360448 368640 376832   Ns
1           # of NBs
256         NBs
0            PMAP process mapping (0=Row-,1=Column-major)
1            # of process grids (P x Q)
8         Ps
4         Qs
16.0         threshold
1            # of panel fact
0        PFACTs (0=left, 1=Crout, 2=Right)
1            # of recursive stopping criterium
4          NBMINs (>= 1)
1            # of panels in recursion
2            NDIVs
1            # of recursive panel fact.
0        RFACTs (0=left, 1=Crout, 2=Right)
1            # of broadcast
2          BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)
1            # of lookahead depth
0            DEPTHs (>=0)
1            SWAP (0=bin-exch,1=long,2=mix)
192          swapping threshold
1            L1 in (0=transposed,1=no-transposed) form
0            U  in (0=transposed,1=no-transposed) form
1            Equilibration (0=no,1=yes)
8            memory alignment in double (> 0)
```

## Input file format
Every HPL.dat you write must contain: HPLinpack, Ns, NBs, Ps, Qs

## System context
per node: 128 CPU cores per node, 256 GB memory per node
filesystems available: /eagle, /home

## Instructions
Determine the parameters and configuration the application requires for this workload, then write out each input file in full. Do NOT write a job script or scheduler directives — input files only.

Additional requirements:
(a) Use only directives and keywords you are certain exist in this application's input format — omit a feature rather than invent a keyword for it.
(b) Never fabricate the contents of binary or runtime-generated files (databases, wavefunction or checkpoint files, restart files, outputs) — list those as produced at runtime instead of writing text into them.
(c) Treat the worked example above as a demonstration of FORM ONLY: block names, keyword spellings, card ordering. Its numerical values, chemical species, pseudopotential filenames and comment headers describe a DIFFERENT system and must not be carried over.
(d) Make sure any count you declare matches the entries you actually write out (a declared atom count against the positions listed, for example).

Every file you write must contain the sections named under Input file format above. That section says what must appear inside each file; it does not give the values, which are yours to determine.

## Output
For each required file, give its filename and its complete contents in a fenced code block, then one line on why each is needed. You are writing file contents as text; you have no filesystem access and are not expected to create anything on disk.
````
