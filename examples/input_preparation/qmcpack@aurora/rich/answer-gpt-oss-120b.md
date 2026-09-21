# gpt-oss-120b — qmcpack@aurora, rich arm

Input preparation. **FAIL** (correctness 0/2, completeness 0/2, usability 0/2, fatal; 5 of 9 requirements violated).

````
**File:** `si_bulk_2x2x2_dmc.in.xml`  

```xml
<?xml version="1.0"?>
<simulation>
  <!-- --------------------------------------------------- -->
  <!-- Project identification -->
  <!-- --------------------------------------------------- -->
  <project id="Si_bulk_2x2x2_DMC" series="0"/>

  <!-- --------------------------------------------------- -->
  <!-- Physical system definition -->
  <!-- --------------------------------------------------- -->
  <qmcsystem>
    <!-- Lattice of a 2×2×2 conventional Si cell (a = 5.43 Å → 10.263 Bohr) -->
    <simulationcell>
      <parameter name="lattice" units="bohr">
        20.52600000   0.00000000   0.00000000
        0.00000000   20.52600000   0.00000000
        0.00000000   0.00000000   20.52600000
      </parameter>
      <parameter name="bconds">p p p</parameter>
      <!-- Long‑range cutoff – default is fine for this size -->
      <parameter name="LR_dim_cutoff">15</parameter>
    </simulationcell>

    <!-- --------------------------------------------------- -->
    <!-- Electron particle set -->
    <!-- --------------------------------------------------- -->
    <particleset name="e" random="yes">
      <!-- 128 up‑spin electrons -->
      <group name="u" size="128" mass="1.0">
        <parameter name="charge">-1</parameter>
        <parameter name="mass">1.0</parameter>
      </group>
      <!-- 128 down‑spin electrons -->
      <group name="d" size="128" mass="1.0">
        <parameter name="charge">-1</parameter>
        <parameter name="mass">1.0</parameter>
      </group>
    </particleset>

    <!-- --------------------------------------------------- -->
    <!-- Ion (Si) particle set – 64 atoms -->
    <!-- --------------------------------------------------- -->
    <particleset name="ion0">
      <group name="Si" size="64" mass="28.0855">
````
