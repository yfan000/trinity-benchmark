#!/usr/bin/env python3
"""Site conventions and verified worked examples supplied to the benchmark prompts.

These are facts an agent with no tools cannot discover. Withholding them tests recall of
what ALCF documents rather than the ability to do the subtask, which is what we measure.
Each was validated on a 10-sample preview before being folded in here:

  Batch job creation   6% -> 53% fully correct  (conventions + worked example + account)
  Input preparation   25% -> 33% fully correct  (verified example deck)

The worked examples deliberately describe a DIFFERENT physical system from the one under
test, so they teach grammar without carrying the answer.
"""
from __future__ import annotations
from pathlib import Path

EX = Path(__file__).resolve().parent.parent / "results" / "skills" / "trinity" / "examples"

CONVENTIONS = {
 "PBS Pro": """- Directives are NOT shell-expanded: never use $VAR or ${VAR} in #PBS -o/-e paths.
- Never put a trailing comment on a #PBS line; PBS reads it as another directive.
- Job arrays use `#PBS -J 1-N` and the index variable `$PBS_ARRAY_INDEX` (NOT -t / $PBS_ARRAYID).
- Node list is `$PBS_NODEFILE`; node count is `wc -l < $PBS_NODEFILE` (there is no $PBS_NNODES).
- `cd ${PBS_O_WORKDIR}` in the script body, not in a directive.
- ALCF requires `#PBS -l filesystems=<list>` naming every filesystem the job touches
  (Polaris/Crux/Sophia: home:eagle - Aurora: home:flare) or the job is rejected or hangs.
- An account is required: `#PBS -A <project>`.
- Nodes are allocated exclusively; ncpus in select= describes the whole node.
- Any output directory referenced by -o/-e must already exist.""",
 "Slurm": """- Perlmutter selects the queue by QOS: `#SBATCH -q debug` (there is no --partition=debug).
- GPU jobs require the architecture constraint `#SBATCH -C gpu`.
- The account carries a `_g` suffix for GPU allocations: `#SBATCH -A <project>_g`.
- Job arrays use `#SBATCH --array=1-N` with `$SLURM_ARRAY_TASK_ID`.
- Launch with `srun`, not mpiexec.
- Any output directory referenced by -o/-e must already exist.""",
}

# Withholding the account produced a contradiction we measured: the model correctly wrote a
# placeholder, and the judge marked the script unsubmittable. Supplying it removes a defect
# that was never about the model's competence.
ACCOUNTS = {"polaris": "TrinityAgent", "aurora": "TrinityAgent", "sunspot": "TrinityAgent",
            "crux": "TrinityAgent", "sophia": "TrinityAgent",
            "perlmutter": "m4553", "frontier": "CHM202"}


def worked_script(scheduler: str) -> str:
    """A complete, correct batch script for a DIFFERENT application on the same scheduler.

    One per scheduler family, so a Slurm sample is not handicapped against a PBS one — the
    example carries most of the Batch-job-creation gain, and giving it to only 8 of 10
    anchors would put the scheduler split into the score rather than into the measurement.
    """
    f = EX / ("_pbs_script.txt" if scheduler == "PBS Pro" else "_slurm_script.txt")
    return f.read_text().strip() if f.exists() else ""


def worked_deck(app: str) -> str:
    """A real input deck from the application's own repository, for a different system."""
    f = EX / f"{app}.txt"
    return f.read_text().strip() if f.exists() else ""


def account(system: str) -> str:
    return ACCOUNTS.get(system, "TrinityAgent")
