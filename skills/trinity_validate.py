#!/usr/bin/env python3
"""Re-check every stored sample against the CURRENT spec, not the spec it was born under.

The `leaked` field written at generation time reflects whatever the rules were then. Those
rules kept changing as false positives and real leaks were found, so a sample generated
early can carry a clean flag while violating a rule added later. This re-derives the verdict
from scratch and rewrites the field.

Usage:
    python skills/trinity_validate.py            # report
    python skills/trinity_validate.py --fix      # rewrite `leaked`, so a regen picks them up
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from skills.trinity_generate import leaks, strip_catalog  # noqa: E402
from skills.trinity_task_spec import SUBTASKS  # noqa: E402

SAMPLES = ROOT / "results" / "skills" / "trinity" / "samples.jsonl"
SECTIONS = ("Task", "Workload", "Instructions", "Output")


def has_section(prompt: str, name: str) -> bool:
    """Accept "Name:", "**Name:**" and "## Name" heading styles."""
    import re as _re
    return bool(_re.search(rf"(?:^|\n)\s*(?:#+\s*|\*\*)?{name}\b\s*:?\s*(?:\*\*)?\s*(?:\n|$|[A-Z])",
                           prompt, _re.I))


def check(r: dict) -> list[str]:
    spec = SUBTASKS[r["subtask"]]
    if not r["prompt"]:
        return ["<empty>"]
    app = r["grading_key"].get("app", "")
    # An application named by an earlier pipeline stage is not a leak downstream.
    terms = [t for t in spec["leak_terms"]
             if not (spec["order"] >= 2 and app and t.lower() in app.lower())]
    supplies = any(spec.get(f) for f in ("needs_software_list", "needs_input_spec",
                                         "needs_app_setup"))
    checked = strip_catalog(r["prompt"]) if supplies else r["prompt"]
    bad = leaks(checked, terms, True)
    bad += [f"missing section {k}" for k in SECTIONS if not has_section(r["prompt"], k)]
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix", action="store_true")
    args = ap.parse_args()

    rows = [json.loads(l) for l in SAMPLES.open()]
    now = {r["sample_id"]: check(r) for r in rows}
    stale = [r for r in rows if bool(now[r["sample_id"]]) != bool(r["leaked"])]
    bad = [r for r in rows if now[r["sample_id"]]]

    print(f"{len(rows)} samples re-checked against the current spec")
    print(f"  {len(bad)} violate a current rule")
    print(f"  {len(stale)} carry a stale verdict from an older ruleset")
    for r in bad:
        print(f"    {r['sample_id']}  {r['subtask']:<20}{r['domain']:<30}{now[r['sample_id']]}")
    if bad:
        print(f"\n  by subtask: {dict(Counter(r['subtask'] for r in bad))}")

    if args.fix:
        for r in rows:
            r["leaked"] = now[r["sample_id"]]
        SAMPLES.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
        print(f"\nrewrote `leaked` on {len(rows)} rows — rerun trinity_generate.py to "
              f"regenerate the {len(bad)} failures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
