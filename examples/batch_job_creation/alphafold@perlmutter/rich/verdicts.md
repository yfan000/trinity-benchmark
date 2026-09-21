# Verdicts — alphafold@perlmutter, rich arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `97a5909a740c`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | not_applicable | This PBS `-A` directive requirement is excluded because the target scheduler is Slurm. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script consistently uses Slurm `#SBATCH` directives and contains no PBS directives. |
| `BATCH.common.filesystems_declared` | fatal | not_applicable | This requirement applies only to PBS Pro; Perlmutter uses Slurm. |
| `BATCH.common.inputs_reachable` | major | satisfied | After `cd ${SLURM_SUBMIT_DIR}`, the command explicitly passes `--fasta_paths=run.fasta`. |
| `BATCH.common.invokes_application` | fatal | satisfied | It launches AlphaFold with `srun -n 1 -G 1 python run_alphafold.py` and the supplied AlphaFold arguments. |
| `BATCH.common.no_directive_comments` | major | not_applicable | This requirement concerns trailing comments on PBS directives, but the script uses Slurm. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All application paths, allocation, input filename, and working-directory paths are concrete; `%x` and `%j` are valid Slurm output substitutions. |
| `BATCH.common.queue_declared` | fatal | not_applicable | This PBS `-q` requirement is excluded because the target scheduler is Slurm. |
| `BATCH.common.queue_exists` | fatal | satisfied | The script selects `#SBATCH --qos=debug`, and `debug` is a listed Perlmutter queue/QOS. |
| `BATCH.common.select_declared` | major | not_applicable | This PBS `-l select=` requirement is excluded because the target scheduler is Slurm. |
| `BATCH.common.walltime_declared` | fatal | not_applicable | This PBS `-l walltime=` requirement is excluded because the target scheduler is Slurm. |
| `BATCH.slurm.account_declared` | major | satisfied | The script charges the GPU allocation with `#SBATCH -A m4553_g`. |
| `BATCH.slurm.no_directive_comments` | minor | satisfied | None of the `#SBATCH` directive lines has a trailing comment. |
| `BATCH.slurm.nodes_declared` | major | satisfied | The script requests one node with `#SBATCH --nodes=1`. |
| `BATCH.slurm.queue_or_qos_declared` | major | satisfied | The script selects the Perlmutter QOS with `#SBATCH --qos=debug`. |
| `BATCH.slurm.srun_launcher` | major | satisfied | The application is launched with an `srun` command rather than `mpiexec` or `mpirun`. |
| `BATCH.slurm.walltime_declared` | fatal | satisfied | The script requests walltime with `#SBATCH --time=02:00:00`. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | not_applicable | This PBS-specific account-directive requirement does not apply to Slurm. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script exclusively uses Slurm `#SBATCH` directives for the Slurm-based Perlmutter system. |
| `BATCH.common.filesystems_declared` | fatal | not_applicable | This requirement applies only to PBS Pro, while Perlmutter uses Slurm. |
| `BATCH.common.inputs_reachable` | major | satisfied | After `cd $SLURM_SUBMIT_DIR`, the command explicitly passes `--fasta_paths=run.fasta`, matching the supplied input filename. |
| `BATCH.common.invokes_application` | fatal | satisfied | The `srun -n 1 -G 1 .../bin/python run_alphafold.py` line launches the AlphaFold application. |
| `BATCH.common.no_directive_comments` | major | not_applicable | This requirement concerns trailing comments on PBS directives, and the script contains no PBS directives. |
| `BATCH.common.no_placeholders` | fatal | satisfied | The script uses concrete allocation, database, binary, input, and output values and contains no unresolved placeholder tokens. |
| `BATCH.common.queue_declared` | fatal | not_applicable | This PBS-specific queue-directive requirement does not apply to the Slurm target. |
| `BATCH.common.queue_exists` | fatal | satisfied | The script requests `#SBATCH -q debug`, and `debug` is a listed Perlmutter queue/QOS. |
| `BATCH.common.select_declared` | major | not_applicable | This PBS Pro select-resource requirement does not apply to Slurm. |
| `BATCH.common.walltime_declared` | fatal | not_applicable | This requirement applies only to PBS Pro; the script correctly uses a Slurm time directive instead. |
| `BATCH.slurm.account_declared` | major | satisfied | The script declares the GPU allocation account with `#SBATCH -A m4553_g`. |
| `BATCH.slurm.no_directive_comments` | minor | satisfied | None of the `#SBATCH` directive lines has a trailing comment. |
| `BATCH.slurm.nodes_declared` | major | satisfied | The script states `#SBATCH --nodes=1`. |
| `BATCH.slurm.queue_or_qos_declared` | major | satisfied | The script selects the Perlmutter QOS with `#SBATCH -q debug`. |
| `BATCH.slurm.srun_launcher` | major | satisfied | The application is launched with `srun -n 1 -G 1`. |
| `BATCH.slurm.walltime_declared` | fatal | satisfied | The script requests `#SBATCH --time=02:00:00`. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | not_applicable | This is a PBS Pro account-directive requirement; Slurm account declaration is assessed separately. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script consistently uses Slurm `#SBATCH` directives and `srun`, with no PBS directives. |
| `BATCH.common.filesystems_declared` | fatal | not_applicable | This requirement applies only to PBS Pro, while Perlmutter uses Slurm. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to `${SLURM_SUBMIT_DIR}`, it passes `--fasta_paths=run.fasta`, matching the stated input file in the working directory. |
| `BATCH.common.invokes_application` | fatal | satisfied | It launches `python run_alphafold.py` through `srun`. |
| `BATCH.common.no_directive_comments` | major | not_applicable | This requirement concerns trailing comments on PBS `#PBS` directives and does not apply to Slurm. |
| `BATCH.common.no_placeholders` | fatal | satisfied ⚠︎ flipped across runs | The script uses concrete allocation, paths, input filename `run.fasta`, and database locations without placeholder tokens. |
| `BATCH.common.queue_declared` | fatal | not_applicable | This is a PBS Pro `-q` requirement; queue selection on this Slurm system is via QOS. |
| `BATCH.common.queue_exists` | fatal | satisfied | The script selects `#SBATCH --qos=debug`, and `debug` is a listed Perlmutter queue/QOS. |
| `BATCH.common.select_declared` | major | not_applicable | This is a PBS Pro `-l select=` requirement and does not apply to Slurm. |
| `BATCH.common.walltime_declared` | fatal | not_applicable | This is a PBS Pro `-l walltime=` requirement; the submitted script uses Slurm. |
| `BATCH.slurm.account_declared` | major | satisfied | The directive `#SBATCH -A m4553_g` declares the GPU project allocation. |
| `BATCH.slurm.no_directive_comments` | minor | **violated** | Multiple `#SBATCH` lines have trailing comments, e.g. `#SBATCH --job-name=alphafold_ubiquitin                 # descriptive name`. |
| `BATCH.slurm.nodes_declared` | major | satisfied | The directive `#SBATCH --nodes=1` declares the requested node count. |
| `BATCH.slurm.queue_or_qos_declared` | major | satisfied | The directive `#SBATCH --qos=debug` selects the Perlmutter debug QOS. |
| `BATCH.slurm.srun_launcher` | major | satisfied | The application is launched with `srun -n 4 -G 4 python run_alphafold.py ...`. |
| `BATCH.slurm.walltime_declared` | fatal | satisfied | The directive `#SBATCH --time=02:00:00` requests the required walltime. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | not_applicable | This PBS Pro account-directive requirement is excluded because the target scheduler is Slurm. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script consistently uses Slurm `#SBATCH` directives and `srun`, with no PBS directives. |
| `BATCH.common.filesystems_declared` | fatal | not_applicable | This PBS Pro `#PBS -l filesystems=` requirement is excluded because Perlmutter uses Slurm. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `/pscratch/sd/b/bkowalski/alphafold_run` and passes `--fasta_paths=run.fasta`, which is the supplied input in that directory. |
| `BATCH.common.invokes_application` | fatal | **violated** | The launch line is `srun -n 1 -G 1 python /global/.../bin/python run_alphafold.py`; this asks the conda `python` interpreter to execute the Python executable binary as a script, rather than invoking `/global/.../bin/python run_alphafold.py`. |
| `BATCH.common.no_directive_comments` | major | not_applicable | This requirement concerns trailing comments on PBS `#PBS` directives, which are not used on this Slurm job. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, account values, and input names are concrete; no placeholder tokens or unsubstituted example filename remain. |
| `BATCH.common.queue_declared` | fatal | not_applicable | This PBS Pro `#PBS -q` requirement is excluded because the target scheduler is Slurm. |
| `BATCH.common.queue_exists` | fatal | satisfied | The script requests `#SBATCH --qos=debug`, and `debug` is a listed Perlmutter queue/QOS. |
| `BATCH.common.select_declared` | major | not_applicable | This PBS Pro `select=` requirement is excluded because the target scheduler is Slurm. |
| `BATCH.common.walltime_declared` | fatal | not_applicable | This PBS Pro walltime requirement is excluded because the target scheduler is Slurm. |
| `BATCH.slurm.account_declared` | major | satisfied | The script declares `#SBATCH -A m4553_g`. |
| `BATCH.slurm.no_directive_comments` | minor | satisfied | None of the `#SBATCH` directive lines has a trailing comment. |
| `BATCH.slurm.nodes_declared` | major | satisfied | The script declares `#SBATCH --nodes=1`. |
| `BATCH.slurm.queue_or_qos_declared` | major | satisfied | The script declares `#SBATCH --qos=debug`. |
| `BATCH.slurm.srun_launcher` | major | satisfied | The application is launched through a line beginning `srun -n 1 -G 1`. |
| `BATCH.slurm.walltime_declared` | fatal | **violated** | There is no `#SBATCH --time=...` or `#SBATCH -t ...` directive, despite the decided walltime being `02:00:00`. |
