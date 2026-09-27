#!/usr/bin/env python3
"""Derive the capability arms from an existing Software-selection arm, by insertion.

WHY THESE ARMS EXIST. `SOFT.common.claims_true_to_catalog` grades an answer against the
catalog's `gpu_support` field, and no arm has ever shown that field to a model. The listing the
model sees is built by `generate.installed()`, which projects `name` + `description` and nothing
else, so "the answer contradicts the supplied catalog" was never a statement about anything the
model was supplied. Two models are locked at 3/3 violated on `qe@aurora` across all three
published arms — 18 runs out of 18 — while picking the right application every time. The
failure is entirely in the justifying prose.

Until the field is shown, "does a model understand `gpu_support: false`" is untested. These
arms show it, two ways, so that presentation can be priced separately from content:

    fieldbool    each catalog line gains  [gpu_support: false]
    fieldprose   each catalog line gains  [CPU-only build; no GPU offload]
    contract     the Instructions gain a clause forbidding unrecorded facility claims

`fieldbool` and `fieldprose` carry exactly the same fact and differ only in wording. `contract`
supplies no fact at all — the rule is satisfiable by abstention, and this arm tests whether
abstention can be induced without handing over the answer.

WHY INSERTION AND NOT REGENERATION. The same reason `arm.py` gives: the generator runs at
temperature 1.0, so asking it for a capability-annotated sample returns a rewritten prompt, not
the same prompt plus a tag. Measured rewriting noise is around 3 points per 10-sample cell
against an effect of similar size. So every arm here is the source prompt plus a splice, and
`--verify` asserts that stripping the splice returns the source byte for byte.

CONTRACT ARM, READ THIS BEFORE CHANGING THE WORDING. An instruction of this shape has regressed
this benchmark before. `task_spec.py` records that v3 told models to ground every claim in a
catalog field and say nothing the catalog omits, which "taught it that a sparse entry
disqualifies a code" — wrong-application picks went 2/30 to 6/28, and
`software_selection/_common.yaml` still carries the free-choice axis added in response ("A thin
catalog entry is NOT evidence against an application"). The wording below therefore constrains
only what may be ASSERTED, and says explicitly that a thin entry is not a reason to reject an
application. `SOFT.common.correct_application` is the guard rail and must not regress.

Usage:
    python -m benchmark.arm_capability --derive --arm fieldbool
    python -m benchmark.arm_capability --verify --arm fieldbool
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from benchmark.generate import app_yaml, CATALOG  # noqa: E402

TRIN = ROOT / "data" / "corpus" / "v8"
ARM_SUBTASK = "Software selection"

# Appended to the Instructions section, never inserted into the catalog listing: the contract is
# about what the answer may assert, not about what the catalog says.
CONTRACT = (
    "State only facility properties that the supplied catalog records — GPU support, module "
    "names, install paths, how the code is loaded. Where the catalog does not record a "
    "property, say nothing about it rather than inferring it from the machine or from the "
    "application's capabilities elsewhere. A sparse catalog entry is not evidence against an "
    "application; it is only a reason not to make claims the entry does not support."
)

TAGS = {
    "fieldbool":  lambda gs: f"gpu_support: {str(bool(gs)).lower()}",
    "fieldprose": lambda gs: ("GPU-accelerated build" if gs
                              else "CPU-only build; no GPU offload"),
}

# The listing the generator emits is an indented `Name — description` block under an
# "Installed software" heading. Heading spelling varies the same three ways `arm.py` documents.
_HEAD = re.compile(r"(?m)^[ \t]*(?:#+[ \t]*|\*\*)?Installed software\b[^\n]*\n")
_NEXT_HEAD = re.compile(r"(?m)^[ \t]*(?:#+[ \t]*|\*\*)?[A-Z][A-Za-z ]{2,30}:?\s*(?:\*\*)?\s*$")
_TAG = re.compile(r"[ \t]{2}\[[^\]\n]*\]$")


def _gpu_by_name(system: str) -> dict[str, object]:
    """name -> gpu_support, for every entry the listing could contain."""
    out: dict[str, object] = {}
    for f in sorted((CATALOG / "software" / system).glob("*.yaml")):
        if f.stem.startswith("_"):
            continue
        d = app_yaml(system, f.stem) or {}
        gs = d.get("gpu_support")
        if gs is None:
            continue                      # silence stays silence; never invent a tag
        for key in {str(d.get("name") or f.stem), f.stem}:
            out[key.strip().lower()] = gs
    return out


def _listing_span(prompt: str) -> tuple[int, int] | None:
    """Character span of the catalog listing body, excluding its heading."""
    m = _HEAD.search(prompt)
    if not m:
        return None
    start = m.end()
    for line in _NEXT_HEAD.finditer(prompt, start):
        # a heading only ends the listing if it is not itself an indented catalog entry
        if "—" not in prompt[line.start():line.end()]:
            return start, line.start()
    return start, len(prompt)


def derive(row: dict, arm: str) -> dict:
    """Return `row` with each catalog line tagged. Untouched if there is no listing."""
    out = dict(row)
    if row.get("subtask") != ARM_SUBTASK:
        return out
    p = row["prompt"]
    if arm == "contract":
        out["prompt"], out["arm_sha"] = _append_contract(p), "contract"
        return out
    span = _listing_span(p)
    if span is None:
        return out
    a, b = span
    gpu, tag = _gpu_by_name(row["system"]), TAGS[arm]
    lines = []
    for ln in p[a:b].split("\n"):
        name = ln.split("—")[0].strip().lower() if "—" in ln else ""
        gs = gpu.get(name)
        lines.append(f"{ln}  [{tag(gs)}]" if (ln.strip() and gs is not None) else ln)
    out["prompt"] = p[:a] + "\n".join(lines) + p[b:]
    out["arm_sha"] = arm
    return out


def _append_contract(p: str) -> str:
    """Splice the clause in as the last paragraph of Instructions.

    Insert at the Output heading and touch nothing else. An earlier version rstripped the
    Instructions body before appending, which normalised trailing newlines that `undo` then
    could not restore — `--verify` caught it as not reversible on all ten Software-selection
    rows. Insertion must be a pure splice, never a reformat.
    """
    m = re.search(r"(?m)^[ \t]*(?:#+[ \t]*|\*\*)?Instructions\b[^\n]*\n", p)
    if not m:
        return p
    nxt = re.search(r"(?m)^[ \t]*(?:#+[ \t]*|\*\*)?Output\b", p[m.end():])
    cut = m.end() + (nxt.start() if nxt else len(p) - m.end())
    return p[:cut] + CONTRACT + "\n\n" + p[cut:]


def undo(prompt: str, arm: str) -> str:
    """Inverse of `derive`. `--verify` asserts this returns the source byte for byte."""
    if arm == "contract":
        return prompt.replace(CONTRACT + "\n\n", "", 1)
    span = _listing_span(prompt)
    if span is None:
        return prompt
    a, b = span
    return prompt[:a] + "\n".join(_TAG.sub("", ln) for ln in prompt[a:b].split("\n")) + prompt[b:]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True, choices=["fieldbool", "fieldprose", "contract"])
    ap.add_argument("--src", default="samples_v8base.jsonl")
    ap.add_argument("--dst")
    ap.add_argument("--derive", action="store_true")
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()
    src = TRIN / a.src
    dst = TRIN / (a.dst or f"samples_v8{a.arm}.jsonl")
    rows = [json.loads(l) for l in src.open()]

    if a.derive:
        out = [derive(r, a.arm) for r in rows]
        dst.write_text("".join(json.dumps(r) + "\n" for r in out))
        n = sum(1 for s, d in zip(rows, out) if s["prompt"] != d["prompt"])
        print(f"wrote {dst.name}: {n} of {len(rows)} prompts changed")
        return 0

    if a.verify:
        bad = 0
        for r in rows:
            d = derive(r, a.arm)
            if undo(d["prompt"], a.arm) != r["prompt"]:
                bad += 1
                print(f"  NOT REVERSIBLE: {r['subtask']} {r.get('app')}@{r.get('system')}")
        print(f"reversible on {len(rows) - bad}/{len(rows)} rows")
        return 1 if bad else 0

    ap.error("pass --derive or --verify")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
