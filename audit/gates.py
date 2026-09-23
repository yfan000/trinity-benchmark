#!/usr/bin/env python3
"""Prove the enriched blocks cannot hand over the answer — before they reach any prompt.

The governing rule of this benchmark is that a prompt states the task explicitly but never
contains the answer being tested. The RICH arm deliberately moves that line: it supplies the
FORMAT of each input file, keeping the VALUES as the test. Moving a line on purpose still
requires knowing exactly where it now sits, per block and per subtask.

Three things are asserted, and the third is the one that catches a broken gate:

  positive   the contract and system-context blocks are clean against Input preparation's own
             leak terms on every anchor
  redaction  `input_scaling` does not merely come back clean — it must be shown to have FIRED,
             on the anchors whose scaling_notes really do leak. A filter that never runs and a
             filter that works look identical from the output alone.
  negative   the same contract scored against SOFTWARE SELECTION's terms must still light up.
             Those blocks name applications; if this returns zero, either the gate that keeps
             the contract out of Software selection has broken or `leaks()` has regressed.

Usage:
    python skills/leak_audit.py
    python skills/leak_audit.py --subset      # the 10 frozen anchors only
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from benchmark import catalog
from benchmark.generate import (format_contract, system_context,  # noqa: E402
                                     input_scaling, leaks)
from benchmark.task_spec import ANCHORS, SUBSET, SUBTASKS  # noqa: E402

# Strings that would prove we had reintroduced the detection-marker mistake: the amino-acid
# alphabet, which no real FASTA contains, and NWChem's optional convenience directive.
FORBIDDEN = ["ACDEFGHIKLMNPQRSTVWY", "memory stack"]


def pairs(subset_only: bool) -> list[tuple[str, str]]:
    src = SUBSET if subset_only else ANCHORS
    seen, out = set(), []
    for row in src:
        app, system = row[1], row[2]
        if (system, app) not in seen:
            seen.add((system, app))
            out.append((system, app))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subset", action="store_true")
    a = ap.parse_args()

    inp_terms = SUBTASKS["Input preparation"]["leak_terms"]
    soft_terms = SUBTASKS["Software selection"]["leak_terms"]
    anchors = pairs(a.subset)
    fail = 0

    print(f"{len(anchors)} (system, app) anchors\n")

    # --- positive: the new blocks are clean where they are actually used ------------------
    print("POSITIVE — enriched blocks vs Input preparation leak terms")
    for system, app in anchors:
        for name, block in (("contract", format_contract(system, app)),
                            ("sysctx", system_context(system)),
                            ("scaling", input_scaling(system, app, inp_terms))):
            hits = leaks(block, inp_terms, True)
            if hits:
                fail += 1
                print(f"  LEAK  {app}@{system:<12} {name:<9} {hits}")
    print(f"  {'clean' if not fail else f'{fail} LEAKS'}"
          f" across {len(anchors)*3} blocks\n")

    # --- forbidden strings ----------------------------------------------------------------
    print("FORBIDDEN STRINGS — the detection-marker mistake must not come back")
    bad = 0
    for system, app in anchors:
        blob = format_contract(system, app)
        for s in FORBIDDEN:
            if s in blob:
                bad += 1
                print(f"  PRESENT  {app}@{system}: {s!r}")
    print(f"  {'none present' if not bad else f'{bad} PRESENT'}\n")
    fail += bad

    # --- redaction actually fires ----------------------------------------------------------
    print("REDACTION — scaling_notes that leak before filtering")
    fired = []
    for system, app in anchors:
        raw = " ".join(str(catalog.merged(system, app).get("scaling_notes") or "").split())
        if raw and leaks(raw, inp_terms, True):
            after = input_scaling(system, app, inp_terms)
            still = leaks(after, inp_terms, True)
            fired.append((f"{app}@{system}", leaks(raw, inp_terms, True), bool(still)))
            print(f"  fired  {app+'@'+system:<24} raw leaked {leaks(raw, inp_terms, True)}"
                  f"{'   STILL LEAKS' if still else ''}")
            if still:
                fail += 1
    if not fired:
        print("  WARNING: the filter never fired on any anchor. Either the corpus changed or\n"
              "           the filter is a no-op — it is not evidence of safety.")
    print()

    # --- negative control -------------------------------------------------------------------
    # Scores the FILE INVENTORY, not the format block. The inventory is what carries
    # application-identifying strings (log.lammps, topol.top, HPL.dat); the format block was
    # reduced to content requirements ("integrator, nsteps") and legitimately cannot leak a
    # name any more — at which point this control silently became vacuous and said so, which
    # is the whole reason it exists.
    from benchmark.generate import _input_spec as _inv
    print("NEGATIVE CONTROL — the file inventory vs Software selection terms (must NOT be clean)")
    n_hit = sum(1 for system, app in anchors
                if leaks(_inv(system, app), soft_terms, True))
    print(f"  {n_hit} of {len(anchors)} anchors leak the application name")
    if n_hit == 0:
        fail += 1
        print("  BROKEN: expected these to leak. Either leaks() regressed or the contract is\n"
              "          empty. This control exists because a silently-empty block would pass\n"
              "          every other check here.")
    fail += coherence_check()
    fail += example_check()
    print(f"\n{'AUDIT PASSED' if not fail else f'AUDIT FAILED ({fail} problems)'}")
    return 1 if fail else 0



def coherence_check() -> int:
    """No two parts of a prompt may assert different things.

    Every check here exists because one instance of it reached a model and was then punished by
    a rule. They are the generalised forms:
      queue        hpl@crux was told "queue workq"; Crux has no workq. All four models obeyed
                   and were failed FATALLY by BATCH.common.queue_exists. 26 catalog entries
                   name a queue their own system lacks.
      nodes/time   a carry-forward inside a queue the machine rejects is equally unusable —
                   Polaris `prod` exists but refuses anything under 10 nodes.
      compiled     required_inputs lists .tpr / .re2 / .h5, which the toolchain builds; asking
                   for them contradicts the fatal rules that forbid authoring them.
      launch       the catalog run_command carries placeholder filenames that disagree with the
                   workload's, so it must be labelled a FORM, never stated as site fact.
      gpu count    scaling_notes said "-ntmpi 8 for 8 GPUs per node" on a 4-GPU machine.
    """
    import re as _re
    import yaml as _y
    from benchmark import catalog as C
    from benchmark.generate import (prior_block, _input_spec, _app_setup,
                                         system_context, format_contract)
    FC = (_y.safe_load((ROOT / "judge" / "skills" / "format_contracts.yaml").read_text())
          or {}).get("contracts", {})
    seen, bad = set(), []
    for _, app, s in ANCHORS:
        if (app, s) in seen:
            continue
        seen.add((app, s))
        A = f"{app}@{s}"
        qs, hw, d = C.queues(s), C.hardware(s), C.defaults(s, app)
        binr = {b.lower() for b in ((FC.get(app) or {}).get("binary") or [])}
        pb = prior_block("Batch job creation", s, app, app)
        m = _re.search(r"queue (\S+)", pb)
        if m and m.group(1) not in qs:
            bad.append((A, "carry-forward names a queue the machine lacks", m.group(1)))
        mn = _re.search(r"(\d+) node", pb)
        if m and mn and m.group(1) in qs:
            q, n = qs[m.group(1)], int(mn.group(1))
            if q.min_nodes and n < q.min_nodes:
                bad.append((A, "carry-forward nodes below queue minimum", f"{n}<{q.min_nodes}"))
            if q.max_nodes and n > q.max_nodes:
                bad.append((A, "carry-forward nodes above queue maximum", f"{n}>{q.max_nodes}"))
        if d.ppn and hw.cpus_per_node and d.ppn > hw.cpus_per_node:
            bad.append((A, "build ppn exceeds cores per node", f"{d.ppn}>{hw.cpus_per_node}"))
        inv = _input_spec(s, app)
        for b in binr:
            if _re.search(rf"(?i)WRITE[^\n]*{_re.escape(b)}", inv):
                bad.append((A, "inventory asks the model to write a compiled file", b))
        st = _app_setup(s, app)
        if st and _re.search(r"(?m)^launch", st) and "FORM" not in st:
            bad.append((A, "launch line presented as fact, not a form", ""))
        for g in _re.findall(r"(\d+)\s*GPUs?\s*per\s*node", system_context(s), _re.I):
            if hw.gpus_per_node and int(g) != hw.gpus_per_node:
                bad.append((A, "system context GPU count contradicts hardware", g))
    print(f"PROMPT COHERENCE — {len(seen)} anchors x 6 invariants")
    for a, w, dd in bad:
        print(f"  BAD {a:<24}{w:<46}{dd}")
    print(f"  {'no part of any prompt contradicts another' if not bad else f'{len(bad)} CONTRADICTIONS'}\n")
    return len(bad)


def example_check() -> int:
    """EVERY format the model must write needs an example. Not just one of them.

    The first version of this gate passed if the example matched ANY file to write, and that
    was too weak: nekRS must write a `.par` AND a `.udf` — INI and C, entirely different
    formats — and only `turbPipe.par` was supplied, so the `.udf` had no form reference at all
    while the rubric still required the file. GROMACS was worse, 1 of 3: an `.mdp` example
    against `.mdp` + `.gro` + `.top`.

    "ONE of these extensions" cases need only one example, because only one file is written.
    """
    import re as _re
    from benchmark.generate import _input_spec
    from benchmark import site as trinity_site

    SUB = {"nwchem": "polaris", "lammps": "polaris", "nekrs": "polaris", "qe": "aurora",
           "qmcpack": "aurora", "hpl": "crux", "gromacs": "sirius",
           "alphafold": "perlmutter", "vllm": "frontier", "pytorch": "sophia"}

    def names_it(filename: str, token: str) -> bool:
        # Real upstream inputs do not all END in their extension: LAMMPS ships `in.melt`, the
        # reference HPL.dat is `HPL.dat_2N_dgx2`, QE's is `scf.in` against a `.scf.in` entry.
        tok = _re.escape(token.lstrip(".").lower())
        return bool(_re.search(rf"(^|[._]){tok}($|[._])", filename.lower()))

    print("WORKED EXAMPLE — every format the model must write needs one, IN THE PROMPT")
    bad = 0
    # Read the GENERATED PROMPT, not the example file on disk. Checking the file passed while
    # judge.py truncated the example to 44 lines, so GROMACS models saw only the .mdp of three
    # required files. The gate has to measure what the model receives.
    import json as _json
    gen = {}
    # BASE specifically, not "whichever exists". The rich arm is derived from base, so a rich
    # file without a base file is stale by definition — and accepting it let this gate report
    # PASS against a corpus two regenerations old.
    _p = ROOT / "data" / "corpus" / "v8" / "samples_v8base.jsonl"
    if _p.exists():
        for _r in (_json.loads(l) for l in _p.open()):
            if _r["subtask"] == "Input preparation":
                gen.setdefault(_r["app"], _r["prompt"])
    if not gen:
        # Do NOT quietly fall back to the example files on disk. That fallback let this gate
        # report PASS while no prompts existed at all — and checking the file is precisely the
        # weaker test that missed judge.py truncating the example to 44 lines. An absent
        # corpus is an unknown result, not a good one.
        print("  CANNOT CHECK — no generated prompts found. Run trinity_generate first.\n")
        return 1

    for app, system in sorted(SUB.items()):
        ex = gen.get(app) or trinity_site.worked_deck(app) or ""
        src = "prompt" if app in gen else "file"
        fc = _input_spec(system, app)
        m = _re.search(r"WRITE[^:]*: (.+)", fc)
        if not m or not ex:
            print(f"  --  {app+'@'+system:<22} no contract or no example")
            continue
        # "WRITE ONE file" means the listed forms are ALTERNATIVE NAMES for a single
        # deliverable, so one example covers them. Keyed on the sentence the inventory
        # actually emits — the previous key ("any of these extensions") was older wording, and
        # when it stopped matching the gate silently demanded an example per alternative.
        alt = fc.splitlines()[0].startswith("WRITE ONE file")
        want = [x.strip() for x in _re.split(r"[,/]", m.group(1)) if x.strip()]
        shown = _re.findall(r"# =====\s*(\S+?)\s*=====", ex) or \
                [(_re.search(r"source:\s*(\S+)", ex) or _re.match("", "")).group(1).rsplit("/", 1)[-1]]
        covered = [w for w in want if any(names_it(n, w) for n in shown)]
        ok = bool(covered) if alt else len(covered) == len(want)
        if not ok:
            bad += 1
        missing = [w for w in want if w not in covered]
        print(f"  {'ok ' if ok else 'BAD'} {app+'@'+system:<22}"
              f"writes {', '.join(want):<30} [{src}] shows {', '.join(shown)}"
              + (f"   MISSING {missing}" if not ok else ""))
    print(f"  {'every required format has an example' if not bad else f'{bad} INCOMPLETE'}\n")
    return bad


if __name__ == "__main__":
    sys.exit(main())
