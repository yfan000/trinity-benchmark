# Verdicts — nwchem@polaris, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `73bf007d6891`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | Includes `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | Uses PBS Pro `#PBS` directives and no directives from another scheduler. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | Includes `#PBS -l filesystems=home:eagle`, covering the Eagle working, software, and output paths. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `${PBS_O_WORKDIR}`, which is the stated directory containing `run.nw`, and explicitly passes `run.nw` to NWChem. |
| `BATCH.common.invokes_application` | fatal | satisfied | Launches NWChem with `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} nwchem run.nw`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines contains a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, allocation, queue, executable invocation, and input filename are concrete with no placeholder tokens. |
| `BATCH.common.queue_declared` | fatal | satisfied | Includes `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The requested `debug` queue is listed as an available Polaris queue. |
| `BATCH.common.select_declared` | major | satisfied | Includes `#PBS -l select=1:system=polaris`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | Includes `#PBS -l walltime=00:30:00`. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | Includes `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | Uses PBS Pro `#PBS` directives and contains no directives from another scheduler dialect. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | Includes `#PBS -l filesystems=home:eagle`, covering the eagle working/output/software paths and home. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `${PBS_O_WORKDIR}` and explicitly supplies the stated input file as `nwchem run.nw`. |
| `BATCH.common.invokes_application` | fatal | satisfied | Launches NWChem with `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} nwchem run.nw`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines contains a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All directive paths, allocation, input filename, and launch settings are concrete; no placeholder tokens are present. |
| `BATCH.common.queue_declared` | fatal | satisfied | Includes `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The selected `debug` queue is listed in the Polaris catalog. |
| `BATCH.common.select_declared` | major | satisfied | Includes `#PBS -l select=1:system=polaris`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | Includes `#PBS -l walltime=00:30:00`. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | It charges the requested allocation with `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script exclusively uses PBS Pro directives such as `#PBS -l`, `#PBS -q`, and `#PBS -A`. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the eagle working/software paths and home. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `${PBS_O_WORKDIR}` as required and explicitly passes the provided input filename as `run.nw`. |
| `BATCH.common.invokes_application` | fatal | **violated** | Although the launcher says `mpiexec ... nwchem run.nw`, all supplied NWChem PATH and library exports misspell the required `/eagle/datascience/hzheng/...` prefix as `/eagle/datascience/hzhheng/...`, so `nwchem` will not be found through the configured PATH. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All directives, paths, allocation, input filename, and launch values are concrete; no placeholder syntax is present. |
| `BATCH.common.queue_declared` | fatal | satisfied | It names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The selected `debug` queue is listed in the Polaris catalog queues. |
| `BATCH.common.select_declared` | major | satisfied | It requests one Polaris node using `#PBS -l select=1:system=polaris`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | It requests `#PBS -l walltime=0:30:00`. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | Includes `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | Uses PBS Pro `#PBS` directives and contains no conflicting scheduler dialect. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | Includes `#PBS -l filesystems=home:eagle`, covering the Eagle working/software paths and home filesystem. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `${PBS_O_WORKDIR}` and explicitly supplies the stated existing input file as `run.nw`. |
| `BATCH.common.invokes_application` | fatal | satisfied | Launches NWChem with `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} nwchem run.nw`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All directives, paths, allocation, executable invocation, and input filename are concrete with no placeholders. |
| `BATCH.common.queue_declared` | fatal | satisfied | Includes `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The requested `debug` queue exists on Polaris and supports one node with a 30-minute walltime. |
| `BATCH.common.select_declared` | major | satisfied | Includes `#PBS -l select=1:system=polaris`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | Includes `#PBS -l walltime=0:30:00`. |
