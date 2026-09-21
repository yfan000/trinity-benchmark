# Prompt — qe@aurora

Subtask: **Input preparation**. Base arm, exactly as the model received it.

````
**Task:** Determine and write the input file(s) that Quantum ESPRESSO's `pw.x` requires for the workload described below.

---

**Workload:**
- System: 3C-SiC in the zinc-blende structure, 2x2x2 conventional supercell (64 atoms), SCF total-energy calculation, plane-wave cutoff 60 Ry, charge-density cutoff 480 Ry, 4x4x4 Monkhorst-Pack k-grid, PBE functional, ultrasoft pseudopotentials
- Target machine: Aurora (ALCF)
- Working directory: `/lus/flare/projects/PlasmaEdge/dokafor/qe_run`
- Purpose: benchmarking run to establish scaling behaviour

---

**Required input files:**

```
3csic_64atom.scf.in
```

---

**Worked example** (demonstrates block structure and keyword spelling only — different system, do not copy values, species, pseudopotential names, or comments):

```fortran
# source: https://raw.githubusercontent.com/QEF/q-e/develop/test-suite/pw_scf/scf.in
# minimal pw.x SCF input

 &control
    calculation = 'scf'
    tstress=.true.
 /
 &system
    ibrav=2, celldm(1) =10.20,
    nat=2, ntyp=1,
    ecutwfc=12.0
 /
 &electrons
 /
ATOMIC_SPECIES
 Si  28.086  Si.pz-vbc.UPF
ATOMIC_POSITIONS (alat)
 Si 0.00 0.00 0.00
 Si 0.25 0.25 0.25
K_POINTS
  2
   0.250000  0.250000  0.250000   1.00
   0.250000  0.250000  0.750000   3.00
```

---

**Instructions:**

Determine the parameters and configuration `pw.x` requires for this workload, then write out each input file in full.

- Do NOT write a job script or scheduler directives — input files only.
- (a) Use only directives and keywords you are certain exist in this application's input format — omit a feature rather than invent a keyword for it.
- (b) Never fabricate the contents of binary or runtime-generated files (e.g., wavefunction files, restart files, outputs) — list those as produced at runtime rather than writing text into them.
- (c) Treat the worked example above as a demonstration of FORM ONLY: block names, keyword spellings, card ordering. Its numerical values, chemical species, pseudopotential filenames, and comment header describe a different system and must not be carried over.
- (d) Make sure any count you declare matches the entries you actually write out (e.g., a declared `nat` must equal the number of `ATOMIC_POSITIONS` lines you write).

---

**Output:**

For each required file, give its filename and its complete contents in a fenced code block, then one line explaining why it is needed. You are writing file contents as text; you have no filesystem access and are not expected to create anything on disk.
````
