# Verdicts — alphafold@perlmutter, base arm

Majority across three judge replicates, judged by `gpt56terra` under rubric **r27**, scored under **r28** (sha `97a5909a740c`) — a rule retired since the grades were collected is listed but no longer counted. A rule marked *flipped across runs* did not get the same verdict all three times.

## nemotron-3-ultra — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | not_applicable | This requirement applies only to PBS Pro; the script uses the Slurm account directive. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script exclusively uses Slurm '#SBATCH' directives and an 'srun' launcher. |
| `BATCH.common.filesystems_declared` | fatal | not_applicable | This requirement applies only to PBS Pro, while Perlmutter uses Slurm. |
| `BATCH.common.inputs_reachable` | major | satisfied | After 'cd $SLURM_SUBMIT_DIR', the command explicitly supplies '--fasta_paths=run.fasta', which is stated to be present in the working directory. |
| `BATCH.common.invokes_application` | fatal | satisfied | It launches AlphaFold with 'srun -n 1 -G 1 python run_alphafold.py' and the supplied AlphaFold arguments. |
| `BATCH.common.no_directive_comments` | major | not_applicable | This restriction concerns trailing comments on PBS '#PBS' directives, and the script contains no PBS directives. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, allocation values, filenames, and command arguments are concrete; it uses 'run.fasta' rather than the example placeholder input filename. |
| `BATCH.common.queue_declared` | fatal | not_applicable | This requirement applies only to PBS Pro; Perlmutter queue selection is via Slurm QOS. |
| `BATCH.common.queue_exists` | fatal | satisfied | The script requests '#SBATCH -q debug', and 'debug' is a listed Perlmutter queue/QOS. |
| `BATCH.common.select_declared` | major | not_applicable | This requirement applies only to PBS Pro, not Slurm. |
| `BATCH.common.walltime_declared` | fatal | not_applicable | This requirement applies only to PBS Pro; the script correctly uses Slurm walltime syntax. |
| `BATCH.slurm.account_declared` | major | satisfied | The script includes '#SBATCH -A m4553_g', with the required GPU allocation suffix. |
| `BATCH.slurm.no_directive_comments` | minor | satisfied | None of the '#SBATCH' directive lines contains a trailing comment. |
| `BATCH.slurm.nodes_declared` | major | satisfied | The script includes '#SBATCH --nodes=1'. |
| `BATCH.slurm.queue_or_qos_declared` | major | satisfied | The script selects the Perlmutter QOS using '#SBATCH -q debug'. |
| `BATCH.slurm.srun_launcher` | major | satisfied | The application is launched with an 'srun' command, not mpiexec or mpirun. |
| `BATCH.slurm.walltime_declared` | fatal | satisfied | The script includes '#SBATCH --time=02:00:00'. |

## gemma-4-31b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | not_applicable | This requirement concerns PBS account syntax and does not apply to Slurm. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses Slurm `#SBATCH` directives throughout and contains no PBS directives. |
| `BATCH.common.filesystems_declared` | fatal | not_applicable | This requirement applies only to PBS Pro, while Perlmutter uses Slurm. |
| `BATCH.common.inputs_reachable` | major | satisfied | After `cd $SLURM_SUBMIT_DIR`, the launcher explicitly passes `--fasta_paths=run.fasta`, matching the supplied input filename. |
| `BATCH.common.invokes_application` | fatal | satisfied | The `srun` command invokes the AlphaFold application as `/global/cfs/cdirs/dasrepo/hzheng/software/perlmutter/alphafold_venv_v3/bin/python run_alphafold.py`. |
| `BATCH.common.no_directive_comments` | major | not_applicable | This requirement applies only to trailing comments on PBS `#PBS` directives. |
| `BATCH.common.no_placeholders` | fatal | satisfied | The script supplies concrete allocation, input, database, executable, and output values with no unsubstituted placeholder token such as `<...>` or `/path/to/`. |
| `BATCH.common.queue_declared` | fatal | not_applicable | This PBS-specific queue directive requirement does not apply to the Slurm target. |
| `BATCH.common.queue_exists` | fatal | satisfied | The script requests `#SBATCH -q debug`, and `debug` is listed among the Perlmutter queues. |
| `BATCH.common.select_declared` | major | not_applicable | This PBS-specific select directive requirement does not apply to Slurm. |
| `BATCH.common.walltime_declared` | fatal | not_applicable | This requirement applies only to PBS Pro; the script correctly uses Slurm time syntax instead. |
| `BATCH.slurm.account_declared` | major | satisfied | The script declares the GPU allocation account with `#SBATCH -A m4553_g`. |
| `BATCH.slurm.no_directive_comments` | minor | satisfied | None of the `#SBATCH` directive lines has a trailing comment. |
| `BATCH.slurm.nodes_declared` | major | satisfied | The script states the requested node count with `#SBATCH --nodes=1`. |
| `BATCH.slurm.queue_or_qos_declared` | major | satisfied | The script selects the Perlmutter QOS using `#SBATCH -q debug`. |
| `BATCH.slurm.srun_launcher` | major | satisfied | The application is launched with a line beginning `srun -n 1 -G 1`. |
| `BATCH.slurm.walltime_declared` | fatal | satisfied | The script requests walltime with `#SBATCH -t 02:00:00`. |

## gpt-oss-120b — PASS

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | not_applicable | This PBS-specific account-directive requirement does not apply to the Slurm target. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses Slurm `#SBATCH` directives and contains no PBS directives. |
| `BATCH.common.filesystems_declared` | fatal | not_applicable | This requirement applies only to PBS Pro, while Perlmutter uses Slurm. |
| `BATCH.common.inputs_reachable` | major | satisfied | The script changes to `$SLURM_SUBMIT_DIR` and passes `--fasta_paths=run.fasta`, making the stated input reachable when submitted from the working directory. |
| `BATCH.common.invokes_application` | fatal | satisfied | The `srun -n 4 -G 4 python run_alphafold.py ...` command launches the AlphaFold application. |
| `BATCH.common.no_directive_comments` | major | not_applicable | This requirement concerns trailing comments on PBS directives and does not apply to Slurm. |
| `BATCH.common.no_placeholders` | fatal | satisfied ⚠︎ flipped across runs | The script uses concrete allocation, database, input, and output values and contains no unsubstituted placeholder token. |
| `BATCH.common.queue_declared` | fatal | not_applicable | This PBS-specific queue-directive requirement does not apply to the Slurm target. |
| `BATCH.common.queue_exists` | fatal | satisfied | The script requests `#SBATCH --qos=debug`, and `debug` is a listed Perlmutter queue/QOS. |
| `BATCH.common.select_declared` | major | not_applicable | This PBS-specific select directive requirement does not apply to the Slurm target. |
| `BATCH.common.walltime_declared` | fatal | not_applicable | This PBS-specific walltime requirement does not apply to the Slurm target. |
| `BATCH.slurm.account_declared` | major | satisfied | The script contains `#SBATCH -A m4553_g`. |
| `BATCH.slurm.no_directive_comments` | minor | **violated** | Several Slurm directives have trailing comments, e.g. `#SBATCH --job-name=alphafold_ubiquitin          # descriptive name`. |
| `BATCH.slurm.nodes_declared` | major | satisfied | The script contains `#SBATCH --nodes=1`. |
| `BATCH.slurm.queue_or_qos_declared` | major | satisfied | The script contains `#SBATCH --qos=debug`. |
| `BATCH.slurm.srun_launcher` | major | satisfied | The application is launched with `srun` rather than `mpiexec` or `mpirun`. |
| `BATCH.slurm.walltime_declared` | fatal | satisfied | The script contains `#SBATCH -t 02:00:00`. |

## llama-3.1-8b — FAIL

| requirement | severity | verdict | judge's evidence |
|---|---|---|---|
| `BATCH.common.account_declared` | major | not_applicable | This PBS Pro-only requirement does not apply to the Slurm target system. |
| `BATCH.common.correct_dialect` | fatal | satisfied | The script uses Slurm `#SBATCH` directives exclusively and contains no PBS directives. |
| `BATCH.common.filesystems_declared` | fatal | not_applicable | This PBS Pro-only requirement does not apply to the Slurm target system. |
| `BATCH.common.inputs_reachable` | major | satisfied | After changing to `/pscratch/sd/b/bkowalski/alphafold_run`, the command explicitly supplies `--fasta_paths=run.fasta`, which is the stated input file in that directory. |
| `BATCH.common.invokes_application` | fatal | **violated** | The launcher uses `python /global/.../bin/python run_alphafold.py`; this asks the activated environment's `python` to execute the Python interpreter binary as a script, rather than executing `run_alphafold.py` with that binary or using `python run_alphafold.py`. |
| `BATCH.common.no_directive_comments` | major | not_applicable | This requirement concerns trailing comments on PBS directives and does not apply to Slurm. |
| `BATCH.common.no_placeholders` | fatal | satisfied | All paths, allocation names, input filenames, and output paths are concrete; no placeholder token is present. |
| `BATCH.common.queue_declared` | fatal | not_applicable | This PBS Pro-only requirement does not apply to the Slurm target system. |
| `BATCH.common.queue_exists` | fatal | satisfied | The script selects `#SBATCH --qos=debug`, and `debug` is a listed Perlmutter queue/QOS. |
| `BATCH.common.select_declared` | major | not_applicable | This PBS Pro-only requirement does not apply to the Slurm target system. |
| `BATCH.common.walltime_declared` | fatal | not_applicable | This PBS Pro-only requirement does not apply to the Slurm target system. |
| `BATCH.slurm.account_declared` | major | satisfied | The script includes both `#SBATCH --account=m4553_g` and `#SBATCH -A m4553_g`. |
| `BATCH.slurm.no_directive_comments` | minor | satisfied | None of the `#SBATCH` directive lines contains a trailing comment. |
| `BATCH.slurm.nodes_declared` | major | satisfied | The script declares `#SBATCH --nodes=1`. |
| `BATCH.slurm.queue_or_qos_declared` | major | satisfied | The script declares `#SBATCH --qos=debug`. |
| `BATCH.slurm.srun_launcher` | major | satisfied | The application launch line begins with `srun -n 4`. |
| `BATCH.slurm.walltime_declared` | fatal | **violated** | No `#SBATCH --time=...` or `#SBATCH -t ...` directive is present. |
