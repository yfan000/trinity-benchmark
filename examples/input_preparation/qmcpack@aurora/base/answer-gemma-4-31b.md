# gemma-4-31b — qmcpack@aurora, base arm

Input preparation. **FAIL** (correctness 0/2, completeness 1/2, usability 0/2, fatal; 3 of 9 requirements violated).

````
### Configuration Notes
To run this workload, a trial wavefunction and orbital information must be imported from a DFT calculation. This is typically done using the `pw2qmcpack` tool (provided by the Quantum ESPRESSO to QMCPACK interface) to convert a `.save` directory or `.xml` file from DFT into a QMCPACK-compatible HDF5 file.

**Required external file:** `si_diamond_2x2x2.h5`
**Production Command:** `pw2qmcpack.x -in dft_output.xml -out si_diamond_2x2x2.h5` (or equivalent toolchain command).

Below is the input XML for the Diffusion Monte Carlo (DMC) run.

### Input Files

**Filename:** `dmc_si_bulk.xml`
```xml
<?xml version="1.0"?>
<simulation>
  <project id="si_bulk_dmc">
    <application name="qmcapp" role="dmc" class="serial" version="1.0"/>
    <parameter name="driver_version">legacy</parameter>
  </project>

  <qmcsystem>
    <simulationcell>
      <!-- 2x2x2 supercell for Silicon (Diamond structure) -->
      <!-- Lattice constant a approx 5.43 Angstroms -> 10.3 bohr -->
      <parameter name="lattice" units="bohr">
        20.6000 0.0000 0.0000
        0.0000 20.6000 0.0000
        0.0000 0.0000 20.6000
      </parameter>
      <parameter name="bconds">p p p</parameter>
    </simulationcell>

    <particleset name="e" random="yes">
      <!-- Si has 4 valence electrons; 64 atoms * 4 = 256 electrons -->
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
        <parameter name="mass">28.085</parameter>
        <attrib name="position" datatype="posArray" condition="0">
          <!-- 64 positions for 2x2x2 supercell diamond lattice -->
          0.000000 0.000000 0.000000
          2.550000 2.550000 2.550000
          5.100000 0.000000 0.000000
          7.650000 2.550000 2.550000
          0.000000 5.100000 0.000000
          2.550000 7.650000 2.550000
          5.100000 5.100000 0.000000
          7.650000 7.650000 2.550000
          0.000000 0.000000 5.100000
          2.550000 2.550000 7.650000
          5.100000 0.000000 5.100000
          7.650000 2.550000 7.650000
          0.000000 5.100000 5.100000
          2.550000 7.650000 7.650000
          5.100000 5.100000 5.100000
          7.650000 7.650000 7.650000
          2.550000 0.000000 2.550000
          5.100000 2.550000 5.100000
          7.650000 0.000000 2.550000
          0.000000 2.550000 5.100000
          2.550000 5.100000 7.650000
          5.100000 7.650000 5.100000
          7.650000 5.100000 7.650000
          0.000000 7.650000 0.000000
          2.550000 0.000000 7.650000
          5.100000 2.550000 0.000000
          7.650000 7.650000 0.000000
          0.000000 5.100000 2.550000
          2.550000 7.650000 0.000000
          5.100000 5.100000 2.550000
          7.650000 7.650000 0.000000
          0.000000 0.000000 7.650000
          2.550000 2.550000 0.000000
          5.100000 0.000000 7.650000
          7.650000 2.550000 0.000000
          0.000000 5.100000 7.650000
          2.550000 7.650000 5.100000
          5.100000 5.100000 7.650000
          7.650000 7.650000 5.100000
          2.550000 0.000000 5.100000
          5.100000 2.550000 7.650000
          7.650000 0.000000 5.100000
          0.000000 2.550000 7.650000
          2.550000 5.100000 0.000000
          5.100000 7.650000 7.650000
          7.650000 5.100000 0.000000
          0.000000 7.650000 2.550000
          2.550000 0.000000 0.000000
          5.100000 2.550000 2.550000
          7.650000 7.650000 2.550000
          0.000000 5.100000 5.100000
          2.550000 7.650000 2.550000
          5.100000 5.100000 5.100000
          7.650000 7.650000 5.100000
          0.000000 0.000000 2.550000
          2.550000 2.550000 5.100000
          5.100000 0.000000 2.550000
          7.650000 2.550000 5.100000
          0.000000 5.100000 0.000000
          2.550000 7.650000 5.100000
          5.100000 5.100000 0.000000
          7.650000 7.650000 5.100000
          0.000000 0.000000 0.000000
          2.550000 2.550000 2.550000
        </attrib>
      </group>
    </particleset>

    <wavefunction name="psi0" target="e">
      <!-- Load Slater-Jastrow wavefunction from DFT-converted HDF5 file -->
      <parameter name="file">si_diamond_2x2x2.h5</parameter>
    </wavefunction>
  </qmcsystem>

  <dmc>
    <parameter name="timestep">0.005</parameter>
    <parameter name="blocks">200</parameter>
    <parameter name="walkers">4096</parameter>
  </dmc>
</simulation>
```
*This file defines the physical system (Si diamond supercell), the trial wavefunction source, and the DMC-specific parameters (walkers, timestep, and blocks).*
````
