# Verdicts — alphafold@perlmutter, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `c03c63fc5fbf`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's facility-relevant statement that AlphaFold is provided through a conda environment and supports GPU acceleration agrees with the catalog entry; it makes no contradicting installation or loading claim. |
| `SOFT.common.correct_application` | fatal | satisfied | AlphaFold is the catalog-listed DeepMind AlphaFold2 protein structure prediction application and directly fits ab initio single-chain prediction from an amino-acid sequence. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects one application: “Selected Application: AlphaFold.” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes AlphaFold as designed and optimized for GPU acceleration, but does not promise performance or completion time for this run. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The response does not make any facility-specific loading, path, dependency, or GPU claims that contradict the catalog; its capability description is consistent with AlphaFold’s catalog description. |
| `SOFT.common.correct_application` | fatal | satisfied | AlphaFold is the catalog-listed DeepMind AlphaFold2 application for protein structure prediction from sequence, matching the requested single-chain ab initio structure-prediction workload. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects exactly one application: “Selected Application: AlphaFold.” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It makes no promise about runtime or performance for this run; calling AlphaFold “specifically designed” and an “industry standard” describes suitability rather than predicted performance. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's facility claim that AlphaFold has GPU/CUDA capability is consistent with the authoritative catalog field “gpu_support: true”; no recorded catalog fact is contradicted. |
| `SOFT.common.correct_application` | fatal | satisfied | AlphaFold is installed on Perlmutter and its catalog description is “DeepMind AlphaFold2 protein structure prediction,” directly matching single-chain protein structure prediction from sequence. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly identifies one selection: “Selected application: AlphaFold (DeepMind AlphaFold2).” |
| `SOFT.common.no_vague_performance_claims` | minor | **violated** | It makes unquantified run-performance/resource promises, including “for fast inference” and “the memory and compute demand comfortably fit within a single GPU allocation.” |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's facility-related statement that AlphaFold is installed as a conda environment agrees with the catalog; it does not contradict recorded GPU support or other catalog facts. |
| `SOFT.common.correct_application` | fatal | satisfied | AlphaFold is the catalog-listed DeepMind AlphaFold2 protein structure prediction application and matches prediction of a single protein structure from an amino acid sequence. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly recommends one application: “AlphaFold.” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes AlphaFold as suited to the task but makes no promise about this run's speed, overhead, or completion time. |
