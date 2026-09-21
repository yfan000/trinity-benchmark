# llama-3.1-8b — nekrs@polaris, base arm

Input preparation. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 2 of 9 requirements violated).

````
## Required Input Files

### `.par` file

```par
# ===== pipe_flow.par =====

userSections = CASEDATA

[GENERAL]
polynomialOrder = 7
numSteps = 20000
dt = 1e-03
timeStepper = tombo2
checkpointInterval = 0

[PROBLEMTYPE]
equation = NavierStokes

[FLUID VELOCITY]
boundaryTypeMap = zeroDirichletN/zeroNeumann
residualTol = 1e-12
rho = 1.0
viscosity = 1.0
frictionReynolds = 550

[FLUID PRESSURE]
residualTol = 1e-08

[CASEDATA]
numStatsSteps = 10000
```

This file, `pipe_flow.par`, contains the problem parameters and configuration required by NekRS. The numerical values and boundary conditions describe the turbulent pipe flow problem specified in the workload.

### `.udf` file

```udf
# ===== pipe_flow.udf =====

#include "ci.inc"

static deviceMemory<dfloat> o_nekFU;
static deviceMemory<dfloat> o_nekMue;

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
  platform->par->extract("casedata", "numStatsSteps", numStatsSteps);
}

void UDF_Setup()
{
  nrs->fluid->o_numStatsSteps = numStatsSteps;
}
```

This file, `pipe_flow.udf`, contains the user-defined functions (UDFs) required by NekRS. The UDFs are used to set up the problem and collect statistics.

### `nek2to3` / `exo2nek` / `gmsh2nek` toolchain command

```bash
nek2to3 -i pipe_flow.geo -o pipe_flow.exo
exo2nek pipe_flow.exo -o pipe_flow.nek
gmsh2nek pipe_flow.msh -o pipe_flow.re2
```

This command generates the binary geometry file `pipe_flow.re2` from the mesh description `pipe_flow.geo`.

### Mesh description file

```geo
// pipe_flow.geo

Point(1) = {0, 0, 0, 1.0};
Point(2) = {1, 0, 0, 1.0};
Point(3) = {1, 1, 0, 1.0};
Point(4) = {0, 1, 0, 1.0};

Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};

Circle(1) = {1, 2, 3};
Circle(2) = {3, 4, 1};

Extrude{1} {2} Through {3} In {4} Using {1};
```

This file, `pipe_flow.geo`, contains the mesh description for the turbulent pipe flow problem.

### Build command for `pipe_flow.re2` file

```bash
nek2to3 -i pipe_flow.geo -o pipe_flow.exo
exo2nek pipe_flow.exo -o pipe_flow.nek
gmsh2nek pipe_flow.msh -o pipe_flow.re2
```

This command builds the binary geometry file `pipe_flow.re2` from the mesh description `pipe_flow.geo`.
````
