# Verdicts — alphafold@perlmutter, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `c03c63fc5fbf`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's facility-related claim that AlphaFold is available as a conda environment and supports GPU use is consistent with the catalog description and gpu_support: true; no catalog fact is contradicted. |
| `SOFT.common.correct_application` | fatal | satisfied | AlphaFold is the catalog-listed DeepMind AlphaFold2 protein-structure prediction application and directly fits ab initio monomer prediction from an amino-acid sequence. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects exactly one application: “Selected Application: AlphaFold”. |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It makes no promise about this run's runtime, overhead, or likelihood of completing within a walltime; “Proven accuracy” describes the method generally rather than run performance. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's facility-related statement that AlphaFold is provided via a dedicated conda environment agrees with the catalog description and does not contradict any recorded fact. |
| `SOFT.common.correct_application` | fatal | satisfied | AlphaFold is the installed application described in the catalog as "DeepMind AlphaFold2 protein structure prediction," matching ab initio single-chain structure prediction from sequence. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects one application: "Application: AlphaFold". |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It makes no promise about runtime, overhead, or likely performance of this specific run. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer’s facility-relevant claim that AlphaFold is provided in a conda environment with GPU support agrees with the catalog entry; no recorded catalog fact is contradicted. |
| `SOFT.common.correct_application` | fatal | satisfied | AlphaFold is the installed DeepMind AlphaFold2 application and is directly suited to predicting a protein’s 3D structure from an amino-acid sequence. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly identifies only “AlphaFold” as the selected application; chai-lab is mentioned only as a comparison. |
| `SOFT.common.no_vague_performance_claims` | minor | **violated** | It makes the unquantified run-performance claim that Perlmutter GPU nodes are “delivering high throughput for single-run predictions.” |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's facility claims that AlphaFold is installed as a conda environment and supports GPU acceleration agree with the catalog description and gpu_support: true. |
| `SOFT.common.correct_application` | fatal | satisfied | AlphaFold is the catalog-listed DeepMind AlphaFold2 protein structure prediction application and directly fits ab initio prediction from an amino acid sequence. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly recommends only "the AlphaFold application" as the selected application. |
| `SOFT.common.no_vague_performance_claims` | minor | **violated** ⚠︎ flipped across runs | It makes an unquantified run-performance prediction: GPU acceleration "should provide a significant speedup for this type of computation." |
