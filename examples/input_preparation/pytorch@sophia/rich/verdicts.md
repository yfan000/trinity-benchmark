# Verdicts — pytorch@sophia, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `98dca67530dc`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | not_applicable ⚠︎ flipped across runs | The authoritative catalog facts provide no required-input file list for PyTorch (MPI), so no catalog-mandated filename can be checked. |
| `INP.common.exact_filenames_used` | major | not_applicable | PyTorch training scripts and checkpoint paths are selected by the user or launch arguments; this application has no fixed, format-mandated input filename. |
| `INP.common.file_identifiable` | major | satisfied | The supplied file is recognisably a PyTorch distributed-training Python script, using `torch`, `DistributedDataParallel`, `torchvision.models.resnet50`, and `init_process_group`. |
| `INP.common.mandatory_sections_present` | major | satisfied | `train_resnet50.py` is a complete Python training program containing distributed setup, data loading, model/optimizer setup, mixed precision, resume logic, training, and checkpoint saving. |
| `INP.common.no_binary_contents` | fatal | satisfied ⚠︎ flipped across runs | No binary checkpoint contents are fabricated in the response. |
| `INP.common.no_invented_keywords` | fatal | satisfied | The code uses valid Python, PyTorch, torchvision, and torch.distributed APIs such as `init_process_group`, `DDP`, `GradScaler`, and `autocast`. |
| `INP.common.no_output_as_input` | major | satisfied | The answer writes only the Python source input; although the source calls `torch.save`, it does not author contents for the runtime-generated checkpoint file. |
| `INP.common.no_truncation` | major | satisfied | The Python file is written in full and contains no ellipsis-based truncation, placeholder path, TODO, or FIXME marker. |
| `INP.common.values_match_physical_system` | major | satisfied | The script specifies `resnet50`, `batch_size=256`, mixed precision, and `epochs=10`, consistent with the stated workload. |

## gemma-4-31b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | satisfied ⚠︎ flipped across runs | The answer provides the executable PyTorch training input, `train_resnet50.py`, and identifies the required pre-existing restart checkpoint, `checkpoint.pth`. |
| `INP.common.exact_filenames_used` | major | not_applicable | PyTorch training scripts and checkpoint paths are chosen by the user or launcher; the catalog supplies no fixed input filename contract. |
| `INP.common.file_identifiable` | major | satisfied | The supplied `train_resnet50.py` is recognizable PyTorch input code, importing `torch`, `torchvision`, `DistributedDataParallel`, `GradScaler`, and `autocast`. |
| `INP.common.mandatory_sections_present` | major | satisfied | `train_resnet50.py` includes distributed initialization, dataset/sampler/DataLoader setup, ResNet-50/DDP setup, AMP training, checkpoint restore, and checkpoint saving. |
| `INP.common.no_binary_contents` | fatal | **violated** ⚠︎ flipped across runs | `checkpoint.pth` is a binary runtime-generated PyTorch checkpoint, but the answer supplies a fenced pseudo-content block (`[Binary data produced at runtime]`) rather than only listing it as an existing runtime-produced file without contents. |
| `INP.common.no_invented_keywords` | fatal | satisfied | The script uses valid Python and PyTorch APIs such as `init_process_group`, `DistributedSampler`, `DDP`, `torch.load`, `GradScaler`, and `autocast`. |
| `INP.common.no_output_as_input` | major | **violated** ⚠︎ flipped across runs | The answer presents `checkpoint.pth` in a fenced contents block even though the script itself writes that same runtime-produced file via `torch.save(..., checkpoint_path)`. |
| `INP.common.no_truncation` | major | satisfied | The Python script is written in full with no ellipses, TODOs, placeholder paths, or truncation markers. |
| `INP.common.values_match_physical_system` | major | satisfied | The script sets `batch_size = 256`, `epochs = 10`, selects `list(range(100000))`, uses ResNet-50, and enables CUDA mixed precision, matching the stated workload. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | **violated** | The answer supplies an unsupported `config.yaml` and a partial manifest but does not supply the required executable PyTorch training input (`train.py`) implementing DDP, AMP, data loading, checkpoint restore, and checkpoint saving. |
| `INP.common.exact_filenames_used` | major | not_applicable | PyTorch does not require a fixed-name input deck; the training script and checkpoint path are selected by the launch command or program arguments. |
| `INP.common.file_identifiable` | major | **violated** | `config.yaml` is generic YAML rather than a recognisable PyTorch input format, and no Python program is supplied that would parse its keys or perform the requested PyTorch training. |
| `INP.common.mandatory_sections_present` | major | **violated** | No training script is provided, so the necessary PyTorch sections for `init_process_group`, ResNet-50/DDP setup, DataLoader/DistributedSampler, AMP loop, and checkpoint resume logic are absent. |
| `INP.common.no_binary_contents` | fatal | satisfied | For `checkpoints/resnet50_epoch_03.pt`, the answer states "Not written here" and does not invent binary checkpoint contents. |
| `INP.common.no_invented_keywords` | fatal | **violated** | Keys such as `world_size`, `precision`, `resume`, `lr_scheduler`, and `dataset.manifest` are not PyTorch input-language keywords; they are invented configuration conventions with no supplied program to define or consume them. |
| `INP.common.no_output_as_input` | major | satisfied | The checkpoint is explicitly identified as a runtime-produced binary and no checkpoint contents are authored. |
| `INP.common.no_truncation` | major | **violated** | The purported manifest contains `# …` and says "(total 100 000 lines...)" rather than writing all required entries in full. |
| `INP.common.values_match_physical_system` | major | **violated** | The configuration declares `world_size: 64` and `batch_size_per_gpu: 256`, which implies a global batch size of 16,384, but declares `total_batch_size: 2048` and incorrectly comments it as `256 × 8 GPUs per node × 8 nodes`. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `INP.common.all_required_files_present` | fatal | not_applicable | The authoritative catalog facts supplied do not list any fixed required input files for PyTorch (MPI). |
| `INP.common.exact_filenames_used` | major | not_applicable | PyTorch training scripts and checkpoints are selected by launch arguments or Python code rather than opened under a catalog-defined fixed filename. |
| `INP.common.file_identifiable` | major | satisfied | The supplied `.py` files are recognisable Python/PyTorch training, data-loading, configuration, and distributed-setup source files. |
| `INP.common.mandatory_sections_present` | major | **violated** | `train.py` is not a complete runnable training input: it calls undefined `resnet50()` and `ddp_setup()` without importing either, and it lacks the required mixed-precision and full checkpoint-resume state handling. |
| `INP.common.no_binary_contents` | fatal | satisfied | No fabricated text contents are provided for the binary PyTorch checkpoint. |
| `INP.common.no_invented_keywords` | fatal | satisfied | The answer uses ordinary Python syntax and valid PyTorch/torchvision API names rather than unsupported application-format directives. |
| `INP.common.no_output_as_input` | major | satisfied | The answer does not write checkpoint contents; it states that `checkpoint.pth` is runtime-generated. |
| `INP.common.no_truncation` | major | **violated** | `datautils.py` contains the unresolved placeholder dataset path `root="/path/to/imagenet"`. |
| `INP.common.values_match_physical_system` | major | satisfied | The declared `num_epochs = 10`, `batch_size = 256`, `num_samples = 100000`, and one node with eight GPUs are consistent with the stated workload and Sophia node hardware. |
