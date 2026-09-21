# Prompt — lammps@polaris

Subtask: **Input preparation**. Base arm, exactly as the model received it.

````
**Task:** Construct the LAMMPS input file required to simulate Lennard-Jones argon on this system.

---

**Workload:**
- Software: LAMMPS (already selected)
- System: Polaris (ALCF)
- Working directory: `/eagle/NuclearMPX/jmartinez/lammps_run`
- Physical problem: Lennard-Jones argon, 500,000 atoms on an fcc lattice, reduced density 0.8442, reduced temperature 0.72, NVE, 100,000 timesteps, cutoff 2.5 sigma
- Source context: input deck being ported from a different facility's system (OLCF/Frontier); only the physics parameters are known, not any prior file

---

**Required input files:**

Write exactly one input file:

```
in.lj_argon
```

---

**Worked example** *(different physical system — demonstrates form only; do not copy its numbers, species, or comments)*:

```
# source: https://raw.githubusercontent.com/lammps/lammps/develop/examples/melt/in.melt
# LJ melt, smaller box — same family, different size to our 500k-atom task

# 3d Lennard-Jones melt

units           lj
atom_style      atomic

lattice         fcc 0.8442
region          box block 0 10 0 10 0 10
create_box      1 box
create_atoms    1 box
mass            1 1.0

velocity        all create 3.0 87287 loop geom

pair_style      lj/cut 2.5
pair_coeff      1 1 1.0 1.0 2.5

neighbor        0.3 bin
neigh_modify    every 20 delay 0 check no

fix             1 all nve

#dump           id all atom 50 dump.melt

#dump           2 all image 25 image.*.jpg type type &
#               axes yes 0.8 0.02 view 60 -30
#dump_modify    2 pad 3

#dump           3 all movie 25 movie.mpg type type &
#               axes yes 0.8 0.02 view 60 -30
#dump_modify    3 pad 3

thermo          50
run             250
```

---

**Instructions:**

Determine the parameters and configuration LAMMPS requires for this workload, then write out each input file in full.

- Do **not** write a job script or any scheduler directives — input files only.
- (a) Use only directives and keywords you are certain exist in LAMMPS's input format — omit a feature rather than invent a keyword for it.
- (b) Never fabricate the contents of binary or runtime-generated files (restart files, dump trajectories, log files) — list those as produced at runtime instead of writing text into them.
- (c) Treat the worked example above as a demonstration of **form only**: block names, keyword spellings, card ordering. Its numerical values, box size, velocity seed, and comment header describe a **different** system and must not be carried over.
- (d) Make sure any count you declare matches the entries you actually write out (e.g. a declared atom count must equal what the lattice and region commands will produce).
- The fcc lattice density is 0.8442 (reduced units) and the system must contain 500,000 atoms — choose box dimensions accordingly and state your reasoning in a brief comment inside the file.
- Use reduced (LJ) units throughout; argon in LJ reduced units has epsilon = 1.0, sigma = 1.0, mass = 1.0.

---

**Output:**

For each required file, give its filename and its complete contents in a fenced code block, then one line explaining why that file is needed. You are writing file contents as text; you have no filesystem access and are not expected to create anything on disk.
````
