#!/usr/bin/env python3
"""How many `values_match_physical_system` violations could a checker catch mechanically?

WHY THIS EXISTS, AND WHAT IT IS NOT. `INP.common.values_match_physical_system` is the largest
single defect in the benchmark — 21 of the 29 failing Input-preparation cells in the rich arm
violate it, and it is the #1 rule for all four models. It is judge-decided, and the question
that sizes every possible fix is whether a machine could have caught the same thing.

This is a PROBE, not a rule and not a judge. It runs candidate checks over the frozen answers
and reports how often each one independently reproduces a violation the judge already found.
It decides nothing and is wired into no grading path. The point is to replace a guess ("some of
these look mechanical") with a count, before anyone builds a validator on the strength of the
guess.

READ THE RESULT NARROWLY. A check firing where the judge fired means the defect is DETECTABLE.
It does not mean a model handed that feedback would fix it — the same corpus shows models
computing a constraint correctly, writing "FAIL", and then proceeding anyway. Detectability is
a precondition for the tool-assisted experiment, not evidence that it would work.

Usage:
    python -m audit.arith_probe
"""
from __future__ import annotations

import collections
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "corpus" / "v8"
RULE = "INP.common.values_match_physical_system"
AVOGADRO = 6.02214076e23
AMU_PER_ELECTRON_MASS = 1822.888486         # QMCPACK masses are in electron masses


def _num(s: str) -> float | None:
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def check_md_duration(ans: str, want: str) -> str | None:
    """nsteps x dt against the duration the workload asks for. Pure multiplication."""
    ns = re.search(r"(?mi)^\s*nsteps\s*=\s*([0-9]+)", ans)
    dt = re.search(r"(?mi)^\s*dt\s*=\s*([0-9.eE+-]+)", ans)
    tgt = re.search(r"([0-9.]+)\s*ns\b", want)
    if not (ns and dt and tgt):
        return None
    got = int(ns.group(1)) * (_num(dt.group(1)) or 0) / 1000.0     # dt is ps -> ns
    exp = _num(tgt.group(1))
    if exp and got and abs(got - exp) / exp > 0.05:
        return f"nsteps*dt = {got:g} ns, workload asks {exp:g} ns"
    return None


def check_molarity(ans: str, want: str) -> str | None:
    """Ion concentration from cubic box edge and ion count. n/(V*NA)."""
    box = re.findall(r"(?m)^\s*([0-9]+\.[0-9]+)\s+\1\s+\1\s*$", ans)      # cubic gro box line
    na = re.search(r"(?mi)^\s*(?:NA|Na\+?)\s+([0-9]+)\s*$", ans)
    tgt = re.search(r"([0-9.]+)\s*M\b", want)
    if not (box and na and tgt):
        return None
    edge_nm = _num(box[-1])
    vol_l = (edge_nm * 1e-8) ** 3 / 1000.0 * 1000.0                       # nm^3 -> L
    vol_l = (edge_nm ** 3) * 1e-24                                        # nm^3 -> L directly
    got = int(na.group(1)) / (vol_l * AVOGADRO)
    exp = _num(tgt.group(1))
    if exp and got and abs(got - exp) / exp > 0.10:
        return f"{na.group(1)} ions in a {edge_nm} nm box = {got:.3f} M, workload asks {exp:g} M"
    return None


def check_declared_count(ans: str, want: str) -> str | None:
    """A declared count against the entries actually written (QE nat, QMCPACK size)."""
    nat = re.search(r"(?mi)\bnat\s*=\s*([0-9]+)", ans)
    if not nat:
        return None
    m = re.search(r"(?mis)ATOMIC_POSITIONS[^\n]*\n(.*?)(?:\n\s*\n|\nK_POINTS|\Z)", ans)
    if not m:
        return None
    rows = [l for l in m.group(1).splitlines()
            if re.match(r"\s*[A-Z][a-z]?\s+[-0-9.]", l)]
    if rows and int(nat.group(1)) != len(rows):
        return f"nat = {nat.group(1)} but {len(rows)} ATOMIC_POSITIONS lines written"
    return None


def check_qmcpack_mass(ans: str, want: str) -> str | None:
    """A mass given in amu where QMCPACK wants electron masses is off by ~1823x."""
    for m in re.finditer(r'mass\s*=\s*"([0-9.]+)"', ans):
        v = _num(m.group(1))
        if v and 1.0 < v < 300.0:        # an amu-scale value in a field that wants m_e
            return (f'mass="{m.group(1)}" is amu-scale; QMCPACK wants electron masses '
                    f"(~{v * AMU_PER_ELECTRON_MASS:.0f})")
    return None


def check_duplicate_sites(ans: str, want: str) -> str | None:
    """Repeated coordinate triples WITHIN one structure block.

    Scoped to a single block on purpose. Run over the whole answer it fired on the NWChem
    sweep, where the deck is ten separate water molecules and the oxygen sits at the origin in
    every one — ten legitimate copies of `0.0 0.0 0.0`. It happened to land on two genuinely
    violated cells, which is exactly the kind of right-for-the-wrong-reason hit that makes a
    detection count meaningless if left in.
    """
    blocks = re.split(r"(?mi)^\s*(?:geometry|ATOMIC_POSITIONS|<particleset)\b", ans)
    for blk in blocks[1:]:
        blk = blk[:4000]
        trip = re.findall(r"(?m)^\s*(?:[A-Z][a-z]?\s+)?(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+"
                          r"(-?\d+\.\d+)\s*$", blk)
        if len(trip) < 8:
            continue
        dup = [t for t, n in collections.Counter(trip).items() if n > 1]
        if dup:
            return f"{len(dup)} coordinate triple(s) repeated in one structure, e.g. {' '.join(dup[0])}"
    return None


def check_bond_geometry(ans: str, want: str) -> str | None:
    """Bond angle recomputed from the Cartesian coordinates actually written.

    The workload fixes an angle ("H-O-H angle fixed at 104.5 degrees") and the answer writes
    coordinates. Whether they agree is trigonometry, not chemistry.
    """
    tgt = re.search(r"angle\D{0,30}?([0-9]{2,3}\.[0-9])\s*(?:deg|°)", want, re.I)
    if not tgt:
        return None
    exp = _num(tgt.group(1))
    for blk in re.split(r"(?mi)^\s*geometry\b", ans)[1:]:
        atoms = re.findall(r"(?m)^\s*([A-Z][a-z]?)\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s+"
                           r"(-?\d+\.?\d*)\s*$", blk[:1200])
        cen = [a for a in atoms if a[0] == "O"]
        out = [a for a in atoms if a[0] == "H"]
        if len(cen) != 1 or len(out) != 2:
            continue
        o = [float(x) for x in cen[0][1:]]
        v = [[float(x) - y for x, y in zip(h[1:], o)] for h in out]
        n = [math.dist(w, [0, 0, 0]) for w in v]
        if min(n) < 1e-6:
            return "two atoms share a position, so no bond angle is defined"
        cos = sum(a * b for a, b in zip(*v)) / (n[0] * n[1])
        got = math.degrees(math.acos(max(-1.0, min(1.0, cos))))
        if abs(got - exp) > 0.15:
            return f"coordinates give an angle of {got:.2f} deg, workload fixes it at {exp} deg"
    return None


CHECKS = {
    "md_duration":     check_md_duration,
    "molarity":        check_molarity,
    "declared_count":  check_declared_count,
    "qmcpack_mass":    check_qmcpack_mass,
    "duplicate_sites": check_duplicate_sites,
    "bond_geometry":   check_bond_geometry,
}


def main() -> int:
    samples = {(r["subtask"], r["app"], r["system"]): r
               for r in map(json.loads, (CORPUS / "samples_v8rich.jsonl").open())}
    answers = {(r["subtask"], r["app"], r["system"], r["model"]): r.get("answer") or ""
               for r in map(json.loads, (CORPUS / "answers_v8rich.jsonl").open())}

    verd = collections.defaultdict(list)
    for i in (1, 2, 3):
        for g in map(json.loads,
                     (CORPUS / f"grades_v8rich__gpt56terra__r27__SKILLMODE__run{i}.jsonl").open()):
            if g["subtask"] == "Input preparation":
                verd[(g["subtask"], g["app"], g["system"], g["model"])].append(
                    (g.get("requirements") or {}).get(RULE, {}).get("verdict"))

    viol = {k for k, v in verd.items() if v.count("violated") >= 2}
    clean = set(verd) - viol
    hit_v, hit_c, detail = set(), set(), []
    for k in verd:
        want = samples[(k[0], k[1], k[2])]["prompt"]
        for name, fn in CHECKS.items():
            try:
                msg = fn(answers.get(k, ""), want)
            except Exception:
                msg = None
            if msg:
                (hit_v if k in viol else hit_c).add(k)
                if k in viol:
                    detail.append(f"    {k[3]:<18}{k[1]}@{k[2]:<12}[{name}] {msg}")
                break

    print(f"{RULE}, rich arm, Input preparation\n")
    print(f"  judge says violated : {len(viol)} cells")
    print(f"  judge says clean    : {len(clean)} cells\n")
    print(f"  probe fires on      : {len(hit_v)}/{len(viol)} violated "
          f"({len(hit_v)/max(1,len(viol)):.0%} detected)")
    print(f"  probe false alarms  : {len(hit_c)}/{len(clean)} clean cells\n")
    print("  detected:")
    print("\n".join(sorted(detail)) or "    (none)")
    print("\n  NOTE: five hand-written checks, not a validator. Detection is a lower bound on")
    print("  what is mechanisable, and says nothing about whether a model would act on it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
