#!/usr/bin/env python3
"""Classify every recorded defect in the v2 run, and say what could actually fix it.

Counting defects is easy and nearly useless on its own: the number that matters is how many
are reachable by changing the prompt, versus how many are the model not knowing the science,
versus how many are the judge being wrong. The last category is real and unmeasured — Opus 5
has never been checked against a human here, and three miscalibrations have already been
found by reading its output — so it gets a label rather than being silently counted against
the models.

Each defect is tagged twice:
  category   what kind of mistake it is
  fixable    prompt      a better prompt could plausibly prevent it
             capability  the model does not know the domain fact; no prompt supplies it
             judge       the objection is wrong or out of scope; the answer was fine
             ambiguous   genuinely unclear from the defect text alone

Usage:
    python skills/trinity_errors.py --classify
    python skills/trinity_errors.py --report
"""
from __future__ import annotations
import argparse, json, re, sys, threading
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import judge  # noqa: E402
from skills.trinity_task_spec import SUBTASKS  # noqa: E402

TRIN = ROOT / "results" / "skills" / "trinity"
GRADES = TRIN / "grades_v2.jsonl"
OUT = TRIN / "defects_v2.json"
BATCH = 18

CATEGORIES = {
 "invented-syntax":      "a keyword, directive or flag that does not exist in that format",
 "format-structure":     "right vocabulary, wrong file structure: required lines missing, "
                         "positional order broken, sections in the wrong place",
 "domain-value-wrong":   "a scientifically wrong value: geometry, cutoff, functional, "
                         "basis set, physical parameter",
 "fabricated-evidence":  "cites a timing, scaling or benchmark figure that appears nowhere "
                         "in the prompt",
 "arithmetic":           "the numbers do not follow from each other",
 "ignored-supplied-fact":"contradicts or fails to use a fact the prompt explicitly gave",
 "queue-illegality":     "the request violates the queue limits stated in the prompt, or "
                         "names a queue that does not exist",
 "layout-mismatch":      "rank / GPU / thread layout inconsistent with the hardware or with "
                         "the application's build defaults",
 "missing-artifact":     "a required file, section or deliverable is simply absent",
 "scope-violation":      "did something the subtask explicitly excluded",
 "vacuous-self-check":   "asserted that it verified something without actually verifying it",
 "copied-from-example":  "carried values, species or comment headers out of the worked example",
 "unsupported-claim":    "a confident assertion with no basis given, not a number",
 "other":                "does not fit the above",
}

PROMPT = """You are auditing a grading run on an HPC agent benchmark. Below are defects a
judge recorded against model answers for the subtask "{subtask}".

Subtask goal: {goal}
What the prompt already supplies to the model: {supplies}

For EACH numbered defect, return a category and a fixability verdict.

Categories (use the exact key):
{cats}

Fixability — be strict and honest here:
  "prompt"     — a change to the PROMPT could plausibly prevent this. Only if the fix is a
                 rule or a fact that can be written into a prompt. Say which change, briefly.
  "capability" — the model does not know the domain fact, or cannot construct the artifact.
                 No prompt supplies competence. Most wrong scientific values are this.
  "judge"      — the objection is wrong, out of scope for what the subtask asked, or
                 penalises something the answer was right to do. The judge is NOT assumed
                 correct; flag these.
  "ambiguous"  — cannot tell from the defect text alone.

Return ONLY a JSON array, one object per defect, in order:
[{{"n": 1, "category": "...", "fixable": "...", "fix": "<short phrase, or empty>"}}]

Defects:
{items}"""


def load() -> list[dict]:
    return [json.loads(l) for l in GRADES.open()]


def supplies(st: str) -> str:
    return {
     "Software selection": "the full list of software installed on that system",
     "Input preparation": "the chosen application, the required-file inventory, the physical "
                          "system to model, and a real input deck for a DIFFERENT system as a "
                          "form-only example",
     "Resource selection": "the chosen application, the machine's hardware and full queue "
                           "table with node and walltime limits, the application's build "
                           "defaults and scaling notes, and the physical system size",
     "Batch job creation": "the chosen application, the input files already produced, the "
                           "allocation already decided, the site's module lines, the "
                           "scheduler's site conventions, a complete worked script for a "
                           "different application, and the project account",
    }[st]


def classify(workers: int) -> None:
    grades = load()
    flat = []
    for g in grades:
        for e in g.get("errors", []):
            flat.append({"subtask": g["subtask"], "model": g["model"], "app": g["app"],
                         "system": g["system"], "text": " ".join(str(e).split())})
    print(f"{len(flat)} defects to classify, {workers} workers")

    batches = []
    for st in SUBTASKS:
        rows = [d for d in flat if d["subtask"] == st]
        for i in range(0, len(rows), BATCH):
            batches.append((st, rows[i:i + BATCH]))

    cats = "\n".join(f"  {k} — {v}" for k, v in CATEGORIES.items())
    lock, done = threading.Lock(), [0]

    def one(job):
        st, rows = job
        items = "\n".join(f"{i+1}. {r['text']}" for i, r in enumerate(rows))
        p = PROMPT.format(subtask=st, goal=SUBTASKS[st]["goal"], supplies=supplies(st),
                          cats=cats, items=items)
        try:
            msg = judge._get_client().messages.create(
                model=judge.TRINITY_JUDGE_MODEL, max_tokens=4000,
                messages=[{"role": "user", "content": p}])
            raw = judge._text_of(msg)
            m = re.search(r"\[.*\]", raw, re.DOTALL)
            arr = json.loads(m.group()) if m else []
        except Exception as e:
            print(f"   ! {st}: {type(e).__name__}")
            arr = []
        for a in arr:
            i = a.get("n", 0) - 1
            if 0 <= i < len(rows):
                rows[i].update(category=a.get("category", "other"),
                               fixable=a.get("fixable", "ambiguous"),
                               fix=a.get("fix", ""))
        with lock:
            done[0] += 1
            print(f"   {done[0]}/{len(batches)}  {st}", flush=True)
        return rows

    out = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for fut in as_completed([pool.submit(one, b) for b in batches]):
            out += fut.result()
    OUT.write_text(json.dumps(out, indent=1))
    n = sum(1 for d in out if d.get("category"))
    print(f"{n}/{len(out)} classified -> {OUT}")


def report() -> None:
    d = json.loads(OUT.read_text())
    d = [x for x in d if x.get("category")]
    print(f"{len(d)} classified defects\n")

    print("FIXABILITY, overall")
    tot = Counter(x["fixable"] for x in d)
    for k, n in tot.most_common():
        print(f"  {k:<12}{n:>5}{n/len(d):>7.0%}")

    print("\nFIXABILITY by subtask")
    order = ["prompt", "capability", "judge", "ambiguous"]
    print(f"{'subtask':<22}" + "".join(f"{k:>13}" for k in order) + f"{'n':>7}")
    for st in SUBTASKS:
        r = [x for x in d if x["subtask"] == st]
        c = Counter(x["fixable"] for x in r)
        print(f"{st:<22}" + "".join(f"{f'{c[k]} ({c[k]/len(r):.0%})':>13}" for k in order)
              + f"{len(r):>7}")

    print("\nCATEGORY by subtask (top 5 each)")
    for st in SUBTASKS:
        r = [x for x in d if x["subtask"] == st]
        print(f"\n  {st}  ({len(r)} defects)")
        for cat, n in Counter(x["category"] for x in r).most_common(5):
            fx = Counter(x["fixable"] for x in r if x["category"] == cat)
            tag = ", ".join(f"{k} {v}" for k, v in fx.most_common())
            print(f"    {n:>4}  {cat:<24} [{tag}]")

    print("\nPROPOSED PROMPT FIXES, by how many defects they would reach")
    fixes = defaultdict(list)
    for x in d:
        if x["fixable"] == "prompt" and x.get("fix"):
            fixes[(x["subtask"], x["fix"].strip().lower()[:70])].append(x)
    for (st, fx), rows in sorted(fixes.items(), key=lambda kv: -len(kv[1]))[:18]:
        print(f"  {len(rows):>3}  [{st[:18]:<18}] {fx}")

    print("\nDEFECTS THE JUDGE MAY HAVE GOT WRONG (sample)")
    for x in [x for x in d if x["fixable"] == "judge"][:12]:
        print(f"  [{x['subtask'][:14]:<14}] {x['text'][:104]}")


# ---------------------------------------------------------------------------------------
CLUSTER = """Below are individual fix suggestions written against separate defects on the
HPC subtask "{subtask}". They are repetitive and over-specific.

Consolidate them into AT MOST 6 concrete prompt rules, ordered by how many of the listed
defects each would prevent. A rule must be something that can literally be written into a
prompt as an instruction to the answering model. Merge near-duplicates aggressively.

Reject any suggestion that amounts to "know the domain better" — that is not a prompt rule.

Return ONLY JSON:
[{{"rule": "<the instruction, one sentence, imperative>", "reaches": <int, how many of the
listed defects it prevents>, "why": "<what defect pattern it kills, one short clause>"}}]

Defects and their suggested fixes:
{items}"""


def cluster(workers: int) -> None:
    """Turn 357 one-off fix suggestions into a short list of writable prompt rules."""
    d = [x for x in json.loads(OUT.read_text())
         if x.get("fixable") == "prompt" and x.get("fix")]
    res = {}

    def one(st):
        rows = [x for x in d if x["subtask"] == st]
        items = "\n".join(f"- defect: {r['text'][:150]}\n  suggested: {r['fix'][:110]}"
                          for r in rows[:120])
        # 8000, not 3000: Opus 5 thinks before answering here, and a 3000 budget was
        # consumed entirely by the thinking block, returning no text at all.
        # A long thinking pass on 100+ defects runs past the default socket timeout, so
        # give it room and retry rather than losing the whole subtask.
        for attempt in range(3):
            try:
                msg = judge._get_client().with_options(timeout=900).messages.create(
                    model=judge.TRINITY_JUDGE_MODEL, max_tokens=8000,
                    messages=[{"role": "user",
                               "content": CLUSTER.format(subtask=st, items=items)}])
                m = re.search(r"\[.*\]", judge._text_of(msg), re.DOTALL)
                if m:
                    return st, json.loads(m.group()), len(rows)
            except Exception as e:
                print(f"   ! {st} attempt {attempt + 1}: {type(e).__name__}", flush=True)
        return st, [], len(rows)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        for fut in as_completed([pool.submit(one, st) for st in SUBTASKS]):
            st, rules, n = fut.result()
            res[st] = {"n_prompt_defects": n, "rules": rules}
    (TRIN / "fix_rules_v2.json").write_text(json.dumps(res, indent=1))
    for st in SUBTASKS:
        r = res.get(st, {})
        print(f"\n=== {st}  ({r.get('n_prompt_defects', 0)} prompt-fixable defects) ===")
        for x in r.get("rules", []):
            print(f"  reaches ~{x.get('reaches', 0):>3}  {x.get('rule', '')}")
            print(f"                 {x.get('why', '')}")


def judge_inflation() -> None:
    """How much of the failure rate is the judge being wrong rather than the model?

    A defect tagged "judge" is one the auditor thought was not the model's fault. If every
    such defect were withdrawn, some answers would have no defects left — those are the
    samples the scoreboard is currently marking down for nothing.
    """
    d = json.loads(OUT.read_text())
    bad = defaultdict(int)
    tot = defaultdict(int)
    for x in d:
        if not x.get("category"):
            continue
        k = (x["model"], x["subtask"], x["app"], x["system"])
        tot[k] += 1
        if x["fixable"] == "judge":
            bad[k] += 1
    grades = {(g["model"], g["subtask"], g["app"], g["system"]): g for g in load()}
    wholly = [k for k in tot if bad[k] == tot[k] and bad[k] > 0]
    print(f"\n{len(bad)} answers carry at least one questionable defect")
    print(f"{len(wholly)} answers where EVERY recorded defect was judged questionable")
    by = Counter(k[1] for k in wholly)
    for st in SUBTASKS:
        r = [g for g in grades.values() if g["subtask"] == st]
        n = sum(1 for g in r if g["correctness"] == 2 and g["completeness"] == 2
                and g["usability"] == 2 and not g["fatal_error"])
        print(f"  {st:<22} fully correct {n:>2}/{len(r)}  "
              f"+{by.get(st, 0)} would have no defects left "
              f"-> up to {n + by.get(st, 0)}/{len(r)}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--classify", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--cluster", action="store_true")
    ap.add_argument("--inflation", action="store_true")
    ap.add_argument("--workers", type=int, default=5)
    a = ap.parse_args()
    if a.classify:
        classify(a.workers)
    if a.cluster:
        cluster(4)
    if a.inflation:
        judge_inflation()
    if a.report or not (a.classify or a.cluster or a.inflation):
        report()
    return 0





if __name__ == "__main__":
    sys.exit(main())
