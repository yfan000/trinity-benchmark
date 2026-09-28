#!/usr/bin/env python3
"""Validate a generated input deck against the grammar its application publishes.

Supersedes `audit/par_validate.py`, which was nekRS-only and carried a bug bad enough to
invalidate its own numbers — see FENCE BUG below.

WHY. `INP.common.no_invented_keywords` is fatal, fires 11 times in the augmented arm, and is
judge-decided, so every verdict is a language model asserting from pre-training what a parser
would settle. Supplying the grammar in the prompt was measured and only half worked: closing
the list of SECTIONS stopped 2 of 4 models inventing sections, and the other 2 moved the
invention down to KEYS. Closing the other half in the prompt means pasting a reference manual,
which this repo has already learned makes decks worse. Checking costs nothing in the prompt.

THREE THINGS IT DELIBERATELY DOES NOT DO.

FENCE BUG, fixed here and the reason for the rewrite. par_validate extracted ``` blocks and
scanned those. One QE answer opens a fence and never closes it, so its deck fell outside every
captured block and the checker returned CLEAN on an answer containing thirty invented
variables. Every one of these formats is self-delimiting — `&NAME ... /`, `[SECTION]` — so the
whole answer is scanned and fences are ignored entirely. The nekRS figures reported before this
fix are a lower bound.

VERSION, which has already caused a real defect. nekRS renamed [VELOCITY]/[PRESSURE] to
[FLUID VELOCITY]/[FLUID PRESSURE] between v23 and master, and the catalog installs BOTH —
aurora records v23, polaris "next", frontier "git-main". A grammar taken from master will call
correct v23 syntax invented, which is exactly how a wrong spelling got into
format_contracts.yaml. Every grammar records the ref it came from; where the installed version
differs, findings are reported as VERSION-SENSITIVE and never as errors.

DEPRECATION IS NOT INVENTION, and this tool does not pretend to tell them apart. GROMACS answers
use `ns_type`, `nstxtcout`, `title` and `pmeorder`, none of which appear in the current
mdp-options.rst. They were valid in older releases. Asserting "deprecated" would mean me
supplying a list from recollection — the precise habit that put the wrong nekRS sections into
the contract. So the finding is stated as what it is: NOT IN the reference version named, with
the version printed. Resolving it needs the older reference fetched, not an opinion.

Usage:
    python -m audit.grammar_check --corpus
    python -m audit.grammar_check --app qe --file deck.in
"""
from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
GRAM = ROOT / "data" / "grammars"
CORPUS = ROOT / "data" / "corpus" / "v8"

GRAMMARS = {"nekrs": "nekrs_par.yaml", "qe": "qe_pw_in.yaml", "gromacs": "gromacs_mdp.yaml"}
# Sections this grammar knows under another name in an older release. Reported, never an error.
RENAMED_NEKRS = {"VELOCITY": "FLUID VELOCITY", "PRESSURE": "FLUID PRESSURE"}


def grammar(app: str) -> dict | None:
    """The vendored grammar for `app`, or None when there is none.

    The membership test is load-bearing: `GRAM / ""` is the grammars DIRECTORY, whose .exists()
    is True, so an unmapped application (qmcpack, alphafold, vllm, pytorch — most of them) hit
    read_text() on a directory and raised instead of returning None.
    """
    if app not in GRAMMARS:
        return None
    f = GRAM / GRAMMARS[app]
    return yaml.safe_load(f.read_text()) if f.exists() else None


def _fold(s: str) -> str:
    return s.strip().lower()


def _sep(s: str) -> str:
    """GROMACS and friends treat - and _ as the same character. They do NOT ignore separators:
    `pme-order` and `pme_order` are one key, `pmeorder` is a different (nonexistent) one."""
    return _fold(s).replace("-", "_")


def classify(app: str, token: str, installed: str | None = None) -> tuple[str, str]:
    """Was this token REMOVED from the grammar, or was it never in it?

    Derived by diffing adjacent upstream releases, never asserted. A token present in one
    release and absent from the next was removed in between; that is a fact about two files.
    Tokens absent from every release we hold are reported as such and NOT called invented —
    `title` and `nstxtcout` predate the oldest reference fetched, so this method cannot
    classify them and says so rather than guessing.

    The verdict is unaffected either way: a key removed in 2021 is still an error on a 2024
    install. This changes the EXPLANATION, which is what a reader needs to act on.
    """
    f = GRAM / f"{app}_versions.yaml"
    if not f.exists():
        return "unclassified", "no versioned grammar for this application"
    d = yaml.safe_load(f.read_text())
    want = _sep(token)
    for k, v in (d.get("removed") or {}).items():
        if _sep(k.split(":")[-1]) == want:
            inst = f" (installed {installed})" if installed else ""
            return "removed", (f"real in {v['last_seen']}, removed by {v['gone_by']}"
                               f"{inst} — not a fabrication, but not valid here either")
    oldest = (d.get("installed_versions_in_catalog") or ["?"])[0]
    return "absent", f"in no release we hold (oldest fetched: {oldest})"


def check_qe(text: str, g: dict) -> list[str]:
    """&NAMELIST ... / is self-delimiting; scan the whole answer.

    Also checks CARD ARGUMENTS, which the first version could not see. The judge caught
    `K_POINTS (mp)` — a real card taking an option that does not exist — and the checker passed
    it, because it validated namelist variables only. INPUT_PW.def declares each card's legal
    arguments as an `enum`, so this is a lookup like the rest.
    """
    known = {_fold(n): {_fold(v) for v in vs} for n, vs in g["namelists"].items()}
    cards = {_fold(c): {_fold(v) for v in vs} for c, vs in (g.get("card_options") or {}).items()}
    out, cur = [], None
    for ln in text.splitlines():
        s = ln.split("!")[0].strip()
        if (m := re.match(r"^&(\w+)", s)):
            cur = _fold(m.group(1))
            continue
        if s == "/":
            cur = None
            continue
        # A card line: NAME followed by an optional argument, bare or parenthesised/braced.
        if (m := re.match(r"^([A-Z][A-Z_]{3,})\b[ \t]*[({]?\s*([A-Za-z_][\w./^]*)?\s*[)}]?\s*$", s)):
            name, arg = _fold(m.group(1)), m.group(2)
            if name in cards:
                cur = None                       # a card closes any open namelist
                if arg and _fold(arg) not in cards[name]:
                    out.append(f"{m.group(1)}: option {arg!r} "
                               f"(accepts {', '.join(sorted(cards[name]))})")
                continue
        if cur in known and (m := re.match(r"^([A-Za-z_]\w*)\s*(?:\([^)]*\))?\s*=", s)):
            if _fold(m.group(1)) not in known[cur]:
                out.append(f"&{cur.upper()}: {m.group(1)}")
    return sorted(set(out))


def check_gromacs(text: str, g: dict) -> list[str]:
    """.mdp is flat. Hyphen and underscore are interchangeable."""
    known = {_fold(k).replace("-", "_") for k in g["flat_keys"]}
    out = []
    for ln in text.splitlines():
        s = ln.split(";")[0].strip()
        if (m := re.match(r"^([A-Za-z][\w-]*)\s*=", s)):
            if _fold(m.group(1)).replace("-", "_") not in known:
                out.append(m.group(1))
    return sorted(set(out))


def check_nekrs(text: str, g: dict) -> tuple[list[str], list[str]]:
    known = {_fold(k): {_fold(x) for x in v} for k, v in g["sections"].items()}
    pats = [(re.compile(p["pattern"], re.I), {_fold(k) for k in p["keys"]})
            for p in g["section_patterns"]]
    common = {_fold(k) for k in g["common_field_keys"]}
    field = {_fold(f) for f in g["field_sections"]}
    declared = {_fold(v) for m in re.finditer(r"(?mi)^\s*userSections\s*=([^\n]*)", text)
                for v in re.split(r"[,\s]+", m.group(1)) if v.strip()}
    out, ver, cur = [], [], ""
    for ln in text.splitlines():
        s = ln.split("#")[0].strip()
        if (m := re.match(r"^\[([^\]]+)\]$", s)):
            cur = m.group(1).strip()
            f = _fold(cur)
            if f in known or any(p.match(cur) for p, _ in pats) or f in declared:
                continue
            if f.upper() in RENAMED_NEKRS:
                ver.append(f"[{cur}] is the pre-v24 name for [{RENAMED_NEKRS[f.upper()]}]")
            else:
                out.append(f"section [{cur}]")
        elif (m := re.match(r"^([A-Za-z_][\w./<>-]*)\s*=", s)):
            f, k = _fold(cur), _fold(m.group(1))
            if not cur:
                # A key before any [SECTION]. This used to `continue`, and it is the single
                # largest gap the two-judge adjudication exposed: four nekRS decks wrote bare
                # KEY = value with no sections at all (ELEMENT_ORDER, TIME_STEP, param(1),
                # lx1, lelg), the judge called every one invented, and the parser reported
                # clean because it never looked. .par requires [GENERAL], so a key outside any
                # section is malformed whatever the key is named.
                if k not in {_fold(x) for x in g["toplevel_keys"]}:
                    out.append(f"{m.group(1)} outside any section")
                continue
            if f in declared:
                continue
            allowed = set(known.get(f, ()))
            for p, ks in pats:
                if p.match(cur):
                    allowed |= ks
            if f in field or any(p.match(cur) for p, _ in pats):
                allowed |= common
            if f.upper() in RENAMED_NEKRS:
                allowed |= known.get(_fold(RENAMED_NEKRS[f.upper()]), set()) | common
            if allowed and k not in allowed:
                out.append(f"[{cur}] {m.group(1)}")
    return sorted(set(out)), sorted(set(ver))


def validate(app: str, text: str) -> dict | None:
    g = grammar(app)
    if not g:
        return None
    if app == "nekrs":
        bad, ver = check_nekrs(text, g)
    else:
        bad = {"qe": check_qe, "gromacs": check_gromacs}[app](text, g)
        ver = []
    return {"app": app, "unknown": bad, "version_sensitive": ver,
            "ref": f"{g['source']['repo']}@{g['source']['ref']}"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", action="store_true")
    ap.add_argument("--app", choices=sorted(GRAMMARS))
    ap.add_argument("--file")
    a = ap.parse_args()
    if a.file:
        r = validate(a.app, Path(a.file).read_text())
        print(json.dumps(r, indent=1))
        return 1 if r and r["unknown"] else 0
    if not a.corpus:
        ap.error("pass --corpus or --app/--file")

    import sys
    sys.path.insert(0, str(ROOT))
    from benchmark.generate import app_yaml
    for app in sorted(GRAMMARS):
        g = grammar(app)
        print(f"\n=== {app}  vs {g['source']['repo']}@{g['source']['ref']} "
              f"({g['source']['path']}) ===")
        n = tot = 0
        for arm in ("bare", "base", "rich"):
            p = CORPUS / f"answers_v8{arm}.jsonl"
            for row in map(json.loads, p.open()):
                if row.get("subtask") != "Input preparation" or row.get("app") != app:
                    continue
                tot += 1
                r = validate(app, row.get("answer") or "")
                inst = (app_yaml(row["system"], app) or {}).get("version") or "?"
                if r["unknown"]:
                    n += 1
                    print(f"  {arm}/{row['model']:<18}installed {inst:<10}"
                          f"{len(r['unknown'])} not in reference: "
                          f"{', '.join(r['unknown'][:5])}" + (" …" if len(r['unknown']) > 5 else ""))
                for v in r["version_sensitive"]:
                    print(f"  {arm}/{row['model']:<18}installed {inst:<10}VERSION-SENSITIVE: {v}")
        print(f"  -> {n}/{tot} answers use syntax absent from the reference version")
    print("\n  A probe. Decides nothing, wired into no grading path. 'Absent from the reference'")
    print("  is NOT the same as invented — see the DEPRECATION note in this file's docstring.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
