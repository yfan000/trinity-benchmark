# Verdicts — nekrs@polaris, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `73bf007d6891`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The allocation is specified by `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro directives exclusively, including `#PBS -l`, `#PBS -q`, and `#PBS -A`. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the Eagle working directory and NekRS installation paths. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to `${PBS_O_WORKDIR}`, the command uses `--setup case`, which resolves the supplied `case.par`, `case.re2`, and `case.udf` in the working directory; restart checkpoint handling is performed by the NekRS case setup. |
| `BATCH.common.invokes_application` | fatal | satisfied | The final launcher invokes NekRS through `mpiexec ... ./.lhelper nekrs --setup case --backend CUDA --device-id 0`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines contains a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | The script contains concrete account, queue, paths, case stem, and resource values with no unsubstituted placeholder syntax. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `debug` is listed as an available Polaris PBS queue and the one-node, 30-minute request is within its limits. |
| `BATCH.common.select_declared` | major | satisfied | The script requests one Polaris node via `#PBS -l select=1:system=polaris`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script requests `#PBS -l walltime=00:30:00`. |

## gemma-4-31b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The project allocation is supplied with `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The submission directives consistently use PBS Pro syntax (`#PBS`) and contain no directives from another scheduler. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the Eagle working directory and NekRS installation. |
| `BATCH.common.inputs_reachable` | major | **violated** | Although the script changes to the directory containing `case.par`, `case.re2`, and `case.udf`, its launch line uses `nekrs case` rather than the catalog-required command form `nekrs --setup case`; consequently the case stem is not supplied through the documented setup option. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launcher invokes NekRS through `mpiexec ... ./.lhelper nekrs ...` after adding `$NEKRS_HOME/bin` to `PATH`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All scheduler paths, project, queue, resources, and case stem are concrete; no unsubstituted placeholder is present. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `debug` is a listed Polaris PBS queue and the one-node, 30-minute request is within its limits. |
| `BATCH.common.select_declared` | major | satisfied | The node request is stated as `#PBS -l select=1:system=polaris`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The directive `#PBS -l walltime=00:30:00` requests the required walltime. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | It charges the specified allocation using `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script consistently uses PBS Pro directives such as `#PBS -l`, `#PBS -q`, and `#PBS -A`, with no Slurm directives. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the stated Eagle working directory and software paths. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to the PBS submission directory, `--setup case` resolves the present `case.par`, `case.re2`, and `case.udf` inputs; `--restart` requests checkpoint restart behavior. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launch command invokes NekRS through MPI: `mpiexec ... ./.lhelper nekrs --setup case ...`. |
| `BATCH.common.no_directive_comments` | major | **violated** | The directive `#PBS -V          # export all environment variables to the job` has a trailing comment, which PBS may parse as directive arguments. |
| `BATCH.common.no_placeholders` | fatal | satisfied | The script uses concrete paths, allocation, queue, case name, and log filenames, with no unresolved placeholder tokens. |
| `BATCH.common.queue_declared` | fatal | satisfied | It names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The selected `debug` queue is listed in the Polaris catalog. |
| `BATCH.common.select_declared` | major | satisfied | It requests one Polaris node using `#PBS -l select=1:system=polaris`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | It requests walltime with `#PBS -l walltime=00:30:00`. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | It charges the requested allocation using `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro `#PBS` directives and contains no directives from another scheduler dialect. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the Eagle paths used for the working directory, logs, and NekRS installation. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to the PBS submission working directory, `--setup case` resolves the supplied `case.par`, `case.re2`, and `case.udf` case files in that directory. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launch line invokes NekRS through MPI: `mpiexec ... ./.lhelper nekrs --setup case --backend CUDA --device-id 0 --restart`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied ⚠︎ flipped across runs | The script uses concrete paths, allocation, queue, case stem, and resource values, with no unsubstituted placeholder tokens. |
| `BATCH.common.queue_declared` | fatal | satisfied | It names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The specified `debug` queue is listed as an available Polaris PBS queue. |
| `BATCH.common.select_declared` | major | satisfied | It requests one Polaris node with `#PBS -l select=1:system=polaris`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | It requests walltime with `#PBS -l walltime=0:30:00`. |
