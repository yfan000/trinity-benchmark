#!/usr/bin/env python3
"""Construct-validity checks for the HPC mapping.

Same idea as check_validity.py: state what the mapping *should* show based on what each task
means, then test it. Predictions are derived from the task definitions in hpc_task_spec.py.

Predictions are framing-specific, and that split was itself a finding. The first version of
this file predicted "Job submission requires Instruction/format following" and it came back
at 0% for advisory — because an advisory instance asks the model to *explain* a submission,
which carries no output constraint at all. The prediction was not wrong about HPC; it was
wrong about which framing tests it. Under execution framing the same prediction holds at 88%.

Honest limit: the benchmark-side checks in check_validity.py drew their predictions from
third-party documentation written by people who had never seen our taxonomy. These come from
task definitions we wrote, so they can catch a classifier that is badly wrong but cannot
certify one that is right.

Usage:
    python skills/hpc_check_validity.py
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAPPING = ROOT / "results" / "skills" / "hpc" / "mapping.json"

# (task, skill, min_share) — what the task definition demands, per framing
EXPECTED = {
    "advisory": [
        ("Failure diagnosis", "Diagnosis", 0.70),
        ("Failure diagnosis", "Causal reasoning", 0.30),
        ("Performance analysis", "Causal reasoning", 0.40),
        ("Performance analysis", "Diagnosis", 0.50),
        ("Data management", "Factual recall", 0.50),
        ("Job monitoring", "Factual recall", 0.50),
        ("Environment and software", "Diagnosis", 0.40),
        ("Resource selection", "Expert domain knowledge", 0.60),
    ],
    "execution": [
        # Every execution task states a concrete deliverable and an output constraint.
        ("Job submission", "Instruction/format following", 0.60),
        ("Job monitoring", "Instruction/format following", 0.60),
        ("Failure diagnosis", "Instruction/format following", 0.60),
        # Emitting a script or command line is code generation.
        ("Job submission", "Code generation", 0.50),
        ("Workflow management", "Code generation", 0.50),
        # Still diagnosing, even though the deliverable is now a fix.
        ("Failure diagnosis", "Diagnosis", 0.40),
    ],
}

# (task, skill, max_share) — a popular tag bleeding somewhere it does not belong
FORBIDDEN = {
    "advisory": [
        ("Job monitoring", "Mathematical problem solving", 0.15),
        ("Failure diagnosis", "Creative/open-ended generation", 0.15),
        ("Resource selection", "Coreference resolution", 0.10),
        ("Data management", "Symbolic/abstract manipulation", 0.10),
    ],
    "execution": [
        ("Job monitoring", "Creative/open-ended generation", 0.15),
        ("Data management", "Coreference resolution", 0.10),
        ("Performance analysis", "Stylistic control", 0.15),
    ],
}

# The cross-cutting claim: "HPC knowledge" is not a sibling task but a prerequisite every
# task carries. If true, Expert domain knowledge should be near-universal across all of them.
CROSS_CUTTING = ("Expert domain knowledge", 0.60, "advisory")


def main() -> int:
    m = json.loads(MAPPING.read_text())
    fails = 0

    for framing in m["framings"]:
        tasks = m["framings"][framing]
        print(f"=== {framing.upper()} ===")
        for task, skill, floor in EXPECTED.get(framing, []):
            share = tasks[task]["shares"].get(skill, 0.0)
            ok = share >= floor
            fails += not ok
            print(f"  {'ok  ' if ok else 'MISS'} {task:<26} {skill:<32} "
                  f"{share:5.0%} (need {floor:.0%})")
        for task, skill, ceiling in FORBIDDEN.get(framing, []):
            share = tasks[task]["shares"].get(skill, 0.0)
            ok = share <= ceiling
            fails += not ok
            print(f"  {'ok  ' if ok else 'BLED'} {task:<26} {skill:<32} "
                  f"{share:5.0%} (max {ceiling:.0%})")
        print()

    skill, floor, framing = CROSS_CUTTING
    tasks = m["framings"][framing]
    print(f"CROSS-CUTTING [{framing}] — is '{skill}' universal, as the hypothesis that "
          f"'HPC knowledge is a\nprerequisite, not a task' predicts? (need >= {floor:.0%} everywhere)")
    universal = True
    for task in sorted(tasks):
        share = tasks[task]["shares"].get(skill, 0.0)
        universal &= share >= floor
        print(f"  {'ok  ' if share >= floor else 'LOW '} {task:<26} {share:5.0%}")
    print(f"  => {'CONFIRMED' if universal else 'NOT confirmed'}: {skill} is "
          f"{'present on every' if universal else 'absent from some'} HPC task")

    print(f"\n{fails} check(s) failed" if fails else "\nall checks passed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
