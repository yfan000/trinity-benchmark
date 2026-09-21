# gemma-4-31b — qmcpack@aurora, rich arm

Input preparation. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 2 of 9 requirements violated).

````
To execute a Diffusion Monte Carlo (DMC) simulation for bulk silicon on Aurora, QMCPACK requires a simulation configuration file and the wavefunction/pseudopotential data.

### Data Generation Note
The `.h5` file (containing the Slater-Jastrow trial wavefunction and orbital coefficients from the DFT run) is produced by a converter tool such as `pw2qmcpack.x` (from Quantum ESPRESSO) or the QMCPACK `h5` toolset. This binary file must be present in the working directory `/lus/flare/projects/CosmoSurvey/aschmidt/qmcpack_run` before the simulation starts.

### Input Files

**Filename:** `si_bulk_dmc.xml`
```xml
<?xml version="1.0"?>
<simulation>
  <project id="si_bulk_dmc" series="0">
    <application name="qmcapp" role="dmc" class="gpu" version="1.0"/>
  </project>

  <qmcsystem>
    <simulationcell>
      <!-- 2x2x2 Supercell of Diamond Silicon (a ~ 10.26 bohr) -->
      <parameter name="lattice" units="bohr">
        20.520000    0.000000    0.000000
        0.000000    20.520000    0.000000
        0.000000    0.000000    20.520000
      </parameter>
      <parameter name="bconds">p p p</parameter>
    </simulationcell>

    <particleset name="e" random="yes">
      <group name="valence" size="256" mass="1.0">
        <parameter name="charge">-1</parameter>
        <parameter name="mass">1.0</parameter>
      </group>
    </particleset>

    <particleset name="ion0">
      <group name="Si" size="64" mass="28.085">
        <parameter name="charge">4</parameter>
        <parameter name="valence">4</parameter>
        <parameter name="atomicnumber">14</parameter>
        <attrib name="position" datatype="posArray" condition="0">
          <!-- 2x2x2 Supercell Diamond Structure -->
          0.000000 0.000000 0.000000
          5.130000 5.130000 5.130000
          10.26000 0.000000 0.000000
          15.39000 5.130000 5.130000
          0.000000 10.26000 0.000000
          5.130000 15.39000 5.130000
          10.26000 10.26000 0.000000
          15.39000 15.39000 5.130000
          0.000000 0.000000 10.26000
          5.130000 5.130000 15.39000
          10.26000 0.000000 10.26000
          15.39000 5.130000 15.39000
          0.000000 10.26000 10.26000
          5.130000 15.39000 15.39000
          10.26000 10.26000 10.26000
          15.39000 15.39000 15.39000
          2.565000 2.565000 2.565000
          7.695000 7.695000 2.565000
          12.82500 2.565000 2.565000
          17.95500 7.695000 2.565000
          2.565000 7.695000 7.695000
          7.695000 12.82500 7.695000
          12.82500 7.695000 7.695000
          17.95500 12.82500 7.695000
          2.565000 2.565000 12.82500
          7.695000 7.695000 17.95500
          12.82500 2.565000 12.82500
          17.95500 7.695000 17.95500
          2.565000 12.82500 12.82500
          7.695000 17.95500 17.95500
          12.82500 12.82500 12.82500
          17.95500 17.95500 17.95500
          2.565000 2.565000 0.000000
          7.695000 7.695000 0.000000
          12.82500 2.565000 0.000000
          17.95500 7.695000 0.000000
          2.565000 7.695000 5.130000
          7.695000 12.82500 5.130000
          12.82500 7.695000 5.130000
          17.95500 12.82500 5.130000
          2.565000 2.565000 5.130000
          7.695000 7.695000 10.26000
          12.82500 2.565000 5.130000
          17.95500 7.695000 10.26000
          2.565000 12.82500 5.130000
          7.695000 17.95500 10.26000
          12.82500 12.82500 5.130000
          17.95500 17.95500 10.26000
          2.565000 2.565000 10.26000
          7.695000 7.695000 10.26000
          12.82500 2.565000 10.26000
          17.95500 7.695000 10.26000
          2.565000 7.695000 15.39000
          7.695000 12.82500 15.39000
          12.82500 7.695000 15.39000
          17.95500 12.82500 15.39000
          2.565000 2.565000 15.39000
          7.695000 7.695000 15.39000
          12.82500 2.565000 15.39000
          17.95500 7.695000 15.39000
          2.565000 12.82500 15.39000
          7.695000 17.95500 15.39000
          12.82500 12.82500 15.39000
          17.95500 17.95500 15.39000
        </attrib>
      </group>
    </particleset>

    <wavefunction name="psi0" target="e">
      <slater determinant="det0" orbitals="orbitals.h5"/>
      <jastrow name="jastrow0" target="e"/>
    </wavefunction>

    <hamiltonian name="ham0" target="e">
      <parameter name="pseudopotential">Si.pspp</parameter>
    </hamiltonian>
  </qmcsystem>

  <dmc>
    <parameter name="walkers">4096</parameter>
    <parameter name="timestep">0.005</parameter>
    <parameter name="blocks">200</parameter>
  </dmc>
</simulation>
```
**Reason:** This is the primary configuration file that defines the system geometry (2x2x2 supercell), the electron count, the wavefunction components (referencing the H5 file), and the DMC-specific parameters (walkers, timestep, and blocks).
````
