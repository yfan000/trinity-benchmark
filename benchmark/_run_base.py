#!/usr/bin/env python3
"""Run the Trinity benchmark: answer each sample with a model, then grade with Opus 5.

Two phases, kept separate so a judge change never requires re-running inference:
    --answer   send every sample to a model, store the raw response
    --grade    grade stored responses against the catalog-derived key

Models are addressed by short name; the endpoint (Sophia / Minerva / Argo) is resolved from
config.py. Both phases resume: an interrupted run picks up where it stopped.

Usage:
    python skills/trinity_run.py --answer --models gpt-oss-120b,nemotron-3-ultra
    python skills/trinity_run.py --grade
    python skills/trinity_run.py --report
"""
from __future__ import annotations
import argparse
import json
import sys
import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import config  # noqa: E402
from benchmark import prompt as judge
from benchmark.task_spec import SUBTASKS  # noqa: E402

TRIN = ROOT / "data" / "corpus" / "v8"
SAMPLES = TRIN / "samples.jsonl"
ANSWERS = TRIN / "answers.jsonl"
GRADES = TRIN / "grades.jsonl"

# short name -> (endpoint, full model id). Sophia and Minerva use the Globus bearer token;
# Argo authenticates with the ANL username instead.
MODELS = {
    "gpt-oss-120b":     ("sophia",  "openai/gpt-oss-120b"),
    "gpt-oss-20b":      ("sophia",  "openai/gpt-oss-20b"),
    "llama-3.1-8b":     ("sophia",  "meta-llama/Meta-Llama-3.1-8B-Instruct"),
    "llama-3.3-70b":    ("sophia",  "meta-llama/Llama-3.3-70B-Instruct"),
    "gemma-4-31b":      ("sophia",  "google/gemma-4-31B-it"),
    "nemotron-3-ultra": ("minerva", "nemotron-3-ultra"),
    "inkling-bf16":     ("minerva", "inkling-bf16"),
    "claudeopus48":     ("argo",    "claudeopus48"),
    # Frontier commercial reference: strongest GPT and Gemini on the Argo roster, so the
    # on-prem models are compared against a real ceiling rather than a weak sibling.
    "gpt56terra":       ("argo",    "gpt56terra"),
    "gemini35flash":    ("argo",    "gemini35flash"),
}
MAX_TOKENS = 4096  # job scripts and input decks are long; truncation reads as a wrong answer

# Reasoning models spend the budget on thinking BEFORE any answer is emitted, so a cap that
# is generous for a normal model truncates them — or returns nothing at all. Measured on the
# 40-sample v6 set: nemotron-3-ultra hit a 4,096 cap on 13 of 40 prompts (32%), 10 of them
# emitting zero characters, every one reporting finish_reason="length" at exactly 4,096
# completion tokens. Software selection never truncated (670 tokens mean); Resource selection
# truncated 6 times in 10 (3,183 tokens mean when it completed). The other three models are
# not reasoning models, never approach the cap, and are left alone so their results stand.
REASONING_MAX_TOKENS = 16384
REASONING_MODELS = {"nemotron-3-ultra"}


def max_tokens_for(model: str) -> int:
    return REASONING_MAX_TOKENS if model in REASONING_MODELS else MAX_TOKENS

# Answer-style prefixes, applied at run time rather than baked into the samples so the same
# benchmark can be run under different prompting regimes and the difference measured.
#
# Motivation: on Software selection, 83% of answers named the correct application but only
# 22% were fully correct. The loss was almost entirely invented supporting detail — module
# names, versions, build provenance, benchmark claims. "grounded" targets exactly that.
STYLES = {
    "plain": "",
    "grounded": (
        "Answer only what the task asks for, and nothing more.\n"
        "State only what you can support from the information you were given. Do not invent "
        "module names, version numbers, build details, file paths, hardware specifications, "
        "or performance claims. If a specific was not provided to you, either omit it or say "
        "explicitly that it must be confirmed \u2014 never guess a plausible-looking value.\n"
        "A short, correct answer scores better than a long one padded with unverifiable "
        "detail.\n\n"),
}


def endpoint(kind: str) -> tuple[str, dict]:
    if kind == "sophia":
        return config.SOPHIA_URL, {"Authorization": f"Bearer {config.ALCF_TOKEN}"}
    if kind == "minerva":
        return config.MINERVA_URL, {"Authorization": f"Bearer {config.ALCF_TOKEN}"}
    # Argo took the username in the body here and in a Bearer header everywhere else; all
    # three forms were verified against the live endpoint to return 200, so this now sends
    # both from one definition rather than leaving the two conventions to drift apart.
    return config.ARGO_URL, config.argo_auth()[0]


def ask(model: str, prompt: str, style: str = "plain") -> tuple[str, str]:
    """Return (answer, error). One retry, since a transient 5xx should not score as failure."""
    kind, full = MODELS[model]
    url, hdr = endpoint(kind)
    body = {"model": full,
            "messages": [{"role": "user", "content": STYLES[style] + prompt}],
            "max_tokens": max_tokens_for(model)}
    if kind == "argo":
        body["user"] = config.ARGO_USER
    for attempt in (1, 2, 3):
        try:
            r = httpx.post(url.rstrip("/") + "/chat/completions",
                           headers={**hdr, "Content-Type": "application/json"},
                           json=body, timeout=300.0)
            if r.status_code != 200:
                if attempt < 3:
                    time.sleep(5 * attempt)   # back off; 504s cluster when a node is busy
                    continue
                return "", f"HTTP {r.status_code}: {r.text[:120]}"
            d = r.json()
            ch = (d.get("choices") or [{}])[0]
            msg = ch.get("message") or {}
            txt = (msg.get("content") or msg.get("reasoning_content") or "").strip()
            # finish_reason="length" means the budget ran out mid-answer. Reasoning length
            # varies between calls on the same prompt, so a retry often succeeds; scoring the
            # fragment would charge the model for our cap.
            if ch.get("finish_reason") == "length" and attempt < 3:
                time.sleep(3 * attempt)
                continue
            if not txt and attempt < 3:
                time.sleep(3 * attempt)
                continue
            return txt, ("" if txt else "empty generation")
        except Exception as e:
            if attempt < 3:
                time.sleep(5 * attempt)
                continue
            return "", f"{type(e).__name__}: {str(e)[:110]}"
    return "", "exhausted retries"


def load(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.open()] if path.exists() else []


def phase_answer(models: list[str], workers: int, limit: int | None,
                 style: str = "plain", only: str | None = None) -> int:
    samples = load(SAMPLES)
    if only:
        samples = [s for s in samples if s["subtask"] == only]
    if limit:
        samples = samples[:limit]
    # Only successful answers count as done — an endpoint 504 is transient, and persisting
    # it as complete would bake a Minerva outage into the scoreboard as a model's silence.
    # Style is part of the identity so plain and grounded runs do not mask each other.
    done = {(a["model"], a["sample_id"], a.get("style", "plain"))
            for a in load(ANSWERS) if not a["error"]}
    jobs = [(m, s) for m in models for s in samples
            if (m, s["sample_id"], style) not in done]
    print(f"{len(samples)} samples x {len(models)} models = {len(samples)*len(models)}; "
          f"{len(jobs)} to run, {workers} workers")
    if not jobs:
        return 0

    lock, t0, n = threading.Lock(), time.perf_counter(), 0
    with ANSWERS.open("a") as f, ThreadPoolExecutor(max_workers=workers) as pool:
        futs = {pool.submit(ask, m, s["prompt"], style): (m, s) for m, s in jobs}
        for fut in as_completed(futs):
            m, s = futs[fut]
            ans, err = fut.result()
            with lock:
                f.write(json.dumps({"model": m, "sample_id": s["sample_id"],
                                    "subtask": s["subtask"], "app": s["app"],
                                    "system": s["system"], "style": style,
                                    "answer": ans, "error": err}, ensure_ascii=False) + "\n")
                f.flush()
                n += 1
                if n % 25 == 0 or err:
                    rate = n / max(time.perf_counter() - t0, 1e-9)
                    print(f"  {n}/{len(jobs)} ({rate*60:.0f}/min)"
                          f"{'  ERR ' + m + ' ' + s['sample_id'] + ': ' + err[:60] if err else ''}",
                          flush=True)
    errs = sum(1 for a in load(ANSWERS) if a["error"])
    print(f"done in {(time.perf_counter()-t0)/60:.1f} min; {errs} errored overall")
    return 0


def phase_grade(workers: int) -> int:
    samples = {s["sample_id"]: s for s in load(SAMPLES)}
    answers = [a for a in load(ANSWERS) if not a["error"]]
    done = {(g["model"], g["sample_id"], g.get("style", "plain")) for g in load(GRADES)}
    todo = [a for a in answers
            if (a["model"], a["sample_id"], a.get("style", "plain")) not in done]
    print(f"{len(answers)} answers, {len(todo)} to grade with {judge.TRINITY_JUDGE_MODEL}")
    if not todo:
        return 0

    def work(a):
        s = samples[a["sample_id"]]
        spec = SUBTASKS[s["subtask"]]
        return a, judge.judge_trinity(s["subtask"], spec["goal"], s["system"],
                                      s["grading_key"].get("scheduler", ""),
                                      s["prompt"], a["answer"], s["grading_key"],
                                      grading_note=spec.get("grading_note", ""))

    lock, t0, n = threading.Lock(), time.perf_counter(), 0
    with GRADES.open("a") as f, ThreadPoolExecutor(max_workers=workers) as pool:
        failed = 0
        for fut in as_completed([pool.submit(work, a) for a in todo]):
            a, g = fut.result()
            with lock:
                n += 1
                if g.get("judge_failed"):
                    # Not persisted, so the next --grade retries it rather than baking a
                    # judge outage into the scoreboard as a model's zero.
                    failed += 1
                    continue
                f.write(json.dumps({"model": a["model"], "sample_id": a["sample_id"],
                                    "subtask": a["subtask"], "app": a["app"],
                                    "system": a["system"],
                                    "style": a.get("style", "plain"),
                                    **g}, ensure_ascii=False) + "\n")
                f.flush()
                if n % 25 == 0:
                    print(f"  {n}/{len(todo)}", flush=True)
    print(f"graded in {(time.perf_counter()-t0)/60:.1f} min"
          + (f"; {failed} judge failures NOT recorded — rerun --grade to retry" if failed else ""))
    return 0


def is_pass(g: dict) -> bool:
    """Strict: every dimension perfect and nothing fatal.

    A 0-6 mean is the wrong output for a routing decision — 4.5/6 does not tell you whether
    a script would run. This asks the only question that matters operationally: was the
    answer completely right?
    """
    return (g["correctness"] == 2 and g["completeness"] == 2
            and g["usability"] == 2 and not g["fatal_error"])


def is_core(g: dict) -> bool:
    """The substance is right, whatever else is wrong.

    `correctness` is the judge's verdict that the answer matches the ground truth — the
    right application, the right sizing, the right script. An answer can be core-correct and
    still not fully correct: on Software selection 95% named the right application but 85%
    were flawless, the gap being fabricated justification. Which column matters depends on
    whether anything downstream reads more than the headline answer.
    """
    return g["correctness"] == 2


def phase_report() -> int:
    grades = load(GRADES)
    if not grades:
        print("no grades yet")
        return 1
    by = defaultdict(lambda: defaultdict(list))
    for g in grades:
        by[g["model"]][g["subtask"]].append(g)
    subs = sorted({g["subtask"] for g in grades}, key=lambda s: SUBTASKS[s]["order"])
    order = sorted(by, key=lambda m: -sum(is_pass(x) for v in by[m].values() for x in v))

    for title, fn, blurb in (
            ("ANSWER CORRECT", is_core,
             "the substance matches the catalog — right application, sizing or script"),
            ("FULLY CORRECT", is_pass,
             "answer correct AND complete AND usable as-is, with no fatal error")):
        print(f"\n{title} — {blurb}\n")
        print(f"{'model':<18}" + "".join(f"{s[:15]:>17}" for s in subs) + f"{'overall':>13}")
        for m in order:
            cells, allg = [], [x for v in by[m].values() for x in v]
            for s in subs:
                v = by[m].get(s, [])
                cells.append(f"{sum(fn(x) for x in v)}/{len(v)}" if v else "—")
            p = sum(fn(x) for x in allg)
            print(f"{m:<18}" + "".join(f"{c:>17}" for c in cells)
                  + f"{p}/{len(allg)} = {100*p/len(allg):.0f}%".rjust(13))

    print("\nPartial credit, for diagnosing how close the failures are "
          "(mean of 3 dimensions, max 6)\n")
    print(f"{'model':<18}" + "".join(f"{s[:15]:>17}" for s in subs) + f"{'overall':>10}{'fatal':>9}")
    for m in order:
        cells, allg = [], [x for v in by[m].values() for x in v]
        for s in subs:
            v = by[m].get(s, [])
            cells.append(f"{sum(x['correctness']+x['completeness']+x['usability'] for x in v)/len(v):.2f}"
                         if v else "—")
        overall = sum(x['correctness']+x['completeness']+x['usability'] for x in allg)/len(allg)
        fatal = sum(1 for x in allg if x["fatal_error"])
        print(f"{m:<18}" + "".join(f"{c:>17}" for c in cells) +
              f"{overall:>10.2f}{str(fatal)+'/'+str(len(allg)):>9}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--answer", action="store_true")
    ap.add_argument("--grade", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--models", default="gpt-oss-120b,nemotron-3-ultra,llama-3.1-8b")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--limit", type=int, help="first N samples only, for a smoke test")
    ap.add_argument("--style", choices=sorted(STYLES), default="plain")
    ap.add_argument("--only", help="restrict to one subtask")
    args = ap.parse_args()

    if args.answer:
        models = [m.strip() for m in args.models.split(",")]
        bad = [m for m in models if m not in MODELS]
        if bad:
            print(f"unknown models: {bad}\nknown: {sorted(MODELS)}")
            return 1
        return phase_answer(models, args.workers, args.limit, args.style, args.only)
    if args.grade:
        return phase_grade(args.workers)
    if args.report:
        return phase_report()
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
