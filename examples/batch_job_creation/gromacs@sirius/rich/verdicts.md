# Verdicts — gromacs@sirius, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `73bf007d6891`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The account directive is present as `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The answer uses PBS Pro `#PBS` directives and contains no directives from another scheduler. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:tegu`, matching the required Sirius filesystem value. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to the PBS working directory, `-deffnm run` causes GROMACS file options to use the `run` stem, including the supplied `run.tpr` input. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launch line invokes GROMACS through MPI: `mpiexec ... gmx_mpi mdrun ...`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, allocation values, and command arguments are concrete; no placeholder markers or replacement instructions remain. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q workq`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `workq` is listed in the Sirius catalog as an available queue. |
| `BATCH.common.select_declared` | major | satisfied | The script requests one Sirius node with `#PBS -l select=1:system=sirius`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script includes `#PBS -l walltime=00:30:00`. |

## gemma-4-31b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The script includes the required project directive `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro directives (`#PBS`) and contains no conflicting scheduler dialect directives. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:tegu`, the required Sirius filesystem value. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to `${PBS_O_WORKDIR}`, the launch explicitly supplies `-s run.tpr`, matching the stated input file in the working directory. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launcher invokes GROMACS through MPI: `mpiexec ... /lus/tegu/projects/PolarisAT/hzheng/software/gromacs/bin/gmx_mpi mdrun ...`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | The script uses concrete allocation, paths, filenames, queue, and account values and contains no unsubstituted placeholders. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script includes `#PBS -q workq`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `workq` is listed in the Sirius catalog as an available queue. |
| `BATCH.common.select_declared` | major | **violated** ⚠︎ flipped across runs | Although a select directive is present, it requests `#PBS -l select=1:system=polaris`; the target system is Sirius, so this is not a valid Sirius node request. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script includes `#PBS -l walltime=00:30:00`. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | It includes the allocation directive `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script consistently uses PBS Pro directives (`#PBS`) and contains no conflicting scheduler dialect. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:tegu`, covering the stated Sirius filesystem. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to `${PBS_O_WORKDIR}`, the command explicitly supplies the provided input as `-s run.tpr`. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launch command invokes GROMACS through MPI: `mpiexec ... gmx_mpi mdrun ...`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines contains a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All directives, paths, allocation, resource counts, and application arguments are concrete; no unresolved placeholder token is present. |
| `BATCH.common.queue_declared` | fatal | satisfied | It names a queue using `#PBS -q workq`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The requested queue is `workq`, which is listed in the Sirius catalog. |
| `BATCH.common.select_declared` | major | satisfied | It states the node selection as `#PBS -l select=1:system=sirius`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | It requests walltime with `#PBS -l walltime=0:30:00`. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The script charges the specified project using `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script consistently uses PBS Pro directives (`#PBS`) and contains no conflicting scheduler dialect. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:tegu`, the required Sirius filesystem value. |
| `BATCH.common.inputs_reachable` | major | **violated** | The supplied input is `run.tpr`, but the launch line has no `-s run.tpr`; with `-deffnm md`, GROMACS would instead resolve its default input as `md.tpr`. |
| `BATCH.common.invokes_application` | fatal | satisfied | It launches GROMACS through MPI: `mpiexec -n ${N_RANKS} --ppn ${N_RANKS} gmx_mpi mdrun ...`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | The script contains concrete resource values, paths, module names, and command arguments, with no unsubstituted placeholder markers. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names a queue with `#PBS -q workq`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `workq` is the catalog-listed queue for Sirius. |
| `BATCH.common.select_declared` | major | satisfied | The directive `#PBS -l select=1:system=sirius` requests one Sirius node. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The directive `#PBS -l walltime=00:30:00` requests the decided 30-minute walltime. |
