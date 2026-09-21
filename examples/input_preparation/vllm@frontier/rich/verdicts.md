# Verdicts — vllm@frontier, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `98dca67530dc`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied | The answer provides a complete Python vLLM offline-inference driver, `offline_inference.py`, which is the required authored input for this workload. |
| `INP.common.exact_filenames_used` | major | not_applicable | vLLM offline inference does not require an application input file with an exact fixed filename; the Python driver filename is user-selected. |
| `INP.common.file_identifiable` | major | satisfied | `offline_inference.py` is recognizably a vLLM offline inference script through `from vllm import LLM, SamplingParams`, `LLM(...)`, and `llm.generate(...)`. |
| `INP.common.mandatory_sections_present` | major | satisfied | The Python driver contains the required executable structure: imports, a prompt list, `SamplingParams`, `LLM` construction, and `llm.generate()` invocation; the JSON file is syntactically complete JSON. |
| `INP.common.no_binary_contents` | fatal | satisfied | No binary, checkpoint, model-weight, or other runtime-generated file contents are authored; the model path is only referenced for runtime loading. |
| `INP.common.no_invented_keywords` | fatal | satisfied | The vLLM API arguments used—`model`, `tensor_parallel_size`, `dtype`, `trust_remote_code`, `gpu_memory_utilization`, `temperature`, `top_p`, and `max_tokens`—are valid vLLM Python API parameters. |
| `INP.common.no_output_as_input` | major | satisfied | The answer does not provide contents for `inference_results.json`; it only includes Python code that creates that output at runtime. |
| `INP.common.no_truncation` | major | satisfied | Both displayed files are written without ellipses, placeholder paths, TODOs, or truncation markers. |
| `INP.common.values_match_physical_system` | major | satisfied ⚠︎ flipped across runs | The script uses the specified model path, declares exactly 50 prompt entries, sets `max_tokens=50`, and sets `tensor_parallel_size=4` as required. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | not_applicable ⚠︎ flipped across runs | The supplied catalog facts record no required input-file list for vLLM (ROCm) on Frontier; the answer nevertheless provides the needed Python offline-inference driver. |
| `INP.common.exact_filenames_used` | major | not_applicable | vLLM offline inference does not require an input file opened under a fixed filename; the Python driver filename is user-selectable. |
| `INP.common.file_identifiable` | major | satisfied | The file is recognisably a vLLM offline-inference Python driver through `from vllm import LLM, SamplingParams`, `LLM(...)`, and `llm.generate(...)`. |
| `INP.common.mandatory_sections_present` | major | satisfied | `inference.py` completely defines imports, a 50-entry `prompts` list, `SamplingParams`, an `LLM` instance, generation, and output handling required by the vLLM Python API. |
| `INP.common.no_binary_contents` | fatal | satisfied | No binary, checkpoint, model-weight, or runtime-generated file is authored; the existing model directory is only referenced in `model=`. |
| `INP.common.no_invented_keywords` | fatal | satisfied | `SamplingParams(max_tokens=50)`, `LLM(model=..., tensor_parallel_size=4)`, and `llm.generate(prompts, sampling_params)` are valid vLLM Python API usage. |
| `INP.common.no_output_as_input` | major | satisfied | The answer authors only `inference.py`; generated results are printed at runtime and no output file contents are supplied as input. |
| `INP.common.no_truncation` | major | satisfied | The complete Python script is provided with no ellipses, placeholder paths, TODOs, or truncation markers. |
| `INP.common.values_match_physical_system` | major | satisfied | The script uses the specified model path, `tensor_parallel_size=4`, `max_tokens=50`, and contains exactly 50 prompt strings. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | not_applicable ⚠︎ flipped across runs | The catalog facts supplied do not list any required input filenames or required_inputs field for vLLM on Frontier. |
| `INP.common.exact_filenames_used` | major | not_applicable | vLLM offline inference uses a user-authored Python driver and does not require inputs under an application-fixed filename. |
| `INP.common.file_identifiable` | major | satisfied | `run_vllm_offline.py` is recognisably a vLLM offline-inference driver through `from vllm import LLM, SamplingParams`, `LLM(...)`, and `llm.generate(prompts, sampling_params)`. |
| `INP.common.mandatory_sections_present` | major | satisfied | The supplied Python driver has imports, configuration loading, prompt loading, LLM construction, generation, and output handling; the JSON and text files are syntactically complete for the driver. |
| `INP.common.no_binary_contents` | fatal | satisfied | The model location is referenced as `/lustre/orion/csc708/scratch/hzheng/models/llama-3.1-8b`, but no model weights, checkpoints, or other binary/runtime-generated contents are fabricated. |
| `INP.common.no_invented_keywords` | fatal | satisfied | The vLLM driver uses established offline API objects and arguments including `LLM`, `SamplingParams`, `model`, `tensor_parallel_size`, `device`, `max_tokens`, `temperature`, and `top_p`; the JSON keys are consumed by the authored driver rather than claimed as native vLLM deck directives. |
| `INP.common.no_output_as_input` | major | satisfied | `outputs.json` is only opened for writing in the driver (`RESULT_FILE.open("w")`) and no contents for that runtime output are authored in the answer. |
| `INP.common.no_truncation` | major | satisfied | All three supplied files are written in full, with no placeholder paths, TODOs, truncation markers, or ellipses standing in for omitted content. |
| `INP.common.values_match_physical_system` | major | satisfied | The driver references the specified model path, sets `tensor_parallel_size=4`, asserts exactly 50 prompt entries, and sets `max_tokens=50`. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | **violated** ⚠︎ flipped across runs | No vLLM offline-inference Python driver is provided; the answer supplies unattached text/JSON files but no file that imports vLLM, constructs `LLM`, and calls `generate()`. |
| `INP.common.exact_filenames_used` | major | not_applicable | vLLM offline inference does not require an input file with a fixed application-opened filename; the Python driver filename is user-chosen. |
| `INP.common.file_identifiable` | major | **violated** | `sampling_params.json`, `llm_config.json`, `run_config.json`, and `input.json` are not recognized vLLM offline-inference input formats, and no vLLM Python driver is present. |
| `INP.common.mandatory_sections_present` | major | **violated** | The purported input set lacks the required executable offline-inference structure (Python imports, `SamplingParams`, `LLM(...)`, and `llm.generate(...)`) needed for vLLM to consume the prompts and settings. |
| `INP.common.no_binary_contents` | fatal | satisfied | The answer does not fabricate contents for `model.bin` or any other binary/runtime-generated file. |
| `INP.common.no_invented_keywords` | fatal | **violated** | The answer invents a JSON configuration interface for vLLM, including unsupported configuration keys such as `num_sequences`, `num_parallel`, `model_path`, and `num_return_sequences`, rather than using the vLLM Python API. |
| `INP.common.no_output_as_input` | major | satisfied | `model.bin` and `output.txt` are only listed as runtime-produced files and no contents are authored for either. |
| `INP.common.no_truncation` | major | satisfied | All authored blocks are fully written without ellipses, TODOs, placeholder paths, or truncation markers. |
| `INP.common.values_match_physical_system` | major | satisfied | The answer declares 50 numbered prompts, `max_tokens: 50`, and `tensor_parallel_size: 4`, which match the stated workload; the stated 8 GPUs is within one Frontier node. |
