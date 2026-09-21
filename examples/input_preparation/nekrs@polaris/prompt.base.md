# Prompt — nekrs@polaris

Subtask: **Input preparation**. Base arm, exactly as the model received it.

````
## Task
Determine and write out every text input file that NekRS requires to simulate the given workload. Do not write a job script or scheduler directives.

## Workload
- Problem: turbulent pipe flow at friction Reynolds number 550, 32,000 spectral elements at polynomial order 7, 20,000 timesteps, statistics collected over the final 10,000
- System: Polaris (ALCF)
- Working directory: /eagle/ClimateRegional/tnakamura/nekrs_run
- Software selection: NekRS
- The mesh (binary geometry file, not hand-written) must be built with the `nek2to3` / `exo2nek` / `gmsh2nek` toolchain from a suitable mesh description; give the command that generates it but do not fabricate its binary contents

## Required input files
WRITE these 2 files, one fenced code block each, filenames are yours to choose: `.par`, `.udf`

DO NOT write contents for:
- `.re2` — built by the toolchain, not written by hand; give the command that builds it
- `*.fld`, `*.f0*`, `logfile`, `SESSION.NAME`, `nekRS.log*` — the run produces these

## Worked example
The following is a real input deck for a **different** physical system taken from the NekRS repository. It demonstrates required block names, keyword spellings, and card ordering **only**. Its numerical values, boundary conditions, and comment headers describe a different problem and must not be carried over.

```
# ===== channel.par =====
# source: https://raw.githubusercontent.com/Nek5000/nekRS/master/examples/channel/channel.par
# a real input for a DIFFERENT system — form only

userSections = CASEDATA

[GENERAL]
polynomialOrder = 7
#startFrom = "restart.fld"
numSteps = 100
dt = 1e-03
timeStepper = tombo2
checkpointInterval = 0

[PROBLEMTYPE]
equation = Stokes+variableViscosity

[FLUID VELOCITY]
boundaryTypeMap = zeroDirichletN/zeroNeumann
residualTol = 1e-12
rho = 1.0
viscosity = 0.1

[FLUID PRESSURE]
residualTol = 1e-08

[CASEDATA]
p_rot = 0.7853981633974483 # \pi / 4
```

```
# ===== channel.udf =====
# source: https://raw.githubusercontent.com/Nek5000/nekRS/master/examples/channel/channel.udf
# a real input for a DIFFERENT system — form only

#include "ci.inc"

static deviceMemory<dfloat> o_nekFU;
static deviceMemory<dfloat> o_nekMue;
static dfloat P_ROT;

#ifdef __okl__

#endif

void userf(double time)
{
  nrs->fluid->o_explicitTerms().copyFrom(o_nekFU, nrs->fluid->fieldOffsetSum);
}

void uservp(double time)
{
  auto mesh = nrs->meshV;
  platform->linAlg->fill(mesh->Nlocal, 1.0, nrs->fluid->o_rho);
  nrs->fluid->o_mue.copyFrom(o_nekMue, mesh->Nlocal);
}

void UDF_Setup0(MPI_Comm comm, setupAide &options)
{
  options.getArgs("CI-MODE", ciMode);
  if (ciMode) {
    ciSetup(comm, options);
  }
  platform->par->extract("casedata", "p_rot", P_ROT);
  if (platform->options.compareArgs("BUILD ONLY", "FALSE")) {
    *nek::ptr<double>("p_rot") = P_ROT;
  }
}

void UDF_Setup()
{
[... 31 more lines of this file omitted — the form above is what matters]
```

## Instructions
Determine the parameters and configuration NekRS requires for this workload, then write out each input file in full. Do NOT write a job script or scheduler directives — input files only.

(a) Use only directives and keywords you are certain exist in NekRS's input format — omit a feature rather than invent a keyword for it.
(b) Never fabricate the contents of binary or runtime-generated files (mesh binaries, checkpoint files, outputs) — list those as produced at runtime or by a build tool instead.
(c) Treat the worked example above as a demonstration of FORM ONLY: block names, keyword spellings, card ordering. Its numerical values, boundary conditions, and comment headers describe a different system and must not be carried over.
(d) Make sure any count you declare matches the entries you actually write out.

## Output
For each required file, give its filename and its complete contents in a fenced code block, then one line explaining why each file is needed. You are writing file contents as text; you have no filesystem access and are not expected to create anything on disk.
````
