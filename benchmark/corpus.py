#!/usr/bin/env python3
"""Freeze a named corpus so "the v6 results" means one specific set of bytes.

Judge work only produces trustworthy numbers when the answers being judged cannot move
underneath it. Two measurements are otherwise conflated:

    model quality   varies with model sampling   ~3 points per 10-sample cell, measured
    judge quality   varies only with the rubric  ~0, IF the answers are frozen

A 10-sample cell moved 3 points between two runs of byte-identical prompts (Software
selection, nemotron: 8/10 -> 5/10, no truncation involved). So any rubric comparison run on
freshly sampled answers is measuring the model, not the rubric. Freezing removes that term
entirely and lets a rubric change be assessed by a paired test on the same items.

A corpus is the sample file, the answer file, the exact set of (model, subtask, app, system)
keys, the token cap each model ran under, and a sha256 of each file. `--verify` re-hashes and
fails loudly, because a silent edit to an answers file invalidates every grade derived from it
and the existing `.bak` files show in-place editing has happened before.

Usage:
    python skills/trinity_corpus.py --freeze v6
    python skills/trinity_corpus.py --verify v6
    python skills/trinity_corpus.py --list
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from benchmark._run_base import max_tokens_for  # noqa: E402

TRIN = ROOT / "data" / "corpus" / "v8"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def load(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.open()] if path.exists() else []


def freeze(ver: str) -> int:
    samples_p, answers_p = TRIN / f"samples_{ver}.jsonl", TRIN / f"answers_{ver}.jsonl"
    for p in (samples_p, answers_p):
        if not p.exists():
            print(f"missing {p}")
            return 1
    samples, answers = load(samples_p), load(answers_p)
    usable = [a for a in answers if a.get("answer") and not a.get("error")]

    keys = sorted({(a["model"], a["subtask"], a["app"], a["system"]) for a in usable})
    models = sorted({k[0] for k in keys})
    manifest = {
        "corpus": ver,
        "frozen_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "samples": {"path": samples_p.name, "sha256": sha256(samples_p), "n": len(samples)},
        "answers": {"path": answers_p.name, "sha256": sha256(answers_p),
                    "n_rows": len(answers), "n_usable": len(usable)},
        "models": models,
        "max_tokens": {m: max_tokens_for(m) for m in models},
        "by_subtask": dict(Counter(s["subtask"] for s in samples)),
        "coverage": {m: sum(1 for k in keys if k[0] == m) for m in models},
        # Keys are the unit every grade row joins on, so they are part of the frozen identity.
        "keys": ["::".join(k) for k in keys],
    }
    out = TRIN / f"corpus_{ver}.json"
    out.write_text(json.dumps(manifest, indent=1))
    print(f"froze {ver}: {len(samples)} samples, {len(usable)} usable answers, "
          f"{len(models)} models -> {out.name}")
    for m in models:
        print(f"   {m:18} {manifest['coverage'][m]:>3}/{len(samples)} answers  "
              f"max_tokens={manifest['max_tokens'][m]}")
    missing = len(samples) * len(models) - len(keys)
    if missing:
        print(f"   note: {missing} (model, sample) cells have no usable answer")
    return 0


def verify(ver: str) -> int:
    man_p = TRIN / f"corpus_{ver}.json"
    if not man_p.exists():
        print(f"no manifest for {ver} — run --freeze first")
        return 1
    man = json.loads(man_p.read_text())
    bad = []
    for part in ("samples", "answers"):
        p = TRIN / man[part]["path"]
        if not p.exists():
            bad.append(f"{part}: {p.name} is gone")
        elif sha256(p) != man[part]["sha256"]:
            bad.append(f"{part}: {p.name} changed since freeze "
                       f"({man[part]['sha256']} -> {sha256(p)})")
    if bad:
        print(f"CORPUS {ver} HAS DRIFTED — grades derived from it are not comparable:")
        for b in bad:
            print(f"   {b}")
        return 1
    print(f"corpus {ver} intact: {man['samples']['n']} samples, "
          f"{man['answers']['n_usable']} usable answers, frozen {man['frozen_at']}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--freeze", metavar="VER")
    ap.add_argument("--verify", metavar="VER")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.freeze:
        return freeze(a.freeze)
    if a.verify:
        return verify(a.verify)
    if a.list or True:
        for p in sorted(TRIN.glob("corpus_*.json")):
            m = json.loads(p.read_text())
            print(f"{m['corpus']:8} {m['samples']['n']:>3} samples  "
                  f"{m['answers']['n_usable']:>3} answers  {len(m['models'])} models  "
                  f"frozen {m['frozen_at'][:10]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
