# Verdicts — vllm@frontier, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `c03c63fc5fbf`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer’s Frontier AMD MI250X ROCm support and 271.5 tok/s at concurrency 16/TP 8 claims agree with the authoritative catalog facts. |
| `SOFT.common.correct_application` | fatal | satisfied | vLLM (ROCm) is the catalog-listed Frontier application specifically suited to ROCm LLM inference serving and matches the stated validated LLaMA throughput. |
| `SOFT.common.names_one_application` | major | satisfied | The answer names only “vLLM (ROCm)” as the selected application. |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes vLLM’s intended concurrency-oriented features and cites the quantified 271.5 tok/s validation, without promising a particular performance outcome for this run. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's Frontier MI250X and validated 271.5 tok/s assertions agree with the catalog; its PagedAttention discussion does not contradict any recorded facility fact. |
| `SOFT.common.correct_application` | fatal | satisfied | "vLLM (ROCm)" is the catalog application specifically intended and validated for LLM inference on Frontier MI250X hardware at the cited concurrency and TP=8 configuration. |
| `SOFT.common.names_one_application` | major | satisfied | The answer names one selected application: "vLLM (ROCm)". |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It describes vLLM as engineered for high-throughput inference and references the validated 271.5 tok/s result, but makes no unquantified promise about this run's performance. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | **violated** ⚠︎ flipped across runs | The answer states TP=8 runs “across the two MI250X GPUs per node,” whereas the catalog validation specifies use of 8 MI250X GCDs; Frontier’s validated TP=8 configuration is not across two MI250X GPUs. |
| `SOFT.common.correct_application` | fatal | satisfied | vLLM (ROCm) is the catalog application specifically intended for ROCm LLM inference on Frontier and is validated at the cited 271.5 tok/s, c=16, TP=8 configuration. |
| `SOFT.common.names_one_application` | major | satisfied | The answer explicitly selects exactly one application: “vLLM (ROCm).” |
| `SOFT.common.no_vague_performance_claims` | minor | **violated** ⚠︎ flipped across runs | It makes an unquantified run-performance promise by saying dynamic batching is needed to increase concurrency “while keeping latency low.” |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `SOFT.common.claims_true_to_catalog` | major | satisfied | The answer's Frontier, AMD MI250X, ROCm, LLaMA-3.1-8B, TP=8, concurrency-16, and 271.5 tok/s statements agree with the supplied workload and catalog facts. |
| `SOFT.common.correct_application` | fatal | satisfied | "vLLM (ROCm)" is the catalog application specifically intended and validated for LLM inference serving on Frontier MI250X GPUs. |
| `SOFT.common.names_one_application` | major | satisfied | The answer recommends exactly one application: "vLLM (ROCm)". |
| `SOFT.common.no_vague_performance_claims` | minor | satisfied | It cites the prior quantified validation result (271.5 tok/s at concurrency 16) and does not promise unquantified performance for this run. |
