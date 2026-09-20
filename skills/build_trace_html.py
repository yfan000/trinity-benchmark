#!/usr/bin/env python3
"""results/trinity_trace_<ver>.html — the whole pipeline for one answer, end to end.

Prompt → answer → what the code decided → what the judge decided → the derived score, with the
evidence behind every verdict and, where a human reviewed the row, their mark beside it.

This exists because the scoreboard cannot answer the question that matters. "Batch job creation
33/40" tells you nothing about whether a rule is right, whether the code saw what it claims to
have seen, or whether a score follows from its verdicts. Every substantive finding today came
from reading a single judgement — that the walltime rule was unsatisfiable, that
`claims_true_to_catalog` fired on silence, that `all_required_files_present` accepted a mention
as a file. None was visible in an aggregate.

The columns are deliberately separated:
  CODE    deterministic checks, run before the judge; these cannot vary between runs
  JUDGE   the residual that needs reading comprehension
  HUMAN   shown only where a review exists, as the arbiter of the other two
  SCORE   computed in Python from the verdicts, with the derivation printed

Usage:
    TRINITY_VER=v7 RUBRIC=r13 python skills/build_trace_html.py
"""
from __future__ import annotations
import html
import json
import os
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from skills.judging.loader import load as load_skill  # noqa: E402

TRIN = ROOT / "results" / "skills" / "trinity"
VER = os.environ.get("TRINITY_VER", "v7")
RUBRIC = os.environ.get("RUBRIC", "r13")
JUDGE = os.environ.get("JUDGE", "gpt56terra")
OUT = ROOT / "results" / f"trinity_trace_{VER}.html"
SUBS = ["Software selection", "Input preparation", "Resource selection", "Batch job creation"]


def esc(s) -> str:
    return html.escape(str(s or ""))


def load(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.open()] if p.exists() else []


def human_marks() -> dict:
    """Reviewer marks, if a review CSV exists for this corpus. Keyed by (row, requirement)."""
    import csv
    out = {}
    d = TRIN / "review"
    keyf = TRIN / f"worksheet_key_{VER}_r4.json"
    if not d.exists() or not keyf.exists():
        return out
    key = {k["n"]: k for k in json.loads(keyf.read_text())}
    for f in d.glob("*.csv"):
        for r in csv.DictReader(f.open()):
            if not r.get("human"):
                continue
            k = key.get(int(r["n"]))
            if k:
                out[(k["model"], r["subtask"], r["app"], r["system"],
                     r["requirement"])] = r["human"]
    return out


def main() -> int:
    samples = {(s["subtask"], s["app"], s["system"]): s
               for s in load(TRIN / f"samples_{VER}.jsonl")}
    answers = {(a["model"], a["subtask"], a["app"], a["system"]): a["answer"]
               for a in load(TRIN / f"answers_{VER}.jsonl") if a.get("answer")}
    runs = defaultdict(list)
    for p in sorted(TRIN.glob(f"grades_{VER}__{JUDGE}__{RUBRIC}__run*.jsonl")):
        for r in load(p):
            runs[(r["model"], r["subtask"], r["app"], r["system"])].append(r)
    if not runs:
        print(f"no graded cell {VER}/{JUDGE}/{RUBRIC}")
        return 1
    hm = human_marks()

    cards, tally = "", Counter()
    for key in sorted(runs, key=lambda k: (SUBS.index(k[1]) if k[1] in SUBS else 9, k[2], k[0])):
        model, st, app, system = key
        rows = runs[key]
        s = samples.get((st, app, system))
        if not s:
            continue
        med = {d: int(statistics.median([r[d] for r in rows]))
               for d in ("correctness", "completeness", "usability")}
        fatal = sum(bool(r.get("fatal_error")) for r in rows) > len(rows) / 2
        ok = all(med[d] == 2 for d in med) and not fatal
        tally["pass" if ok else "fail"] += 1
        reqs = rows[0].get("requirements") or {}
        unstable = any(len({(r.get("requirements") or {}).get(i, {}).get("verdict")
                            for r in rows}) > 1 for i in reqs)

        tr = ""
        for rid, v in sorted(reqs.items(), key=lambda kv: (kv[1].get("verdict") != "violated",
                                                           kv[0])):
            vd = v.get("verdict", "")
            by = v.get("decided_by", "judge")
            h = hm.get((model, st, app, system, rid), "")
            dis = h and h != vd
            tally[f"{by}:{vd}"] += 1
            tr += (f'<tr class="rq" data-v="{esc(vd)}" data-by="{esc(by)}"'
                   f'{" data-dis=1" if dis else ""}>'
                   f'<td><code>{esc(rid)}</code>'
                   f'<div class="ev">{esc(v.get("evidence",""))[:260]}</div></td>'
                   f'<td><span class="by {esc(by)}">{"code" if by=="deterministic" else "judge"}'
                   f'</span></td>'
                   f'<td><span class="v {esc(vd)}">{esc(vd).replace("_"," ")}</span></td>'
                   f'<td>{f'<span class="v {esc(h)} hum">{esc(h).replace("_"," ")}</span>' if h else ""}'
                   f'{" <b class=dis>≠</b>" if dis else ""}</td></tr>')

        cards += (
          f'<article class="card" data-sub="{esc(st)}" data-model="{esc(model)}" '
          f'data-res="{"pass" if ok else "fail"}">'
          f'<header><div><h3>{esc(app)} <span class="on">on</span> {esc(system)}</h3>'
          f'<p class="meta">{esc(st)} &middot; <b>{esc(model)}</b>'
          + (' &middot; <span class="warn">verdict varied across replicates</span>'
             if unstable else '') + '</p></div>'
          f'<div class="sc {"ok" if ok else "no"}">'
          f'<span>c{med["correctness"]}</span><span>p{med["completeness"]}</span>'
          f'<span>u{med["usability"]}</span>'
          + ('<span class="f">FATAL</span>' if fatal else '') + '</div></header>'
          f'<p class="deriv">{esc(rows[0].get("derivation","")) or "&mdash;"}</p>'
          f'<details><summary>Prompt given to the model</summary>'
          f'<pre>{esc(s["prompt"])}</pre></details>'
          f'<details><summary>The model&rsquo;s answer</summary>'
          f'<pre>{esc(answers.get(key,""))}</pre></details>'
          f'<table class="reqs"><thead><tr><th>requirement &amp; evidence</th><th>decided by</th>'
          f'<th>verdict</th><th>human</th></tr></thead><tbody>{tr}</tbody></table>'
          '</article>')

    det = sum(v for k, v in tally.items() if k.startswith("deterministic:"))
    jud = sum(v for k, v in tally.items() if k.startswith("judge:"))
    OUT.write_text(PAGE.format(
        cards=cards, ver=esc(VER), rubric=esc(RUBRIC), judge=esc(JUDGE),
        n=tally["pass"] + tally["fail"], npass=tally["pass"],
        det=det, jud=jud, nhum=len(hm),
        models="".join(f'<option>{esc(m)}</option>' for m in sorted({k[0] for k in runs})),
        subs="".join(f'<option>{esc(x)}</option>' for x in SUBS)))
    print(f"{OUT}  ({OUT.stat().st_size//1024} KB)  "
          f"{tally['pass']+tally['fail']} traces, {det} code + {jud} judge verdicts"
          + (f", {len(hm)} human marks overlaid" if hm else ""))
    return 0


PAGE = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Trinity Pipeline Trace</title>
<style>
:root{{--bg:#F4F4F2;--panel:#fff;--sunk:#EDECE8;--ink:#141412;--ink2:#57544E;--ink3:#8F8B83;
 --line:#DEDBD4;--acc:#35566B;--accs:#E1EAF0;--acct:#233D4E;--ok:#2C7A57;--oks:#E0EFE8;
 --no:#AE3B2B;--nos:#F7E3DF;--na:#847F77;--nas:#EBE9E5;--warn:#9E6B14;--warns:#F6EAD5;
 --mono:ui-monospace,"SF Mono",Menlo,monospace;--sans:ui-sans-serif,-apple-system,"Segoe UI",Arial,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#101111;--panel:#191A1A;
 --sunk:#212222;--ink:#ECEAE6;--ink2:#A8A49C;--ink3:#6D6961;--line:#2B2C2C;--acc:#6FA3BF;
 --accs:#152833;--acct:#9CC8DF;--ok:#5CBB8D;--oks:#11291F;--no:#DE6D59;--nos:#2D1714;
 --na:#7A756D;--nas:#212222;--warn:#CE9A3F;--warns:#2B2110}}}}
:root[data-theme="dark"]{{--bg:#101111;--panel:#191A1A;--sunk:#212222;--ink:#ECEAE6;--ink2:#A8A49C;
 --ink3:#6D6961;--line:#2B2C2C;--acc:#6FA3BF;--accs:#152833;--acct:#9CC8DF;--ok:#5CBB8D;
 --oks:#11291F;--no:#DE6D59;--nos:#2D1714;--na:#7A756D;--nas:#212222;--warn:#CE9A3F;--warns:#2B2110}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:14px;line-height:1.5}}
.wrap{{max-width:1120px;margin:0 auto;padding:28px 18px 90px}}
h1{{font-size:clamp(22px,3.2vw,31px);margin:10px 0 6px;font-weight:660;letter-spacing:-.02em}}
.sub{{color:var(--ink2);max-width:76ch;margin:0 0 18px}}
.stats{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px}}
.stat{{background:var(--panel);border:1px solid var(--line);border-radius:9px;padding:9px 14px}}
.stat b{{display:block;font-family:var(--mono);font-size:18px;font-weight:660}}
.stat span{{font-size:9.5px;text-transform:uppercase;letter-spacing:.07em;color:var(--ink3);font-weight:670}}
.bar{{position:sticky;top:0;z-index:20;background:var(--bg);padding:10px 0;border-bottom:1px solid var(--line);
 display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:14px}}
select,button{{font:inherit;font-size:12.5px;background:var(--panel);color:var(--ink);
 border:1px solid var(--line);border-radius:7px;padding:6px 9px;cursor:pointer}}
select:hover,button:hover{{border-color:var(--acc)}}
.count{{margin-left:auto;font-family:var(--mono);font-size:11.5px;color:var(--ink3)}}
.card{{background:var(--panel);border:1px solid var(--line);border-radius:11px;padding:15px 17px;margin-bottom:12px}}
header{{display:flex;justify-content:space-between;gap:14px;align-items:flex-start;margin-bottom:7px}}
h3{{margin:0;font-size:15px;font-family:var(--mono);font-weight:660;letter-spacing:-.01em}}
h3 .on{{color:var(--ink3);font-family:var(--sans);font-weight:400;font-size:12px}}
.meta{{margin:2px 0 0;font-size:11.5px;color:var(--ink3)}}
.meta b{{color:var(--ink2)}}
.warn{{color:var(--warn);font-weight:640}}
.sc{{display:flex;gap:5px;flex:none}}
.sc span{{font-family:var(--mono);font-size:11.5px;font-weight:670;padding:3px 7px;border-radius:6px;
 background:var(--sunk);color:var(--ink2)}}
.sc.ok span{{background:var(--oks);color:var(--ok)}}
.sc.no span{{background:var(--nos);color:var(--no)}}
.sc .f{{background:var(--no);color:#fff}}
.deriv{{margin:0 0 9px;font-size:12px;color:var(--ink3);font-style:italic}}
details{{border:1px solid var(--line);border-radius:8px;background:var(--sunk);margin-bottom:8px}}
summary{{cursor:pointer;padding:7px 11px;font-size:12px;font-weight:600;color:var(--ink2);list-style:none}}
summary::-webkit-details-marker{{display:none}}
summary::before{{content:"\\25B8 ";color:var(--acc)}}
details[open]>summary::before{{content:"\\25BE "}}
pre{{margin:0 11px 11px;padding:11px 13px;background:var(--panel);border:1px solid var(--line);
 border-radius:7px;font-family:var(--mono);font-size:11.5px;line-height:1.55;white-space:pre-wrap;
 word-break:break-word;max-height:430px;overflow:auto;color:var(--ink2)}}
table.reqs{{width:100%;border-collapse:collapse;margin-top:4px}}
table.reqs th{{font-size:9.5px;text-transform:uppercase;letter-spacing:.06em;color:var(--ink3);
 font-weight:700;text-align:left;padding:0 8px 5px 0;border-bottom:1px solid var(--line)}}
table.reqs td{{padding:7px 8px 7px 0;border-bottom:1px solid var(--line);vertical-align:top;font-size:12px}}
td code{{font-family:var(--mono);font-size:11px;color:var(--ink);font-weight:600}}
.ev{{color:var(--ink3);font-size:11.5px;margin-top:2px;max-width:58ch;line-height:1.45}}
.by{{font-size:9.5px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;padding:2px 7px;border-radius:20px}}
.by.deterministic{{background:var(--accs);color:var(--acct)}}
.by.judge{{background:var(--warns);color:var(--warn)}}
.v{{font-size:11px;font-weight:660;padding:2px 8px;border-radius:6px;white-space:nowrap}}
.v.satisfied{{background:var(--oks);color:var(--ok)}}
.v.violated{{background:var(--nos);color:var(--no)}}
.v.not_applicable,.v.not_evaluated{{background:var(--nas);color:var(--na)}}
.v.hum{{outline:1px dashed var(--ink3)}}
b.dis{{color:var(--no);font-size:13px}}
tr[data-dis] td{{background:var(--nos)}}
.hide{{display:none!important}}
footer{{margin-top:26px;padding-top:14px;border-top:1px solid var(--line);font-size:11.5px;
 color:var(--ink3);line-height:1.6}}
</style>
<div class="wrap">
<h1>Pipeline trace &mdash; {ver} under {rubric}</h1>
<p class="sub">Every answer end to end: the prompt it was given, what it wrote, which
requirements <b>code</b> decided before the judge ran, which the <b>judge</b> ruled on, and the
score computed from those verdicts. Where a human reviewed a row, their mark sits beside the
verdict and a <b>&ne;</b> marks disagreement.</p>

<div class="stats">
 <div class="stat"><b>{npass}/{n}</b><span>fully correct</span></div>
 <div class="stat"><b>{det}</b><span>decided in code</span></div>
 <div class="stat"><b>{jud}</b><span>decided by judge</span></div>
 <div class="stat"><b>{nhum}</b><span>human marks</span></div>
 <div class="stat"><b>{judge}</b><span>judge model</span></div>
</div>

<div class="bar">
 <select id="fsub"><option value="">All subtasks</option>{subs}</select>
 <select id="fmod"><option value="">All models</option>{models}</select>
 <select id="fres"><option value="">All outcomes</option>
  <option value="pass">fully correct</option><option value="fail">not fully correct</option></select>
 <select id="fv"><option value="">All verdicts</option>
  <option value="violated">violations only</option><option value="dis">human disagreed</option></select>
 <button id="ex">Expand answers</button><button id="co">Collapse</button>
 <span class="count" id="count"></span>
</div>
{cards}
<footer>Requirements marked <b>code</b> are evaluated in Python before the judge is called and
cannot vary between runs; those marked <b>judge</b> need reading comprehension. Scores are
computed from the verdicts, not written by the judge &mdash; the line under each header is the
derivation. A card flagged <i>verdict varied across replicates</i> got different answers from
the same judge on the same input.</footer>
</div>
<script>
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
function apply(){{
 const sb=$('#fsub').value,md=$('#fmod').value,rs=$('#fres').value,v=$('#fv').value;
 let n=0;
 $$('.card').forEach(c=>{{
  let ok=(!sb||c.dataset.sub===sb)&&(!md||c.dataset.model===md)&&(!rs||c.dataset.res===rs);
  if(ok&&v==='violated')ok=!!c.querySelector('tr.rq[data-v="violated"]');
  if(ok&&v==='dis')ok=!!c.querySelector('tr.rq[data-dis]');
  c.classList.toggle('hide',!ok); if(ok)n++;
 }});
 $$('tr.rq').forEach(r=>r.classList.toggle('hide',
   (v==='violated'&&r.dataset.v!=='violated')||(v==='dis'&&!r.dataset.dis)));
 $('#count').textContent=n+' of '+$$('.card').length+' traces';
}}
['fsub','fmod','fres','fv'].forEach(i=>$('#'+i).addEventListener('change',apply));
$('#ex').addEventListener('click',()=>$$('details').forEach(d=>d.open=true));
$('#co').addEventListener('click',()=>$$('details').forEach(d=>d.open=false));
apply();
</script>
"""

if __name__ == "__main__":
    sys.exit(main())
