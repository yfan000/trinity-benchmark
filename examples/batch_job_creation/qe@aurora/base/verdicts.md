# Verdicts — qe@aurora, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `73bf007d6891`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The script charges the requested project with `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script consistently uses PBS Pro directives (`#PBS`) and contains no Slurm directives. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:flare`, covering the required Aurora filesystems. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to `${PBS_O_WORKDIR}`, the script explicitly passes the supplied input file as `-in scf.scf.in`. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launch line invokes Quantum ESPRESSO via `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} $PW_X -in scf.scf.in`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines contains a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All scheduler values, paths, binary locations, input names, and rank counts are concrete; no placeholder tokens remain. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue using `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The selected `debug` queue is listed in the Aurora catalog and supports 1 node for up to 1 hour. |
| `BATCH.common.select_declared` | major | satisfied | The script states the node selection with `#PBS -l select=1:system=aurora`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script requests walltime with `#PBS -l walltime=00:30:00`. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The script charges the requested project via `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro directives exclusively, including `#PBS -l`, `#PBS -q`, and `#PBS -A`. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:flare`, matching the Aurora filesystems named in the prompt. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to `${PBS_O_WORKDIR}`, the launch command explicitly supplies the existing input filename `-in scf.scf.in`. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launch line invokes the supplied Quantum ESPRESSO binary through MPI: `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} $PW_X -in scf.scf.in`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, resource values, filenames, queue, and account values are concrete; no placeholder markers remain. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `debug` is listed as an Aurora PBS queue in the catalog and permits one node for up to one hour. |
| `BATCH.common.select_declared` | major | satisfied | The script states a one-node request with `#PBS -l select=1`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script requests walltime with `#PBS -l walltime=00:30:00`. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The allocation directive is present as `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The answer uses PBS Pro `#PBS` directives and contains no conflicting scheduler directive dialect. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:flare`, covering the Aurora home and flare filesystems it uses. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to `${PBS_O_WORKDIR}`, the script explicitly passes the provided input filename as `-in scf.scf.in`. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launch command invokes Quantum ESPRESSO through `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} ${PW_X} -in scf.scf.in`. |
| `BATCH.common.no_directive_comments` | major | **violated** | Every PBS directive has a trailing comment, for example `#PBS -N SiC_scf                                    # job name`; PBS does not treat this as a shell comment within directives. |
| `BATCH.common.no_placeholders` | fatal | satisfied | The script uses concrete paths, project, input filename, queue, and rank counts, with no unsubstituted placeholder tokens. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `debug` is an authoritative Aurora PBS queue and the requested one node and 30-minute walltime are within its limits. |
| `BATCH.common.select_declared` | major | satisfied | The script requests one node with `#PBS -l select=1:system=aurora`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script includes `#PBS -l walltime=0:30:00`. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The script includes `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro `#PBS` directives and contains no conflicting scheduler dialect directives. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:flare`. |
| `BATCH.common.inputs_reachable` | major | satisfied | After `cd ${PBS_O_WORKDIR}`, the launcher explicitly passes the provided input filename `-in scf.scf.in`. |
| `BATCH.common.invokes_application` | fatal | satisfied | It invokes Quantum ESPRESSO through `mpiexec ... $PW_X -in scf.scf.in` with `PW_X` set to the supplied `pw.x` binary. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines contains a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | The script contains concrete paths, queue, account, input filename, and resource values, with no unsubstituted placeholder tokens. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `debug` is an Aurora PBS Pro queue listed in the catalog. |
| `BATCH.common.select_declared` | major | satisfied | The script states a node request with `#PBS -l select=1:system=aurora`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script requests `#PBS -l walltime=00:30:00`. |
