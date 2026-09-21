# gemma-4-31b — nekrs@polaris, base arm

Input preparation. **FAIL** (correctness 1/2, completeness 2/2, usability 2/2; 1 of 9 requirements violated).

````
### Mesh Generation Command
To generate the binary geometry file `.re2` from a mesh description (e.g., an ExodusII file `pipe.exo`), use the following command:
`exo2nek pipe.exo pipe.re2`

---

### Required Input Files

**pipe.par**
```
# ===== pipe.par =====
userSections = CASEDATA

[GENERAL]
polynomialOrder = 7
numSteps = 20000
dt = 1e-04
timeStepper = tombo2
checkpointInterval = 1000

[PROBLEMTYPE]
equation = NavierStokes

[FLUID VELOCITY]
boundaryTypeMap = zeroDirichletN/zeroNeumann
residualTol = 1e-12
rho = 1.0
viscosity = 0.001

[FLUID PRESSURE]
residualTol = 1e-08

[CASEDATA]
re_friction = 550.0
statsStartStep = 10000
```
*This file defines the simulation physics, numerical precision, time-stepping parameters, and custom problem constants.*

**pipe.udf**
```cpp
#include "ci.inc"

static dfloat RE_FRIC;
static int STATS_START;

void userf(double time)
{
  // User-defined forcing or source terms
}

void uservp(double time)
{
  auto mesh = nrs->meshV;
  platform->linAlg->fill(mesh->Nlocal, 1.0, nrs->fluid->o_rho);
}

void UDF_Setup0(MPI_Comm comm, setupAide &options)
{
  options.getArgs("CI-MODE", ciMode);
  if (ciMode) {
    ciSetup(comm, options);
  }
  platform->par->extract("casedata", "re_friction", RE_FRIC);
  platform->par->extract("casedata", "statsStartStep", STATS_START);
}

void UDF_Setup()
{
  // Initialization of flow field based on Re_friction
}
```
*This file contains the C++ User Defined Functions required to implement specific boundary conditions, forcing, and the logic for calculating statistics.*
````
