# Verdicts — qmcpack@aurora, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `73bf007d6891`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The project account is supplied as `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro directives exclusively (`#PBS`) and contains no Slurm directives. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:flare`, covering the Aurora home and flare filesystems it uses. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `${PBS_O_WORKDIR}` and explicitly passes the supplied input file `qmc.xml` to QMCPACK. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launch line `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} qmcpack qmc.xml` invokes QMCPACK through the supplied MPI launcher form. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All scheduler values, paths, filenames, project, and queue are concrete; no placeholder markers are present. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `debug` is an Aurora PBS queue listed in the authoritative catalog and supports one node for up to one hour. |
| `BATCH.common.select_declared` | major | satisfied | The script states the node request as `#PBS -l select=1:system=aurora`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script requests walltime with `#PBS -l walltime=01:00:00`. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | Includes `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro directives exclusively, such as `#PBS -l`, `#PBS -q`, and `#PBS -A`. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | Declares `#PBS -l filesystems=home:flare`, covering the Aurora filesystems specified by the prompt. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `${PBS_O_WORKDIR}` and explicitly passes the supplied input file `qmc.xml` to QMCPACK. |
| `BATCH.common.invokes_application` | fatal | satisfied | Launches QMCPACK with `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} qmcpack qmc.xml` after adding the supplied QMCPACK binary directory to `PATH`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All directives, paths, allocation, queue, resources, and input filename are concrete; no placeholder tokens are present. |
| `BATCH.common.queue_declared` | fatal | satisfied | Includes `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The requested `debug` queue is listed in the Aurora catalog. |
| `BATCH.common.select_declared` | major | satisfied | Includes `#PBS -l select=1:system=aurora`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | Includes `#PBS -l walltime=01:00:00`. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | It charges the specified allocation using `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script consistently uses PBS Pro `#PBS` directives and contains no directives from another scheduler. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:flare`, covering the Aurora home and flare filesystems used. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to `${PBS_O_WORKDIR}`, the command explicitly passes `qmc.xml`, which is stated to be present in the working directory. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launch line `mpiexec -n 6 --ppn 6 qmcpack qmc.xml` invokes QMCPACK through the supplied MPI launcher form. |
| `BATCH.common.no_directive_comments` | major | **violated** | Every PBS directive has a trailing comment, for example `#PBS -N silicon_dmc                     # (a) job name`; PBS does not treat that trailing text as a shell comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All resource values, paths, account, queue, and input filename are concrete; no placeholder markers are present. |
| `BATCH.common.queue_declared` | fatal | satisfied | It names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The selected `debug` queue is listed in the Aurora catalog. |
| `BATCH.common.select_declared` | major | satisfied | It requests a node using `#PBS -l select=1:system=aurora`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | It includes `#PBS -l walltime=01:00:00`. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The allocation is supplied with `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro directives exclusively, including `#PBS -l`, `#PBS -q`, and `#PBS -A`. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:flare`, covering the required Aurora filesystems. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `${PBS_O_WORKDIR}` and passes the supplied input explicitly as `qmc.xml`, so the input is reachable when submitted from the stated working directory. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launcher line runs QMCPACK: `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} ... qmcpack qmc.xml`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, allocation values, resource values, and the input filename are concrete; no placeholder tokens are present. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `debug` is an Aurora PBS Pro queue listed in the authoritative catalog and supports 1 node for up to one hour. |
| `BATCH.common.select_declared` | major | satisfied | The node request is stated as `#PBS -l select=1:system=aurora`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script includes `#PBS -l walltime=01:00:00`. |
