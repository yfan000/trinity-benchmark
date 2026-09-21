# Verdicts — vllm@frontier, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `97a5909a740c`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | not_applicable ⚠︎ flipped across runs | This requirement applies only to PBS Pro, while Frontier uses Slurm. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses Slurm `#SBATCH` directives exclusively and contains no PBS directives. |
| `BATCH.common.filesystems_declared` | fatal | not_applicable | This requirement applies only to PBS Pro, while Frontier uses Slurm. |
| `BATCH.common.inputs_reachable` | major | satisfied | `bench.py` is created inline before launch and references the model using the supplied absolute path `/lustre/orion/csc708/scratch/hzheng/models/llama-3.1-8b`. |
| `BATCH.common.invokes_application` | fatal | satisfied | It launches the specified vLLM environment Python binary through `srun /lustre/orion/csc708/scratch/hzheng/vllm-rocm-env/bin/python bench.py`. |
| `BATCH.common.no_directive_comments` | major | not_applicable | This requirement applies only to PBS `#PBS` directives, which are not used on this Slurm system. |
| `BATCH.common.no_placeholders` | fatal | satisfied | The script uses concrete allocation, model, environment, executable, and script names without unsubstituted placeholder paths or TODO markers. |
| `BATCH.common.queue_declared` | fatal | not_applicable | This requirement applies only to PBS Pro, while Frontier uses Slurm. |
| `BATCH.common.queue_exists` | fatal | satisfied | The script requests Frontier's existing batch partition and debug QOS via `#SBATCH -p batch` and `#SBATCH -q debug`. |
| `BATCH.common.select_declared` | major | not_applicable | This requirement applies only to PBS Pro, while Frontier uses Slurm. |
| `BATCH.common.walltime_declared` | fatal | not_applicable | This requirement applies only to PBS Pro, while Frontier uses Slurm. |
| `BATCH.slurm.account_declared` | major | satisfied | The script charges the requested project using `#SBATCH -A CHM202`. |
| `BATCH.slurm.no_directive_comments` | minor | satisfied | None of the `#SBATCH` directive lines contains a trailing comment. |
| `BATCH.slurm.nodes_declared` | major | satisfied | The script requests one node with `#SBATCH --nodes=1`. |
| `BATCH.slurm.queue_or_qos_declared` | major | satisfied | The script selects both `#SBATCH -p batch` and `#SBATCH -q debug`. |
| `BATCH.slurm.srun_launcher` | major | satisfied | The application is launched using an `srun` command rather than mpiexec or mpirun. |
| `BATCH.slurm.walltime_declared` | fatal | satisfied | The script requests walltime with `#SBATCH -t 00:30:00`. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | not_applicable | This PBS-specific account-directive requirement does not apply to Slurm. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script consistently uses Slurm `#SBATCH` directives and contains no PBS directives. |
| `BATCH.common.filesystems_declared` | fatal | not_applicable | This requirement applies only to PBS Pro, while Frontier uses Slurm. |
| `BATCH.common.inputs_reachable` | major | satisfied | `bench.py` is written inline and references the concrete model path `/lustre/orion/csc708/scratch/hzheng/models/llama-3.1-8b`; its 50 prompts are generated within the script. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launch line `srun /lustre/orion/csc708/scratch/hzheng/vllm-rocm-env/bin/python bench.py` runs the specified vLLM Python workload. |
| `BATCH.common.no_directive_comments` | major | not_applicable | This requirement applies only to PBS `#PBS` directives. |
| `BATCH.common.no_placeholders` | fatal | satisfied | The script supplies concrete model, environment, working-directory, account, and executable paths; `%x` and `%j` are valid Slurm output filename substitutions rather than unsubstituted placeholders. |
| `BATCH.common.queue_declared` | fatal | not_applicable | This PBS-specific requirement does not apply to the Slurm target system. |
| `BATCH.common.queue_exists` | fatal | satisfied | The script requests `#SBATCH -p batch` and `#SBATCH -q debug`; both batch and debug are defined Frontier scheduler options, with debug specified by the prompt as a QOS. |
| `BATCH.common.select_declared` | major | not_applicable | This PBS-specific node-selection requirement does not apply to Slurm. |
| `BATCH.common.walltime_declared` | fatal | not_applicable | This requirement applies only to PBS Pro, while the script correctly uses a Slurm walltime directive. |
| `BATCH.slurm.account_declared` | major | satisfied | The script includes `#SBATCH -A CHM202`. |
| `BATCH.slurm.no_directive_comments` | minor | satisfied | None of the `#SBATCH` directive lines has a trailing comment. |
| `BATCH.slurm.nodes_declared` | major | satisfied | The script includes `#SBATCH --nodes=1`. |
| `BATCH.slurm.queue_or_qos_declared` | major | satisfied | The script includes both `#SBATCH -p batch` and `#SBATCH -q debug`, matching Frontier's partition and debug-QOS convention. |
| `BATCH.slurm.srun_launcher` | major | satisfied | The application is launched with `srun`, not mpiexec or mpirun. |
| `BATCH.slurm.walltime_declared` | fatal | satisfied | The script includes `#SBATCH --time=00:30:00`. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | not_applicable | This requirement applies only to PBS Pro, while Frontier uses Slurm. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses Slurm `#SBATCH` directives only, matching Frontier's Slurm scheduler. |
| `BATCH.common.filesystems_declared` | fatal | not_applicable | This requirement applies only to PBS Pro, while Frontier uses Slurm. |
| `BATCH.common.inputs_reachable` | major | satisfied | `bench.py` is created inline before launch and references the model through the concrete absolute path `/lustre/orion/csc708/scratch/hzheng/models/llama-3.1-8b`. |
| `BATCH.common.invokes_application` | fatal | satisfied | The launch command is `srun /lustre/orion/csc708/scratch/hzheng/vllm-rocm-env/bin/python bench.py`, which runs the supplied application Python binary. |
| `BATCH.common.no_directive_comments` | major | not_applicable | This requirement concerns trailing comments on PBS `#PBS` directives and does not apply to Slurm. |
| `BATCH.common.no_placeholders` | fatal | satisfied | The model path, environment path, allocation, prompt list, and launch command are concrete; the generated 50-prompt list is executable as written. |
| `BATCH.common.queue_declared` | fatal | not_applicable | This requirement applies only to PBS Pro, while Frontier uses Slurm. |
| `BATCH.common.queue_exists` | fatal | satisfied | The script requests `#SBATCH --qos=debug` and `#SBATCH --partition=batch`; both debug and batch are listed Frontier queues. |
| `BATCH.common.select_declared` | major | not_applicable | This requirement applies only to PBS Pro, while Frontier uses Slurm. |
| `BATCH.common.walltime_declared` | fatal | not_applicable | This requirement applies only to PBS Pro, while Frontier uses Slurm. |
| `BATCH.slurm.account_declared` | major | satisfied | The script includes `#SBATCH -A CHM202`. |
| `BATCH.slurm.no_directive_comments` | minor | **violated** | Multiple `#SBATCH` lines have trailing comments, for example `#SBATCH --time=00:30:00                  # wall-clock limit`. |
| `BATCH.slurm.nodes_declared` | major | satisfied | The script includes `#SBATCH --nodes=1`. |
| `BATCH.slurm.queue_or_qos_declared` | major | satisfied | The script includes both `#SBATCH --qos=debug` and `#SBATCH --partition=batch`. |
| `BATCH.slurm.srun_launcher` | major | satisfied | The application is launched with an `srun` command rather than mpiexec or mpirun. |
| `BATCH.slurm.walltime_declared` | fatal | satisfied | The script includes `#SBATCH --time=00:30:00`. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | not_applicable | This requirement applies only to PBS Pro; Frontier uses Slurm. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script consistently uses Slurm `#SBATCH` directives and no PBS directives. |
| `BATCH.common.filesystems_declared` | fatal | not_applicable | This requirement applies only to PBS Pro; Frontier uses Slurm. |
| `BATCH.common.inputs_reachable` | major | satisfied | The inline program specifies the supplied absolute model path `/lustre/orion/csc708/scratch/hzheng/models/llama-3.1-8b`. |
| `BATCH.common.invokes_application` | fatal | satisfied | It launches the configured vLLM environment Python binary with `srun /lustre/orion/csc708/scratch/hzheng/vllm-rocm-env/bin/python bench.py`. |
| `BATCH.common.no_directive_comments` | major | not_applicable | This requirement applies only to PBS `#PBS` directive lines. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, allocation, model, prompt count, and launch command are concrete; no placeholder tokens are present. |
| `BATCH.common.queue_declared` | fatal | not_applicable | This requirement applies only to PBS Pro; Frontier uses Slurm. |
| `BATCH.common.queue_exists` | fatal | satisfied | The script requests `#SBATCH -p batch` and `#SBATCH --qos=debug`, both of which are listed for Frontier. |
| `BATCH.common.select_declared` | major | not_applicable | This requirement applies only to PBS Pro; Frontier uses Slurm. |
| `BATCH.common.walltime_declared` | fatal | not_applicable | This requirement applies only to PBS Pro; Frontier uses Slurm. |
| `BATCH.slurm.account_declared` | major | satisfied | The script charges the requested project with `#SBATCH -A CHM202`. |
| `BATCH.slurm.no_directive_comments` | minor | satisfied | None of the `#SBATCH` directive lines contains a trailing comment. |
| `BATCH.slurm.nodes_declared` | major | satisfied | The script requests one node with `#SBATCH --nodes=1`. |
| `BATCH.slurm.queue_or_qos_declared` | major | satisfied | The script selects both the Frontier partition and debug QOS with `#SBATCH -p batch` and `#SBATCH --qos=debug`. |
| `BATCH.slurm.srun_launcher` | major | satisfied | The application is launched through a line beginning with `srun`. |
| `BATCH.slurm.walltime_declared` | fatal | **violated** | There is no `#SBATCH --time=...` or `#SBATCH -t ...` directive, despite the required walltime being 00:30:00. |
