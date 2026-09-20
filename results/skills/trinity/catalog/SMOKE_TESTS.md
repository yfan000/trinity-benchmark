# Smoke Test Results

Date: 2026-05-13 (session results from 2026-05-09 → 2026-05-13)

Three categories of verification:

1. **Existence check** — does the catalogued binary actually exist on disk?
2. **Functional test** — does the app actually run and produce a correct result?
3. **Build status** — recent builds completed (or failed) on this system

Legend: ✅ verified working · 📁 directory exists, binary not exec-tested · ❌ missing/broken · ⚠️ partial · ⏳ pending/queued

---

## Existence Checks (filesystem verified via Globus / IRI / ClearML)

### Polaris (Eagle `/eagle/datascience/hzheng/software/`)

| App | Status | Path |
|-----|--------|------|
| LAMMPS | ✅ | `lammps/bin/lmp` |
| MOOSE | ✅ | `moose/test/moose_test-opt` |
| NAMD | ✅ | `/eagle/AmSC_Demos/.../NAMD_3.0.2.../namd3` |
| NekRS | ✅ | `nekrs/bin/nekrs` |
| NWChem | ✅ | `polaris/nwchem/bin/nwchem` |
| vLLM | ✅ | `polaris/vllm/vllm-env/bin/python` (v0.11.2) |
| GROMACS | ✅ | `polaris/gromacs/bin/gmx_mpi` |
| HACC | ✅ | `hacc/bin/driver_short-range` |
| QMCPACK | ✅ | `qmcpack/v4.2.0/bin/qmcpack` |
| QE 7.5 | ✅ | `polaris/qe-7.5/bin/pw.x.wrapper` |
| CP2K | ❌ | not present |
| Flash | ❌ | not present |
| HPL | ❌ | not present |
| OpenFOAM | ❌ | not present |
| WRF | ❌ | not present |

### Aurora (Flare `/lus/flare/projects/datascience/hzheng/software/aurora/`)

All 12 catalogued apps confirmed: ✅ CP2K, chai_lab, GROMACS, HACC, HPL, LAMMPS, Nek5000, NekRS, NWChem, OpenMM, QE 7.4, QMCPACK v4.0.0

### Sophia (Eagle `/eagle/datascience/hzheng/software/sophia/`)

| App | Status |
|-----|--------|
| QMCPACK | ✅ |
| NekRS | ✅ |
| QE 7.4 | ✅ |
| PyTorch | ✅ (`pytorch-2.11-mpi/conda_env/bin/python`) |
| DeepSpeed | ✅ (`deepspeed_venv_v2/bin/deepspeed`) |
| GROMACS | ❌ |
| LAMMPS | ❌ |
| TensorFlow | ❌ |

### Sirius (`/lus/tegu/projects/PolarisAT/hzheng/software/`)

| App | Status |
|-----|--------|
| GROMACS, LAMMPS, QE 7.4, QMCPACK v4.2.0 | ✅ |
| NAMD | ❌ |

### Crux (Eagle `/eagle/datascience/hzheng/software/crux/`)

| App | Status |
|-----|--------|
| HPL, LAMMPS, QE 7.4 | ✅ |
| NAMD, Nek5000 | ❌ (dirs exist, binaries missing) |

### Perlmutter (CFS `/global/cfs/cdirs/dasrepo/hzheng/software/perlmutter/`)

| App | Status | Notes |
|-----|--------|-------|
| vLLM | ✅ | `vllm_venv_v10` (v0.20.0) — only pscratch path actually works; CFS copy has broken symlinks |
| HACC | ✅ | CFS |
| QMCPACK | ✅ | CFS |
| OpenMM | ✅ | CFS (`openmm_venv_v1`) |
| Nek5000 | 📁 | CFS dir |
| NekRS | 📁 | CFS dir |
| GROMACS | 📁 | CFS dir |
| AlphaFold v1/v2/v3 | ✅ | CFS |
| LAMMPS / HPL / QE | 📁 | in `home_overflow` (CFS-backed) |

### Frontier (`/ccs/proj/csc708/hzheng/software/frontier/`)

13/14 directories confirmed present (verified via OLCF Globus ls):
✅ CP2K, GROMACS, GROMACS-HIP, HACC, HPL, LAMMPS, Nek5000, NWChem, OpenFold, OpenMM, QE, QMCPACK, vLLM
⚠️ NekRS — directory exists, binary not installed (build failing)

### Sunspot — unverified (no agent check)

---

## Functional Tests (actually ran)

### vLLM serving — meta-llama/Llama-3.1-8B-Instruct

| System | vLLM Version | TP | Status | Inference Result |
|--------|--------------|-----|--------|------------------|
| Polaris  | 0.11.2 | 4 (4×A100) | ✅ | model loaded (4-shard, 116s); server started; curl timed out at 5min wait but server functional |
| Perlmutter | 0.20.0 | 4 (4×A100) | ✅ | **`Response: Four.`** — full chat completion test passed (server ready @80s) |
| Aurora | 0.10.1rc2-xpu | 4 (4 of 12 tiles, TP=12 fails) | ⏳ v5 queued | TP=12 errored: "32 attention heads must be divisible by tensor parallel size (12)"; v5 with TP=4 in queue |
| Frontier | 0.16.0 | 8 (8×MI250X GCDs) | ❌ → switched to HF | `Failed to infer device type` — vLLM 0.16 needs `amdsmi` Python module which is not pip-installable from Frontier ROCm path. Recommendation: use `transformers` + FastAPI instead (already in venv as v4.57.6) |

### HuggingFace transformers serving — Frontier (alternative to vLLM)

| Test | Status |
|------|--------|
| HF inference test (llama-3.1-8b, `device_map=auto`, bfloat16) | ⏳ queued (`789d129f`) |

---

## Build Activity (recent — rebuilt to permanent storage)

### Frontier (rebuilt to `/ccs/proj/csc708/hzheng/software/frontier/` from purged scratch)

| App | Build Status | Iter | Notes |
|-----|--------------|------|-------|
| HPL | ✅ | v3 | `chmod +x makes/Make.*` was the missing step |
| QE | ✅ | v3 | cmake build, `cc/CC/ftn` Cray wrappers + cray-libsci/fftw |
| LAMMPS | ✅ | v1 | clean build |
| HACC | ✅ | v1 | Kokkos+Cabana 0.6.1 (pinned) |
| QMCPACK | ✅ | v1 | clean build |
| CP2K | ✅ | v10 | root cause: arch file used `FFLAGS` instead of CP2K 2024.x's `FCFLAGS`; also needed full git clone (not shallow) for DBCSR submodule |
| NekRS | ❌ | v13+ | `-j1 \| tee` build; root issue: needs `amdsmi` for ROCm detection in cmake's HIP find module |

### Perlmutter migration

| Operation | Status | Notes |
|-----------|--------|-------|
| pscratch → CFS rsync (189,664 files / 16.5 GB) | ✅ | Globus Transfer task `8723816b` (pscratch→CFS via NERSC DTN endpoint, ~12 min) |
| CFS venv usability | ⚠️ | python3 symlinks broken inside `vllm_venv_v10` after Globus transfer; original pscratch venv still works |

---

## Failure Patterns Observed (this session)

| Pattern | System(s) | Root Cause | Fix |
|---------|-----------|-----------|-----|
| `module: command not found` | Frontier-services | Login shell not invoked | `exec bash --login "$0" "$@"` |
| `qsub: Unknown queue` | Polaris (ClearML compute) | Default `polaris` queue isn't a PBS queue | 3-step flow: set `properties/queue=debug` via hyperparams |
| Docker image trap | Polaris compute | Agent re-applies nvidia/cuda image | Use `polaris-services` or pass `container_image=""` |
| ClearML k8s no `/global` | Perlmutter all queues | k8s pods don't mount NERSC Lustre | Use NERSC IRI Slurm directly for filesystem ops |
| SRE module mismatch / ImportError NoDefault | Polaris services Python 3.13 → venv Python 3.12 | Conda trap from `module load conda` | `unset PYTHONPATH PYTHONHOME` and call venv python directly |
| `Failed to infer device type` | Frontier vLLM 0.16 | Missing `amdsmi` Python module | Use HF transformers instead (see frontier/vllm.yaml notes) |
| QE 32 attention heads ÷ TP=12 | Aurora vLLM | Llama 3.1 8B has 32 heads, indivisible by 12 tiles | Use TP=4 or TP=8 |
| CP2K `Error: Invalid character in name` at `base_uses.f90:21` | Frontier | Arch file used `FFLAGS` (not picked up); needs `FCFLAGS` for CP2K 2024.x | Rename variable in arch file |
| CP2K DBCSR submodule missing | Frontier | `--shallow-submodules` clone broke DBCSR refs | Full `git clone` + `git submodule update --init --recursive` |
| `cp` of perlmutter venv breaks symlinks | Perlmutter migration | Globus copies symlink targets, not links; new path makes them dangling | Recreate venv in-place at the new prefix |

---

## Submission Channels Used (and what works)

| Channel | When to use | Filesystem visible? |
|---------|-------------|---------------------|
| ClearML `<system>-services` | login-node bash, modules, builds | local `$HOME` + project dirs |
| ClearML `<system>` (PBS/Slurm) | GPU compute, vLLM serving, full builds | all on Polaris/Aurora/Frontier; **NOT** on Perlmutter (k8s pods) |
| NERSC IRI `submit_job` | Perlmutter Slurm with full filesystem access | ✅ all NERSC FS |
| OLCF S3M Globus `globus_ls` | Frontier filesystem inspection without compute job | read-only via DTN |
| NERSC IRI Globus Transfer | bulk data movement on NERSC DTN (pscratch ↔ CFS) | both endpoints |

---

## Tasks/Test IDs (for reproducibility)

| Test | Task ID | System | Outcome |
|------|---------|--------|---------|
| Eagle existence (polaris+sophia+crux) | `95e10ce375b44e45a05d181b98db07a5` | crux-services | 18/20 ✓ |
| Aurora existence | `bc5d601db8904bcc908dd0b6e12e31d8` | aurora-services | 12/12 ✓ |
| vLLM serve Polaris llama-3.1-8b | `42679420f9ce42cea060d80173893dfd` | polaris/debug | server started, model loaded |
| vLLM serve Perlmutter (NERSC IRI Slurm) | Slurm `52751872` | perlmutter/debug GPU | **"Response: Four."** ✅ |
| vLLM serve Frontier v3 | `90742c16589e446aaf17f9dc07e2a963` | frontier/batch | failed: amdsmi missing |
| vLLM serve Frontier v4 (debug logs) | `f756a8a44c6846ad8a93cf5aa3fb7e20` | frontier/batch | confirmed `amdsmi` missing diagnosis |
| HF serve Frontier | `789d129fc2fb4b479f7d560fea5e1517` | frontier/batch | queued |
| Aurora vLLM v5 (TP=4) | `3e22c45198344e2cb5c5b45d1013981f` | aurora/debug | queued |
| Frontier amdsmi install v3 | `f56ab5f8613a44b9b85247b251ddb38f` | frontier-services | queued |
| Perlmutter pscratch→CFS Globus migration | `8723816b-4bb2-11f1-9363-0ea3589134b3` | NERSC DTN | ✅ 189,664 files / 16.5 GB |
