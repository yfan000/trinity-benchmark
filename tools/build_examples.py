#!/usr/bin/env python3
"""Regenerate examples/ from the v8 corpus — every anchor, both arms, all four models.

Generated, never hand-written. A walkthrough written by hand drifts the moment a prompt or a
rule changes, and then it misleads a reader about what the harness does.

This writes the whole corpus out as readable markdown: for each of the 40 anchors, the prompt as
each arm posed it, Claude's reference answer, what all four models wrote, and every requirement
verdict with the judge's evidence — the same 320 graded answers the HTML browsers show, in a
form that reads in a text editor and diffs in git.

    python tools/build_examples.py

The prompt differs between arms only for Input preparation; elsewhere `prompt.rich.md` is
omitted and the anchor page says so, rather than shipping 30 identical pairs.
"""
from __future__ import annotations

import collections
import json
import pathlib
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from audit.matrix import replay                              # noqa: E402
from judge.skills.loader import load as load_skill          # noqa: E402

RUBRIC = "r28"                     # the library as it stands
GRADED_UNDER = "r27"               # what the shipped grades were produced under
# not_copied_from_example was removed in r28 but appears in the r27 grades. Label it rather
# than showing a bare em dash, so a reader is not left wondering why a rule has no severity.
RETIRED = {"INP.common.not_copied_from_example": "removed in r28"}

CORPUS = ROOT / "data" / "corpus" / "v8"
OUT = ROOT / "examples"
ARMS = ("base", "rich")
MODELS = ["nemotron-3-ultra", "gemma-4-31b", "gpt-oss-120b", "llama-3.1-8b"]
SUBTASKS = ["Software selection", "Input preparation",
            "Resource selection", "Batch job creation"]
SLUG = {"Software selection": "software_selection", "Input preparation": "input_preparation",
        "Resource selection": "resource_selection", "Batch job creation": "batch_job_creation"}
ASKS = {
 "Software selection": "Name the application to run for a stated workload on a stated machine, "
                       "and justify it from what the facility actually provides.",
 "Input preparation":  "Write the input files the application needs, complete and runnable, for "
                       "the physical system the prompt describes.",
 "Resource selection": "Choose nodes, ranks, walltime and queue for a stated job, within the "
                       "limits the prompt states.",
 "Batch job creation": "Write the submission script: directives, environment, launch command.",
}


def load(name: str) -> list[dict]:
    p = CORPUS / name
    return [json.loads(l) for l in p.open()] if p.exists() else []


def fence(text: str) -> str:
    """Fence content that itself contains fences. Answers are full of ``` blocks."""
    n = 3
    while "`" * (n + 1) in (text or ""):
        n += 1
    f = "`" * max(4, n + 1)
    return f"{f}\n{text or '(none)'}\n{f}\n"


class Cell:
    """One (model, anchor, arm): the answer, the k verdicts, and the derived result."""

    def __init__(self, answer: dict | None, grades: list[dict]):
        self.answer = (answer or {}).get("answer") or ""
        # Re-derive under the CURRENT rubric rather than reading the stored r27 scores. The
        # verdicts are the judge's and do not move; the scores are arithmetic over them, and
        # showing r27 arithmetic beside an r28 headline is how a walkthrough starts contradicting
        # the table it illustrates.
        self.grades = [replay(g, RUBRIC)[0] for g in grades]
        grades = self.grades
        med = lambda f: statistics.median_low([g.get(f, 0) for g in grades]) if grades else 0
        self.c, self.p, self.u = med("correctness"), med("completeness"), med("usability")
        self.fatal = bool(grades) and sum(bool(g.get("fatal_error")) for g in grades) > len(grades) / 2
        self.ok = self.c == 2 and self.p == 2 and self.u == 2 and not self.fatal

    def verdicts(self, sev: dict) -> tuple[list[str], int, int]:
        ids = set().union(*[set(g.get("requirements") or {}) for g in self.grades]) \
            if self.grades else set()
        rows, nviol = [], 0
        for rid in sorted(ids):
            vs = [(g.get("requirements") or {}).get(rid, {}) for g in self.grades]
            verds = [v.get("verdict") for v in vs if v.get("verdict")]
            if not verds:
                continue
            top = collections.Counter(verds).most_common(1)[0][0]
            evid = next((v.get("evidence", "") for v in vs if v.get("verdict") == top), "")
            flip = " ⚠︎ flipped across runs" if len(set(verds)) > 1 else ""
            label = sev.get(rid) or RETIRED.get(rid, "—")
            mark = f"**{top}**" if top == "violated" else top
            nviol += top == "violated"
            rows.append(f"| `{rid}` | {label} | {mark}{flip} | {evid.replace('|', '\\|')} |")
        return rows, nviol, len(rows)


def main() -> int:
    samples, answers, grades = {}, {}, collections.defaultdict(list)
    for arm in ARMS:
        for r in load(f"samples_v8{arm}.jsonl"):
            samples[(arm, r["subtask"], r["app"], r["system"])] = r
        for r in load(f"answers_v8{arm}.jsonl"):
            answers[(arm, r["model"], r["subtask"], r["app"], r["system"])] = r
        for i in (1, 2, 3):
            for r in load(f"grades_v8{arm}__gpt56terra__{GRADED_UNDER}__SKILLMODE__run{i}.jsonl"):
                grades[(arm, r["model"], r["subtask"], r["app"], r["system"])].append(r)
    if not samples:
        print(f"  no corpus under {CORPUS} — nothing to build")
        return 1

    anchors = sorted({k[1:] for k in samples}, key=lambda a: (SUBTASKS.index(a[0]), a[1], a[2]))
    written, tally = 0, collections.Counter()
    per_subtask: dict = collections.defaultdict(list)

    for st, app, system in anchors:
        slug, name = SLUG[st], f"{app}@{system}"
        d = OUT / slug / name
        d.mkdir(parents=True, exist_ok=True)
        skill = load_skill(st, app, system, rubric_id=RUBRIC)
        sev = {r["id"]: r.get("severity", "major") for r in skill.requirements}

        base_s = samples.get(("base", st, app, system), {})
        rich_s = samples.get(("rich", st, app, system), {})
        same_prompt = base_s.get("prompt") == rich_s.get("prompt")

        (d / "prompt.base.md").write_text(
            f"# Prompt — {name}\n\nSubtask: **{st}**. Base arm, exactly as the model received "
            f"it.\n\n{fence(base_s.get('prompt'))}")
        if not same_prompt:
            (d / "prompt.rich.md").write_text(
                f"# Prompt — {name}, enriched arm\n\nSubtask: **{st}**. The base prompt with "
                f"catalog material inserted — format contract, setup and run commands, scaling "
                f"notes. Derived from the base arm by verified-reversible text insertion, never "
                f"regenerated, so the two arms are paired.\n\n{fence(rich_s.get('prompt'))}")
        (d / "reference.md").write_text(
            f"# Reference answer — {name}\n\nWritten by Claude and shown to the judge as *one* "
            f"correct answer, never as the correct one. The judge is told explicitly not to "
            f"deduct for differing from it where the requirements are met.\n\n"
            f"{fence(base_s.get('reference'))}")

        lines, results = [], {}
        for arm in ARMS:
            ad = d / arm
            ad.mkdir(exist_ok=True)
            vtable = []
            for model in MODELS:
                key = (arm, model, st, app, system)
                if key not in grades:
                    continue
                cell = Cell(answers.get(key), grades[key])
                rows, nviol, nreq = cell.verdicts(sev)
                results[(arm, model)] = (cell.ok, nviol, nreq)
                tally[cell.ok] += 1
                written += 1
                (ad / f"answer-{model}.md").write_text(
                    f"# {model} — {name}, {arm} arm\n\n{st}. **{'PASS' if cell.ok else 'FAIL'}** "
                    f"(correctness {cell.c}/2, completeness {cell.p}/2, usability {cell.u}/2"
                    f"{', fatal' if cell.fatal else ''}; {nviol} of {nreq} requirements "
                    f"violated).\n\n{fence(cell.answer)}")
                vtable.append(
                    f"\n## {model} — {'PASS' if cell.ok else 'FAIL'}\n\n"
                    f"| requirement | severity | verdict | judge's evidence |\n|---|---|---|---|\n"
                    + "\n".join(rows) + "\n")
            if vtable:
                (ad / "verdicts.md").write_text(
                    f"# Verdicts — {name}, {arm} arm\n\nMajority across three judge replicates, "
                    f"judged by `gpt56terra` under rubric **{GRADED_UNDER}**, scored "
                    f"under **{RUBRIC}** (sha `{skill.rubric_sha256[:12]}`) — a rule retired "
                    f"since the grades were collected is listed but no longer counted. "
                    f"A rule marked *flipped across runs* did not get the same verdict all three "
                    f"times.\n" + "".join(vtable))

        for model in MODELS:
            b, r = results.get(("base", model)), results.get(("rich", model))
            if not b and not r:
                continue
            cell = lambda x: "—" if not x else (f"pass ({x[2]} rules)" if x[0]
                                                else f"**fail** ({x[1]}/{x[2]} violated)")
            lines.append(f"| `{model}` | {cell(b)} | {cell(r)} |")
        npass = sum(1 for v in results.values() if v[0])
        (d / "README.md").write_text(
            f"# {name} — {st}\n\n{ASKS[st]}\n\n**{npass} of {len(results)} attempts passed.**\n\n"
            f"| model | base arm | enriched arm |\n|---|---|---|\n" + "\n".join(lines) + "\n\n"
            f"- [`prompt.base.md`](prompt.base.md) — what the models saw\n"
            + (f"- [`prompt.rich.md`](prompt.rich.md) — the enriched arm's prompt\n"
               if not same_prompt else
               "- the enriched arm's prompt is byte-identical to the base arm's: enrichment "
               "touches Input preparation only, so this anchor is one of the 30 that act as the "
               "A/B control\n")
            + f"- [`reference.md`](reference.md) — Claude's reference answer\n"
            f"- [`base/`](base/) · [`rich/`](rich/) — each model's answer and `verdicts.md`\n")
        per_subtask[st].append((name, npass, len(results)))

    index = ["# Examples\n",
             "The whole of corpus v8 as readable markdown: for each anchor, the prompt as each arm",
             "posed it, Claude's reference answer, what all four models wrote, and every requirement",
             "verdict with the judge's evidence. Same 320 graded answers the HTML browsers show.\n",
             f"Judged by `gpt56terra` at k=3 under rubric **{GRADED_UNDER}**; severities shown are "
             f"the current library, **{RUBRIC}**.\n",
             f"**{tally[True]} of {tally[True] + tally[False]} attempts passed.** An attempt is one "
             "model on one anchor in one arm; a pass is 2/2 on correctness, completeness and "
             "usability with no fatal violation, taken as the majority of three judge replicates.\n"]
    for st in SUBTASKS:
        rows = per_subtask.get(st, [])
        p, n = sum(r[1] for r in rows), sum(r[2] for r in rows)
        index.append(f"\n## {SLUG[st]} — {p}/{n}\n")
        index.append(ASKS[st] + "\n")
        for nm, a, b in rows:
            index.append(f"- [`{nm}`]({SLUG[st]}/{nm}/) — {a}/{b} passed")
    (OUT / "README.md").write_text("\n".join(index) + "\n")

    for st in SUBTASKS:
        rows = per_subtask.get(st, [])
        (OUT / SLUG[st] / "README.md").write_text(
            f"# {st}\n\n{ASKS[st]}\n\n**{sum(r[1] for r in rows)} of {sum(r[2] for r in rows)} "
            f"attempts passed** across {len(rows)} anchors, four models, two prompt arms.\n\n"
            + "\n".join(f"- [`{nm}`]({nm}/) — {a}/{b} passed" for nm, a, b in rows) + "\n")
        print(f"  {SLUG[st]:<22}{len(rows):>3} anchors  "
              f"{sum(r[1] for r in rows):>3}/{sum(r[2] for r in rows)} passed")
    print(f"  {written} answers written under {OUT.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
