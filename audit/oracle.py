#!/usr/bin/env python3
"""Freeze the deterministic verdict map for a corpus, so a refactor can be proved harmless.

The catalog rewrite (benchmark/catalog.py) touches the code path behind every deterministic check.
Nothing in it is *supposed* to change a verdict on the frozen corpus — the three files it
repairs are not in SUBSET — but "supposed to" is how `polaris/qe.yaml` went unnoticed for
months while `app_yaml()` swallowed its ParserError and returned `{}`.

So: snapshot every (model, subtask, app, system, requirement) -> verdict before the refactor,
and diff after each phase. A change that is not on the expected list is a regression, and the
diff names the rule rather than moving a pass count by one and leaving you to guess.

Only deterministic verdicts are captured. Judged verdicts move on their own (the judge's
test-retest instability is 12/141), so they cannot serve as an oracle.

Usage:
    python skills/trinity_oracle.py --snapshot --corpus v7
    python skills/trinity_oracle.py --diff     --corpus v7
    python skills/trinity_oracle.py --diff     --corpus v7 --expect expected_changes.txt
"""
from __future__ import annotations
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from judge.checks import evaluate, extraction_cache, cache_get, TRIN  # noqa: E402

SEP = "|"


def _key(model: str, subtask: str, app: str, system: str, rid: str) -> str:
    return SEP.join((model, subtask, app, system, rid))


def oracle_path(corpus: str) -> Path:
    return TRIN / f"oracle_{corpus}.json"


def build(corpus: str) -> dict[str, str]:
    """Evaluate every deterministic check over the frozen answers. No LLM calls."""
    cp = extraction_cache(corpus)
    cache = json.loads(cp.read_text()) if cp.exists() else {}
    rows = [json.loads(l) for l in (TRIN / f"answers_{corpus}.jsonl").open()]
    rows = [r for r in rows if r.get("answer")]

    out: dict[str, str] = {}
    for r in rows:
        # Mirrors trinity_checks.main()'s lookup exactly, so the oracle tracks the real code
        # path rather than a copy of it that can drift.
        ex = cache_get(cache, r["subtask"], r["model"], r["app"], r["system"])
        res = evaluate(r["subtask"], r["app"], r["system"], r["answer"], ex)
        for rid, v in res.items():
            out[_key(r["model"], r["subtask"], r["app"], r["system"], rid)] = v["verdict"]
    return out


def diff(old: dict[str, str], new: dict[str, str]) -> dict[str, list]:
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    changed = sorted(k for k in set(old) & set(new) if old[k] != new[k])
    return {"added": added, "removed": removed, "changed": changed}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="v7")
    ap.add_argument("--snapshot", action="store_true")
    ap.add_argument("--diff", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="overwrite an existing snapshot (refuses by default)")
    a = ap.parse_args()

    p = oracle_path(a.corpus)

    if a.snapshot:
        if p.exists() and not a.force:
            print(f"refusing to overwrite {p.name} — the oracle is only meaningful if it "
                  f"predates the changes it judges. Pass --force if you mean it.")
            return 1
        cur = build(a.corpus)
        p.write_text(json.dumps(cur, indent=0, sort_keys=True))
        by_v = Counter(cur.values())
        print(f"wrote {p.name}: {len(cur)} deterministic verdicts")
        for k in ("satisfied", "violated", "not_applicable", "not_evaluated"):
            print(f"  {k:<16}{by_v[k]:>5}")
        return 0

    if a.diff:
        if not p.exists():
            print(f"no snapshot at {p.name} — run --snapshot first")
            return 1
        old = json.loads(p.read_text())
        new = build(a.corpus)
        d = diff(old, new)
        n = sum(len(v) for v in d.values())
        if not n:
            print(f"{len(new)} verdicts, ZERO changes against {p.name}")
            return 0

        print(f"{len(new)} verdicts, {n} differences against {p.name}\n")
        for kind in ("changed", "added", "removed"):
            rows = d[kind]
            if not rows:
                continue
            # Group by requirement id — the rule is the unit that gets edited.
            by_req: dict[str, list[str]] = {}
            for k in rows:
                by_req.setdefault(k.rsplit(SEP, 1)[1], []).append(k)
            print(f"{kind.upper()}  ({len(rows)})")
            for rid, ks in sorted(by_req.items(), key=lambda kv: -len(kv[1])):
                if kind == "changed":
                    trans = Counter(f"{old[k]} -> {new[k]}" for k in ks)
                    for t, c in trans.most_common():
                        print(f"   {rid:<44}{c:>3}  {t}")
                else:
                    print(f"   {rid:<44}{len(ks):>3}")
            print()
        return 2

    ap.error("pass --snapshot or --diff")


if __name__ == "__main__":
    sys.exit(main())
