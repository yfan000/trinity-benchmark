#!/usr/bin/env python3
"""Preview only — builds prompts that carry the CANONICAL prior-step outputs.

Writes nothing into the benchmark. Each subtask is still answered independently; it is simply
told what the earlier steps correctly decided, taken from the catalog rather than from another
model's output, so a failure here is this subtask's failure and not inherited.
"""
import sys, json
sys.path.insert(0, '.')
import judge
from skills.trinity_task_spec import SUBTASKS, PHYSICAL_SYSTEMS, VARIATIONS
from skills.trinity_generate import (installed, workdir, scheduler, grading_key,
                                     machine_spec, _input_spec, _app_setup,
                                     app_yaml, CATALOG)

def prior_block(subtask, system, app):
    """What the earlier stages correctly produced, per the catalog."""
    d = app_yaml(system, app)
    name = d.get("name") or d.get("app") or app
    order = SUBTASKS[subtask]["order"]
    lines = []
    if order >= 2:
        lines.append(f"Software selection chose: {name}")
    if order >= 3:
        req = d.get("required_inputs") or d.get("input_files") or []
        stem = {"nwchem": "run", "qe": "scf", "cp2k": "run", "lammps": "in",
                "nekrs": "case", "qmcpack": "qmc"}.get(app, "run")
        files = ", ".join(f"{stem}{e}" for e in req) if req else "(none required)"
        lines.append(f"Input preparation produced: {files} in the working directory")
    if order >= 4:
        df = d.get("defaults") or {}
        wt = df.get("walltime")
        hh = f"{wt//3600:02d}:{(wt%3600)//60:02d}:00" if isinstance(wt, int) else "01:00:00"
        lines.append(f"Resource selection determined: {df.get('nodes','1')} node(s), "
                     f"{df.get('ppn','4')} ranks per node, walltime {hh}, "
                     f"queue {df.get('queue','debug')}")
    if not lines:
        return ""
    return ("\nDecisions already made by earlier pipeline stages — state these in the Workload "
            "as given facts, since this subtask is answered independently and must not have to "
            "re-derive them:\n  " + "\n  ".join(lines) + "\n")

CASES = [
    ("Input preparation",  "nwchem",  "polaris", "Computational chemistry"),
    ("Input preparation",  "qe",      "aurora",  "Electronic structure (DFT)"),
    ("Resource selection", "lammps",  "polaris", "Molecular dynamics"),
    ("Resource selection", "nekrs",   "polaris", "Computational fluid dynamics"),
    ("Resource selection", "qmcpack", "aurora",  "Quantum Monte Carlo"),
    ("Batch job creation", "lammps",  "polaris", "Molecular dynamics"),
    ("Batch job creation", "nwchem",  "aurora",  "Computational chemistry"),
    ("Batch job creation", "hacc",    "polaris", "Cosmology"),
    ("Batch job creation", "gromacs", "aurora",  "Molecular dynamics (biomolecular)"),
    ("Batch job creation", "alphafold","perlmutter","Protein structure prediction"),
]

out=[]
for i,(st, app, sysn, dom) in enumerate(CASES):
    spec = SUBTASKS[st]
    r = judge.generate_trinity_sample(
        st, spec["goal"], dom, sysn.capitalize(), VARIATIONS[i % len(VARIATIONS)],
        spec["instructions"], spec["output"], spec["withhold"],
        (CATALOG/"systems"/f"{sysn}.yaml").read_text(), installed(sysn),
        (CATALOG/"software"/sysn/f"{app}.yaml").read_text(),
        prior=prior_block(st, sysn, app),
        sched=scheduler(sysn),
        workdir=workdir(sysn, app, st, neutral=spec.get("needs_software_list", False)),
        phys=PHYSICAL_SYSTEMS.get(app,"") if spec.get("needs_physical_system") else "",
        mach=machine_spec(sysn) if spec.get("needs_machine_spec") else "",
        gives_sched=spec.get("gives_scheduler", False),
        show_catalog=spec.get("needs_software_list", False),
        input_spec=_input_spec(sysn, app) if spec.get("needs_input_spec") else "",
        app_setup=_app_setup(sysn, app) if spec.get("needs_app_setup") else "")
    out.append({"n": i+1, "subtask": st, "app": app, "system": sysn,
                "prompt": r["prompt"], "reference": r["reference"]})
    print(f"  [{i+1}/10] {'ok ' if r['prompt'] else 'EMPTY'} {st} · {app}@{sysn}", flush=True)
json.dump(out, open("/tmp/preview_prior.json","w"), indent=1)
