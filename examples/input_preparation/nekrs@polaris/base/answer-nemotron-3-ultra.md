# nemotron-3-ultra — nekrs@polaris, base arm

Input preparation. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 1 of 9 requirements violated).

````
# ===== pipe_re550.par =====
# Turbulent pipe flow at Re_tau = 550
# 32,000 spectral elements, polynomial order 7
# 20,000 timesteps, statistics over final 10,000
# Mesh generated with: gmsh -3 pipe.geo -o pipe.msh && gmsh2nek pipe.msh pipe_re550.re2 7

userSections = CASEDATA

[GENERAL]
mesh = pipe_re550
polynomialOrder = 7
numSteps = 20000
dt = 5e-4
timeStepper = bdf2
checkpointInterval = 5000
writeInterval = 5000

[PROBLEMTYPE]
equation = incompressibleNavierStokes

[FLUID VELOCITY]
# Boundary IDs: 1=wall (no-slip), 2 and 3=periodic (inlet/outlet faces)
boundaryTypeMap = zeroDirichlet/periodic/periodic
residualTol = 1e-10
rho = 1.0
viscosity = 0.0018181818181818182

[FLUID PRESSURE]
residualTol = 1e-8

[SOLVER]
pressureSolver = amg
velocitySolver = amg
amgCoarsenType = HMIS
amgRelaxType = SOR_JACOBI
amgNumSweeps = 1

[STATISTICS]
computeStatistics = true
statisticsStartStep = 10000
statisticsInterval = 1
statisticsOutputInterval = 1000

[CASEDATA]
pipe_radius = 1.0
friction_Re = 550
pressure_gradient = -2.0

This file provides all simulation control parameters: mesh reference, discretization order, time-stepping scheme and step count, fluid properties tuned for Re_tau=550 (nu=1/550), boundary conditions for a periodic pipe, solver tolerances and AMG settings, and statistics collection configuration for the final 10,000 steps. The CASEDATA section passes problem-specific values to the UDF.

# ===== pipe_re550.udf =====
// User-defined functions for turbulent pipe flow at Re_tau = 550
// Adds constant pressure gradient forcing in streamwise (z) direction

#include "udf.hpp"
#include "ci.inc"

static dfloat PRESSURE_GRADIENT;
static dfloat PIPE_RADIUS;

#ifdef __okl__

@kernel void pressureGradientKernel(const int N, const dfloat pressureGrad, 
                                     dfloat *FU) {
  for (int n = 0; n < N; ++n; @tile(256, @outer, @inner)) {
    // Add pressure gradient to z-momentum (3rd component, offset 2*N)
    FU[n + 2*N] += pressureGrad;
  }
}

#endif

void usrSource(nrs_t *nrs, dfloat time, occa::memory o_U, occa::memory o_FU) {
  // Forcing = -dp/dz; pressure_gradient from .par is -2.0
  const dfloat forcing = -PRESSURE_GRADIENT;
  auto mesh = nrs->meshV;
  const int N = mesh->Nlocal;
  pressureGradientKernel(N, forcing, o_FU);
}

void UDF_Setup0(MPI_Comm comm, setupAide &options) {
  options.getArgs("CI-MODE", ciMode);
  if (ciMode) {
    ciSetup(comm, options);
  }
  
  // Extract case data from .par [CASEDATA] section
  platform->par->extract("casedata", "pressure_gradient", PRESSURE_GRADIENT);
  platform->par->extract("casedata", "pipe_radius", PIPE_RADIUS);
  
  if (platform->options.compareArgs("BUILD ONLY", "FALSE")) {
    *nek::ptr<double>("pressure_gradient") = PRESSURE_GRADIENT;
    *nek::ptr<double>("pipe_radius") = PIPE_RADIUS;
  }
}

void UDF_Setup(nrs_t *nrs) {
  // Initialize velocity to zero; flow develops under pressure gradient
  auto mesh = nrs->meshV;
  const int N = mesh->Nlocal;
  platform->linAlg->fill(3*N, 0.0, nrs->o_U);
  platform->linAlg->fill(N, 0.0, nrs->o_P);
}

void UDF_ExecuteStep(nrs_t *nrs, dfloat time, int tstep) {
  // Apply constant pressure gradient forcing each timestep
  usrSource(nrs, time, nrs->o_U, nrs->fluid->o_explicitTerms());
  // Statistics collection handled by built-in module (see [STATISTICS] in .par)
}

This file implements the physics not covered by standard keywords: a constant streamwise pressure gradient body force (via an OCCA kernel) to drive the periodic pipe flow at the target friction Reynolds number, reads case parameters from the .par file, initializes the flow field, and hooks the forcing into the timestep loop.
````
