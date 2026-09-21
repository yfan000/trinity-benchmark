# Prompt — qmcpack@aurora

Subtask: **Input preparation**. Base arm, exactly as the model received it.

````
## Task
Determine the parameters and configuration that QMCPACK requires for this workload, then write out each input file in full.

## Workload
- **Software:** QMCPACK (already selected)
- **System:** Aurora (ALCF)
- **Working directory:** `/lus/flare/projects/CosmoSurvey/aschmidt/qmcpack_run`
- **Scientific problem:** bulk silicon in the diamond structure, 2x2x2 supercell (64 atoms), diffusion Monte Carlo with a Slater-Jastrow trial wavefunction from a prior DFT run, 4096 walkers, timestep 0.005 Ha⁻¹, 200 DMC blocks
- **First run of this workload on this machine**

## Required input files
WRITE this file (filename is yours to choose): `.xml`

DO NOT write contents for:
- `.h5` — built by the toolchain (e.g., `pw2qmcpack.x` or equivalent converter), not written by hand; provide the command or note that produces it
- `*.scalar.dat` — produced at runtime by the application

Optional, only if this workload needs them: `.BFD.xml`, `.ccECP.xml`

## Worked example
```xml
# source: https://raw.githubusercontent.com/QMCPACK/qmcpack/develop/tests/solids/diamondC_1x1x1_pp/qmc_short.in.xml
# a real input for a DIFFERENT system — form only

<?xml version="1.0"?>
<simulation>
   <project id="qmc_short" series="0">
      <application name="qmcapp" role="molecu" class="serial" version="1.0"/>
    <parameter name="driver_version">legacy</parameter>
   </project>
   <qmcsystem>
      <simulationcell>
         <parameter name="lattice" units="bohr">
                  3.37316115        3.37316115        0.00000000
                  0.00000000        3.37316115        3.37316115
                  3.37316115        0.00000000        3.37316115
         </parameter>
         <parameter name="bconds">
            p p p
         </parameter>
         <parameter name="LR_dim_cutoff"       >    15                 </parameter>
      </simulationcell>
      <particleset name="e" random="yes">
         <group name="u" size="4" mass="1.0">
            <parameter name="charge"              >    -1                    </parameter>
            <parameter name="mass"                >    1.0                   </parameter>
         </group>
         <group name="d" size="4" mass="1.0">
            <parameter name="charge"              >    -1                    </parameter>
            <parameter name="mass"                >    1.0                   </parameter>
         </group>
      </particleset>
      <particleset name="ion0">
         <group name="C" size="2" mass="21894.7135906">
            <parameter name="charge"              >    4                     </parameter>
            <parameter name="valence"             >    4                     </parameter>
            <parameter name="atomicnumber"        >    6                     </parameter>
            <parameter name="mass"                >    21894.7135906            </parameter>
            <attrib name="position" datatype="posArray" condition="0">
                     0.00000000        0.00000000        0.00000000
                     1.68658058        1.68658058        1.68658058
            </attrib>
         </group>
      </particleset>
      <wavefunction name="psi0" target="e">
[... 52 more lines of this file omitted — the form above is what matters]
```

## Instructions
Determine the parameters and configuration QMCPACK requires for this workload, then write out each input file in full. Do NOT write a job script or scheduler directives — input files only.

Additionally:
(a) Use only directives and keywords you are certain exist in this application's input format — omit a feature rather than invent a keyword for it.
(b) Never fabricate the contents of binary or runtime-generated files (databases, wavefunction or checkpoint files, restart files, outputs) — list those as produced at runtime instead of writing text into them.
(c) Treat the worked example above as a demonstration of FORM ONLY: block names, keyword spellings, card ordering. Its numerical values, chemical species, pseudopotential filenames and comment headers describe a DIFFERENT system and must not be carried over.
(d) Make sure any count you declare matches the entries you actually write out (a declared atom count against the positions listed, for example).

## Output
For each required file, give its filename and its complete contents in a fenced code block, then one line on why each is needed. You are writing file contents as text; you have no filesystem access and are not expected to create anything on disk.
````
