# Verdicts — qmcpack@aurora, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `73bf007d6891`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | Includes `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | Uses PBS Pro directives consistently (`#PBS`) and contains no conflicting scheduler dialect. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | Declares `#PBS -l filesystems=home:flare`, covering the home and flare filesystems used by the job. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `${PBS_O_WORKDIR}` and invokes QMCPACK with the supplied input filename `qmc.xml`, so the input is reachable when submitted from the stated working directory. |
| `BATCH.common.invokes_application` | fatal | satisfied | Launches QMCPACK through MPI with `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} qmcpack qmc.xml`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, account, queue, resources, executable invocation, and input filename are concrete; no placeholder markers are present. |
| `BATCH.common.queue_declared` | fatal | satisfied | Includes `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The requested `debug` queue is listed in the Aurora catalog and permits 1 node with up to one hour walltime. |
| `BATCH.common.select_declared` | major | satisfied | Includes `#PBS -l select=1:system=aurora`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | Includes `#PBS -l walltime=01:00:00`. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | Includes `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script consistently uses PBS Pro directives such as `#PBS -l`, `#PBS -q`, and `#PBS -A`, with no Slurm directives. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | Includes `#PBS -l filesystems=home:flare`, covering the home and flare filesystems used by the job. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `${PBS_O_WORKDIR}` and explicitly passes the supplied `qmc.xml` input to QMCPACK, allowing its associated `qmc.h5` file in that directory to be reached. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launch line `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} qmcpack qmc.xml` invokes QMCPACK through MPI. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines contains a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All directives, paths, allocation, queue, and input names are concrete; no placeholder syntax or replacement instructions remain. |
| `BATCH.common.queue_declared` | fatal | satisfied | Includes `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The requested `debug` queue is listed in the authoritative Aurora queue catalog and supports one node for up to one hour. |
| `BATCH.common.select_declared` | major | satisfied | Includes `#PBS -l select=1:system=aurora`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | Includes `#PBS -l walltime=01:00:00`. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The allocation directive is present as `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The answer uses PBS Pro `#PBS` directives and contains no directives from another scheduler dialect. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:flare`, covering the Aurora home and flare filesystems used by the job. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to the submit working directory, the launch command explicitly supplies `qmc.xml`, which is listed as present there. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launch line `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} qmcpack qmc.xml` invokes QMCPACK through the supplied MPI launcher form. |
| `BATCH.common.no_directive_comments` | major | **violated** | Multiple PBS directives have trailing comments, for example `#PBS -N Si_bulk_DMC                     # job name`; PBS does not treat these as shell comments within directives. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, allocation, queue, resources, and input filename are concrete; no placeholder tokens or replacement instructions appear. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `debug` is an Aurora PBS queue listed in the authoritative catalog and supports one node for up to one hour. |
| `BATCH.common.select_declared` | major | satisfied | The script requests the node with `#PBS -l select=1:system=aurora`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script includes `#PBS -l walltime=01:00:00`, matching the requested one-hour walltime. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The script charges the requested allocation with `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro `#PBS` directives and contains no Slurm directives. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:flare`. |
| `BATCH.common.inputs_reachable` | major | satisfied | After `cd ${PBS_O_WORKDIR}`, the launch command explicitly supplies the present input file `qmc.xml`. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launcher line invokes QMCPACK: `mpiexec ... qmcpack qmc.xml`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | The script contains concrete paths, account, queue, resource values, and input filename, with no placeholder tokens. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue using `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `debug` is an Aurora PBS queue listed in the authoritative catalog and supports 1 node for up to one hour. |
| `BATCH.common.select_declared` | major | satisfied | The script states the node request as `#PBS -l select=1:system=aurora`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script requests walltime with `#PBS -l walltime=01:00:00`. |
