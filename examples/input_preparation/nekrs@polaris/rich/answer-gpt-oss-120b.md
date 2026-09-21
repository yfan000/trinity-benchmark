# gpt-oss-120b — nekrs@polaris, rich arm

Input preparation. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 2 of 9 requirements violated).

````
**pipe.par** – main simulation parameters (mesh, solver, fluid, and case‑specific data)  

```text
# pipe.par
# NekRS input deck for turbulent pipe flow (Reτ = 550)

userSections = CASEDATA

[GENERAL]
polynomialOrder = 7
numSteps       = 20000            # total timesteps
dt             = 1e-04            # time step size (chosen to give a Courant ≲ 0.5)
timeStepper    = bdf2             # second‑order implicit scheme
checkpointInterval = 0           # no restart files written during this run
#startFrom   = "restart.fld"     # (not used for a fresh start)

[PROBLEMTYPE]
equation = NavierStokes        # incompressible Navier–Stokes

[FLUID VELOCITY]
boundaryTypeMap = zeroDirichletN     # no‑slip wall; other faces are periodic in the mesh file
residualTol   = 1e-10
rho           = 1.0
viscosity     = 0.001818            # ν = 1/Reτ  (Reτ = 550) → 1/550 ≈ 0.001818

[FLUID PRESSURE]
residualTol   = 1e-08

[CASEDATA]
dpdx = -0.005                # constant axial pressure gradient that drives the flow
```

*Why this file is needed:*  
`pipe.par` tells NekRS everything it needs to know about the numerical method, physical parameters, and case‑specific data (the driving pressure gradient). The `[GENERAL]` section sets the polynomial order, number of steps, and time‑stepper; the fluid sections give density, viscosity, and solver tolerances; `CASEDATA` supplies a value that the UDF will read to apply the body force.

---

**pipe.udf** – user‑defined functions that inject the pressure‑gradient forcing and expose the case data to the solver  

```c
/* pipe.udf
   Minimal UDF for a periodic pipe driven by a constant pressure gradient.
*/

#include "udf.hpp"

static dfloat DPX;                // axial pressure gradient read from CASEDATA

/* Called once before the solver starts – read case data and store it in NekRS */
void UDF_Setup0(MPI_Comm comm, setupAide &options)
{
  platform->par->extract("casedata", "dpdx", DPX);
  // NekRS exposes a scalar named "dpdx" that is used as a body force in the x‑direction.
  // The following line copies the user‑provided value into that scalar.
  *nek::ptr<double>("dpdx") = DPX;
}

/* Called after the mesh and fields are allocated – nothing special needed here */
void UDF_Setup()
{
}

/* Optional hook for user‑defined source terms (not needed because the body force is set above) */
void userf(double time)
{
}

/* Optional hook for user‑defined velocity‑boundary updates (pipe walls are no‑slip, set in the mesh) */
void uservp(double time)
{
}
```

*Why this file is needed:*  
`pipe.udf` supplies the only user‑defined piece of physics: a constant axial pressure gradient (`dpdx`) that drives the turbulent pipe flow. The value is read from the `[CASEDATA]` section of `pipe.par` and copied into NekRS’s internal scalar that the solver adds to the momentum equations.

---

### Mesh generation command (binary geometry file `.re2`)

The binary mesh required by NekRS is produced from a Gmsh description of the pipe (e.g., `pipe.geo`). The typical tool chain on Polaris is:

```bash
# 1. Create a 2‑D/3‑D Gmsh mesh (Msh‑2 format)
gmsh -2 pipe.geo -format msh2 -o pipe.msh

# 2. Convert the Gmsh mesh to NekRS binary geometry (.re2)
gmsh2nek -m pipe.msh -o pipe.re2

# 3. (optional) Convert to legacy Nek5000 .rea if needed
nek2to3 -i pipe.re2 -o pipe.rea
```

*Why the command is needed:*  
NekRS reads a binary mesh file (`*.re2`). The commands above take a human‑editable mesh description (`pipe.geo`), generate a Gmsh mesh, and then translate it into the required binary format. The optional `nek2to3` step is included for completeness if a legacy `.rea` file is ever wanted.
````
