# Verdicts — vllm@frontier, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `97a5909a740c`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | not_applicable | This PBS-specific account-directive requirement does not apply to Slurm. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script consistently uses Slurm `#SBATCH` directives and contains no PBS directives. |
| `BATCH.common.filesystems_declared` | fatal | not_applicable | This requirement applies only to PBS Pro; Frontier uses Slurm. |
| `BATCH.common.inputs_reachable` | major | satisfied | `bench.py` uses the supplied absolute model path and constructs its 50 prompts inline, so required inference inputs are reachable. |
| `BATCH.common.invokes_application` | fatal | satisfied | It launches the vLLM inference script with `srun /lustre/orion/csc708/scratch/hzheng/vllm-rocm-env/bin/python bench.py`. |
| `BATCH.common.no_directive_comments` | major | not_applicable | This requirement concerns trailing comments on PBS directives and applies only to PBS Pro. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, allocation, model name, prompts, and launch command are concrete; no placeholder tokens are present. |
| `BATCH.common.queue_declared` | fatal | not_applicable | This PBS-specific queue requirement does not apply to Frontier's Slurm scheduler. |
| `BATCH.common.queue_exists` | fatal | satisfied | The script requests `#SBATCH -q debug`, and `debug` is a Frontier queue/QOS named in the supplied catalog and site conventions. |
| `BATCH.common.select_declared` | major | not_applicable | This PBS-specific select directive requirement does not apply to Slurm. |
| `BATCH.common.walltime_declared` | fatal | not_applicable | This requirement applies only to PBS Pro; the script uses Slurm walltime syntax. |
| `BATCH.slurm.account_declared` | major | satisfied | The directive `#SBATCH -A CHM202` charges the requested project allocation. |
| `BATCH.slurm.no_directive_comments` | minor | satisfied | None of the `#SBATCH` directive lines has a trailing comment. |
| `BATCH.slurm.nodes_declared` | major | satisfied | The directive `#SBATCH -N 1` requests one node. |
| `BATCH.slurm.queue_or_qos_declared` | major | satisfied | The script correctly provides both Frontier partition and debug QOS directives: `#SBATCH -p batch` and `#SBATCH -q debug`. |
| `BATCH.slurm.srun_launcher` | major | satisfied | The final launch line begins with `srun`, as required for Frontier. |
| `BATCH.slurm.walltime_declared` | fatal | satisfied | The directive `#SBATCH -t 00:30:00` requests the required walltime. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | not_applicable | This PBS-specific account-directive requirement does not apply to Slurm. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script consistently uses Slurm `#SBATCH` directives and contains no PBS directives. |
| `BATCH.common.filesystems_declared` | fatal | not_applicable | This requirement applies only to PBS Pro, while Frontier uses Slurm. |
| `BATCH.common.inputs_reachable` | major | satisfied | `bench.py` constructs its 50 prompts inline and uses the concrete model path `/lustre/orion/csc708/scratch/hzheng/models/llama-3.1-8b`. |
| `BATCH.common.invokes_application` | fatal | satisfied | It launches the supplied vLLM environment Python binary with `srun /lustre/orion/csc708/scratch/hzheng/vllm-rocm-env/bin/python bench.py`. |
| `BATCH.common.no_directive_comments` | major | not_applicable | This requirement concerns trailing comments on PBS directives and the script contains no PBS directives. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, account, model, resource values, and generated prompt inputs are concrete; `%x` and `%j` are valid Slurm output filename substitutions. |
| `BATCH.common.queue_declared` | fatal | not_applicable | This PBS-specific queue-directive requirement does not apply to the Slurm target. |
| `BATCH.common.queue_exists` | fatal | satisfied | The script requests Frontier's valid batch partition and debug QOS via `#SBATCH -p batch` and `#SBATCH -q debug`. |
| `BATCH.common.select_declared` | major | not_applicable | This PBS Pro select-resource requirement does not apply to Slurm. |
| `BATCH.common.walltime_declared` | fatal | not_applicable | This requirement applies only to PBS Pro, while the submitted script uses Slurm directives. |
| `BATCH.slurm.account_declared` | major | satisfied | The script charges the requested project using `#SBATCH -A CHM202`. |
| `BATCH.slurm.no_directive_comments` | minor | satisfied | None of the `#SBATCH` directive lines has a trailing comment. |
| `BATCH.slurm.nodes_declared` | major | satisfied | The script requests one node with `#SBATCH --nodes=1`. |
| `BATCH.slurm.queue_or_qos_declared` | major | satisfied | The script selects `#SBATCH -p batch` and `#SBATCH -q debug`, matching Frontier's partition and debug-QOS convention. |
| `BATCH.slurm.srun_launcher` | major | satisfied | The application launch line begins with `srun` and does not use mpiexec or mpirun. |
| `BATCH.slurm.walltime_declared` | fatal | satisfied | The script requests walltime with `#SBATCH --time=00:30:00`. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | not_applicable | This PBS-specific account directive requirement does not apply to Slurm. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses Slurm `#SBATCH` directives exclusively and contains no PBS directives. |
| `BATCH.common.filesystems_declared` | fatal | not_applicable | This requirement applies only to PBS Pro, while Frontier uses Slurm. |
| `BATCH.common.inputs_reachable` | major | satisfied | `bench.py` embeds the concrete model path `/lustre/orion/csc708/scratch/hzheng/models/llama-3.1-8b` and generates its 50 prompts internally. |
| `BATCH.common.invokes_application` | fatal | satisfied | It launches the supplied vLLM environment Python binary with `srun /lustre/orion/csc708/scratch/hzheng/vllm-rocm-env/bin/python bench.py`. |
| `BATCH.common.no_directive_comments` | major | not_applicable | This requirement concerns trailing comments on PBS directives and does not apply to Slurm. |
| `BATCH.common.no_placeholders` | fatal | satisfied | The model path, allocation, working behavior, Python binary, and generated 50-prompt workload are concrete; no unsubstituted placeholder token is present. |
| `BATCH.common.queue_declared` | fatal | not_applicable | This PBS-specific queue directive requirement does not apply to Slurm. |
| `BATCH.common.queue_exists` | fatal | satisfied | The script requests `#SBATCH --qos=debug` and `#SBATCH -p batch`; both debug and batch are catalog-listed Frontier queues/QOS values. |
| `BATCH.common.select_declared` | major | not_applicable | This PBS-specific select directive requirement does not apply to Slurm. |
| `BATCH.common.walltime_declared` | fatal | not_applicable | This PBS-specific walltime directive requirement does not apply to Slurm. |
| `BATCH.slurm.account_declared` | major | satisfied | The script contains `#SBATCH -A CHM202`. |
| `BATCH.slurm.no_directive_comments` | minor | **violated** | Multiple `#SBATCH` directives have trailing comments, for example `#SBATCH --job-name=vllm_infer                     # a short job name`. |
| `BATCH.slurm.nodes_declared` | major | satisfied | The script contains `#SBATCH --nodes=1`. |
| `BATCH.slurm.queue_or_qos_declared` | major | satisfied | The script contains both `#SBATCH --qos=debug` and `#SBATCH -p batch`. |
| `BATCH.slurm.srun_launcher` | major | satisfied | The application launch line begins with `srun`. |
| `BATCH.slurm.walltime_declared` | fatal | satisfied | The script contains `#SBATCH --time=00:30:00`. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | not_applicable | This requirement applies only to PBS Pro, while Frontier uses Slurm. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses Slurm "#SBATCH" directives and contains no PBS directives. |
| `BATCH.common.filesystems_declared` | fatal | not_applicable | This requirement applies only to PBS Pro, while Frontier uses Slurm. |
| `BATCH.common.inputs_reachable` | major | **violated** | The required bench.py is never created: the unquoted Python block beginning "if __name__ == '__main__':" is interpreted as invalid Bash rather than being redirected into bench.py. |
| `BATCH.common.invokes_application` | fatal | **violated** | Although an srun line is present, the Python source is placed directly in the Bash script rather than written via a heredoc, causing Bash syntax failure before "srun ... python bench.py" can run. |
| `BATCH.common.no_directive_comments` | major | not_applicable | This requirement applies only to PBS "#PBS" directives, which are not used. |
| `BATCH.common.no_placeholders` | fatal | satisfied | The script uses concrete allocation, model, environment, and executable paths and contains no unresolved placeholder token. |
| `BATCH.common.queue_declared` | fatal | not_applicable | This requirement applies only to PBS Pro, while Frontier uses Slurm. |
| `BATCH.common.queue_exists` | fatal | satisfied | The script requests the existing Frontier partition and QOS with "#SBATCH -p batch" and "#SBATCH --qos=debug". |
| `BATCH.common.select_declared` | major | not_applicable | This requirement applies only to PBS Pro, while Frontier uses Slurm. |
| `BATCH.common.walltime_declared` | fatal | not_applicable | This requirement applies only to PBS Pro, while Frontier uses Slurm. |
| `BATCH.slurm.account_declared` | major | satisfied | The script charges the requested project with "#SBATCH -A CHM202". |
| `BATCH.slurm.no_directive_comments` | minor | satisfied | None of the #SBATCH directive lines has a trailing comment. |
| `BATCH.slurm.nodes_declared` | major | satisfied | The script requests one node with "#SBATCH --nodes=1". |
| `BATCH.slurm.queue_or_qos_declared` | major | satisfied | The script selects Frontier resources with "#SBATCH --qos=debug" and "#SBATCH -p batch". |
| `BATCH.slurm.srun_launcher` | major | satisfied | The launch command begins with "srun --cpu-bind=cores" and does not use mpiexec or mpirun. |
| `BATCH.slurm.walltime_declared` | fatal | **violated** | There is no "#SBATCH --time=" or "#SBATCH -t" directive requesting the required 00:30:00 walltime. |
