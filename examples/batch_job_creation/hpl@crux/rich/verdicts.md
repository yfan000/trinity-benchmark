# Verdicts — hpl@crux, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `73bf007d6891`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | Includes `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | Uses PBS Pro directives exclusively, including `#PBS -l`, `#PBS -q`, and `#PBS -A`. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | Includes `#PBS -l filesystems=home:eagle`, covering the required ALCF filesystems declaration. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `${PBS_O_WORKDIR}`, which is the stated working directory where the fixed-name `HPL.dat` input is already present; `xhpl` therefore finds its default input. |
| `BATCH.common.invokes_application` | fatal | satisfied | Launches HPL with `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} xhpl` after adding the supplied HPL binary directory to PATH. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines contains a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All directives, paths, account, queue, and executable references are concrete; no placeholder tokens are present. |
| `BATCH.common.queue_declared` | fatal | satisfied | Includes `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The requested `debug` queue is listed as an existing Crux queue in the catalog. |
| `BATCH.common.select_declared` | major | satisfied | Includes `#PBS -l select=1:system=crux`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | Includes `#PBS -l walltime=0:30:00`. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The allocation directive is present as `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The submission directives consistently use PBS Pro syntax (`#PBS`) and contain no Slurm directives. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the home and Eagle filesystems used. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `${PBS_O_WORKDIR}` as required, and the prompt states that fixed-name input `HPL.dat` is already present in the working directory, where `xhpl` will find it. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launcher command `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} xhpl` invokes the supplied HPL executable available through the configured PATH. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines contains a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, account, queue, resource values, and executable names are concrete; no placeholder text is present. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script includes `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `debug` is listed as an available Crux PBS queue and the requested one node and 30-minute walltime are within its limits. |
| `BATCH.common.select_declared` | major | satisfied | The script states a node request with `#PBS -l select=1:ncpus=128`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The directive `#PBS -l walltime=00:30:00` requests the required walltime. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | Includes `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro `#PBS` directives and contains no directives from another scheduler. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | Includes `#PBS -l filesystems=home:eagle`, covering the eagle filesystem used by the working directory, logs, and binary. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `${PBS_O_WORKDIR}` and runs `xhpl`, which reads the supplied fixed-name `HPL.dat` already present in the stated working directory. |
| `BATCH.common.invokes_application` | fatal | satisfied | Launches HPL with `mpiexec -n "${NTOTRANKS}" --ppn "${NRANKS_PER_NODE}" xhpl`. |
| `BATCH.common.no_directive_comments` | major | **violated** | Multiple PBS directive lines have trailing comments, e.g. `#PBS -N HPL_linpack                     # job name`, which PBS may parse as directive arguments. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, allocation, queue, and resource values are concrete; no placeholder markers are present. |
| `BATCH.common.queue_declared` | fatal | satisfied | Includes `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The requested queue is `debug`, which is listed as an existing Crux queue. |
| `BATCH.common.select_declared` | major | satisfied | Includes `#PBS -l select=1:system=crux`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | Includes `#PBS -l walltime=0:30:00`. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The directive `#PBS -A TrinityAgent` supplies the project account. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro `#PBS` directives and contains no directives for another scheduler. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the home and Eagle filesystems it uses. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `/eagle/NuclearMPX/aschmidt/hpl_run`, the stated directory containing the fixed-name `HPL.dat` that `xhpl` reads. |
| `BATCH.common.invokes_application` | fatal | **violated** | Although the final line names `xhpl`, `-n ${NNODES * NRANKS_PER_NODE}` is invalid shell parameter expansion rather than arithmetic expansion, so the shell errors with a bad substitution and does not launch the application. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, account, queue, and resource values are concrete; no placeholder markers or TODO text are present. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `debug` is a catalog-listed Crux PBS queue and the requested one node and 30 minutes are within its limits. |
| `BATCH.common.select_declared` | major | satisfied | The directive `#PBS -l select=1:system=crux` states a one-node resource request. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The directive `#PBS -l walltime=00:30:00` requests walltime. |
