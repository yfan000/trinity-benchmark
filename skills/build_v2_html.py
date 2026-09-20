#!/usr/bin/env python3
"""results/trinity_v2_results.html — the 40-sample v2 run, every answer and every judgement.

A scoreboard says a model scored 4/10. It does not show what the model wrote, or why the
judge marked it down. This does: the scoreboard first, then one card per sample carrying the
prompt, the catalog ground truth, and each model's full answer with the judge's per-dimension
scores and its specific defects.

It is also how the judge gets audited. Opus 5 has never been checked against a human here,
and reading cards is what caught the three miscalibrations already fixed — out-of-scope
penalties, an instruction to write files the model cannot write, and smoke-test defaults
being treated as the expected allocation.

The page declares its own charset. Without that line a browser opening the file over
file:// has no encoding to go on, falls back to Windows-1252, and renders every em dash,
arrow and curly quote as mojibake — 863 characters in the first version of this page.

Usage:
    TRINITY_VER=v6 python skills/build_v2_html.py
"""
from __future__ import annotations
import html
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from skills.trinity_task_spec import SUBTASKS  # noqa: E402
from skills.trinity_run_v2 import is_core, is_pass, TARGETS  # noqa: E402
from skills.trinity_run import MAX_TOKENS as _MT  # noqa: E402
MAXTOK = f"{_MT:,}"
# Which cap produced the graded numbers on THIS page.
NEMO_CAP = 4096 if os.environ.get("TRINITY_VER", "v2").endswith("cap") else 16384
OTHER_CAP = 16384 if NEMO_CAP == 4096 else 4096

TRIN = ROOT / "results" / "skills" / "trinity"
VER = os.environ.get("TRINITY_VER", "v2")
OUT = ROOT / "results" / f"trinity_{VER}_results.html"
SUBS = list(SUBTASKS)

# What each subtask's prompt gained, and the preview measurement that justified it.
VERSION_NOTE = {
 "v6cap": "The same v6 prompts, with nemotron-3-ultra held to the 4,096-token cap the other "
          "three models use. Its reasoning consumes that budget before the answer starts, so "
          "13 of its 40 answers were truncated and 10 came back empty.",
 "v2": "Every prompt carries the fixes validated on a 10-sample preview first.",
 "v4": "v2, plus two rules for Batch job creation only.",
 "v5": "v2, plus the Batch rules and a strict Resource-selection legality procedure.",
 "v6": "The assembled best configuration: v2's Software selection and Input preparation "
       "unchanged, the two Batch job creation rules from v4, and the Resource-selection "
       "queue-legality procedure with its output format left free.",
}

LEVERS = {
 "Software selection": "Installed-software catalog supplied verbatim",
 "Input preparation":  "Prior-step context - verified upstream input deck - no-fabrication "
                       "and form-only rules - closing self-check",
 "Resource selection": "Prior-step context - an ordered queue-legality procedure (size the "
                       "work, eliminate queues whose ceilings are too low, verify each limit) "
                       "- ranks taken from build defaults - no invented timings - closing "
                       "restatement",
 "Batch job creation": "Prior-step context - site scheduler conventions - a real worked "
                       "script per scheduler family - the project account",
}


def load(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.open()] if p.exists() else []


def esc(s) -> str:
    return html.escape(str(s or ""))


def build() -> str:
    samples = {(s["subtask"], s["app"], s["system"]): s for s in load(TRIN / f"samples_{VER}.jsonl")}
    grades = defaultdict(dict)
    for g in load(TRIN / f"grades_{VER}.jsonl"):
        grades[(g["subtask"], g["app"], g["system"])][g["model"]] = g
    # Un-truncated re-runs, shown ALONGSIDE the capped original rather than replacing it:
    # the capped answer is what the scoreboard measured, and quietly swapping it would make
    # the page disagree with the numbers above it.
    rerun = {}
    for r in load(TRIN / f"capped_4096_{VER}.jsonl"):
        rerun[(r["subtask"], r["app"], r["system"], r["model"])] = r

    answers = defaultdict(dict)
    for a in load(TRIN / f"answers_{VER}.jsonl"):
        if a.get("answer") and not a.get("error"):
            answers[(a["subtask"], a["app"], a["system"])][a["model"]] = a["answer"]

    models = [m for m in TARGETS if any(m in v for v in grades.values())]
    flat = [g for v in grades.values() for g in v.values()]

    # ---- scoreboard -------------------------------------------------------------------
    def table(fn, label, note):
        rows = ""
        for m in models:
            mine = [g for g in flat if g["model"] == m]
            if not mine:
                continue
            cells = ""
            for s in SUBS:
                r = [g for g in mine if g["subtask"] == s]
                if not r:
                    cells += '<td class="r dim">-</td>'
                    continue
                k = sum(map(fn, r))
                pct = k / len(r)
                cls = "hi" if pct >= .7 else "mid" if pct >= .4 else "lo" if pct > 0 else "zero"
                cells += (f'<td class="r"><span class="cell {cls}">{k}/{len(r)}</span></td>')
            tot = sum(map(fn, mine))
            cells += (f'<td class="r tot">{tot}/{len(mine)}'
                      f'<i>{tot / len(mine):.0%}</i></td>')
            rows += f"<tr><td>{esc(m)}</td>{cells}</tr>"
        head = "".join(f'<th class="r">{esc(s)}</th>' for s in SUBS)
        return (f'<div class="board"><h3>{label}</h3><p class="note">{note}</p>'
                f'<table><thead><tr><th>model</th>{head}'
                f'<th class="r">overall</th></tr></thead><tbody>{rows}</tbody></table></div>')

    # ---- comparison against the previous configuration ---------------------------------
    # v2 compares against the 156-anchor v1 run; every later version compares against v2,
    # which is the configuration it was derived from by changing one subtask's rules.
    if VER == "v2":
        f_ = TRIN / "baseline_v1.json"
        base = json.loads(f_.read_text()) if f_.exists() else {}
        base_label, base_note = "v1", "the 156-anchor run"
    else:
        prev = [json.loads(l) for l in (TRIN / "grades_v2.jsonl").open()] if (
            TRIN / "grades_v2.jsonl").exists() else []
        base = {}
        for st in SUBS:
            r = [g for g in prev if g["subtask"] == st]
            if r:
                base[st] = {"_": {"n": len(r), "core": sum(map(is_core, r)),
                                  "pass": sum(map(is_pass, r))}}
        base_label, base_note = "v2", "the same 10 anchors before these rule changes"

    delta = ""
    if base:
        rows = ""
        for st in SUBS:
            b = base.get(st, {})
            bn = sum(v["n"] for v in b.values())
            bc, bf = sum(v["core"] for v in b.values()), sum(v["pass"] for v in b.values())
            cur = [g for g in flat if g["subtask"] == st]
            if not cur or not bn:
                continue
            cc, cf = sum(map(is_core, cur)), sum(map(is_pass, cur))

            def arrow(a, b_):
                dd = round((b_ - a) * 100)
                cls = "up" if dd > 0 else "down" if dd < 0 else "flat"
                return f'<span class="{cls}">{dd:+d}</span>'

            rows += (f'<tr><td>{esc(st)}</td>'
                     f'<td class="r dim">{bc / bn:.0%}</td>'
                     f'<td class="r">{cc / len(cur):.0%}</td>'
                     f'<td class="r">{arrow(bc / bn, cc / len(cur))}</td>'
                     f'<td class="r dim">{bf / bn:.0%}</td>'
                     f'<td class="r">{cf / len(cur):.0%}</td>'
                     f'<td class="r">{arrow(bf / bn, cf / len(cur))}</td></tr>')
        delta = (
          f'<div class="board wide"><h3>{esc(base_label)} compared with {esc(VER)}</h3>'
          f'<p class="note">Same models, same subtasks, same judge. <b>{esc(base_label)}</b> '
          f'is {esc(base_note)}. A subtask whose prompt did not change between the two is a '
          f'control and should barely move.</p>'
          '<table><thead><tr><th>subtask</th>'
          '<th class="r" colspan="3">answer correct</th>'
          '<th class="r" colspan="3">fully correct</th></tr>'
          f'<tr><th></th><th class="r">{esc(base_label)}</th><th class="r">{esc(VER)}</th>'
          '<th class="r">&Delta;</th>'
          f'<th class="r">{esc(base_label)}</th><th class="r">{esc(VER)}</th>'
          '<th class="r">&Delta;</th></tr></thead>'
          f'<tbody>{rows}</tbody></table></div>')

    boards = (table(is_core, "Answer correct",
                    "The substance is right &mdash; correctness scored 2 of 2. Reasoning, "
                    "completeness and polish may still be flawed.")
              + table(is_pass, "Fully correct",
                      "Every dimension perfect and no fatal error. This is the bar for "
                      "running a stage unattended.") + delta)

    # ---- per-subtask cards ------------------------------------------------------------
    cards = ""
    for st in SUBS:
        keys = sorted([k for k in samples if k[0] == st], key=lambda k: (k[1], k[2]))
        n = len([g for g in flat if g["subtask"] == st])
        c = sum(1 for g in flat if g["subtask"] == st and is_core(g))
        f = sum(1 for g in flat if g["subtask"] == st and is_pass(g))
        cards += (f'<h2 class="sec" data-sub="{esc(st)}">{esc(st)}'
                  f'<span class="secnum">{c}/{n} answer correct &middot; '
                  f'{f}/{n} fully correct</span></h2>'
                  f'<p class="lever" data-sub="{esc(st)}"><b>Prompt now supplies:</b> '
                  f'{esc(LEVERS[st])}</p>')
        for k in keys:
            s = samples[k]
            gm = grades.get(k, {})
            per = ""
            for m in models:
                g, ans = gm.get(m), answers.get(k, {}).get(m, "")
                if not g and not ans:
                    continue
                sc = ((g.get("correctness", 0), g.get("completeness", 0), g.get("usability", 0))
                      if g else (0, 0, 0))
                verd = ("pass" if g and is_pass(g) else "core" if g and is_core(g)
                        else "fail" if g else "none")
                vtxt = {"pass": "fully correct", "core": "answer correct",
                        "fail": "incorrect", "none": "not graded"}[verd]
                defects = "".join(f"<li>{esc(e)}</li>" for e in (g or {}).get("errors", []))
                fatal = ('<p class="fatal">fatal error</p>'
                         if g and g.get("fatal_error") else "")
                per += (
                  f'<details class="ans {verd}" data-model="{esc(m)}" data-verdict="{verd}">'
                  f'<summary><span class="mname">{esc(m)}</span>'
                  f'<span class="badge {verd}">{vtxt}</span>'
                  f'<span class="scores">correctness <b>{sc[0]}</b>'
                  f'completeness <b>{sc[1]}</b>usability <b>{sc[2]}</b></span></summary>'
                  f'{fatal}'
                  + (f'<h4>Judge&rsquo;s defects</h4><ul class="def">{defects}</ul>'
                     if defects else '<p class="clean">No defects recorded.</p>')
                  + (f'<h4>Judge&rsquo;s note</h4><p class="jnote">'
                     f'{esc((g or {}).get("note", ""))}</p>'
                     if (g or {}).get("note") else "")
                  + f'<h4>Answer</h4><pre>{esc(ans)}</pre></details>')
            for m in models:
                rr = rerun.get((s["subtask"], s["app"], s["system"], m))
                if not rr:
                    continue
                sc = (rr.get("correctness", 0), rr.get("completeness", 0), rr.get("usability", 0))
                good = (sc == (2, 2, 2) and not rr.get("fatal_error"))
                verd = "pass" if good else "core" if sc[0] == 2 else "fail"
                defects = "".join(f"<li>{esc(e)}</li>" for e in rr.get("errors", []))
                per += (
                  f'<details class="ans rerun {verd}" data-model="{esc(m)}" '
                  f'data-verdict="{verd}"><summary>'
                  f'<span class="mname">{esc(m)}</span>'
                  f'<span class="badge rr">re-run &middot; not truncated</span>'
                  f'<span class="badge {verd}">'
                  f'{"fully correct" if good else "answer correct" if sc[0] == 2 else "incorrect"}'
                  f'</span>'
                  f'<span class="scores">correctness <b>{sc[0]}</b>'
                  f'completeness <b>{sc[1]}</b>usability <b>{sc[2]}</b></span></summary>'
                  f'<p class="rrnote">The capped answer above stopped at '
                  f'<code>finish_reason: length</code>. This is the same prompt re-run at '
                  f'{rr.get("max_tokens", 16384):,} tokens, which completed naturally at '
                  f'<code>{esc(rr.get("finish_reason"))}</code> after '
                  f'{rr.get("completion_tokens") or "?"} completion tokens. It is NOT counted '
                  f'in the scoreboard.</p>'
                  + (f'<h4>Judge&rsquo;s defects</h4><ul class="def">{defects}</ul>'
                     if defects else '<p class="clean">No defects recorded.</p>')
                  + f'<h4>Answer</h4><pre>{esc(rr.get("answer", ""))}</pre></details>')

            row = "".join(
                f'<span class="pip {("pass" if gm.get(m) and is_pass(gm[m]) else "core" if gm.get(m) and is_core(gm[m]) else "fail" if gm.get(m) else "none")}" '
                f'title="{esc(m)}"></span>' for m in models)
            cards += (
              f'<article class="card" data-sub="{esc(st)}">'
              f'<header><div><h3>{esc(s["app"])} <span class="on">on</span> '
              f'{esc(s["system"])}</h3>'
              f'<p class="dom">{esc(s["domain"])} &middot; {esc(s.get("variation", ""))}</p>'
              f'</div><div class="pips">{row}</div></header>'
              f'<details class="prompt"><summary>Prompt given to every model</summary>'
              f'<pre>{esc(s["prompt"])}</pre></details>'
              + (f'<details class="prompt ref"><summary>Reference answer (from the catalog)'
                 f'</summary><pre>{esc(s.get("reference", ""))}</pre></details>'
                 if s.get("reference") else "")
              + f'<div class="answers">{per}</div></article>')

    # Reasoning models spend the token budget on thinking before any answer is emitted, so a
    # cap that is generous for a normal model can cut a reasoning model off mid-sentence — or
    # before it writes anything at all. Measured, not assumed: see skills/trinity_run.py.
    trunc = ""
    f_ = TRIN / "nemotron_cap_scan.json"
    if f_.exists():
        sc = json.loads(f_.read_text())
        cut = [o for o in sc if o.get("finish") == "length"]
        if cut:
            zero = sum(1 for o in cut if not o.get("chars"))
            from collections import Counter as _C
            bysub = ", ".join(f"{k} {v}" for k, v in _C(o["subtask"] for o in cut).most_common())
            head_ = ("<b>nemotron-3-ultra is capped at 4,096 tokens on this page, the same "
                     "as the other three.</b> " if NEMO_CAP == 4096 else
                     "<b>nemotron-3-ultra runs at a 16,384-token cap on this page.</b> ")
            trunc = (
              f'<div class="warn">{head_}'
              f'It is a reasoning model: the budget goes to thinking first and the answer '
              f'takes what is left, so the {esc(MAXTOK)}-token cap used for the other three '
              f'truncated it on <b>{len(cut)} of {len(sc)}</b> prompts'
              + (f', {zero} of them emitting no text at all' if zero else '') + ' &mdash; '
              f'every one reporting <code>finish_reason: length</code> at exactly 4,096 '
              f'completion tokens. Worst affected: {esc(bysub)}. At 16,384 tokens <b>none '
              f'truncate</b>. '
              + ('The figures above are the CAPPED run, so nemotron is scored partly on '
                 'answers it was cut off mid-way through &mdash; every model here gets the '
                 'same 4,096 budget, which is equal treatment but not equal opportunity for '
                 'a model that thinks before it answers. '
                 if NEMO_CAP == 4096 else
                 'The figures above are the corrected 16,384-token run. ')
              + f'Cards where the two gradings differ carry the other cap&rsquo;s answer for '
              f'comparison. The other three models never approach 4,096 and are identical on '
              f'both pages.</div>')

    modopts = "".join(f'<option value="{esc(m)}">{esc(m)}</option>' for m in models)
    subopts = "".join(f'<option value="{esc(s)}">{esc(s)}</option>' for s in SUBS)
    return PAGE.format(boards=boards, cards=cards, modopts=modopts, subopts=subopts,
                       nsamples=len(samples), ngrades=len(flat), nmodels=len(models),
                       ver=esc(VER), vernote=esc(VERSION_NOTE.get(VER, "")),
                       trunc=trunc)


PAGE = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Trinity Subtask Results</title>
<style>
:root{{
  --bg:#F4F2EF;--panel:#FFFFFF;--sunk:#EDE9E4;--ink:#171412;--ink-2:#5B534C;
  --ink-3:#918B84;--line:#DED8D1;--accent:#A6521E;--accent-soft:#F6E7DC;
  --accent-ink:#7C3B12;--pass:#2F7D5B;--pass-soft:#E1F0E8;--core:#B07A12;
  --core-soft:#F8EDD4;--fail:#B23A2B;--fail-soft:#F8E3DF;
  --mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
  --sans:ui-sans-serif,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;
  --shadow:0 1px 2px rgba(23,20,18,.05),0 8px 24px rgba(23,20,18,.06);
}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{
  --bg:#12100E;--panel:#1B1815;--sunk:#232019;--ink:#EFEAE4;--ink-2:#ADA49A;
  --ink-3:#6E665E;--line:#2E2A25;--accent:#E08A4E;--accent-soft:#33210F;
  --accent-ink:#F0AE7C;--pass:#5FBE92;--pass-soft:#122C21;--core:#DCA93F;
  --core-soft:#2E2410;--fail:#E2705C;--fail-soft:#311915;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 10px 30px rgba(0,0,0,.45);}}}}
:root[data-theme="dark"]{{
  --bg:#12100E;--panel:#1B1815;--sunk:#232019;--ink:#EFEAE4;--ink-2:#ADA49A;
  --ink-3:#6E665E;--line:#2E2A25;--accent:#E08A4E;--accent-soft:#33210F;
  --accent-ink:#F0AE7C;--pass:#5FBE92;--pass-soft:#122C21;--core:#DCA93F;
  --core-soft:#2E2410;--fail:#E2705C;--fail-soft:#311915;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 10px 30px rgba(0,0,0,.45);}}
*{{box-sizing:border-box;}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);
  font-size:14px;line-height:1.5;}}
.wrap{{max-width:1180px;margin:0 auto;padding:34px 20px 90px;}}
.eyebrow{{font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
  color:var(--accent-ink);background:var(--accent-soft);padding:4px 11px;border-radius:20px;
  display:inline-block;}}
h1{{font-size:clamp(25px,4vw,38px);line-height:1.1;letter-spacing:-.022em;margin:15px 0 8px;
  font-weight:660;max-width:22ch;text-wrap:balance;}}
.sub{{color:var(--ink-2);max-width:70ch;margin:0 0 26px;}}
.boards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(430px,1fr));gap:16px;
  margin-bottom:22px;}}
.board{{background:var(--panel);border:1px solid var(--line);border-radius:11px;
  padding:17px 19px 13px;box-shadow:var(--shadow);}}
.board.wide{{grid-column:1/-1;}}
.up{{color:var(--pass);font-weight:680;}}.down{{color:var(--fail);font-weight:680;}}
.flat{{color:var(--ink-3);}}
td.dim{{color:var(--ink-3);}}
.board h3{{margin:0 0 3px;font-size:13px;text-transform:uppercase;letter-spacing:.09em;
  color:var(--accent-ink);font-weight:700;}}
.note{{margin:0 0 12px;font-size:11.5px;color:var(--ink-3);line-height:1.45;}}
table{{width:100%;border-collapse:collapse;}}
th{{font-size:9.5px;text-transform:uppercase;letter-spacing:.06em;color:var(--ink-3);
  font-weight:700;padding:0 0 6px;border-bottom:1px solid var(--line);text-align:left;}}
th.r,td.r{{text-align:right;}}
td{{padding:6px 0;border-bottom:1px solid var(--line);font-size:12.5px;color:var(--ink-2);
  font-variant-numeric:tabular-nums;}}
td:first-child{{color:var(--ink);font-weight:600;font-size:12px;}}
tbody tr:last-child td{{border-bottom:none;}}
.cell{{font-family:var(--mono);font-size:11.5px;padding:2px 7px;border-radius:5px;
  font-weight:660;}}
.cell.hi{{background:var(--pass-soft);color:var(--pass);}}
.cell.mid{{background:var(--core-soft);color:var(--core);}}
.cell.lo{{background:var(--fail-soft);color:var(--fail);}}
.cell.zero{{background:var(--sunk);color:var(--ink-3);}}
td.tot{{font-family:var(--mono);color:var(--ink);font-weight:670;}}
td.tot i{{display:block;font-style:normal;font-size:10px;color:var(--ink-3);font-weight:600;}}
.bar{{position:sticky;top:0;z-index:9;background:var(--bg);padding:11px 0 12px;
  border-bottom:1px solid var(--line);display:flex;gap:9px;flex-wrap:wrap;align-items:center;
  margin-bottom:8px;}}
select,button{{font:inherit;font-size:12.5px;background:var(--panel);color:var(--ink);
  border:1px solid var(--line);border-radius:7px;padding:6px 9px;cursor:pointer;}}
button:hover,select:hover{{border-color:var(--accent);}}
.count{{margin-left:auto;font-size:11.5px;color:var(--ink-3);font-family:var(--mono);}}
h2.sec{{font-size:19px;margin:34px 0 4px;letter-spacing:-.015em;font-weight:660;
  display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;}}
.secnum{{font-family:var(--mono);font-size:11.5px;color:var(--ink-3);font-weight:600;}}
.lever{{margin:0 0 14px;font-size:12px;color:var(--ink-2);background:var(--accent-soft);
  border-left:3px solid var(--accent);border-radius:0 7px 7px 0;padding:8px 12px;
  line-height:1.5;}}
.lever b{{color:var(--accent-ink);}}
.ans.rerun{{border-left:3px dashed var(--accent);background:var(--bg);}}
.badge.rr{{background:var(--accent-soft);color:var(--accent-ink);}}
.rrnote{{margin:9px 12px;font-size:11.5px;color:var(--ink-3);line-height:1.5;}}
.rrnote code{{font-family:var(--mono);}}
.warn{{background:var(--core-soft);border-left:3px solid var(--core);
  border-radius:0 8px 8px 0;padding:12px 15px;margin-bottom:20px;font-size:12.5px;
  line-height:1.55;color:var(--ink-2);}}
.warn b{{color:var(--ink);}}
.warn code{{font-family:var(--mono);font-size:11.5px;}}
.card{{background:var(--panel);border:1px solid var(--line);border-radius:11px;
  padding:15px 17px;margin-bottom:12px;box-shadow:var(--shadow);}}
.card header{{display:flex;justify-content:space-between;gap:14px;align-items:flex-start;
  margin-bottom:10px;}}
.card h3{{margin:0;font-size:15px;font-weight:660;font-family:var(--mono);
  letter-spacing:-.01em;}}
.card h3 .on{{color:var(--ink-3);font-weight:400;font-family:var(--sans);font-size:12px;}}
.dom{{margin:2px 0 0;font-size:11.5px;color:var(--ink-3);}}
.pips{{display:flex;gap:4px;flex:none;padding-top:4px;}}
.pip{{width:11px;height:11px;border-radius:3px;background:var(--sunk);}}
.pip.pass{{background:var(--pass);}}.pip.core{{background:var(--core);}}
.pip.fail{{background:var(--fail);}}
details{{border-radius:8px;}}
summary{{cursor:pointer;list-style:none;}}
summary::-webkit-details-marker{{display:none;}}
.prompt{{background:var(--sunk);border:1px solid var(--line);margin-bottom:8px;}}
.prompt>summary{{padding:7px 11px;font-size:12px;color:var(--ink-2);font-weight:600;}}
.prompt>summary::before{{content:"\\25B8 ";color:var(--accent);}}
.prompt[open]>summary::before{{content:"\\25BE ";}}
.answers{{display:flex;flex-direction:column;gap:7px;margin-top:9px;}}
.ans{{border:1px solid var(--line);background:var(--panel);}}
.ans.pass{{border-left:3px solid var(--pass);}}
.ans.core{{border-left:3px solid var(--core);}}
.ans.fail{{border-left:3px solid var(--fail);}}
.ans>summary{{display:flex;align-items:center;gap:10px;padding:8px 12px;flex-wrap:wrap;}}
.mname{{font-family:var(--mono);font-size:12.5px;font-weight:660;min-width:150px;}}
.badge{{font-size:10px;text-transform:uppercase;letter-spacing:.06em;font-weight:700;
  padding:2px 8px;border-radius:20px;}}
.badge.pass{{background:var(--pass-soft);color:var(--pass);}}
.badge.core{{background:var(--core-soft);color:var(--core);}}
.badge.fail{{background:var(--fail-soft);color:var(--fail);}}
.badge.none{{background:var(--sunk);color:var(--ink-3);}}
.scores{{margin-left:auto;font-size:10.5px;color:var(--ink-3);font-family:var(--mono);
  display:flex;gap:11px;}}
.scores b{{color:var(--ink);margin-left:4px;}}
.ans h4{{margin:11px 12px 4px;font-size:10px;text-transform:uppercase;letter-spacing:.08em;
  color:var(--ink-3);font-weight:700;}}
.def{{margin:0 12px 10px;padding-left:18px;}}
.def li{{font-size:12.5px;color:var(--fail);margin-bottom:4px;line-height:1.45;}}
.clean,.jnote,.fatal{{margin:8px 12px;font-size:12.5px;color:var(--ink-2);}}
.fatal{{color:var(--fail);font-weight:660;text-transform:uppercase;font-size:10px;
  letter-spacing:.07em;}}
pre{{margin:0 12px 12px;padding:11px 13px;background:var(--sunk);border:1px solid var(--line);
  border-radius:7px;font-family:var(--mono);font-size:11.5px;line-height:1.5;
  white-space:pre-wrap;word-break:break-word;overflow-x:auto;max-height:460px;
  color:var(--ink-2);}}
.prompt pre{{margin:0 11px 11px;}}
.hide{{display:none!important;}}
footer{{margin-top:40px;padding-top:16px;border-top:1px solid var(--line);
  font-size:11.5px;color:var(--ink-3);line-height:1.6;}}
@media(max-width:700px){{.boards{{grid-template-columns:1fr;}}.scores{{margin-left:0;}}}}
</style>
<div class="wrap">
<span class="eyebrow">Trinity agent benchmark &middot; {ver} prompts</span>
<h1>Four pre-submission subtasks, four on-prem models, one judge</h1>
<p class="sub">{nsamples} samples &mdash; 10 stratified (application, system) anchors across each of
Software selection, Input preparation, Resource selection and Batch job creation &mdash; answered by
{nmodels} models and graded by Claude Opus 5. {vernote} Expand any answer to read what the model wrote and exactly what the
judge objected to.</p>

<div class="boards">{boards}</div>
{trunc}

<div class="bar">
  <select id="fsub"><option value="">All subtasks</option>{subopts}</select>
  <select id="fmod"><option value="">All models</option>{modopts}</select>
  <select id="fver"><option value="">All verdicts</option>
    <option value="pass">Fully correct only</option>
    <option value="core">Answer correct only</option>
    <option value="fail">Failures only</option></select>
  <button id="expand">Expand all answers</button>
  <button id="collapse">Collapse all</button>
  <span class="count" id="count"></span>
</div>

{cards}

<footer>
<b>How grading works.</b> Claude Opus 5 scores three dimensions 0&ndash;2 &mdash; correctness
(is the substance right), completeness (is anything required missing), usability (could this be
run as written) &mdash; plus a fatal-error flag. <i>Answer correct</i> means correctness&nbsp;=&nbsp;2
alone; <i>fully correct</i> means all three at 2 with no fatal error.<br>
<b>Caveats.</b> The judge has not been validated against a human rater; reading these cards is
how three miscalibrations were found and fixed. Samples are synthesised from the
<code>application_catalog</code> repository and anchored to (application, system) pairs its smoke
tests confirm exist, but they are not transcripts of real user requests. Ten anchors per subtask
is a small sample: a one-answer difference moves a cell by ten points.
</footer>
</div>
<script>
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
function apply(){{
  const sub=$('#fsub').value, mod=$('#fmod').value, ver=$('#fver').value;
  $$('.ans').forEach(a=>{{
    const okM=!mod||a.dataset.model===mod, okV=!ver||a.dataset.verdict===ver;
    a.classList.toggle('hide',!(okM&&okV));
  }});
  let shown=0;
  $$('.card').forEach(c=>{{
    const okS=!sub||c.dataset.sub===sub;
    const any=[...c.querySelectorAll('.ans')].some(a=>!a.classList.contains('hide'));
    const vis=okS&&any; c.classList.toggle('hide',!vis); if(vis)shown++;
  }});
  $$('.sec,.lever').forEach(h=>h.classList.toggle('hide',!!sub&&h.dataset.sub!==sub));
  $('#count').textContent=shown+' of '+$$('.card').length+' samples shown';
}}
['fsub','fmod','fver'].forEach(i=>$('#'+i).addEventListener('change',apply));
$('#expand').addEventListener('click',()=>$$('.ans').forEach(d=>d.open=true));
$('#collapse').addEventListener('click',()=>$$('details').forEach(d=>d.open=false));
apply();
</script>
"""


def main() -> int:
    OUT.write_text(build())
    print(f"{OUT}  ({OUT.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
