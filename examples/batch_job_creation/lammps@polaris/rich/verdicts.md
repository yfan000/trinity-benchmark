# Verdicts — lammps@polaris, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `73bf007d6891`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | Includes `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | Uses PBS Pro `#PBS` directives and contains no Slurm directives. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | Includes `#PBS -l filesystems=home:eagle`, covering the Eagle working directory and binary path. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `${PBS_O_WORKDIR}` and runs `lmp -in in.lammps`, matching the stated input file in the working directory. |
| `BATCH.common.invokes_application` | fatal | satisfied | Launches LAMMPS via `mpiexec -n ${NTOTRANKS} --ppn ${NRANKS_PER_NODE} lmp ...`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, project, queue, job name, and input filename are concrete; no placeholder markers are present. |
| `BATCH.common.queue_declared` | fatal | satisfied | Includes `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The requested queue is `debug`, which is listed as an available Polaris queue in the catalog. |
| `BATCH.common.select_declared` | major | satisfied | Includes `#PBS -l select=1:system=polaris`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | Includes `#PBS -l walltime=00:30:00`. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | The project allocation is declared with `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script consistently uses PBS Pro directives (`#PBS`) and PBS scheduler variables such as `$PBS_NODEFILE` and `${PBS_O_WORKDIR}`. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the stated Eagle working directory and required ALCF filesystem declaration. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to `${PBS_O_WORKDIR}`, the launch explicitly supplies `-in in.lammps`, which is the input file stated to exist in the working directory. |
| `BATCH.common.invokes_application` | fatal | satisfied | The script launches LAMMPS through `mpiexec ... lmp -in in.lammps -k on g 4 -sf kk -pk kokkos` after placing the supplied LAMMPS binary directory on `PATH`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines contains a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All directives, paths, allocation, queue, and input filename are concrete; no placeholder tokens or replacement instructions are present. |
| `BATCH.common.queue_declared` | fatal | satisfied | The script names the queue with `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | `debug` is a catalog-listed Polaris PBS queue and the one requested by the prompt. |
| `BATCH.common.select_declared` | major | satisfied | The node request is stated as `#PBS -l select=1:system=polaris`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | The script requests walltime with `#PBS -l walltime=00:30:00`. |

## gpt-oss-120b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | It supplies the project account through `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script consistently uses PBS Pro directives (`#PBS`) and no conflicting scheduler dialect. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the Eagle working, log, and software paths. |
| `BATCH.common.inputs_reachable` | major | satisfied | After `cd ${PBS_O_WORKDIR}`, the launch command explicitly reads the supplied `in.lammps` input file. |
| `BATCH.common.invokes_application` | fatal | satisfied | It launches LAMMPS with `mpiexec -n 4 --ppn 4 lmp -in in.lammps -k on g 4 -sf kk -pk kokkos`. |
| `BATCH.common.no_directive_comments` | major | **violated** | Several PBS directives have trailing comments, e.g. `#PBS -N lammps_500k                      # job name` and the `#PBS -o`/`#PBS -e` lines. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, account, queue, and command arguments are concretely specified; no placeholder token is present. |
| `BATCH.common.queue_declared` | fatal | satisfied | It names the queue using `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The requested `debug` queue exists in the Polaris catalog. |
| `BATCH.common.select_declared` | major | satisfied | It requests one Polaris node with `#PBS -l select=1:system=polaris`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | It requests walltime with `#PBS -l walltime=00:30:00`. |

## llama-3.1-8b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | satisfied | It includes `#PBS -A TrinityAgent`. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses PBS Pro directives (`#PBS`) and contains no Slurm directives. |
| `BATCH.common.filesystems_declared` | fatal | satisfied | The script declares `#PBS -l filesystems=home:eagle`, covering the `/eagle/...` working, software, and output paths. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to the PBS submission directory, it explicitly passes the stated existing input file as `-in in.lammps`. |
| `BATCH.common.invokes_application` | fatal | satisfied | The script launches LAMMPS via `mpiexec ... lmp -in in.lammps -k on g 4 -sf kk -pk kokkos`. |
| `BATCH.common.no_directive_comments` | major | satisfied | None of the `#PBS` directive lines has a trailing comment. |
| `BATCH.common.no_placeholders` | fatal | satisfied | The script uses concrete project, working-directory, output, and executable-path values and contains no placeholder tokens. |
| `BATCH.common.queue_declared` | fatal | satisfied | It includes `#PBS -q debug`. |
| `BATCH.common.queue_exists` | fatal | satisfied | The selected `debug` queue is listed in the Polaris catalog. |
| `BATCH.common.select_declared` | major | satisfied | It includes `#PBS -l select=1:system=polaris`. |
| `BATCH.common.walltime_declared` | fatal | satisfied | It includes `#PBS -l walltime=0:30:00`. |
