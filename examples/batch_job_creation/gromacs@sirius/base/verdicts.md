# Verdicts — gromacs@sirius, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `73bf007d6891`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The project account is supplied as `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script consistently uses PBS Pro directives (`#PBS`) and no conflicting scheduler dialect. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:tegu`, covering the required Sirius filesystem. |
| `BATCH.common.inputs_reachable` | major | satisfied | With `-deffnm run`, GROMACS resolves its run-input filename as `run.tpr` in the working directory, which the script reaches via `cd ${PBS_O_WORKDIR}`. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launch line invokes GROMACS through MPI: `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} gmx_mpi mdrun ...`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines contains a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, resource values, queue, account, and command arguments are concrete; no placeholder tokens are present. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names a queue with `#PBS -q workq`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The selected `workq` queue is listed in the Sirius catalog. |
| `BATCH.common.select_declared` | major | satisfied | The node request is stated as `#PBS -l select=1:system=sirius`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script requests walltime with `#PBS -l walltime=00:30:00`. |

## gemma-4-31b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | Includes the required allocation directive `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | Uses PBS Pro directives consistently (`#PBS`) and contains no Slurm directives. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | Includes `#PBS -l filesystems=home:tegu`, the required Sirius filesystem declaration. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to `${PBS_O_WORKDIR}`, the command explicitly supplies the provided input as `-s run.tpr`. |
| `BATCH.common.invokes_application` | fatal | satisfied | Launches GROMACS through MPI: `mpiexec ... /lus/tegu/projects/PolarisAT/hzheng/software/gromacs/bin/gmx_mpi mdrun ...`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, allocation, queue, resource counts, and filenames are concrete; no placeholder tokens remain. |
| `BATCH.common.queue_declared` | fatal | satisfied | Includes `#PBS -q workq`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The specified queue is `workq`, which exists on Sirius according to the catalog facts. |
| `BATCH.common.select_declared` | major | **violated** | Although it has a select directive, it requests `#PBS -l select=1:system=polaris`; the target system is Sirius, so this is not a valid target-system resource request. |
| `BATCH.common.walltime_declared` | fatal | satisfied | Includes `#PBS -l walltime=00:30:00`. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The script charges the required allocation using `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script consistently uses PBS Pro `#PBS` directives and contains no Slurm directives. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:tegu`, the required Sirius filesystem list. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to `${PBS_O_WORKDIR}`, the command explicitly supplies the available input as `-s run.tpr`. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launcher invokes GROMACS via `mpiexec ... gmx_mpi mdrun ...`. |
| `BATCH.common.no_directive_comments` | major | **violated** | Multiple PBS directive lines have trailing comments, for example `#PBS -N gromacs_mdrun                     # job name`, which PBS may parse as directive arguments. |
| `BATCH.common.no_placeholders` | fatal | satisfied | The script uses concrete paths, allocation, queue, input filename, and resource values without unresolved placeholder tokens. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q workq`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The named queue is `workq`, which is listed in the Sirius catalog. |
| `BATCH.common.select_declared` | major | satisfied | The script requests nodes with `#PBS -l select=1:system=sirius`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script includes `#PBS -l walltime=00:30:00`. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The script charges the allocation using `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro `#PBS` directives and contains no directives from another scheduler. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:tegu`. |
| `BATCH.common.inputs_reachable` | major | **violated** | The supplied input is `run.tpr`, but the command has no `-s run.tpr`; with `-deffnm md`, GROMACS will resolve the run input as `md.tpr` rather than the provided `run.tpr`. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launcher executes GROMACS via `mpiexec -n 8 --ppn 8 gmx_mpi mdrun ...`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | The script contains concrete resource values, paths, queue, allocation, and command arguments without placeholder markers. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q workq`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The requested `workq` queue exists for Sirius in the authoritative catalog. |
| `BATCH.common.select_declared` | major | satisfied | The script includes the node selection directive `#PBS -l select=1:system=sirius`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script requests walltime with `#PBS -l walltime=00:30:00`. |
