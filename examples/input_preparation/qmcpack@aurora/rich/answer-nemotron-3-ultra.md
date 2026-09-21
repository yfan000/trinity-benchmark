# nemotron-3-ultra — qmcpack@aurora, rich arm

Input preparation. **FAIL** (correctness 0/2, completeness 2/2, usability 0/2, fatal; 1 of 9 requirements violated).

````
**File: `si_2x2x2_dmc.in.xml`**  
This is the main QMCPACK input file defining the 64-atom silicon supercell, the Slater–Jastrow trial wavefunction (orbitals read from a prior DFT run), the Hamiltonian with BFD pseudopotentials, and the DMC run parameters (4096 walkers, τ = 0.005 Ha⁻¹, 200 blocks).

```xml
<?xml version="1.0"?>
<simulation>
  <project id="si_2x2x2_dmc" series="0">
    <application name="qmcapp" role="molecu" class="serial" version="1.0"/>
    <parameter name="driver_version">legacy</parameter>
  </project>

  <qmcsystem>
    <simulationcell>
      <parameter name="lattice" units="bohr">
        20.526  0.000  0.000
        0.000  20.526  0.000
        0.000  0.000  20.526
      </parameter>
      <parameter name="bconds">p p p</parameter>
      <parameter name="LR_dim_cutoff">15</parameter>
    </simulationcell>

    <particleset name="ion0" random="no">
      <group name="Si" size="64" mass="51200.5">
        <parameter name="charge">4</parameter>
        <parameter name="valence">4</parameter>
        <parameter name="atomicnumber">14</parameter>
        <parameter name="mass">51200.5</parameter>
        <attrib name="position" datatype="posArray" condition="0">
          0.00000000  0.00000000  0.00000000
          0.00000000  5.13150000  5.13150000
          5.13150000  0.00000000  5.13150000
          5.13150000  5.13150000  0.00000000
          2.56575000  2.56575000  2.56575000
          2.56575000  7.69725000  7.69725000
          7.69725000  2.56575000  7.69725000
          7.69725000  7.69725000  2.56575000
          10.26300000  0.00000000  0.00000000
          10.26300000  5.13150000  5.13150000
          15.39450000  0.00000000  5.13150000
          15.39450000  5.13150000  0.00000000
          12.82875000  2.56575000  2.56575000
          12.82875000  7.69725000  7.69725000
          17.96025000  2.56575000  7.69725000
          17.96025000  7.69725000  2.56575000
          0.00000000  10.26300000  0.00000000
          0.00000000  15.39450000  5.13150000
          5.13150000  10.26300000  5.13150000
          5.13150000  15.39450000  0.00000000
          2.56575000  12.82875000  2.56575000
          2.56575000  17.96025000  7.69725000
          7.69725000  12.82875000  7.69725000
          7.69725000  17.96025000  2.56575000
          10.26300000  10.26300000  0.00000000
          10.26300000  15.39450000  5.13150000
          15.39450000  10.26300000  5.13150000
          15.39450000  15.39450000  0.00000000
          12.82875000  12.82875000  2.56575000
          12.82875000  17.96025000  7.69725000
          17.96025000  12.82875000  7.69725000
          17.96025000  17.96025000  2.56575000
          0.00000000  0.00000000  10.26300000
          0.00000000  5.13150000  15.39450000
          5.13150000  0.00000000  15.39450000
          5.13150000  5.13150000  10.26300000
          2.56575000  2.56575000  12.82875000
          2.56575000  7.69725000  17.96025000
          7.69725000  2.56575000  17.96025000
          7.69725000  7.69725000  12.82875000
          10.26300000  0.00000000  10.26300000
          10.26300000  5.13150000  15.39450000
          15.39450000  0.00000000  15.39450000
          15.39450000  5.13150000  10.26300000
          12.82875000  2.56575000  12.82875000
          12.82875000  7.69725000  17.96025000
          17.96025000  2.56575000  17.96025000
          17.96025000  7.69725000  12.82875000
          0.00000000  10.26300000  10.26300000
          0.00000000  15.39450000  15.39450000
          5.13150000  10.26300000  15.39450000
          5.13150000  15.39450000  10.26300000
          2.56575000  12.82875000  12.82875000
          2.56575000  17.96025000  17.96025000
          7.69725000  12.82875000  17.96025000
          7.69725000  17.96025000  12.82875000
          10.26300000  10.26300000  10.26300000
          10.26300000  15.39450000  15.39450000
          15.39450000  10.26300000  15.39450000
          15.39450000  15.39450000  10.26300000
          12.82875000  12.82875000  12.82875000
          12.82875000  17.96025000  17.96025000
          17.96025000  12.82875000  17.96025000
          17.96025000  17.96025000  12.82875000
        </attrib>
      </group>
    </particleset>

    <particleset name="e" random="yes">
      <group name="u" size="128" mass="1.0">
        <parameter name="charge">-1</parameter>
        <parameter name="mass">1.0</parameter>
      </group>
      <group name="d" size="128" mass="1.0">
        <parameter name="charge">-1</parameter>
        <parameter name="mass">1.0</parameter>
      </group>
    </particleset>
  </qmcsystem>

  <wavefunction name="psi0" target="e">
    <determinantset type="molecular" source="ion0" href="si_dft_wfn.h5" tilematrix="1 0 0 0 1 0 0 0 1" twistnum="0" spin="no">
      <slaterdet name="SlaterDet" einspline="yes">
        <determinant id="updet" size="128"/>
        <determinant id="downdet" size="128"/>
      </slaterdet>
    </determinantset>

    <jastrow name="Jastrow_ee" type="Two-Body" function="bspline" source="ion0" print="yes">
      <correlation speciesA="u" speciesB="u" size="8" rcut="10.263"/>
      <correlation speciesA="u" speciesB="d" size="8" rcut="10.263"/>
      <correlation speciesA="d" speciesB="d" size="8" rcut="10.263"/>
    </jastrow>

    <jastrow name="Jastrow_eei" type="Three-Body" function="polynomial" source="ion0" print="yes">
      <correlation speciesA="u" speciesB="u" speciesC="Si" size="4 4" rcut="10.263"/>
      <correlation speciesA="u" speciesB="d" speciesC="Si" size="4 4" rcut="10.263"/>
      <correlation speciesA="d" speciesB="d" speciesC="Si" size="4 4" rcut="10.263"/>
    </jastrow>
  </wavefunction>

  <hamiltonian name="h0" type="generic" target="e">
    <pairpot name="ElecElec" type="coulomb" source="e" physical="true"/>
    <pairpot name="IonIon" type="coulomb" source="ion0" physical="true"/>
    <pairpot name="ElecIon" type="pseudopotential" source="ion0" wavefunction="psi0" format="xml">
      <pseudo elementType="Si" href="Si.BFD.xml"/>
    </pairpot>
  </hamiltonian>

  <qmc method="dmc" move="pbyp" checkpoint="-1" gpu="yes">
    <parameter name="targetWalkers">4096</parameter>
    <parameter name="timestep">0.005</parameter>
    <parameter name="blocks">200</parameter>
    <parameter name="nonlocalmoves">yes</parameter>
    <parameter name="nsteps">1</parameter>
    <estimator name="LocalEnergy" hdf5="no"/>
    <estimator name="OneBodyDensity" hdf5="no"/>
  </qmc>
</simulation>
```

---

**Required auxiliary file (not written by hand):**  
`si_dft_wfn.h5` — Slater determinant orbitals from the prior DFT calculation, converted to QMCPACK’s spline format.  
Typical generation command (Quantum ESPRESSO → QMCPACK):  
```bash
pw2qmcpack.x -in si_dft_pw2qmc.in
```  
where `si_dft_pw2qmc.in` specifies the DFT output prefix, the 2×2×2 supercell, and the `si_dft_wfn.h5` output name.

**Required pseudopotential file (standard, not written here):**  
`Si.BFD.xml` — BFD pseudopotential for silicon (valence 4, local channel s, non-local projectors). Place it in the working directory or in the pseudopotential search path.
````
