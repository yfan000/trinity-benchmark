# gpt-oss-120b — nekrs@polaris, base arm

Input preparation. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 2 of 9 requirements violated).

````
**File:** `pipe.par`  

```ini
# pipe.par
# Input parameter file for a turbulent pipe flow at friction Reynolds number Reτ = 550
# 32 000 spectral elements, polynomial order 7, 20 000 time steps.
# Statistics are collected over the last 10 000 steps (handled at the post‑processing stage).

userSections = CASEDATA          # allow the UDF to read the CASEDATA section

[GENERAL]
polynomialOrder   = 7           # spectral order
numSteps          = 20000       # total number of timesteps
dt                = 1e-04       # timestep size (chosen to give a reasonable CFL)
timeStepper       = bdf2        # second‑order BDF scheme (standard in NekRS)
checkpointInterval = 0        # no checkpoint files – can be changed if a restart is desired

[PROBLEMTYPE]
equation = NavierStokes         # incompressible Navier–Stokes equations

[FLUID VELOCITY]
boundaryTypeMap   = zeroDirichletN/periodic   # no‑slip walls, periodic in the axial direction
residualTol       = 1e-12
rho               = 1.0
viscosity         = 0.00181818181818   # ν = 1 / Reτ (non‑dimensional)

[FLUID PRESSURE]
residualTol       = 1e-08

[CASEDATA]                     # values that the UDF can read
re_tau        = 550           # friction Reynolds number (for diagnostics)
pipe_radius   = 1.0           # pipe radius in the chosen non‑dimensional units
dpdx          = -0.001        # constant streamwise pressure gradient (negative = driving)
```

*Why this file is needed:* `pipe.par` tells NekRS the global simulation settings (time stepping, polynomial order, fluid properties, boundary‑condition mapping) and supplies case‑specific data (`dpdx`, `re_tau`, etc.) that the user‑defined function (`pipe.udf`) will read to apply the driving pressure gradient.

---

**File:** `pipe.udf`  

```c
/* pipe.udf
 * User‑defined functions for the turbulent pipe‑flow case.
 * The only runtime requirement is to impose a constant streamwise
 * pressure gradient that drives the flow. The value of the gradient
 * is read from the CASEDATA section of pipe.par.
 */

#include "ci.inc"

static dfloat DPDX;               // streamwise pressure gradient (negative value)

/* ---------------------------------------------------------------------
 * Setup called once before the solver builds its data structures.
 * Here we read the pressure‑gradient value from the CASEDATA section
 * and copy it into a NekRS global variable that the solver uses as
 * the driving term.
 * --------------------------------------------------------------------- */
void UDF_Setup0(MPI_Comm comm, setupAide &options)
{
  platform->par->extract("casedata", "dpdx", DPDX);

  /* The variable “p_grad” is a built‑in NekRS scalar that multiplies the
   * unit vector in the streamwise direction to create a constant pressure
   * forcing.  We set it only after the “BUILD ONLY” test so that a
   * pre‑compile pass does not attempt to dereference the pointer.
   */
  if (platform->options.compareArgs("BUILD ONLY", "FALSE")) {
    *nek::ptr<double>("p_grad") = DPDX;
  }
}

/* No additional explicit body forces are required. */
void userf(double time) {}

/* No manipulation of velocity/pressure fields is needed each step. */
void uservp(double time) {}
```

*Why this file is needed:* `pipe.udf` provides the only user‑defined code NekRS must execute: it reads the pressure‑gradient parameter (`dpdx`) from the `.par` file and stores it in the solver’s internal variable `p_grad`, which supplies the constant driving force for the pipe flow.

---

**Mesh build command (binary geometry file `.re2`)**

The geometric description of the pipe must be converted to NekRS’s binary mesh format before the run:

```bash
# Convert a Gmsh mesh (pipe.msh) to NekRS binary format and then to the .re2 file
gmsh2nek -p pipe.msh -o pipe.nek && nek2to3 -i pipe.nek -o pipe.re2
```

*Why this command is listed:* `nekRS` reads the mesh from the binary file `pipe.re2`. The command shows how that file is generated from a typical Gmsh mesh; the binary content itself is created at runtime and is **not** written by hand.
````
