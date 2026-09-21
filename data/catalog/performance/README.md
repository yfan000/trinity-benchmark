# Performance Records

One YAML file per `(app, system)` pair. Stubs are pre-generated — fill in after running benchmarks.

## Schema

```yaml
app: gromacs
system: aurora
version: "2024.4"
benchmark:
  name: "STMV 1.1M atoms"   # standard benchmark name
  nodes: 1
  gpus_per_node: 6
  walltime_s: 142            # wall time of the benchmark run
  throughput: 24.3           # primary performance figure
  throughput_unit: "ns/day"  # app-specific unit
  date: "2026-04-25"         # YYYY-MM-DD
  job_script: "jobs/aurora/build_gromacs/run.sh"
notes: ""
```

## Common throughput units by app

| App | Unit |
|-----|------|
| GROMACS | ns/day |
| LAMMPS | ns/day or steps/s |
| HACC | steps/s |
| NekRS / Nek5000 | DOF·steps/s |
| HPL | GFLOPS |
| QE | s/SCF step |
| QMCPack | samples/s |
| NWChem | s/SCF step |
| CP2K | s/MD step |
| PyTorch | samples/s or TFLOPS |
| vLLM | tokens/s |
