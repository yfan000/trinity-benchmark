# Verdicts — nwchem@polaris, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `73bf007d6891`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The script charges the specified allocation using `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script consistently uses PBS Pro directives (`#PBS`) and contains no Slurm directives. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the eagle filesystem used by the working directory, logs, and software paths. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `${PBS_O_WORKDIR}` and explicitly launches NWChem with the supplied `run.nw` input file. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launch command `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} nwchem run.nw` invokes NWChem. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines contains a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, allocation, queue, job name, and input filename are concrete; no placeholder markers are present. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The selected `debug` queue is listed in the Polaris catalog queues. |
| `BATCH.common.select_declared` | major | satisfied | The script states the node request with `#PBS -l select=1:system=polaris`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script requests walltime with `#PBS -l walltime=0:30:00`. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The script charges the requested project using `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script consistently uses PBS Pro directives (`#PBS`) and no conflicting scheduler dialect. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the Eagle working and software paths. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to the PBS submission working directory, the script explicitly passes the supplied input as `nwchem run.nw`. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launcher line `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} nwchem run.nw` invokes NWChem. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines contains a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, project, queue, input filename, and launch settings are concrete; no placeholders are present. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The requested `debug` queue is listed in the Polaris catalog. |
| `BATCH.common.select_declared` | major | satisfied | The script states the node request with `#PBS -l select=1:system=polaris`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script requests walltime with `#PBS -l walltime=00:30:00`. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The allocation is supplied with `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro directives (`#PBS`) and contains no directives from another scheduler. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the Eagle working, software, and log paths. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to `${PBS_O_WORKDIR}`, the launcher explicitly supplies the provided input filename `run.nw`. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launch line invokes NWChem through MPI: `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} nwchem run.nw`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, allocation, queue, job name, and input filename are concrete; no placeholder tokens are present. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `debug` is listed as an available Polaris PBS queue and the requested one node and 30-minute walltime are within its limits. |
| `BATCH.common.select_declared` | major | satisfied | The node request is stated as `#PBS -l select=1:system=polaris`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script requests `#PBS -l walltime=0:30:00`. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The project account is supplied with `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro `#PBS` directives and contains no conflicting scheduler dialect. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the Eagle working and software paths. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `${PBS_O_WORKDIR}` and launches NWChem with the provided input filename `run.nw`. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launch line `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} nwchem run.nw` invokes NWChem. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All directives, paths, allocation, input filename, and launch values are concrete; no placeholder text is present. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `debug` is a listed Polaris PBS Pro queue and the requested one node/30-minute walltime is within its limits. |
| `BATCH.common.select_declared` | major | satisfied | The node request is stated as `#PBS -l select=1:system=polaris`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The directive `#PBS -l walltime=0:30:00` requests the specified walltime. |
