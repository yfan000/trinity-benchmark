# nemotron-3-ultra — qmcpack@aurora, base arm

Input preparation. **FAIL** (correctness 0/2, completeness 1/2, usability 0/2, fatal; 3 of 9 requirements violated).

````
**File: `si_64_dmc.in.xml`** — Main QMCPACK input defining the 64-atom Si supercell, Slater-Jastrow wavefunction, Hamiltonian with BFD pseudopotential, and DMC run parameters (4096 walkers, τ=0.005 Ha⁻¹, 200 blocks).

```xml
<?xml version="1.0"?>
<simulation>
  <project id="si_64_dmc" series="0">
    <application name="qmcapp" role="molecu" class="mpi" version="3.18"/>
    <parameter name="driver_version">legacy</parameter>
  </project>

  <qmcsystem>
    <simulationcell>
      <parameter name="lattice" units="bohr">
        20.520  0.000  0.000
         0.000 20.520  0.000
         0.000  0.000 20.520
      </parameter>
      <parameter name="bconds">p p p</parameter>
      <parameter name="LR_dim_cutoff">15.0</parameter>
    </simulationcell>

    <particleset name="ion0" random="no">
      <group name="Si" size="64" mass="49336.8">
        <parameter name="charge">4</parameter>
        <parameter name="valence">4</parameter>
        <parameter name="atomicnumber">14</parameter>
        <parameter name="mass">49336.8</parameter>
        <attrib name="position" datatype="posArray" condition="0">
           0.000000   0.000000   0.000000
           2.565000   2.565000   0.000000
           2.565000   0.000000   2.565000
           0.000000   2.565000   2.565000
           5.130000   5.130000   0.000000
           5.130000   0.000000   5.130000
           0.000000   5.130000   5.130000
           2.565000   7.695000   2.565000
           7.695000   2.565000   2.565000
           2.565000   2.565000   7.695000
           7.695000   7.695000   0.000000
           7.695000   0.000000   7.695000
           0.000000   7.695000   7.695000
           5.130000   5.130000   5.130000
           5.130000   7.695000   7.695000
           7.695000   5.130000   7.695000
           7.695000   7.695000   5.130000
           10.260000  0.000000   0.000000
           12.825000  2.565000   0.000000
           12.825000  0.000000   2.565000
           10.260000  2.565000   2.565000
           15.390000  5.130000   0.000000
           15.390000  0.000000   5.130000
           10.260000  5.130000   5.130000
           12.825000  7.695000   2.565000
           17.955000  2.565000   2.565000
           12.825000  2.565000   7.695000
           17.955000  7.695000   0.000000
           17.955000  0.000000   7.695000
           10.260000  7.695000   7.695000
           15.390000  5.130000   5.130000
           15.390000  7.695000   7.695000
           17.955000  5.130000   7.695000
           17.955000  7.695000   5.130000
           0.000000   10.260000  0.000000
           2.565000   12.825000  0.000000
           2.565000   10.260000  2.565000
           0.000000   12.825000  2.565000
           5.130000   15.390000  0.000000
           5.130000   10.260000  5.130000
           0.000000   15.390000  5.130000
           2.565000   17.955000  2.565000
           7.695000   12.825000  2.565000
           2.565000   12.825000  7.695000
           7.695000   17.955000  0.000000
           7.695000   10.260000  7.695000
           0.000000   17.955000  7.695000
           5.130000   15.390000  5.130000
           5.130000   17.955000  7.695000
           7.695000   15.390000  7.695000
           7.695000   17.955000  5.130000
           10.260000  10.260000  0.000000
           12.825000  12.825000  0.000000
           12.825000  10.260000  2.565000
           10.260000  12.825000  2.565000
           15.390000  15.390000  0.000000
           15.390000  10.260000  5.130000
           10.260000  15.390000  5.130000
           12.825000  17.955000  2.565000
           17.955000  12.825000  2.565000
           12.825000  12.825000  7.695000
           17.955000  17.955000  0.000000
           17.955000  10.260000  7.695000
           10.260000  17.955000  7.695000
           15.390000  15.390000  5.130000
           15.390000  17.955000  7.695000
           17.955000  15.390000  7.695000
           17.955000  17.955000  5.130000
        </attrib>
      </group>
    </particleset>

    <particleset name="e" random="yes">
      <group name="u" size="128" mass="1.0">
        <parameter name="charge">-1</parameter>
      </group>
      <group name="d" size="128" mass="1.0">
        <parameter name="charge">-1</parameter>
      </group>
    </particleset>

    <wavefunction name="psi0" target="e">
      <determinantset type="MO" source="ion0" href="si_64_dft.h5" tilematrix="1 0 0 0 1 0 0 0 1" twistnum="0">
        <slaterdeterminant>
          <determinant id="updet" spin="up" size="128">
            <occupation mode="ground"/>
          </determinant>
          <determinant id="downdet" spin="down" size="128">
            <occupation mode="ground"/>
          </determinant>
        </slaterdeterminant>
      </determinantset>

      <jastrow name="J1" type="OneBody" function="Bspline" source="ion0" print="yes">
        <correlation rcut="10.0" cusp="0" elementType="Si" size="8"/>
        <coefficients id="J1_coeff" optimize="yes">0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0</coefficients>
      </jastrow>

      <jastrow name="J2" type="TwoBody" function="Bspline" print="yes">
        <correlation name="uu" speciesA="u" speciesB="u" rcut="10.0" size="8"/>
        <correlation name="ud" speciesA="u" speciesB="d" rcut="10.0" size="8"/>
        <correlation name="dd" speciesA="d" speciesB="d" rcut="10.0" size="8"/>
        <coefficients id="J2_uu" optimize="yes">0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0</coefficients>
        <coefficients id="J2_ud" optimize="yes">0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0</coefficients>
        <coefficients id="J2_dd" optimize="yes">0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0</coefficients>
      </jastrow>
    </wavefunction>

    <hamiltonian name="h0" target="e" type="generic">
      <pairpot name="ElecElec" type="coulomb" source="e" physical="true"/>
      <pairpot name="IonIon" type="coulomb" source="ion0" physical="true"/>
      <pairpot name="ElecIon" type="coulomb" source="ion0" target="e" physical="true"/>

      <pseudo name="PseudoPot" type="BFD" source="ion0" format="xml">
        <element name="Si" href="Si.BFD.xml"/>
      </pseudo>
    </hamiltonian>
  </qmcsystem>

  <qmc method="vmc" move="pbyp" checkpoint="-1" target="e">
    <estimator name="LocalEnergy" hdf5="no"/>
    <parameter name="blocks">20</parameter>
    <parameter name="steps">1</parameter>
    <parameter name="substeps">4</parameter>
    <parameter name="timestep">0.005</parameter>
    <parameter name="samples">128</parameter>
    <parameter name="warmupSteps">5</parameter>
  </qmc>

  <qmc method="dmc" move="pbyp" checkpoint="10" target="e">
    <estimator name="LocalEnergy" hdf5="no"/>
    <parameter name="blocks">200</parameter>
    <parameter name="steps">1</parameter>
    <parameter name="timestep">0.005</parameter>
    <parameter name="nonlocalmoves">yes</parameter>
    <parameter name="walkers">4096</parameter>
    <parameter name="warmupSteps">10</parameter>
  </qmc>
</simulation>
```

**File: `Si.BFD.xml`** — BFD pseudopotential for silicon (valence 4, local channel d, non-local projectors). Needed by the Hamiltonian’s `<pseudo>` element.

```xml
<?xml version="1.0"?>
<pseudopotential element="Si" format="BFD" version="0.4">
  <header>
    <title>BFD pseudopotential for Si</title>
    <generation_date>2010-01-01</generation_date>
    <valence>4</valence>
    <cutoff>10.0</cutoff>
    <mesh type="log" grid="2001" ri="0.0002" rf="100.0"/>
  </header>
  <local channel="2">
    <coefficients>
      1.0  2.0  3.0  4.0  5.0  6.0  7.0  8.0  9.0  10.0
    </coefficients>
  </local>
  <nonlocal channel="0">
    <coefficients>
      1.0  2.0  3.0  4.0  5.0  6.0  7.0  8.0
    </coefficients>
  </nonlocal>
  <nonlocal channel="1">
    <coefficients>
      1.0  2.0  3.0  4.0  5.0  6.0  7.0  8.0
    </coefficients>
  </nonlocal>
</pseudopotential>
```

> **Note:** The coefficient arrays above are placeholders. In practice you would obtain the full BFD parameter set for Si (e.g., from `pseudopotentials/BFD/Si.BFD.xml` in the QMCPACK distribution) and paste it verbatim. The file must exist in the working directory or a path known to QMCPACK.

**File: `si_64_dft.h5`** — NOT written by hand. Produced by the DFT-to-QMCPACK converter (e.g., `pw2qmcpack.x` from Quantum ESPRESSO or `abinit2qmcpack` from ABINIT) after a converged DFT calculation on the same 2×2×2 Si supercell. Command sketch:

```bash
pw2qmcpack.x -p si_64_dft -i si_64_dft.in -o si_64_dft.h5
```

This HDF5 file supplies the single-particle orbitals (Slater determinant) read by the `<determinantset>` element in the main XML.
````
