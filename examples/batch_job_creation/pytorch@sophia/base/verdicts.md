# Verdicts — pytorch@sophia, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `73bf007d6891`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The project account is supplied as `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro `#PBS` directives and contains no directives from another scheduler. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering both home and eagle filesystems it touches. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to the submitted working directory containing `train.py` and launches `train.py`, matching the documented command form. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launch command `torchrun --nproc_per_node=${NRANKS_PER_NODE} train.py` invokes the distributed PyTorch training application. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All directives, paths, account, queue, and launch arguments are concrete; no placeholder markers are present. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q by-gpu`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `by-gpu` is listed as an available Sophia queue in the catalog. |
| `BATCH.common.select_declared` | major | satisfied | The script contains `#PBS -l select=1:system=sophia`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script requests `#PBS -l walltime=01:00:00`. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The script charges the project using `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro `#PBS` directives exclusively and contains no Slurm directives. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the home and eagle filesystems used. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to `${PBS_O_WORKDIR}`, the script invokes `train.py`, matching the documented catalog run command that relies on the training script in the working directory. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launch command `torchrun --nproc_per_node=${GPUS_PER_NODE} train.py` invokes the distributed PyTorch training application. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All directive paths, account, queue, and launch values are concrete; no placeholder markers are present. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q by-gpu`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `by-gpu` is listed as an available Sophia PBS Pro queue in the catalog. |
| `BATCH.common.select_declared` | major | satisfied | The script states a node request using `#PBS -l select=1:ncpus=128:ngpus=4`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script requests walltime with `#PBS -l walltime=01:00:00`. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The allocation is charged with `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The answer consistently uses PBS Pro `#PBS` directives and contains no Slurm directives. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the home and eagle filesystems it uses. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to the submitted working directory, the documented command form `torchrun ... train.py` is used, so `train.py` is reachable there. |
| `BATCH.common.invokes_application` | fatal | satisfied | The script launches the training application with `torchrun --nproc_per_node=${NRANKS_PER_NODE} train.py`. |
| `BATCH.common.no_directive_comments` | major | **violated** | Several PBS directives have trailing comments, e.g. `#PBS -N ResNet50_train                           # job name`; PBS does not treat these as comments. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, allocation values, queue names, and the training filename are concrete; no placeholder tokens are present. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script includes `#PBS -q by-gpu`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `by-gpu` is listed as an available Sophia queue in the authoritative catalog. |
| `BATCH.common.select_declared` | major | satisfied | The script includes a node-selection directive: `#PBS -l select=1:system=sophia:ngpus=4`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The directive `#PBS -l walltime=01:00:00` requests the specified walltime. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The project account is declared with `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The submission uses PBS Pro directives exclusively, including `#PBS -l`, `#PBS -q`, and `#PBS -A`. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The directive `#PBS -l filesystems=home:eagle` declares both filesystems touched by the home-hosted conda setup and Eagle working directory. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `/eagle/AlloyDesign/bkowalski/pytorch_run`, where the prompt states `train.py` already exists, before invoking `train.py`. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launcher line invokes `torchrun` and ultimately runs `python train.py`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines contains a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | The script contains concrete queue, account, filesystem, and working-directory values without placeholder tokens. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q by-gpu`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `by-gpu` is listed as an available Sophia queue in the catalog. |
| `BATCH.common.select_declared` | major | satisfied | The script states the node request as `#PBS -l select=1:system=sophia`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script requests walltime with `#PBS -l walltime=01:00:00`. |
