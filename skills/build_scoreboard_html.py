#!/usr/bin/env python3
"""results/trinity_scoreboard.html — the benchmark result, both metrics side by side.

Two numbers, because they answer different questions:
  ANSWER CORRECT  the substance matches the catalog. Right if a human reviews before
                  submission and only needs the thinking done.
  FULLY CORRECT   also complete and runnable as-is. The only number that matters for an
                  unattended pipeline.

The gap between them is the finding. On Batch job creation gpt56terra writes a substantively
correct script 29/38 times and a submittable one 17/38 — an answer that passes review and
fails at qsub.

Usage:
    python skills/build_scoreboard_html.py
"""
from __future__ import annotations
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from skills.trinity_task_spec import SUBTASKS  # noqa: E402

TRIN = ROOT / "results" / "skills" / "trinity"
OUT = ROOT / "results" / "trinity_scoreboard.html"

# Where each model runs, and what that costs.
HOSTING = {
    "gpt56terra":       ("Argo", "commercial API"),
    "gemini35flash":    ("Argo", "commercial API"),
    "nemotron-3-ultra": ("Minerva", "ALCF on-prem"),
    "gemma-4-31b":      ("Sophia", "ALCF on-prem"),
    "gpt-oss-120b":     ("Sophia", "ALCF on-prem"),
    "llama-3.1-8b":     ("Sophia", "ALCF on-prem"),
}
BEFORE = {"Software selection": 22, "Input preparation": 2,
          "Resource selection": 5, "Batch job creation": 0}


def build() -> dict:
    grades = [json.loads(l) for l in (TRIN / "grades.jsonl").open()]
    answers = [json.loads(l) for l in (TRIN / "answers.jsonl").open()]
    subs = sorted({g["subtask"] for g in grades}, key=lambda s: SUBTASKS[s]["order"])

    core = lambda g: g["correctness"] == 2                                       # noqa: E731
    full = lambda g: (g["correctness"] == 2 and g["completeness"] == 2           # noqa: E731
                      and g["usability"] == 2 and not g["fatal_error"])

    by = defaultdict(lambda: defaultdict(list))
    for g in grades:
        by[g["model"]][g["subtask"]].append(g)

    err = defaultdict(lambda: [0, 0])
    for a in answers:
        err[a["model"]][1] += 1
        if a["error"]:
            err[a["model"]][0] += 1

    rows = []
    for m, d in by.items():
        allg = [x for v in d.values() for x in v]
        rows.append({
            "model": m, "cluster": HOSTING.get(m, ("?", "?"))[0],
            "hosting": HOSTING.get(m, ("?", "?"))[1],
            "n": len(allg),
            "core": round(100 * sum(core(x) for x in allg) / len(allg)),
            "full": round(100 * sum(full(x) for x in allg) / len(allg)),
            "err": round(100 * err[m][0] / max(err[m][1], 1)),
            "cells": {s: {"core": sum(core(x) for x in d.get(s, [])),
                          "full": sum(full(x) for x in d.get(s, [])),
                          "n": len(d.get(s, []))} for s in subs},
        })
    rows.sort(key=lambda r: -r["full"])

    per_sub = {s: {"before": BEFORE.get(s),
                   "core": round(100 * sum(core(g) for g in grades if g["subtask"] == s)
                                 / max(sum(1 for g in grades if g["subtask"] == s), 1)),
                   "full": round(100 * sum(full(g) for g in grades if g["subtask"] == s)
                                 / max(sum(1 for g in grades if g["subtask"] == s), 1))}
               for s in subs}
    return {"subs": subs, "rows": rows, "per_sub": per_sub, "total": len(grades)}


TEMPLATE = """<meta charset="utf-8"/>
<title>Trinity Benchmark Scoreboard</title>
<style>
:root{--bg:#F2F4F3;--surface:#FFFFFF;--surface-2:#E9ECEB;--text:#12181B;--text-dim:#55636B;
 --text-faint:#8B979B;--border:#D8DEDD;--accent:#0E7C86;--accent-soft:#D9EEEE;
 --accent-text:#08565D;--good:#2E8B6E;--warn:#C1432E;--onprem:#7A5CC2;--comm:#C2724A;
 --shadow:0 1px 2px rgba(18,24,27,.06),0 4px 12px rgba(18,24,27,.05);--radius:8px;
 --font:ui-sans-serif,-apple-system,"Segoe UI",Arial,sans-serif;
 --mono:ui-monospace,"SF Mono","Cascadia Code",Consolas,monospace;}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#10151A;--surface:#161D22;
 --surface-2:#1D262C;--text:#E7EDEC;--text-dim:#93A2A6;--text-faint:#5E6C70;--border:#263136;
 --accent:#34C6C9;--accent-soft:#16363A;--accent-text:#7FE0E2;--good:#4CBF97;--warn:#D9634C;
 --onprem:#A891E8;--comm:#E39468;--shadow:0 1px 2px rgba(0,0,0,.3),0 4px 16px rgba(0,0,0,.35);}}
:root[data-theme="dark"]{--bg:#10151A;--surface:#161D22;--surface-2:#1D262C;--text:#E7EDEC;
 --text-dim:#93A2A6;--text-faint:#5E6C70;--border:#263136;--accent:#34C6C9;--accent-soft:#16363A;
 --accent-text:#7FE0E2;--good:#4CBF97;--warn:#D9634C;--onprem:#A891E8;--comm:#E39468;
 --shadow:0 1px 2px rgba(0,0,0,.3),0 4px 16px rgba(0,0,0,.35);}
*{box-sizing:border-box;}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--font);font-size:14px;line-height:1.55;}
.wrap{max-width:1180px;margin:0 auto;padding:28px 22px 80px;}
h1{margin:0 0 6px;font-size:22px;font-weight:660;letter-spacing:-.013em;}
.sub{color:var(--text-dim);font-size:13.5px;max-width:92ch;}
h2{font-size:12px;text-transform:uppercase;letter-spacing:.09em;color:var(--text-faint);font-weight:680;margin:32px 0 4px;}
.h2sub{color:var(--text-dim);font-size:12.5px;margin-bottom:10px;max-width:90ch;}
.scroll{overflow-x:auto;border:1px solid var(--border);border-radius:var(--radius);background:var(--surface);box-shadow:var(--shadow);}
table{border-collapse:separate;border-spacing:0;width:100%;font-size:13px;}
th,td{padding:8px 11px;text-align:center;white-space:nowrap;border-bottom:1px solid var(--border);}
thead th{background:var(--surface);font-size:11px;font-weight:660;color:var(--text-faint);
 text-transform:uppercase;letter-spacing:.05em;}
th.l,td.l{text-align:left;}
td.m{font-weight:640;}
.host{display:block;font-size:10.5px;font-weight:600;letter-spacing:.03em;}
.host.on{color:var(--onprem);} .host.co{color:var(--comm);}
td.c{font-family:var(--mono);font-variant-numeric:tabular-nums;}
td.tot{font-family:var(--mono);font-weight:680;background:var(--surface-2);}
.bar{display:block;height:5px;border-radius:3px;background:var(--surface-2);margin-top:3px;overflow:hidden;}
.bar i{display:block;height:100%;background:var(--accent);}
.bar.f i{background:var(--good);}
tr:last-child td{border-bottom:0;}
.delta{font-family:var(--mono);font-size:12px;}
.up{color:var(--good);font-weight:680;}
.note{margin-top:12px;color:var(--text-dim);font-size:12.5px;max-width:94ch;}
.note b{color:var(--text);}
.warnbox{margin-top:26px;padding:13px 16px;background:var(--surface);border:1px solid var(--border);
 border-left:3px solid var(--warn);border-radius:var(--radius);font-size:12.5px;color:var(--text-dim);}
.warnbox b{color:var(--text);}
</style>
<div class="wrap">
<h1>Which model can Trinity trust with which step?</h1>
<div class="sub">156 benchmark samples per model, drawn from Argonne's own software catalog and
graded by Claude Opus 5 against catalog facts. Two metrics, because they answer different
questions &mdash; and the gap between them is the finding.</div>

<h2>Answer correct</h2>
<div class="h2sub">The substance matches the catalog: the right application, the right sizing,
the right script. Use this if a person reviews the output before it is submitted.</div>
<div class="scroll"><table id="t-core"></table></div>

<h2>Fully correct</h2>
<div class="h2sub">Answer correct <em>and</em> complete <em>and</em> runnable as-is, with no
fatal error. The only number that matters for an unattended pipeline.</div>
<div class="scroll"><table id="t-full"></table></div>

<h2>Effect of supplying the facts</h2>
<div class="h2sub">Before, prompts told models to "consult the software catalog" while
containing no catalog, and asked for files from a model with no filesystem. Now the catalog,
file inventory, machine specification and module lines are all supplied.</div>
<div class="scroll"><table id="t-before"></table></div>

<div class="warnbox" id="caveats"></div>
</div>
<script>
const D = __DATA__;
const esc = s => String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));

function grid(el, key){
  const head = `<thead><tr><th class="l">Model</th>` +
    D.subs.map(s=>`<th>${esc(s)}</th>`).join("") +
    `<th>Overall</th></tr></thead>`;
  const body = D.rows.map(r=>{
    const cells = D.subs.map(s=>{
      const c = r.cells[s];
      if(!c || !c.n) return '<td class="c">—</td>';
      const pct = Math.round(100*c[key]/c.n);
      return `<td class="c">${c[key]}/${c.n}
        <span class="bar ${key==='full'?'f':''}"><i style="width:${pct}%"></i></span></td>`;
    }).join("");
    const pct = r[key];
    return `<tr><td class="l m">${esc(r.model)}
        <span class="host ${r.hosting==='ALCF on-prem'?'on':'co'}">${esc(r.cluster)} · ${esc(r.hosting)}</span></td>
      ${cells}<td class="tot">${pct}%</td></tr>`;
  }).join("");
  document.getElementById(el).innerHTML = head + `<tbody>${body}</tbody>`;
}
grid("t-core","core"); grid("t-full","full");

document.getElementById("t-before").innerHTML =
  `<thead><tr><th class="l">Subtask</th><th>Before</th><th>Answer correct</th>
    <th>Fully correct</th><th>Change</th></tr></thead><tbody>` +
  D.subs.map(s=>{
    const p = D.per_sub[s];
    const d = p.before===null?null:(p.full - p.before);
    return `<tr><td class="l">${esc(s)}</td>
      <td class="c">${p.before===null?'—':p.before+'%'}</td>
      <td class="c">${p.core}%</td><td class="c">${p.full}%</td>
      <td class="delta ${d>0?'up':''}">${d===null?'—':(d>0?'+':'')+d+' pts'}</td></tr>`;
  }).join("") + "</tbody>";

document.getElementById("caveats").innerHTML =
  `<b>Read with these caveats.</b> The judge is an LLM and has not been validated against a
   human grader; two rubric miscalibrations were already found and fixed by reading its
   output, so a third is plausible. Samples are synthetic though catalog-grounded &mdash; real
   ALCF tickets would be stronger evidence. Answer-error rates differ sharply by endpoint:
   ` + D.rows.map(r=>`${esc(r.model)} ${r.err}%`).join(", ") + `. Minerva returned HTTP 504s
   under sustained load in all three runs, so nemotron-3-ultra's score reflects answers that
   took three passes and roughly two hours to collect, while the Sophia and Argo models
   completed in one. A model you cannot reach reliably is not usable in a pipeline, whatever
   it scores. ${D.total} graded answers in total.`;
</script>
"""


def main() -> int:
    d = build()
    OUT.write_text(TEMPLATE.replace("__DATA__", json.dumps(d, separators=(",", ":"))))
    print(f"{len(d['rows'])} models x {len(d['subs'])} subtasks, {d['total']} grades -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
