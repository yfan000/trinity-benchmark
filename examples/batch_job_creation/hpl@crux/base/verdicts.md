# Verdicts — hpl@crux, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `73bf007d6891`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | It charges the required project via `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro `#PBS` directives and contains no directives from another scheduler. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the Eagle working, log, and software paths. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `${PBS_O_WORKDIR}`, where the prompt states `HPL.dat` is already present, and `xhpl` reads that fixed default filename. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launch line `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} xhpl` invokes the HPL binary after adding its directory to PATH. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All directives, paths, account, queue, and command values are concrete and contain no placeholder text. |
| `BATCH.common.queue_declared` | fatal | satisfied | It names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The requested `debug` queue is listed as an available Crux PBS Pro queue. |
| `BATCH.common.select_declared` | major | satisfied | It requests one Crux node using `#PBS -l select=1:system=crux`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | It requests walltime with `#PBS -l walltime=00:30:00`. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | Includes `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | Uses PBS Pro directives consistently (`#PBS`) and contains no Slurm directives. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | Includes `#PBS -l filesystems=home:eagle`, covering the home and eagle filesystems used. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `${PBS_O_WORKDIR}`, where the prompt states `HPL.dat` is already present, and `xhpl` uses that fixed default input filename. |
| `BATCH.common.invokes_application` | fatal | satisfied | Launches HPL with `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} xhpl`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, account, queue, resource values, and executable invocation are concrete; no placeholder markers are present. |
| `BATCH.common.queue_declared` | fatal | satisfied | Includes `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The requested `debug` queue is listed in the authoritative Crux queue catalog. |
| `BATCH.common.select_declared` | major | satisfied | Includes a node request directive: `#PBS -l select=1:ncpus=128`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | Includes `#PBS -l walltime=00:30:00`. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | It charges the specified account using `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script consistently uses PBS Pro directives such as `#PBS -l`, `#PBS -q`, and `#PBS -A`, with no Slurm directives. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the home and Eagle filesystems it uses. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `${PBS_O_WORKDIR}` before invoking `xhpl`, allowing xhpl to read the fixed-name `HPL.dat` supplied in the working directory. |
| `BATCH.common.invokes_application` | fatal | satisfied | It launches HPL with `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} xhpl`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines contains a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, project names, queue names, and resource values are concrete; no placeholder markers are present. |
| `BATCH.common.queue_declared` | fatal | satisfied | It names a queue via `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The selected `debug` queue exists on Crux according to the catalog facts. |
| `BATCH.common.select_declared` | major | satisfied | It states a node request with `#PBS -l select=1:ncpus=128:system=crux`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | It requests walltime with `#PBS -l walltime=0:30:00`. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | It charges the requested allocation with `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro directives (`#PBS`) and contains no directives from another scheduler. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the home and Eagle filesystems it references. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script executes `cd ${PBS_O_WORKDIR}` before launching `xhpl`, and the prompt states that `HPL.dat` is already present in the working directory. |
| `BATCH.common.invokes_application` | fatal | **violated** | Although it contains `mpiexec ... xhpl`, the rank expression `-n ${NNODES * NRANKS_PER_NODE}` is invalid shell parameter expansion, so the shell errors before `mpiexec` can launch xhpl. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, queue, account, resources, and command names are concrete; no placeholder markers are present. |
| `BATCH.common.queue_declared` | fatal | satisfied | It names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The selected `debug` queue exists on Crux according to the catalog. |
| `BATCH.common.select_declared` | major | satisfied | It requests a node using `#PBS -l select=1:system=crux`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | It requests walltime with `#PBS -l walltime=00:30:00`. |
