#!/usr/bin/env python3
"""Load the judging skill — the requirement library — and hash it so a grade is traceable.

A "rubric version" is the set of requirement files plus their hashes, not a prose document.
Every grade row records `rubric_id` and `rubric_sha256`, so two grades produced under
different rules can never be silently compared. Today's grade rows record neither, which is
why the v2-v6 series cannot be re-derived.

Requirements are selected for a sample by subtask and software: input-format rules are keyed
on software because they transfer between machines, while queue and directive rules are keyed
on (software, system) because they do not.

Usage:
    python skills/judging/loader.py --subtask "Input preparation" --app qe
    python skills/judging/loader.py --list
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REQ = HERE / "requirements"
REGISTRY = HERE / "registry.json"

SUBTASK_DIR = {
    "Software selection": "software_selection",
    "Input preparation": "input_preparation",
    "Resource selection": "resource_selection",
    "Batch job creation": "batch_job_creation",
}


@dataclass
class Skill:
    """The requirements that apply to one sample, plus the identity of the version."""
    rubric_id: str
    rubric_sha256: str
    requirements: list[dict] = field(default_factory=list)
    free_choice: list[dict] = field(default_factory=list)
    binary_files: list[str] = field(default_factory=list)
    files_used: list[str] = field(default_factory=list)

    @property
    def deterministic(self) -> list[dict]:
        return [r for r in self.requirements if r.get("decided_by") == "deterministic"]

    @property
    def judged(self) -> list[dict]:
        return [r for r in self.requirements if r.get("decided_by") != "deterministic"]

    def render(self) -> str:
        """The requirement block as the judge sees it."""
        out = []
        for r in self.requirements:
            sev = r.get("severity", "major")
            out.append(f"  [{r['id']}]  ({sev}, affects {r.get('dimension','?')})\n"
                       f"      {' '.join(str(r['claim']).split())}")
        s = "REQUIREMENTS — rule on each one separately:\n" + "\n".join(out)
        if self.free_choice:
            fc = "\n".join(f"  - {f['axis']}: {' '.join(str(f['note']).split())}"
                           for f in self.free_choice)
            s += ("\n\nFREE CHOICE — the answer may differ from the exemplar on these axes.\n"
                  "Never deduct for any of them:\n" + fc)
        return s


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text()) or {} if path.exists() else {}


def load(subtask: str, app: str | None = None, system: str | None = None,
         rubric_id: str = "r1") -> Skill:
    """Assemble the requirements for one sample, most general first."""
    d = REQ / SUBTASK_DIR[subtask]
    paths = [REQ / "_common.yaml", d / "_common.yaml"]
    if app:
        paths.append(d / f"{app}.yaml")
    if system:
        # Scheduler-keyed before system-keyed: Perlmutter and Frontier share a dialect, so
        # the Slurm rules belong to the family, not to each machine.
        from benchmark.generate import scheduler as _sched
        fam = {"Slurm": "slurm", "PBS Pro": "pbs"}.get(_sched(system))
        if fam:
            paths.append(d / f"{fam}.yaml")
        paths.append(d / f"{system}.yaml")

    skill = Skill(rubric_id=rubric_id, rubric_sha256="")
    h = hashlib.sha256()
    for p in paths:
        if not p.exists():
            continue
        h.update(p.read_bytes())
        doc = _load(p)
        skill.requirements += doc.get("requirements") or []
        skill.free_choice += doc.get("free_choice") or []
        skill.binary_files += doc.get("binary_files") or []
        skill.files_used.append(str(p.relative_to(REQ)))
    skill.rubric_sha256 = h.hexdigest()[:12]

    # A later file may refine an earlier one; last definition of an id wins.
    seen: dict[str, dict] = {}
    for r in skill.requirements:
        seen[r["id"]] = r
    skill.requirements = list(seen.values())
    return skill


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subtask", default="Input preparation")
    ap.add_argument("--app")
    ap.add_argument("--system")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()

    if a.list:
        tot = 0
        for st, d in SUBTASK_DIR.items():
            files = sorted((REQ / d).glob("*.yaml"))
            n = sum(len(_load(f).get("requirements") or []) for f in files)
            fc = sum(len(_load(f).get("free_choice") or []) for f in files)
            det = sum(1 for f in files for r in (_load(f).get("requirements") or [])
                      if r.get("decided_by") == "deterministic")
            tot += n
            print(f"{st:<22}{n:>3} requirements ({det} deterministic, {n-det} judged), "
                  f"{fc} free-choice axes, {len(files)} files")
        print(f"{'TOTAL':<22}{tot:>3} requirements")
        return 0

    s = load(a.subtask, a.app, a.system)
    print(f"# {a.subtask}" + (f" / {a.app}" if a.app else "")
          + (f" @ {a.system}" if a.system else ""))
    print(f"# rubric {s.rubric_id} sha {s.rubric_sha256} from {', '.join(s.files_used)}")
    print(f"# {len(s.deterministic)} deterministic, {len(s.judged)} judged"
          + (f", binary: {', '.join(sorted(set(s.binary_files)))}" if s.binary_files else ""))
    print()
    print(s.render())
    return 0


if __name__ == "__main__":
    sys.exit(main())
