# Verdicts — qe@aurora, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `73bf007d6891`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The script charges the specified allocation using `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The submission directives consistently use PBS Pro syntax (`#PBS`) and no conflicting scheduler dialect is present. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:flare`, covering the home and flare filesystems it uses. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to `${PBS_O_WORKDIR}`, the command explicitly supplies the stated available input file as `-in scf.scf.in`. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launcher executes Quantum ESPRESSO via `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} ${PW_X} -in scf.scf.in`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines contains a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, resource counts, project, queue, executable, and input filename are concrete; no placeholder tokens remain. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `debug` is listed as an available Aurora PBS queue in the catalog and permits one node with a 30-minute walltime. |
| `BATCH.common.select_declared` | major | satisfied | The script includes the node request `#PBS -l select=1:system=aurora`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script requests `#PBS -l walltime=00:30:00`. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The script supplies the allocation directive `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script consistently uses PBS Pro directives (`#PBS`) and contains no conflicting scheduler directives. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:flare`, covering the Aurora filesystems used by the working directory and software path. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to `${PBS_O_WORKDIR}`, the script explicitly passes the supplied input filename via `-in scf.scf.in`. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launch line invokes Quantum ESPRESSO through MPI: `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} $PW_X -in scf.scf.in`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, resource values, input filename, queue, and account are concrete; no placeholder tokens remain. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `debug` is listed as an available Aurora PBS queue in the catalog and supports one node for the requested 30 minutes. |
| `BATCH.common.select_declared` | major | satisfied | The script states a one-node request with `#PBS -l select=1`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script requests walltime with `#PBS -l walltime=00:30:00`. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | Includes `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro directives exclusively, such as `#PBS -l`, `#PBS -q`, and `#PBS -A`. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | Includes `#PBS -l filesystems=home:flare`, matching the required Aurora filesystems. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to `${PBS_O_WORKDIR}`, the script explicitly passes the supplied input filename via `-in scf.scf.in`. |
| `BATCH.common.invokes_application` | fatal | satisfied | It launches Quantum ESPRESSO with `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} $PW_X -in scf.scf.in`. |
| `BATCH.common.no_directive_comments` | major | satisfied | No `#PBS` directive line contains a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All scheduler directives, paths, executable settings, input filename, and rank values are concrete; no placeholder tokens remain. |
| `BATCH.common.queue_declared` | fatal | satisfied | Includes `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The requested `debug` queue is listed as an Aurora PBS Pro queue and permits one node for up to one hour. |
| `BATCH.common.select_declared` | major | satisfied | Includes `#PBS -l select=1:system=aurora`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | Includes `#PBS -l walltime=00:30:00`. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The script includes the allocation directive `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro `#PBS` directives and contains no Slurm directives. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:flare`, covering the required Aurora filesystems. |
| `BATCH.common.inputs_reachable` | major | satisfied | It changes to `${PBS_O_WORKDIR}` and explicitly passes the provided input filename as `-in scf.scf.in`. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launcher line invokes Quantum ESPRESSO via `mpiexec ... $PW_X -in scf.scf.in` with `PW_X` set to the supplied `pw.x` binary. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | The script uses concrete paths, queue, account, filenames, and resource values, with no unsubstituted placeholder tokens. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script includes `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `debug` is an Aurora PBS Pro queue listed in the catalog and permits one node for up to one hour. |
| `BATCH.common.select_declared` | major | satisfied | The script includes the node request `#PBS -l select=1:system=aurora`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script includes `#PBS -l walltime=00:30:00`. |
