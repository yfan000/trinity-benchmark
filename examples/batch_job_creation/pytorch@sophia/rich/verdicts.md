# Verdicts — pytorch@sophia, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `73bf007d6891`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The script charges the specified project using `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro directives (`#PBS`) and contains no directives from another scheduler. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the home and eagle filesystems it uses. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to the submitted working directory and invokes the provided `train.py` command form, so the training script is reachable there. |
| `BATCH.common.invokes_application` | fatal | satisfied | The script launches the training application with `torchrun --nproc_per_node=4 train.py`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines contains a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, directives, project, queue, and command arguments are concrete and contain no placeholders. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q by-gpu`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `by-gpu` is listed as an available Sophia PBS queue in the catalog. |
| `BATCH.common.select_declared` | major | satisfied | The script states the node allocation as `#PBS -l select=1:system=sophia`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script requests walltime with `#PBS -l walltime=01:00:00`. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The script charges the required project via `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro directives (`#PBS`) and contains no directives from another scheduler dialect. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the home environment source and Eagle working/log paths. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to the PBS submission working directory, the script invokes the documented command form with `train.py`, which is stated to already reside in the working directory. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launch line `torchrun --nproc_per_node=${GPUS_PER_NODE} train.py` invokes the requested distributed PyTorch training application. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, queue, allocation, and executable arguments are concrete; shell variables are used only for runtime values and not as unsubstituted placeholders. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q by-gpu`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `by-gpu` is listed as an available Sophia PBS queue in the catalog. |
| `BATCH.common.select_declared` | major | satisfied | The script includes a node request directive: `#PBS -l select=1:ncpus=48:mpiprocs=4:ngpus=4`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script requests `#PBS -l walltime=01:00:00`. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | It charges the specified project using `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script consistently uses PBS Pro directives (`#PBS`) and contains no Slurm directives. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the home and eagle filesystems it uses. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `${PBS_O_WORKDIR}` and invokes `train.py`, which the prompt states is already in the working directory. |
| `BATCH.common.invokes_application` | fatal | satisfied | It launches distributed PyTorch training through `/eagle/datascience/hzheng/software/sophia/pytorch-2.11-mpi/conda_env/bin/python -m torch.distributed.run --nproc_per_node=${NRANKS_PER_NODE} train.py`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines contains a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, project, queue, resource values, and training filename are concrete; no placeholder tokens are present. |
| `BATCH.common.queue_declared` | fatal | satisfied | It names the queue with `#PBS -q by-gpu`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The selected `by-gpu` queue is listed in the authoritative catalog for Sophia. |
| `BATCH.common.select_declared` | major | satisfied | It provides a select request: `#PBS -l select=1:system=sophia:ngpus=4`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | It requests walltime with `#PBS -l walltime=01:00:00`. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | It charges the required allocation using `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro directives exclusively, including `#PBS -l`, `#PBS -q`, `#PBS -A`, `#PBS -N`, `#PBS -o`, and `#PBS -e`. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the home environment path and Eagle working/output paths. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `${PBS_O_WORKDIR}` and launches the documented `train.py` command form, so the stated training script is reachable from the working directory. |
| `BATCH.common.invokes_application` | fatal | satisfied | The expanded command `${launch_command}` runs `torchrun --nproc_per_node=${GPUS_PER_NODE} train.py`, with `GPUS_PER_NODE=4`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines contains a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All directives, paths, allocation, queue, and launch arguments are concrete; no placeholder tokens are present. |
| `BATCH.common.queue_declared` | fatal | satisfied | It names the queue with `#PBS -q by-gpu`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `by-gpu` is listed as an available Sophia PBS queue in the catalog. |
| `BATCH.common.select_declared` | major | satisfied | It states the node request as `#PBS -l select=1:system=sophia`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | It requests `#PBS -l walltime=01:00:00`. |
