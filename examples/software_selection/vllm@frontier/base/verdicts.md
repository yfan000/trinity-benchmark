# Verdicts — vllm@frontier, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `c03c63fc5fbf`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's Frontier/AMD MI250X ROCm support and 271.5 tok/s at c=16 with TP=8 statements agree with the authoritative catalog entry. |
| `SOFT.common.correct_application` | fatal | satisfied | "vLLM (ROCm)" is the catalog application explicitly intended and validated for LLM inference on Frontier AMD MI250X hardware. |
| `SOFT.common.names_one_application` | major | satisfied | The answer names exactly one selected application: "vLLM (ROCm)". |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It cites the quantified validated result of "271.5 tok/s" and describes vLLM's intended inference features without promising a specific outcome for this run. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's Frontier AMD MI250X validation and 271.5 tok/s baseline claims agree with the catalog; it makes no contradictory facility-specific loading, path, or dependency claim. |
| `SOFT.common.correct_application` | fatal | satisfied | vLLM (ROCm) is the catalog application explicitly suited to ROCm LLM inference on Frontier and validated at the cited concurrency-16, TP=8 throughput. |
| `SOFT.common.names_one_application` | major | satisfied | The answer names exactly one selection: “vLLM (ROCm).” |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes vLLM as designed for high-throughput serving and references an existing measured baseline, without promising a specific performance outcome for this run. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | **violated** | The answer says vLLM is “accessible in the default module system” via “module load vllm/rocm,” but the authoritative catalog states “Build from source required.” |
| `SOFT.common.correct_application` | fatal | satisfied | vLLM (ROCm) is the catalog application specifically intended for ROCm LLM inference on Frontier MI250X GPUs and matches the cited validated workload. |
| `SOFT.common.names_one_application` | major | satisfied | The answer identifies only “vLLM (ROCm)” as the selected application. |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied ⚠︎ flipped across runs | It cites the quantified validated result of 271.5 tok/s at concurrency 16 rather than making an unquantified prediction about the performance of this run. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The stated Frontier AMD MI250X ROCm support and 271.5 tok/s validation at c=16, TP=8 agree with the authoritative catalog facts. |
| `SOFT.common.correct_application` | fatal | satisfied | vLLM (ROCm) is the catalog application for ROCm LLM inference on Frontier MI250X and directly fits increased-concurrency LLaMA serving. |
| `SOFT.common.names_one_application` | major | satisfied | The answer selects exactly one application: "vLLM (ROCm)". |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It cites the quantified validated result of 271.5 tok/s at concurrency 16 rather than making an unquantified promise about this run's performance. |
