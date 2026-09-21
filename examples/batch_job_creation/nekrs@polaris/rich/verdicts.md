# Verdicts — nekrs@polaris, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `73bf007d6891`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The allocation is specified by `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro `#PBS` directives and contains no conflicting scheduler-directive dialect. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the home and Eagle filesystems used. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `${PBS_O_WORKDIR}` and launches with `--setup case`, which resolves the supplied `case.par`, `case.re2`, and `case.udf` files in that working directory. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launcher invokes NekRS through `mpiexec ... ./.lhelper nekrs --setup case --backend CUDA --device-id 0` after adding the NekRS binary directory to `PATH`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All directives, paths, allocation, queue, case stem, and launch arguments are concrete; no unresolved placeholder tokens remain. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `debug` is a catalog-listed Polaris PBS queue and the one-node, 30-minute request is within its limits. |
| `BATCH.common.select_declared` | major | satisfied | The script requests one Polaris node using `#PBS -l select=1:system=polaris`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The directive `#PBS -l walltime=00:30:00` requests the required walltime. |

## gemma-4-31b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The script charges the requested allocation via `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro directives (`#PBS`) and contains no directives from another scheduler dialect. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the Eagle working directory and software paths. |
| `BATCH.common.inputs_reachable` | major | **violated** | The launch command omits the required case stem/setup argument (for example, `--setup case`), so it does not identify the present `case.par`, `case.re2`, and `case.udf` files for the NekRS restart. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launcher invokes NekRS through `mpiexec ... ./.lhelper nekrs --backend CUDA --device-id 0`, with `nekrs` made available by the configured `PATH`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | The script contains concrete paths, allocation, queue, resources, and command arguments without unsubstituted placeholder syntax. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `debug` is a listed valid Polaris PBS queue and the requested one node and 30-minute walltime fit its limits. |
| `BATCH.common.select_declared` | major | satisfied | The script requests one Polaris node using `#PBS -l select=1:system=polaris`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script requests `#PBS -l walltime=00:30:00`. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | It charges the specified allocation using `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro `#PBS` directives and contains no directives from another scheduler. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the Eagle working directory and NekRS installation paths. |
| `BATCH.common.inputs_reachable` | major | **violated** ⚠︎ flipped across runs | Although it changes into the case directory, it uses `--restart case` rather than the supplied NekRS launch form `nekrs --setup case`; the documented command form is what resolves the `case.par`/`case.re2` case stem, so this unsupported substitution is not a reliable runnable input invocation. |
| `BATCH.common.invokes_application` | fatal | satisfied | The `mpiexec` launch invokes NekRS through `$NEKRS_HOME/bin/nekrs`, whose value is the supplied NekRS binary path. |
| `BATCH.common.no_directive_comments` | major | **violated** | Multiple PBS directives have trailing comments, e.g. `#PBS -N nekrs_restart                                   # job name`, which PBS does not safely treat as comments. |
| `BATCH.common.no_placeholders` | fatal | satisfied | The script uses concrete account, queue, working-directory, output/error, and case values, with no unsubstituted placeholder token. |
| `BATCH.common.queue_declared` | fatal | satisfied | It specifies the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The requested `debug` queue is listed in the Polaris queue catalog. |
| `BATCH.common.select_declared` | major | satisfied | It requests one Polaris node with `#PBS -l select=1:system=polaris`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | It requests `#PBS -l walltime=00:30:00`. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | It charges the requested allocation via `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro directives (`#PBS`) and contains no conflicting scheduler dialect directives. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the Eagle working and software paths and Home. |
| `BATCH.common.inputs_reachable` | major | satisfied | After `cd ${PBS_O_WORKDIR}`, `--setup case` resolves the supplied `case.par`, `case.re2`, and `case.udf` files in the working directory; `--restart` requests checkpoint restart. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launcher invokes NekRS through `mpiexec ... ./.lhelper nekrs --setup case ...` after adding `$NEKRS_HOME/bin` to `PATH`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | The script uses concrete resource values, project, paths, and case stem, with no unsubstituted placeholder tokens. |
| `BATCH.common.queue_declared` | fatal | satisfied | It names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The selected `debug` queue exists in the Polaris queue catalog and the one-node, 30-minute request is within its limits. |
| `BATCH.common.select_declared` | major | satisfied | It requests a node using `#PBS -l select=1:system=polaris`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | It requests walltime with `#PBS -l walltime=00:30:00`. |
