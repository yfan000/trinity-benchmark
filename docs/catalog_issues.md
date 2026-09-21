# application_catalog — issues found while wiring it into the Trinity benchmark

Against `github.com/zhenghh04/application_catalog` at HEAD `2026-05-13T18:56:08Z`
(268 YAML files: 144 software, 10 systems, 114 performance).

We built a normalized reader for the catalog so the Trinity agent benchmark could use more than
a thin slice of it. Everything below turned up in that process. The first two are one-character
fixes; the rest are consistency issues that make the catalog harder to consume programmatically.

Happy to send any of this as a PR — the two syntax fixes are ready to go.

---

## 1. Two files do not parse (one-line fixes)

Both break `yaml.safe_load`. Anything reading them gets an exception, and a consumer that
catches it broadly — as ours did — silently sees an empty entry. **`polaris/qe.yaml` is one of
the richest entries in the catalog** (the LD_LIBRARY_PATH workaround, the `module purge`
warning, the verified-failure job IDs) and it was contributing nothing to our pipeline for
months without anyone noticing. It also rendered as `qe — ` with an empty description in the
software listing we show to models.

**`software/polaris/qe.yaml` line 7** — unterminated double-quoted scalar. The opening quote
runs on until the `"nvhpc"` quote inside the line-9 comment.

```diff
-install_path: "/soft/applications/quantum_espresso/7.5-nvhpc24.11-libxc700
+install_path: "/soft/applications/quantum_espresso/7.5-nvhpc24.11-libxc700"
```

**`software/sunspot/qe.yaml` line 20** — unquoted value containing `: `.

```diff
-  mpi: mpich (loaded via: module load frameworks; module load mpich)
+  mpi: "mpich (loaded via: module load frameworks; module load mpich)"
```

## 2. `frontier/gromacs.yaml` is a two-document stream

It uses a `---` separator, so `safe_load` raises `ComposerError` and only `safe_load_all`
reads it. The second document is an entire GPU build carrying `gpu_run_command` and
`gpu_performance: "213.5 ns/day (1 GCD, 7k TIP3P atoms); 2.3x over CPU-only"` — invisible to
any single-document reader. Worth either splitting into `gromacs_hip.yaml` (the convention
already used elsewhere) or flagging in the README.

## 3. Contradictory memory figure for Crux

- `systems/crux.yaml` → `hardware.memory_per_node_gb: 256`
- `software/crux/hpl.yaml` → `scaling_notes: "... Tune N, NB, P, Q parameters in HPL.dat for
  Crux node memory (512 GB/node)."`

This one bites: HPL sizes `N ~ sqrt(total_memory * 0.8 / 8)`, so the memory figure *is* the
answer. We currently prefer the system file and drop the conflicting sentence. Which is right?

`README.md` also lists Perlmutter at 1,536 nodes while `systems/perlmutter.yaml` says 3,072.
(Aurora 10,624 and Frontier 9,408 agree between the two.)

## 4. `input_detection.content_markers` reads as required, but is a detection heuristic

This is the one that cost us the most, so it may be worth a note in the README even if the data
never changes. The field name and content invite reading it as "what a valid input must
contain". We did exactly that, and it became the largest single source of failures in our
Input-preparation benchmark — wrong in nearly every instance:

| entry | marker demanded | why a correct file fails |
|---|---|---|
| `perlmutter/alphafold` | `ACDEFGHIKLMNPQRSTVWY` | the amino-acid *alphabet*; a real FASTA holds a sequence |
| `polaris/nwchem` | `echo`, `memory stack` | both optional directives |
| `polaris/lammps` | `dump` | optional output |
| `sirius/gromacs` | `vdwtype` | grompp defaults it |
| `polaris/nekrs` | `[MESH]`, `[VELOCITY]`, `[PRESSURE]` | optional sections; only `[GENERAL]` is required |

As an **any-of** classifier ("does this look like an NWChem deck?") the lists are good. A
sentence in the README saying so would prevent the next consumer repeating our mistake.
Separating `required_sections` from `detection_markers` would be better still.

## 5. `required_inputs` / `input_files` / `optional_inputs` overlap inconsistently

The convention appears to be `input_files == required ∪ optional` — `polaris/gromacs` has
`input_files [.tpr .gro .mdp .top]`, `required [.tpr]`, `optional [.gro .mdp .top …]`, which
reads cleanly. But:

- **97 entries** carry `required_inputs`, **96** carry `input_files`, and the two sets are not
  the same files, so a consumer must try both.
- **3 entries list identical `input_files` and `optional_inputs`**, which under the convention
  means nothing is required: `aurora/openmm`, `perlmutter/vllm`, `polaris/vllm`.
- Values mix four kinds of thing with no marker distinguishing them: bare extensions (`.nw`),
  literal filenames (`HPL.dat`, `input.xml`), globs (`*.lammps`, `data.*`) and directories
  (`pseudo/`).
- `required_inputs` does not distinguish **all of** from **any of**. LAMMPS accepts `.lammps`,
  `.in` or `.lmp` for the same file; QE lists `.scf.in`, `.relax.in`, `.bands.in`, `.pw.in`,
  which are alternatives, not four files to write. We hard-code the app list that means "any of".
- `perlmutter/alphafold` lists `run_alphafold.py` under `input_detection.filenames` — that is
  the driver script, not an input, and a consumer treating it as one will ask for it to be
  authored.

**42 entries record no input information at all** (mostly the `frontier/` and `sunspot/`
build-record entries).

## 6. Two schema families, undocumented

~129 entries use the runtime schema (`name`/`description`/`input_detection`/`defaults`/…).
15 use a build-record schema (`app`/`system`/`status`/`install_prefix`/`built_date`/`compilers`)
with none of the input fields — all of `frontier/` except `vllm`, plus `sunspot/qe`. A consumer
assuming one shape gets nothing from the other. There is no template for
`software/<system>/<app>.yaml` (unlike `systems/_template.yaml`), which is probably why 109
distinct top-level keys have accumulated.

## 7. Smaller items

- **`defaults.ppn` missing on 33 entries that otherwise have a `defaults` block** — it is the
  field that says how many ranks the build expects per node.
- **Comments leaked into quoted scalars** in `aurora/vllm.yaml`, so the value itself carries
  the commentary:
  `queue: "debug-scaling   # or 'prod' for long-running"`, `account: "datascience   # or 'Aurora_deployment'"`.
- **`sophia/qmcpack.yaml`** has `defaults.queue: sophia`, which is not one of Sophia's queues
  (`by-gpu`, `by-node`, `bigmem`, `single-gpu`, `single-node`).
- **Scheduler dialect varies by key rather than by value**: `queue` (PBS), `qos`
  (perlmutter/qmcpack), `partition` (frontier, odo). Consumers must know all three.
- **Hardware keys vary**: `memory_per_node_gb: 512` on most systems vs
  `memory_per_node: "503GiB"` on Sophia; `cpu_type` vs `cpu`. Likewise `install_path` vs
  `install_prefix`.
- **`SMOKE_TESTS.md` contradicts `build_status`** in several places — it records CP2K, HPL,
  OpenFOAM, WRF and Flash as not present on Polaris while their YAML says `build_status: built`.
  The smoke tests look like the more reliable source; if so, `build_status` may be stale.
- **`performance/` is 96% stubs** — 5 of 114 records populated, all on Polaris. Not a bug, but
  worth knowing before building on it. `performance/README.md`'s per-app throughput-unit table
  is genuinely useful and easy to miss.

---

### What we did on our side

Nothing in the vendored copy was edited. The two syntax fixes live in an overlay
(`skills/catalog_repairs/`) keyed by SHA of the upstream file, so a re-pull is a clean rsync and
the repair is refused rather than silently applied if the bytes change. `skills/catalog.py
--repairs` prints the diffs above; `--fill` prints the coverage and quirk counts.
