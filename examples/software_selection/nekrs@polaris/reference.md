# Reference answer — nekrs@polaris

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
Selected application: NekRS

Rationale: NekRS is the GPU-accelerated spectral element CFD solver (Navier-Stokes) installed on Polaris, targeting A100 GPUs via a native CUDA backend. It directly solves incompressible Navier-Stokes flows using the spectral element method. NekRS writes binary field/restart files (*.fld, *.f0*) at checkpoints and supports restarting from those files by specifying the restart step in the case parameter file, making it the correct choice for resuming an interrupted spectral-element CFD run. Nek5000 is the CPU-only predecessor and lacks GPU support; OpenFOAM is a finite-volume code, not a spectral element solver. NekRS is the only installed application that matches all three requirements: spectral element method, Navier-Stokes incompressible flow, and GPU-resident execution on Polaris A100s with checkpoint/restart capability.
````
