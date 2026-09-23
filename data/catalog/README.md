# Application Catalog

Cross-facility software catalog for ALCF, NERSC, and OLCF systems.

## Contents

```text
application_catalog/
├── MATRIX.md          # app × system availability table (auto-generated)
├── systems/           # copies of systems/*.yaml (hardware, queues, endpoints)
├── software/          # copies of software/<system>/*.yaml (build paths, modules)
│   ├── aurora/
│   ├── polaris/
│   ├── crux/
│   ├── sophia/
│   ├── sirius/
│   ├── frontier/
│   ├── perlmutter/
│   ├── sunspot/
│   └── odo/
└── performance/       # benchmark results, one yaml per (app, system)
    ├── README.md      # schema definition and unit conventions
    ├── aurora/
    ├── polaris/
    └── ...
```

## Systems

| System | Facility | GPU | Nodes |
|--------|----------|-----|-------|
| Aurora | ALCF | Intel Max Series | 10,624 |
| Polaris | ALCF | A100 40GB | 560 |
| Crux | ALCF | A100 40GB | 24 |
| Sophia | ALCF | A100 40/80GB | 24 |
| Sirius | ALCF | A100-SXM4 40GB | 4 |
| Frontier | OLCF | MI250X | 9,408 |
| Perlmutter | NERSC | A100 40GB | 1,536 |
| Sunspot | ALCF | Intel Max Series | 128 (testbed) |
| Odo | ALCF | H100 | — |

## Quick reference

- **MATRIX.md** — which apps are installed on which systems
- **software/<system>/<app>.yaml** — install path, modules, run command
- **performance/<system>/<app>.yaml** — benchmark results (fill in after runs)

## Regenerating MATRIX.md

```bash
python3 /tmp/gen_catalog.py   # or recreate from the script in this README
```

To keep in sync with `software/`, re-copy yamls then re-run the generator.

---

## Benchmark Plan

Job scripts live in `jobs/<system>/bench_<app>/run.sh`. Performance results go in `performance/<system>/<app>.yaml`.

### Phase 1 — Priority 1 apps (7-system coverage), single node

| App | Benchmark input | Metric | Systems |
|-----|----------------|--------|---------|
| **GROMACS** | STMV 1.1M atoms (`stmv.tpr`) | ns/day | Aurora, Polaris, Frontier, Perlmutter |
| **LAMMPS** | LJ melt 256k atoms (`in.lj`) | ns/day | Aurora, Polaris, Frontier, Perlmutter |
| **QE** | Si bulk SCF (`si.scf.in`) | s/SCF step | Aurora, Polaris, Frontier, Perlmutter |
| **QMCPack** | NiO VMC | samples/s | Aurora, Polaris, Frontier, Perlmutter |

### Phase 2 — Priority 2 apps (5–6 system coverage), single node

| App | Benchmark input | Metric |
|-----|----------------|--------|
| **PyTorch** | ResNet-50, synthetic ImageNet, batch=256 | images/s |
| **DeepSpeed** | GPT-2 117M, ZeRO-1 | tokens/s |
| **HPL** | LINPACK, 80% node memory | GFLOPS |
| **HACC** | Built-in cosmological benchmark | steps/s |
| **NekRS** | Turbulent channel flow (`ethier`) | MDOF·s⁻¹ |
| **Nek5000** | Pipe flow (`pipe`) | MDOF·s⁻¹ |
| **CP2K** | H₂O-128 MD (`H2O-128.inp`) | s/MD step |
| **TensorFlow** | ResNet-50, synthetic | images/s |

### Phase 3 — Priority 3 apps (3–4 system coverage), single node

| App | Benchmark input | Metric |
|-----|----------------|--------|
| **NAMD** | ApoA1 92k atoms | ns/day |
| **OpenMM** | DHFR 23k atoms (`benchmark.py`) | ns/day |
| **NWChem** | H₂O trimer MP2 | s/SCF step |
| **vLLM** | Llama-3-8B, `benchmark_throughput.py` | tokens/s |
| **AlphaFold** | T1049 (CASP14 target) | s/prediction |
| **ChaiLab** | T1049 | s/prediction |
| **OpenFOAM** | Motorbike tutorial | cells/s |
| **VASP** | Si bulk DFT | s/ionic step |
| **WRF** | CONUS 12km | sim-hours/wall-hour |

### Phase 4 — Weak/strong scaling (Phase 1 apps, 1→4→16 nodes)

Repeat Phase 1 benchmarks at 1, 4, and 16 nodes to measure scaling efficiency.

### Benchmark input sources

| App | Input source |
|-----|-------------|
| GROMACS | [HECBioSim STMV benchmark](https://github.com/victorusu/GROMACS_Benchmark_Suite) |
| LAMMPS | `bench/in.lj` shipped with source; or generate inline |
| QE | Si ONCV PP from [PseudoDojo](http://www.pseudo-dojo.org); input inline |
| QMCPack | NiO benchmark from [QMCPACK repo](https://github.com/QMCPACK/qmcpack/tree/develop/tests/performance) |
| CP2K | [cp2k-input-tools H2O-128](https://github.com/cp2k/cp2k-input-tools) |
| NekRS | `ethier` shipped with NekRS examples |
| HPL | `HPL.dat` generated from node memory |
| HACC | Built-in; no external input needed |
| vLLM | `benchmark_throughput.py` shipped with vLLM |
| AlphaFold / ChaiLab | Download T1049 FASTA from CASP14 |

### Status

| Phase | Status |
|-------|--------|
| Phase 1 scripts | Pending — waiting for software directories to be finalized |
| Phase 2 scripts | Not started |
| Phase 3 scripts | Not started |
| Phase 4 scripts | Not started |
