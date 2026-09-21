#!/usr/bin/env python3
"""Derive the RICH arm from the BASE arm by textual insertion, not by regenerating it.

THIS IS THE METHODOLOGICAL CORE OF THE A/B, and it inverts the obvious approach.

`judge.generate_trinity_sample` runs at temperature 1.0. Ask it for a RICH sample and it does
not hand back the BASE prompt plus a block — it rewrites every sentence: different workload
framing, different numbers, different phrasing of the instructions. The measured size of that
noise is about 3 points per 10-sample cell (two runs of byte-identical prompts moved
alphafold 2,2,2 -> 1,2,1 and pytorch 2,2,2 -> 0,1,1). The effect under test is roughly 4 points
across 38 rows. Regenerating would bury the signal in prompt-rewriting variance and the result
would be uninterpretable whichever way it came out.

So RICH is BASE with two sections spliced in at a fixed anchor and one clause appended. The
reference answer is carried over UNCHANGED — an exemplar that differed between arms would be a
second uncontrolled variable.

`--verify` asserts the property that licenses the whole comparison: strip the inserted material
from a RICH prompt and you get the BASE prompt back, byte for byte.

Usage:
    python skills/trinity_arm.py --derive  --src samples_v8base.jsonl --dst samples_v8rich.jsonl
    python skills/trinity_arm.py --verify  --src samples_v8base.jsonl --dst samples_v8rich.jsonl
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from benchmark.generate import (format_contract, system_context,  # noqa: E402
                                     input_scaling, leaks)
from benchmark.task_spec import SUBTASKS  # noqa: E402

TRIN = ROOT / "data" / "corpus" / "v8"
ARM_SUBTASK = "Input preparation"

CLAUSE = ("Every file you write must contain the sections named under Input file format "
          "above. That section says what must appear inside each file; it does not give the "
          "values, which are yours to determine.")

# The generator formats headings three ways within a single run — "Instructions:",
# "**Instructions:**" and "## Instructions" all occur in samples_v7 (the last on vllm@frontier
# and gromacs@sirius). Match the same set `trinity_generate.has_section` does; a narrower
# pattern silently skips those rows, which on a 10-row subtask is 20% of the arm.
#
# `[ \t]*`, NOT `\s*`. With re.M, `^\s*` matches at the start of the BLANK line preceding a
# heading and eats the newline, so match.start() lands a line early. Splicing there moved the
# blank line to the wrong side of the inserted text and undo() came back one newline heavier —
# which --verify caught as "not reversible" on all ten rows.
_ANCHOR = re.compile(r"(?m)^[ \t]*(?:#+[ \t]*|\*\*)?Instructions\b")
_OUTPUT = re.compile(r"(?m)^[ \t]*(?:#+[ \t]*|\*\*)?Output\b")


def heading_style(prompt: str) -> str:
    """"##" or "**", whichever this prompt already uses for its own sections.

    The generator picks one per sample and is not consistent across a run. An inserted block in
    the other style reads as a trailing note on whatever came before it — and what comes before
    it here is the worked example, the one block the instructions tell the model NOT to copy.
    Matching the surrounding style is what makes the contract read as a section of its own.
    """
    hashes = len(re.findall(r"(?m)^##\s+\w", prompt))
    bolds = len(re.findall(r"(?m)^\*\*[A-Z][^\n*]{2,40}:?\*\*", prompt))
    return "##" if hashes >= bolds else "**"


def _section(title: str, body: str, style: str) -> str:
    head = f"## {title}" if style == "##" else f"**{title}:**"
    return f"{head}\n{body}\n\n"


def blocks_for(system: str, app: str, style: str = "**") -> tuple[str, str]:
    """(contract section, system-context section) — both already leak-checked by leak_audit."""
    terms = SUBTASKS[ARM_SUBTASK]["leak_terms"]
    contract = format_contract(system, app)
    ctx = system_context(system)
    scaling = input_scaling(system, app, terms)
    body = "\n".join(x for x in (ctx, scaling) if x)
    return (_section("Input file format", contract, style) if contract else "",
            _section("System context", body, style) if body else "")


def derive(row: dict) -> dict:
    """BASE row -> RICH row. Byte-identical outside the inserted material."""
    out = dict(row)
    out["arm"] = "rich"
    if row["subtask"] != ARM_SUBTASK:
        # Every other subtask is carried across untouched, so three quarters of the corpus is
        # a built-in control: any movement there is model sampling noise, and it calibrates the
        # noise floor for reading the Input-preparation delta.
        out["arm_sha"] = ""
        return out

    style = heading_style(row["prompt"])
    contract, ctx = blocks_for(row["system"], row["app"], style)
    p = row["prompt"]
    m = _ANCHOR.search(p)
    if not m:
        raise ValueError(f"no Instructions anchor in {row.get('sample_id')} "
                         f"({row['app']}@{row['system']}) — cannot derive safely")
    at = m.start()
    p = p[:at] + contract + ctx + p[at:]
    # The clause belongs at the END of Instructions, not after the whole prompt. Appended at the
    # very end it landed beneath the Output spec and read as a floating afterthought.
    # The clause points at the contract. On the two sparse anchors the contract says "none
    # recorded", so the clause would order the model to satisfy a list that does not exist.
    if "records no format requirements" in contract:
        out["prompt"] = p
        out["arm_sha"] = hashlib.sha256((contract + ctx).encode()).hexdigest()[:12]
        return out
    om = _OUTPUT.search(p)
    if om:
        p = p[:om.start()].rstrip() + "\n\n" + CLAUSE + "\n\n" + p[om.start():]
    else:
        p = p.rstrip() + "\n\n" + CLAUSE + "\n"
    out["prompt"] = p
    out["arm_sha"] = hashlib.sha256((contract + ctx + CLAUSE).encode()).hexdigest()[:12]
    return out


def undo(rich: str, contract: str, ctx: str) -> str:
    """Remove exactly what derive() added. Used only by --verify."""
    p = rich.replace("\n\n" + CLAUSE + "\n\n", "\n\n", 1)   # no-op when the clause was omitted
    if p.rstrip().endswith(CLAUSE):
        p = p.rstrip()[: -len(CLAUSE)].rstrip() + "\n"
    for blk in (contract, ctx):
        if blk:
            p = p.replace(blk, "", 1)
    return p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="samples_v8base.jsonl")
    ap.add_argument("--dst", default="samples_v8rich.jsonl")
    ap.add_argument("--derive", action="store_true")
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()
    src, dst = TRIN / a.src, TRIN / a.dst

    if a.derive:
        rows = [json.loads(l) for l in src.open() if l.strip()]
        out = [derive(r) for r in rows]
        with dst.open("w") as f:
            for r in out:
                f.write(json.dumps(r) + "\n")
        n = sum(1 for r in out if r["subtask"] == ARM_SUBTASK and r.get("arm_sha"))
        print(f"{len(out)} rows -> {dst.name}; {n} Input-preparation prompts enriched, "
              f"{len(out)-n} carried across unchanged")
        return 0

    if a.verify:
        base = {(r["subtask"], r["app"], r["system"]): r
                for r in (json.loads(l) for l in src.open() if l.strip())}
        rich = [json.loads(l) for l in dst.open() if l.strip()]
        bad = 0
        touched = 0
        terms = SUBTASKS[ARM_SUBTASK]["leak_terms"]
        for r in rich:
            k = (r["subtask"], r["app"], r["system"])
            b = base.get(k)
            if not b:
                print(f"  MISSING in base: {k}")
                bad += 1
                continue
            if r["subtask"] != ARM_SUBTASK:
                if r["prompt"] != b["prompt"]:
                    print(f"  CHANGED outside the arm subtask: {k}")
                    bad += 1
                continue
            touched += 1
            contract, ctx = blocks_for(r["system"], r["app"], heading_style(b["prompt"]))
            if undo(r["prompt"], contract, ctx).strip() != b["prompt"].strip():
                print(f"  NOT REVERSIBLE: {k} — RICH is not BASE + the inserted blocks")
                bad += 1
            if r.get("reference") != b.get("reference"):
                print(f"  EXEMPLAR DIFFERS: {k} — the reference must be identical across arms")
                bad += 1
            hits = leaks(r["prompt"], terms, True)
            if hits:
                print(f"  LEAK in derived prompt: {k} {hits}")
                bad += 1
        print(f"\n{len(rich)} rows, {touched} enriched; "
              f"{'REVERSIBLE — the delta is attributable to the blocks' if not bad else f'{bad} PROBLEMS'}")
        return 1 if bad else 0

    ap.error("pass --derive or --verify")


if __name__ == "__main__":
    sys.exit(main())
