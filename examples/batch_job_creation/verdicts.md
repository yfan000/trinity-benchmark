# Verdicts — nemotron-3-ultra on hpl@crux

Majority across three judge replicates, judged by gpt56terra under rubric **r27**. Severities shown are the current library, **r28** (sha `73bf007d6891`).

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | **satisfied** | It charges the required project via `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | **satisfied** | The script uses PBS Pro `#PBS` directives and contains no directives from another scheduler. |
| `BATCH.common.filesystems_declared` | fatal | **satisfied** | The script declares `#PBS -l filesystems=home:eagle`, covering the Eagle working, log, and software paths. |
| `BATCH.common.inputs_reachable` | major | **satisfied** | The script changes to `${PBS_O_WORKDIR}`, where the prompt states `HPL.dat` is already present, and `xhpl` reads that fixed default filename. |
| `BATCH.common.invokes_application` | fatal | **satisfied** | The launch line `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} xhpl` invokes the HPL binary after adding its directory to PATH. |
| `BATCH.common.no_directive_comments` | major | **satisfied** | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | **satisfied** | All directives, paths, account, queue, and command values are concrete and contain no placeholder text. |
| `BATCH.common.queue_declared` | fatal | **satisfied** | It names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | **satisfied** | The requested `debug` queue is listed as an available Crux PBS Pro queue. |
| `BATCH.common.select_declared` | major | **satisfied** | It requests one Crux node using `#PBS -l select=1:system=crux`. |
| `BATCH.common.walltime_declared` | fatal | **satisfied** | It requests walltime with `#PBS -l walltime=00:30:00`. |
