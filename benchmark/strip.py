#!/usr/bin/env python3
"""Derive the unaugmented prompt arms by deletion, and prove the deletion is reversible.

WHY THIS EXISTS. Every published number comes from a prompt that already hands the model most of
the facility knowledge the task is about: Software selection supplies the installed-software list
(1-of-21 multiple choice, the answer always in it), Resource selection supplies the queue table,
Input preparation the required-file list and a worked deck, Batch the module lines and site
conventions. Both existing arms sit at the augmented end, so nothing measures how much of the
score is the model and how much is our prompt. These arms are the missing control:

    bare   task + workload + output contract, and only instructions that stand alone
    cat    bare + the catalog facts and the instructions that reference them, no worked example
    base   cat + worked examples                                            (exists)
    rich   base + format contracts, setup/run commands, scaling notes       (exists)

bare -> cat prices injected knowledge; cat -> base prices few-shot examples.

WHY DELETION AND NOT REGENERATION. Asking the sample generator for a leaner prompt rewrites every
sentence, and two runs of byte-identical prompts already move a 10-sample cell by ~3 points. That
noise would swamp the effect. Deletion keeps the arms paired item-for-item, exactly as
`benchmark/arm.py` does in the insertion direction.

WHY NOT `strip_catalog()` OR STRING SUBTRACTION. Two traps, both measured:

  - The delivered prompt is written by the sample generator at temperature 1.0, so the blocks are
    TRANSCRIBED, not pasted. `_input_spec()`'s text appears verbatim on 1 of 5 lines in most rows;
    `machine_spec()` as low as 1 of 7. Anything built on `prompt.replace(source_block, "")` is a
    no-op on most of the corpus. We therefore cut spans found in the DELIVERED text.
  - `generate.strip_catalog()` ends its skip only on an exact heading match, so an inline
    `Instructions: Consult the...` never terminates it: run over this corpus it destroys
    Instructions and Output on 10 of 10 Software-selection rows and cuts nothing at all from
    Resource selection. It is for leak-checking, not for building an arm.

Usage:
    python -m benchmark.strip --derive                 # writes samples_v8bare / samples_v8cat
    python -m benchmark.strip --verify                 # rebuilds base from each arm + manifest
    python -m benchmark.strip --show bare hpl crux     # read one stripped prompt
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRIN = ROOT / "data" / "corpus" / "v8"
SRC = TRIN / "samples_v8base.jsonl"

# Heading names the generator emits, in the three styles it uses: "## Name", "**Name:**", "Name:".
# Matching is on the normalised head of a line, prefix-wise, because it also produces
# "### Worked Example (different application - do NOT copy its resource numbers)".
HEADS = ["task", "workload", "installed software", "required input files", "worked example",
         "target system", "build defaults", "software environment", "scheduler conventions",
         "instructions", "output"]

# What each arm removes. Everything not listed is kept, including the workload (it IS the grading
# key: INP.common.values_match_physical_system has source "prompt"), the carry-forward of earlier
# stages (pipeline plumbing, not catalog augmentation), the charge account and the scheduler name
# (withholding either measured one recall fact and drowned out the subtask).
STRIP = {
    "bare": {
        "Software selection":  ["installed software"],
        "Input preparation":   ["required input files", "worked example"],
        "Resource selection":  ["target system", "build defaults"],
        "Batch job creation":  ["software environment", "scheduler conventions", "worked example"],
    },
    "cat": {                       # catalog facts stay; only the demonstration goes
        "Software selection":  [],
        "Input preparation":   ["worked example"],
        "Resource selection":  [],
        "Batch job creation":  ["worked example"],
    },
}

# Each removable topic carries the phrases that REFER to it. Scoping matters: in the `cat` arm the
# queue table is still there, so "go through the supplied queue table" is a valid instruction, not
# a dangling one. Only references to material THIS arm removed may be dropped or flagged.
TOPIC_REFS = {
    "installed software":     r"software catalog|installed software|the (?:list|catalog) above",
    "worked example":         r"worked example|example (?:deck|script)|the example above",
    # NB "the system's queue policy" is deliberately NOT here: the lead instruction says to use
    # the queue policy, which is the task, not a pointer at a block we deleted.
    "target system":          r"queue table|machine specification|hardware (?:above|supplied)",
    "build defaults":         r"build defaults|application defaults|scaling (?:guidance|notes)"
                              r"|ranks-per-node .{0,30} suppl",
    "software environment":   r"module (?:and export )?lines|launch command suppl|exact module"
                              r"|the supplied modules|software environment .{0,20}(?:above|given)",
    "scheduler conventions":  r"site conventions|scheduler conventions",
}
# "...when none is supplied" is not a reference to supplied material.
NOT_REFERENTIAL = re.compile(r"(?i)when\s+none\s+is\s+suppl|if\s+none\s+is\s+suppl|none\s+supplied")


# Topics whose instruction references are REWRITTEN, never deleted — deleting them would remove
# the task statement itself. Software selection's entire instruction is "Consult the system's
# software catalog and identify...", so the clause dropper must keep its hands off it.
REWRITE_ONLY = {"installed software"}


def ref_pattern(topics) -> re.Pattern | None:
    """One regex matching a reference to any of the topics this arm removed."""
    pats = [TOPIC_REFS[t] for t in topics if t in TOPIC_REFS]
    return re.compile("(?i)" + "|".join(f"(?:{p})" for p in pats)) if pats else None


# Software selection's instruction says "Consult the system's software catalog", which dangles once
# the catalog is gone. This is the one edit that is not a deletion, and it is recorded as such.
REWRITE = [("installed software", re.compile(r"(?i)consult the system's software catalog and identify"),
            "Identify"),
           ("installed software", re.compile(r"(?i)consult the software catalog and identify"),
            "Identify")]


def head_of(line: str) -> str:
    """Normalised heading text of a line, or '' if the line is not a heading."""
    s = line.strip()
    if not s:
        return ""
    s = re.sub(r"^#+\s*", "", s)
    s = re.sub(r"^\*\*\s*", "", s)
    s = re.sub(r"\*\*\s*$", "", s)
    s = s.split(":", 1)[0].strip().rstrip("*").strip()
    low = s.lower()
    for h in HEADS:
        if low == h or low.startswith(h + " ") or low.startswith(h + "("):
            return h
    return ""


def sections(prompt: str) -> list[tuple[str, int, int]]:
    """(name, start, end) character spans, in order. A section runs to the next heading."""
    lines, pos, marks = prompt.splitlines(keepends=True), 0, []
    for ln in lines:
        h = head_of(ln)
        if h:
            marks.append((h, pos))
        pos += len(ln)
    out = []
    for i, (h, start) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else len(prompt)
        out.append((h, start, end))
    return out


def fenced_spans(prompt: str) -> list[tuple[int, int]]:
    """Spans of ``` fenced blocks, used to find worked examples that carry no heading."""
    out, open_at = [], None
    pos = 0
    for ln in prompt.splitlines(keepends=True):
        if ln.lstrip().startswith("```"):
            if open_at is None:
                open_at = pos
            else:
                out.append((open_at, pos + len(ln)))
                open_at = None
        pos += len(ln)
    return out


def clause_spans(body: str) -> list[tuple[int, int]]:
    """Split an instruction body into clauses: labelled (a).. if present, else paragraphs.

    Labels are not reliable — 3 Input-preparation rows and 1 Batch row carry none, because the
    generator inlined the rules as prose. So the split falls back to blank-line paragraphs, and
    the decision to drop is made on content either way.
    """
    first_nl = body.find("\n")               # never let a clause span cover the heading line
    floor = first_nl + 1 if first_nl >= 0 else 0
    head_sentences = []
    colon = body.find(":")
    if 0 <= colon < floor:                   # inline heading: split its tail into sentences
        pos = colon + 1
        for sent in re.split(r"(?<=[.;])\s+", body[colon + 1:floor]):
            if sent.strip():
                head_sentences.append((pos, pos + len(sent)))
            pos += len(sent) + 1
    marks = [m.start() for m in re.finditer(r"(?m)^[ \t]*\([a-z]\)\s", body) if m.start() >= floor]
    if len(marks) >= 2:
        return head_sentences + [(s, marks[i + 1] if i + 1 < len(marks) else len(body))
                                 for i, s in enumerate(marks)]
    out, pos = list(head_sentences), 0
    for para in re.split(r"(?<=\n)\n+", body):
        if para.strip() and pos >= floor:
            out.append((pos, pos + len(para)))
        pos += len(para)
    return out


def strip_prompt(prompt: str, subtask: str, arm: str) -> tuple[str, list[dict]]:
    """Return the stripped prompt and a manifest of every removed or rewritten span."""
    cuts: list[dict] = []                      # {start, end, text, why} in ORIGINAL coordinates
    wanted = STRIP[arm][subtask]

    for name, start, end in sections(prompt):
        if name in wanted:
            cuts.append({"start": start, "end": end, "text": prompt[start:end],
                         "why": f"section:{name}"})

    # A worked example folded into a neighbouring section keeps no heading of its own; it is
    # always a fenced block. Only Input prep and Batch carry examples.
    if "worked example" in wanted and not any(c["why"] == "section:worked example" for c in cuts):
        covered = lambda a, b: any(c["start"] <= a and b <= c["end"] for c in cuts)
        for a, b in fenced_spans(prompt):
            if not covered(a, b):
                cuts.append({"start": a, "end": b, "text": prompt[a:b],
                             "why": "fenced:unheaded worked example"})

    # Instruction clauses that name material this arm removed. Scoped to those topics only.
    ref = ref_pattern([w for w in wanted if w not in REWRITE_ONLY])
    if ref:
        for name, start, end in sections(prompt):
            if name != "instructions":
                continue
            body = prompt[start:end]
            for a, b in clause_spans(body):
                clause = body[a:b]
                if ref.search(clause) and not NOT_REFERENTIAL.search(clause):
                    cuts.append({"start": start + a, "end": start + b, "text": clause,
                                 "why": "clause:references stripped material"})

    # Swallow the blank lines left behind, so no post-hoc whitespace collapse is needed — a
    # collapse is not invertible, and --verify is worth more than tidy output.
    for c in cuts:
        e = c["end"]
        while e < len(prompt) and prompt[e] == "\n" and prompt[c["start"] - 1:c["start"]] == "\n":
            e += 1
        c["text"], c["end"] = prompt[c["start"]:e], e

    cuts.sort(key=lambda c: c["start"])
    out, prev = [], 0
    for c in cuts:
        if c["start"] < prev:                  # overlapping cuts: keep the first, drop the rest
            c["skipped"] = True
            continue
        out.append(prompt[prev:c["start"]])
        prev = c["end"]
    out.append(prompt[prev:])
    text = "".join(out)
    cuts = [c for c in cuts if not c.get("skipped")]

    edits = []                                 # (new, old) pairs, invertible by --verify
    for topic, pat, repl in REWRITE:           # the one non-deletion edit, recorded explicitly
        if topic not in wanted:
            continue
        m = pat.search(text)
        if m:
            edits.append((repl, m.group(0), m.start()))
            text = text[:m.start()] + repl + text[m.end():]

    labels = re.findall(r"(?m)^[ \t]*\(([a-z])\)\s", text)
    if labels and labels != [chr(ord("a") + i) for i in range(len(labels))]:
        for i, old in enumerate(labels):
            new = chr(ord("a") + i)
            if new != old:
                m = re.search(rf"(?m)^[ \t]*\({old}\)\s", text)
                if not m:
                    continue
                at = m.start() + m.group(0).index("(")
                edits.append((f"({new})", f"({old})", at))
                text = text[:at] + f"({new})" + text[at + 3:]
    for new, old, at in edits:
        cuts.append({"edit": [new, old], "at": at,
                     "why": "rewrite:dangling reference or clause relabel"})

    trimmed = text.rstrip()
    if trimmed != text:
        cuts.append({"tail": text[len(trimmed):], "why": "rstrip:trailing whitespace"})
    return trimmed + "\n", cuts


def rebuild(stripped: str, cuts: list[dict], original_len: int) -> str:
    """Reinsert every recorded span. Used by --verify; spans are in original coordinates."""
    pieces, prev = [], 0
    src_cuts = [c for c in cuts if "start" in c]           # tail/rewrite entries carry no span
    # Walk the original coordinate space, taking kept text from the stripped string in order.
    kept = []
    for c in src_cuts:
        kept.append((prev, c["start"]))
        prev = c["end"]
    kept.append((prev, original_len))
    pos = 0
    for i, (a, b) in enumerate(kept):
        pieces.append(("KEEP", a, b))
        if i < len(src_cuts):
            pieces.append(("CUT", src_cuts[i]))
    out, sp = [], 0
    for kind, *rest in pieces:
        if kind == "KEEP":
            a, b = rest
            out.append(("keep", b - a))
        else:
            out.append(("cut", rest[0]["text"]))
    # Reconstruct: consume the stripped text in order for KEEP runs, splice CUT text back.
    res, si = [], 0
    for kind, val in out:
        if kind == "keep":
            res.append(stripped[si:si + val])
            si += val
        else:
            res.append(val)
    return "".join(res)


def derive(arm: str) -> int:
    rows = [json.loads(l) for l in SRC.open()]
    dst = TRIN / f"samples_v8{arm}.jsonl"
    n_changed, problems = 0, []
    with dst.open("w") as f:
        for r in rows:
            text, cuts = strip_prompt(r["prompt"], r["subtask"], arm)
            out = dict(r)
            if text != r["prompt"]:
                n_changed += 1
            out["prompt"] = text
            out["arm"] = arm
            out["arm_sha"] = hashlib.sha256(text.encode()).hexdigest()[:12]
            out["strip_manifest"] = {"cuts": cuts, "base_len": len(r["prompt"])}
            f.write(json.dumps(out) + "\n")
            problems += check_row(out, r)
    print(f"  {dst.name}: {len(rows)} rows, {n_changed} changed")
    for p in problems:
        print(f"    !! {p}")
    return len(problems)


SECTIONS_REQUIRED = ("task", "workload", "instructions", "output")


def check_row(out: dict, base: dict) -> list[str]:
    """Every invariant that must hold before a single answer call is spent."""
    bad, p, tag = [], out["prompt"], f"{out['arm']} {out['app']}@{out['system']} {out['subtask']}"
    have = {h for h, _, _ in sections(p)}
    for need in SECTIONS_REQUIRED:
        if need not in have:
            bad.append(f"{tag}: lost section '{need}' — generate.py would mark this row leaked")
    for name in STRIP[out["arm"]][out["subtask"]]:
        if name in have:
            bad.append(f"{tag}: section '{name}' survived the strip")
    ref = ref_pattern(STRIP[out["arm"]][out["subtask"]])
    if ref:
        ins = next((p[s:e] for h, s, e in sections(p) if h == "instructions"), "")
        for m in ref.finditer(ins):
            if NOT_REFERENTIAL.search(ins[max(0, m.start() - 60):m.end() + 20]):
                continue
            frag = ins[max(0, m.start() - 45):m.start() + 45].replace("\n", " ")
            bad.append(f"{tag}: dangling reference — ...{frag}...")
    if len(p) >= len(base["prompt"]) and STRIP[out["arm"]][out["subtask"]]:
        bad.append(f"{tag}: nothing was removed")
    return bad


def verify(arm: str) -> int:
    base = {(r["subtask"], r["app"], r["system"]): r["prompt"]
            for r in (json.loads(l) for l in SRC.open())}
    path = TRIN / f"samples_v8{arm}.jsonl"
    if not path.exists():
        print(f"  {path.name} missing — run --derive first")
        return 1
    bad = 0
    for r in (json.loads(l) for l in path.open()):
        k = (r["subtask"], r["app"], r["system"])
        man = r["strip_manifest"]
        body = r["prompt"][:-1] if r["prompt"].endswith("\n") else r["prompt"]
        for c in reversed([c for c in man["cuts"] if "edit" in c]):
            new, old = c["edit"]
            at = c["at"]
            body = body[:at] + old + body[at + len(new):]
        tail = next((c["tail"] for c in man["cuts"] if "tail" in c), "")
        got = rebuild(body + tail, man["cuts"], man["base_len"])
        if got.strip() != base[k].strip():
            bad += 1
            print(f"    !! {arm} {k[1]}@{k[2]} {k[0]}: rebuild != base "
                  f"({len(got)} vs {len(base[k])} chars)")
    print(f"  {arm}: {'REVERSIBLE' if not bad else f'{bad} rows NOT reversible'}")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--derive", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--show", nargs=3, metavar=("ARM", "APP", "SYSTEM"))
    ap.add_argument("--arms", default="bare,cat")
    a = ap.parse_args()
    arms = a.arms.split(",")

    if a.show:
        arm, app, system = a.show
        for r in (json.loads(l) for l in (TRIN / f"samples_v8{arm}.jsonl").open()):
            if r["app"] == app and r["system"] == system:
                print(f"===== {r['subtask']} =====\n{r['prompt']}\n")
        return 0

    rc = 0
    if a.derive:
        for arm in arms:
            rc += derive(arm)
    if a.verify:
        for arm in arms:
            rc += verify(arm)
    if not (a.derive or a.verify):
        ap.print_help()
    return 1 if rc else 0


if __name__ == "__main__":
    sys.exit(main())
