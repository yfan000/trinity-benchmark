# nemotron-3-ultra — nekrs@polaris, rich arm

Input preparation. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 1 of 9 requirements violated).

````
# Input Files for NekRS Turbulent Pipe Flow at Re_τ=550

## pipe_re550.par
```text
# ===== pipe_re550.par =====
# Turbulent pipe flow at friction Reynolds number 550
# 32,000 spectral elements, polynomial order 7
# 20,000 timesteps, statistics over final 10,000

[GENERAL]
polynomialOrder = 7
dt = 0.0005
numSteps = 20000
startTime = 0.0
timeStepper = BDF2
targetCFL = 0.4
checkpointInterval = 5000
writeControl = timeStep
writeInterval = 5000
outputDirectory = .

[MESH]
meshFile = pipe_re550.re2
dimension = 3

[PROBLEMTYPE]
equation = incompressibleNavierStokes
startFrom = "zero"

[FLUID]
density = 1.0
viscosity = 0.0018181818181818182  # nu = 1/Re_tau for R=1, u_tau=1

[VELOCITY]
solver = CG
preconditioner = multigrid
residualTol = 1e-8
residualProjTol = 1e-6
maxIter = 500

[PRESSURE]
solver = CG
preconditioner = multigrid
residualTol = 1e-8
residualProjTol = 1e-6
maxIter = 500

[BOUNDARY]
# Boundary IDs from mesh: 1 = wall, 2 = periodic_inlet, 3 = periodic_outlet
velocity = 1:noSlip
velocity = 2:periodic
velocity = 3:periodic

[STATISTICS]
enabled = true
startStep = 10001
sampleInterval = 1
outputControl = timeStep
outputInterval = 10000
fields = velocity,pressure,vorticity,wallShearStress

[OUTPUT]
format = vtk
precision = double
writeMesh = true
writeInitial = true
```

**Why this file is needed:** This is the primary parameter deck that tells NekRS every run-time setting: discretization order, time-integrator, step count, fluid properties, solver tolerances, boundary-condition mapping for the three mesh surfaces (wall + periodic pair), and the statistics plan (activate at step 10001, sample every step, dump after the final 10 000 steps). The mesh itself is referenced by name only; its binary contents are produced by the toolchain.

---

## pipe_re550.udf
```text
# ===== pipe_re550.udf =====
# User-defined functions for Re_tau=550 pipe flow
# Imposes constant streamwise pressure gradient to maintain target friction velocity

#include "ci.inc"
#include "udfUtils.inc"

static deviceMemory<dfloat> o_bodyForce;
static dfloat PIPE_RADIUS;
static dfloat TAU_WALL;
static dfloat DP_DZ;

#ifdef __okl__
kernel void udfBodyForceKernel(
  dfloat time,
  const dfloat *U,
  dfloat *FU,
  dfloat *rho,
  dfloat *mue,
  dfloat *P,
  const int n)
{
  int tid = globalId();
  if (tid >= n) return;
  FU[tid + 2*n] += DP_DZ;  // z-component (streamwise) body force
}
#endif

void UDF_Setup0(MPI_Comm comm, setupAide &options)
{
  options.getArgs("CI-MODE", ciMode);
  if (ciMode) ciSetup(comm, options);

  // Target friction Re_tau = 550 with R = 1, rho = 1, u_tau = 1
  PIPE_RADIUS = 1.0;
  TAU_WALL = 1.0;          // u_tau^2 * rho
  DP_DZ = -2.0 * TAU_WALL / PIPE_RADIUS;  // -G = -2*tau_w/R for pipe

  platform->linAlg->initDeviceMemory(nrs->meshV->Nlocal, o_bodyForce);
  platform->linAlg->fill(nrs->meshV->Nlocal, 0.0, o_bodyForce);
  // z-component (offset 2*N) gets DP_DZ
  platform->linAlg->axpy(nrs->meshV->Nlocal, DP_DZ, platform->linAlg->ones, 1, o_bodyForce, 1, 2);
}

void UDF_Setup(MPI_Comm comm) {}

void UDF_ExecuteStep(double time, int tstep)
{
  if (tstep == 10001) {
    if (platform->comm.mpiRank == 0)
      printf("Statistics collection started at step %d\n", tstep);
  }
}

void userf(double time)
{
  // Add constant streamwise body force to momentum equation
  auto mesh = nrs->meshV;
  int N = mesh->Nlocal;
  dfloat *FU = nrs->fluid->o_explicitTerms + 2*N*nrs->fieldOffset; // z-component
  platform->linAlg->axpy(N, 1.0, o_bodyForce + 2*N, 1, FU, 1);
}

void uservp(double time)
{
  auto mesh = nrs->meshV;
  platform->linAlg->fill(mesh->Nlocal, 1.0, nrs->fluid->o_rho);
  platform->linAlg->fill(mesh->Nlocal, nrs->fluid->mu, nrs->fluid->o_mue);
}
```

**Why this file is needed:** The UDF injects the constant axial pressure gradient (−2τ_w/R) that drives the flow at the target friction velocity u_τ=1 (hence Re_τ=550 with R=1, ν=1/550). It also marks the statistics onset at step 10 001 for post-processing hooks. The `userf` kernel is called every stage of the time-stepper to add the body force to the explicit terms.

---

## Mesh Generation Command (not a written file)
```bash
# Generate the binary .re2 mesh from a Gmsh description
gmsh -3 -order 7 pipe_re550.geo -o pipe_re550.msh
gmsh2nek pipe_re550.msh pipe_re550.re2
```
The `.geo` file (not shown) describes a 32 000-element pipe of radius 1 and length ≈2π with periodic inlet/outlet pairing and a no-slip wall boundary. The two commands above produce the required `pipe_re550.re2` binary mesh that the `.par` file references.
````
