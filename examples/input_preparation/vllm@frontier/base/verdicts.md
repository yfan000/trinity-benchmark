# Verdicts — vllm@frontier, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `98dca67530dc`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The answer provides the required offline vLLM Python driver, `run_inference.py`; no additional catalog-required input files are identified. |
| `INP.common.exact_filenames_used` | major | not_applicable | vLLM offline inference accepts a user-selected Python driver filename and does not open an input file with a fixed required name. |
| `INP.common.file_identifiable` | major | satisfied | The file is recognizably a vLLM Python input driver through `from vllm import LLM, SamplingParams` and `llm.generate(prompts, sampling_params)`. |
| `INP.common.mandatory_sections_present` | major | satisfied | `run_inference.py` contains imports, a prompt list, `SamplingParams`, `LLM` construction, `llm.generate()`, and output handling required for a vLLM offline-inference driver. |
| `INP.common.no_binary_contents` | fatal | satisfied | No model weights, checkpoints, binaries, or runtime-generated artifacts are authored; the model is referenced by its existing filesystem path. |
| `INP.common.no_invented_keywords` | fatal | satisfied | `LLM` arguments `model`, `tensor_parallel_size`, and `trust_remote_code`, plus `SamplingParams` arguments `max_tokens`, `temperature`, and `top_p`, are valid vLLM API parameters. |
| `INP.common.no_output_as_input` | major | satisfied | The answer authors only `run_inference.py`; generated text is printed at runtime rather than supplied as an input file. |
| `INP.common.no_truncation` | major | satisfied | The Python file is written without ellipses, placeholder paths, TODOs, or truncated sections. |
| `INP.common.values_match_physical_system` | major | **violated** | The script comments that it has “50 distinct prompts,” but the `prompts` list contains only 48 strings, contradicting the required workload of 50 prompts. |

## gemma-4-31b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The answer provides one complete Python vLLM offline-inference driver, which is the required input type for this workload. |
| `INP.common.exact_filenames_used` | major | not_applicable | vLLM offline inference does not require an input file with a fixed application-opened filename; the Python driver filename is user-selected. |
| `INP.common.file_identifiable` | major | satisfied | The file is recognizable as a vLLM Python offline inference script through `from vllm import LLM, SamplingParams` and `llm.generate(...)`. |
| `INP.common.mandatory_sections_present` | major | satisfied | `inference.py` includes imports, a prompt list, `SamplingParams`, `LLM` construction, generation, and result handling. |
| `INP.common.no_binary_contents` | fatal | satisfied | No model weights, checkpoints, or other binary/runtime-generated files are fabricated; the existing model directory is only referenced by path. |
| `INP.common.no_invented_keywords` | fatal | satisfied | `model`, `tensor_parallel_size`, and `max_tokens` are valid vLLM `LLM`/`SamplingParams` Python API arguments. |
| `INP.common.no_output_as_input` | major | satisfied | The answer authors only `inference.py`; generated text is printed at runtime and no runtime output file is supplied as input. |
| `INP.common.no_truncation` | major | satisfied | The supplied Python file is complete and contains no ellipses, placeholder paths, TODOs, or truncation markers. |
| `INP.common.values_match_physical_system` | major | **violated** | Although the script comments that it has 50 prompts, the `prompts` list contains 51 strings, ending with both "What is the value of pi to two decimal places?" and "What is the capital of Thailand?". |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | **violated** | The required vLLM offline-inference Python driver is not provided; the answer supplies only `prompts.txt` and an unsupported `vllm_config.json`, rather than a script that imports vLLM and calls `LLM(...).generate(...)`. |
| `INP.common.exact_filenames_used` | major | not_applicable | vLLM offline inference is launched through a user-selected Python driver filename and does not require an input file with a fixed application-opened name. |
| `INP.common.file_identifiable` | major | **violated** | `vllm_config.json` is not a vLLM offline-inference input format, and `prompts.txt` alone is merely plain text with no vLLM code to read it or perform generation. |
| `INP.common.mandatory_sections_present` | major | **violated** | No supplied file contains the required offline vLLM driver structure: `from vllm import LLM, SamplingParams`, an `LLM` construction with the model and tensor parallel size, and `llm.generate(prompts, sampling_params)`. |
| `INP.common.no_binary_contents` | fatal | satisfied | No binary, checkpoint, database, or runtime-generated file contents are fabricated; the model path is referenced rather than authored. |
| `INP.common.no_invented_keywords` | fatal | **violated** | The JSON keys are presented as a vLLM configuration input, but vLLM's offline Python API has no `vllm_config.json` input language or `model_path` JSON configuration keyword; it requires Python API arguments such as `model=` and `SamplingParams(max_tokens=...)`. |
| `INP.common.no_output_as_input` | major | satisfied | The answer authors only a prompt list and purported configuration, not generated completions, logs, checkpoints, or other runtime outputs. |
| `INP.common.no_truncation` | major | satisfied | Both displayed files are written without ellipses, TODOs, placeholder paths, or truncation markers, and the prompt list contains 50 entries. |
| `INP.common.values_match_physical_system` | major | satisfied | The answer specifies the given Llama model path, `tensor_parallel_size` 4, `max_tokens` 50, and exactly 50 written prompts; temperature and top-p are permitted free choices. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | **violated** | The answer does not provide an executable Python offline-inference driver (such as the required bench.py) that imports vLLM, constructs LLM, and calls generate(). |
| `INP.common.exact_filenames_used` | major | not_applicable | vLLM offline inference does not require an input file opened under a fixed application-defined filename; the Python driver filename is user-selectable. |
| `INP.common.file_identifiable` | major | **violated** | prompts.txt plus several generic JSON configuration files is not recognisable as a runnable vLLM offline inference input; vLLM requires a Python driver/API invocation. |
| `INP.common.mandatory_sections_present` | major | **violated** | The supplied JSON files are not vLLM offline API inputs and contain no Python imports, LLM(...) construction, SamplingParams(...), or llm.generate(...) call required for the workload. |
| `INP.common.no_binary_contents` | fatal | satisfied | No binary model, checkpoint, cache, or runtime-generated binary content is fabricated; all authored contents are plain text. |
| `INP.common.no_invented_keywords` | fatal | **violated** | Files such as config.json, inference_config.json, vllm_config.json, and vllm_runtime_config.json use unsupported declarative vLLM input keys including "model_path", "inference_mode", "rocms_config", and "runtime_config" rather than the vLLM Python API. |
| `INP.common.no_output_as_input` | major | satisfied | The answer authors only purported prompt/configuration text files and does not provide contents for generated inference outputs or other runtime-produced output files. |
| `INP.common.no_truncation` | major | satisfied | None of the supplied file bodies contains ellipses, placeholder paths, TODOs, FIXMEs, or truncation markers. |
| `INP.common.values_match_physical_system` | major | **violated** | config.json declares "num_prompts": 50, but prompts.txt contains 105 prompt lines, contradicting the requested 50-prompt workload. |
