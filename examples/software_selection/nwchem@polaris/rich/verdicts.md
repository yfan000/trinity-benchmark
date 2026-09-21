# Verdicts — nwchem@polaris, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `c03c63fc5fbf`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The response makes no contradictory facility-specific claim; its statement that NWChem is a computational-chemistry code and is MPI-capable is consistent with the catalog’s NWChem entry and 4-MPI-rank benchmark. |
| `SOFT.common.correct_application` | fatal | satisfied | NWChem is the catalog application benchmarked for the exact “H2O B3LYP/6-31G* single-point energy, 4 MPI ranks” workload. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects exactly one application: “Selected application: NWChem”. |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes NWChem’s MPI model as matching the stated 4-rank workload but makes no unquantified promise about this run’s performance. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The response makes no contradictory facility-specific claims; its statement that NWChem supports MPI is consistent with the catalog benchmark using 4 MPI ranks. |
| `SOFT.common.correct_application` | fatal | satisfied | NWChem is the catalog-listed application benchmarked specifically for "H2O B3LYP/6-31G* single-point energy, 4 MPI ranks". |
| `SOFT.common.names_one_application` | major | satisfied | The answer identifies exactly one selection: "Selected Application: NWChem". |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes NWChem as designed for molecular Gaussian-orbital calculations and notes MPI support, without promising a particular runtime or performance for this run. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer does not contradict recorded facility facts; its CPU-only characterization of CP2K is consistent with the installed-software description, and no CP2K catalog field supplied conflicts with its other facility claims. |
| `SOFT.common.correct_application` | fatal | **violated** | The authoritative catalog identifies NWChem as having the exact measured benchmark “H2O B3LYP/6-31G* single-point energy, 4 MPI ranks” on Polaris, whereas the answer selects CP2K. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects one application: “Selected application: CP2K (CPU build).” |
| `SOFT.common.no_vague_performance_claims` | minor | **violated** | It makes an unquantified performance promise for this run: “For a single-water molecule the overhead is negligible.” |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer makes no claims contradicting cataloged facility facts; its DFT and MPI statements are consistent with NWChem’s catalog description. |
| `SOFT.common.correct_application` | fatal | satisfied | NWChem is the cataloged application with the exact measured benchmark for “H2O B3LYP/6-31G* single-point energy, 4 MPI ranks.” |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly recommends only “NWChem” as the selected application. |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes NWChem’s MPI capability but makes no unquantified promise about this run’s completion time or performance. |
