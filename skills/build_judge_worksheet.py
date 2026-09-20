#!/usr/bin/env python3
"""results/judge_worksheet.html — 40 blind judgements, the only measure of judge ACCURACY.

Everything measured so far is precision or control-based. Replicates showed the judge agreeing
with itself (22/159 unstable under r2), and calibration showed it not marking down real runs
(5/7 clean). Neither says whether it is RIGHT about a model's answer, because no human has
looked. This is that measurement.

Design decisions, each for a reason:

  BLIND, AND THE MODEL HIDDEN. The reviewer sees the prompt, the requirements and the answer —
  never the judge's verdicts, and never which model wrote it. build_v2_html.py shows the model
  name; a reviewer who knows a row is llama-3.1-8b grades it differently. Row order is
  randomised for the same reason: the existing pages group by subtask, which anchors.

  PER-REQUIREMENT, NOT PER-SCORE. The reviewer marks the same unit the judge rules on, so
  agreement is measured where decisions are actually made. The 0-2 scores are derived in code
  from those marks, exactly as they are for the judge, so both sides are scored identically.

  TWO PASSES. Pass A collects independent marks. Pass B reveals the judge and asks WHY the
  reviewer disagrees, in the four categories that map to library edits. Pass B measures
  precision well and recall badly by construction — the reviewer, having seen the judge's
  list, will not independently recall what is missing — so recall comes only from Pass A.

  DEV/TEST SPLIT by a fixed seed. Iterating a rubric against the same labels is a fit
  procedure; TEST exists to catch overfitting and is opened at most twice.

Progress is kept in the browser so the page can be closed and reopened. Export writes a CSV
that skills/compute_judge_agreement.py scores.

Usage:
    python skills/build_judge_worksheet.py --corpus v6 --judge gpt56terra --rubric r4 --n 40
"""
from __future__ import annotations
import argparse
import html
import json
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from skills.judging.loader import load as load_skill  # noqa: E402

TRIN = ROOT / "results" / "skills" / "trinity"
OUT = ROOT / "results" / "judge_worksheet.html"
SUBS = ["Software selection", "Input preparation", "Resource selection", "Batch job creation"]


def esc(s) -> str:
    return html.escape(str(s or ""))


def consensus(corpus, judge, rubric):
    runs = defaultdict(list)
    for p in sorted(TRIN.glob(f"grades_{corpus}__{judge}__{rubric}__run*.jsonl")):
        for r in map(json.loads, p.open()):
            runs[(r["model"], r["subtask"], r["app"], r["system"])].append(r)
    out = {}
    for k, rows in runs.items():
        med = {d: int(statistics.median([r[d] for r in rows]))
               for d in ("correctness", "completeness", "usability")}
        med["fatal_error"] = sum(bool(r.get("fatal_error")) for r in rows) > len(rows) / 2
        med["requirements"] = rows[0].get("requirements", {})
        med["n_replicates"] = len(rows)
        out[k] = med
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="v6")
    ap.add_argument("--judge", default="gpt56terra")
    ap.add_argument("--rubric", default="r4")
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--seed", type=int, default=11)
    a = ap.parse_args()

    samples = {(s["subtask"], s["app"], s["system"]): s
               for s in map(json.loads, (TRIN / f"samples_{a.corpus}.jsonl").open())}
    answers = {(r["model"], r["subtask"], r["app"], r["system"]): r["answer"]
               for r in map(json.loads, (TRIN / f"answers_{a.corpus}.jsonl").open())
               if r.get("answer")}
    grades = consensus(a.corpus, a.judge, a.rubric)
    if not grades:
        print(f"no graded cell for {a.corpus}/{a.judge}/{a.rubric} — run trinity_rejudge first")
        return 1

    # Stratify: equal per subtask, spread across models, so no subtask or model dominates.
    rng = random.Random(a.seed)
    per = max(1, a.n // len(SUBS))
    picked = []
    for st in SUBS:
        ks = [k for k in grades if k[1] == st and k in answers]
        by_model = defaultdict(list)
        for k in ks:
            by_model[k[0]].append(k)
        for v in by_model.values():
            rng.shuffle(v)
        round_robin, i = [], 0
        while len(round_robin) < min(per, len(ks)):
            for m in sorted(by_model):
                if i < len(by_model[m]):
                    round_robin.append(by_model[m][i])
                if len(round_robin) >= per:
                    break
            i += 1
        picked += round_robin[:per]
    rng.shuffle(picked)                       # randomise presentation order

    items = []
    for n, k in enumerate(picked):
        model, st, app, system = k
        s = samples[(st, app, system)]
        skill = load_skill(st, app, system, rubric_id=a.rubric)
        g = grades[k]
        items.append({
            "n": n + 1, "split": "DEV" if n % 10 < 8 else "TEST",
            "subtask": st, "app": app, "system": system,
            # NOTE: the model name is deliberately NOT carried into `items`. An earlier
            # version embedded it with a comment claiming it was withheld, which was false —
            # it sat in the page's JSON, one devtools inspection from a reviewer who wanted
            # it. Identities live only in the key file and are joined at scoring time.
            "prompt": s["prompt"], "answer": answers[k],
            "reqs": [{"id": r["id"], "claim": " ".join(str(r["claim"]).split()),
                      "sev": r.get("severity", "major"), "dim": r.get("dimension"),
                      "det": r.get("decided_by") == "deterministic"}
                     for r in skill.requirements],
            "free": [{"axis": f["axis"], "note": " ".join(str(f["note"]).split())}
                     for f in skill.free_choice],
            "judge": {rid: v.get("verdict") for rid, v in (g.get("requirements") or {}).items()},
            "judge_ev": {rid: v.get("evidence", "")[:220]
                         for rid, v in (g.get("requirements") or {}).items()},
        })

    key = [{"n": it["n"], "model": m, "subtask": it["subtask"], "app": it["app"],
            "system": it["system"], "split": it["split"]}
           for it, m in zip(items, [k[0] for k in picked])]
    (TRIN / f"worksheet_key_{a.corpus}_{a.rubric}.json").write_text(json.dumps(key, indent=1))

    OUT.write_text(PAGE.replace("__ITEMS__", json.dumps(items))
                       .replace("__META__", json.dumps(
                           {"corpus": a.corpus, "judge": a.judge, "rubric": a.rubric,
                            "n": len(items), "seed": a.seed})))
    dev = sum(1 for i in items if i["split"] == "DEV")
    print(f"{len(items)} items ({dev} DEV / {len(items)-dev} TEST) -> {OUT}")
    print(f"key (model identities, for scoring only) -> "
          f"worksheet_key_{a.corpus}_{a.rubric}.json")
    return 0


PAGE = r"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Judge Review Worksheet</title>
<style>
:root{--bg:#F6F4F1;--panel:#fff;--sunk:#EFEBE6;--ink:#16130F;--ink2:#5E564C;--ink3:#968C80;
 --line:#E0D9D0;--acc:#7A4E24;--accs:#F3E7DA;--acct:#5C3A1A;--ok:#2F7D5B;--oks:#E2F0E9;
 --no:#B3402F;--nos:#F8E4E0;--na:#8A8177;--nas:#EEEBE7;
 --mono:ui-monospace,"SF Mono",Menlo,monospace;--sans:ui-sans-serif,-apple-system,"Segoe UI",Arial,sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#121110;--panel:#1B1A18;
 --sunk:#232120;--ink:#EEEAE4;--ink2:#ABA298;--ink3:#6F675D;--line:#2D2A26;--acc:#D08B4F;
 --accs:#2E2013;--acct:#E8AE77;--ok:#5FBE92;--oks:#122A20;--no:#E0705C;--nos:#2E1815;
 --na:#7C736A;--nas:#232120}}
:root[data-theme="dark"]{--bg:#121110;--panel:#1B1A18;--sunk:#232120;--ink:#EEEAE4;--ink2:#ABA298;
 --ink3:#6F675D;--line:#2D2A26;--acc:#D08B4F;--accs:#2E2013;--acct:#E8AE77;--ok:#5FBE92;
 --oks:#122A20;--no:#E0705C;--nos:#2E1815;--na:#7C736A;--nas:#232120}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:14px;line-height:1.5}
.wrap{max-width:1000px;margin:0 auto;padding:26px 18px 90px}
h1{font-size:clamp(21px,3vw,30px);margin:10px 0 6px;font-weight:660;letter-spacing:-.02em}
.sub{color:var(--ink2);max-width:74ch;margin:0 0 18px}
.bar{position:sticky;top:0;z-index:20;background:var(--bg);padding:10px 0;border-bottom:1px solid var(--line);
 display:flex;gap:9px;align-items:center;flex-wrap:wrap;margin-bottom:14px}
button,select{font:inherit;font-size:12.5px;background:var(--panel);color:var(--ink);
 border:1px solid var(--line);border-radius:7px;padding:6px 11px;cursor:pointer}
button:hover,select:hover{border-color:var(--acc)}
button.primary{background:var(--acc);color:#fff;border-color:var(--acc);font-weight:640}
.count{margin-left:auto;font-family:var(--mono);font-size:12px;color:var(--ink3)}
.card{background:var(--panel);border:1px solid var(--line);border-radius:11px;padding:16px 18px;margin-bottom:14px}
.hd{display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:8px}
.hd h2{font-size:15px;margin:0;font-weight:660}
.tag{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;
 background:var(--accs);color:var(--acct);padding:2px 8px;border-radius:20px}
.tag.test{background:var(--nas);color:var(--na)}
details{margin-bottom:9px;border:1px solid var(--line);border-radius:8px;background:var(--sunk)}
summary{cursor:pointer;padding:8px 12px;font-size:12.5px;font-weight:600;color:var(--ink2);list-style:none}
summary::-webkit-details-marker{display:none}
summary::before{content:"\25B8 ";color:var(--acc)}
details[open]>summary::before{content:"\25BE "}
pre{margin:0 11px 11px;padding:11px 13px;background:var(--panel);border:1px solid var(--line);
 border-radius:7px;font-family:var(--mono);font-size:11.5px;line-height:1.55;white-space:pre-wrap;
 word-break:break-word;max-height:440px;overflow:auto;color:var(--ink2)}
.free{margin:0 12px 11px;font-size:12px;color:var(--ink3)}
.free b{color:var(--ink2)}
table.reqs{width:100%;border-collapse:collapse;margin-top:6px}
table.reqs th{font-size:9.5px;text-transform:uppercase;letter-spacing:.06em;color:var(--ink3);
 font-weight:700;text-align:left;padding:0 6px 5px 0;border-bottom:1px solid var(--line)}
table.reqs td{padding:8px 6px 8px 0;border-bottom:1px solid var(--line);font-size:12.5px;vertical-align:top}
.rid{font-family:var(--mono);font-size:11px;color:var(--ink);font-weight:600}
.rclaim{color:var(--ink2);margin-top:2px;max-width:56ch}
.sev{font-size:9.5px;font-weight:700;text-transform:uppercase}
.sev.fatal{color:var(--no)}.sev.major{color:var(--acc)}.sev.minor{color:var(--ink3)}
.opts{display:flex;gap:4px}
.opt{font-size:11px;padding:4px 9px;border:1px solid var(--line);border-radius:6px;cursor:pointer;
 background:var(--panel);color:var(--ink2);white-space:nowrap}
.opt.sel[data-v="satisfied"]{background:var(--oks);border-color:var(--ok);color:var(--ok);font-weight:660}
.opt.sel[data-v="violated"]{background:var(--nos);border-color:var(--no);color:var(--no);font-weight:660}
.opt.sel[data-v="not_applicable"]{background:var(--nas);border-color:var(--na);color:var(--na);font-weight:660}
.jv{font-size:10.5px;font-family:var(--mono);color:var(--ink3);margin-top:4px}
.jv.dis{color:var(--no);font-weight:660}
.why{margin-top:5px}
.why select{font-size:11px;padding:3px 6px}
textarea{width:100%;font:inherit;font-size:12px;background:var(--sunk);color:var(--ink);
 border:1px solid var(--line);border-radius:7px;padding:8px;margin-top:8px;resize:vertical}
.conf{display:flex;gap:6px;align-items:center;margin-top:8px;font-size:12px;color:var(--ink2)}
.done{opacity:.55}
.note{background:var(--accs);border-left:3px solid var(--acc);border-radius:0 8px 8px 0;
 padding:11px 14px;margin-bottom:16px;font-size:12.5px;color:var(--ink2);line-height:1.55}
.note b{color:var(--ink)}
.hide{display:none!important}
</style>
<div class="wrap">
<h1>Judge review worksheet</h1>
<p class="sub">The only measurement of whether the judge is <i>right</i>. Replicates showed it
agrees with itself and calibration showed it does not mark down real runs &mdash; neither says
it judges a model&rsquo;s answer correctly.</p>

<div class="note"><b>Pass A is blind.</b> You see the prompt, the requirements and the answer.
You do not see the judge&rsquo;s verdicts or which model wrote it &mdash; knowing either changes
how people grade, and order is randomised for the same reason. Mark each requirement as you
read the answer. Switch to <b>Pass B</b> only after finishing a card: it reveals the judge and
asks why you disagree, in the four categories that map to a library edit.<br>
<b>Scores are not entered.</b> They are computed from your marks by the same rule applied to
the judge, so both sides are scored identically.</div>

<div class="bar">
 <button id="pass" class="primary">Pass A &mdash; blind</button>
 <select id="fsplit"><option value="">DEV + TEST</option><option>DEV</option><option>TEST</option></select>
 <select id="fdone"><option value="">All</option><option value="todo">Unfinished</option></select>
 <button id="export">Export CSV</button>
 <button id="reset">Clear</button>
 <span class="count" id="count"></span>
</div>
<div id="cards"></div>
<footer style="margin-top:28px;padding-top:14px;border-top:1px solid var(--line);font-size:11.5px;color:var(--ink3)">
Progress is saved in this browser. Export writes a CSV for
<code>skills/compute_judge_agreement.py</code>.</footer>
</div>
<script>
const ITEMS=__ITEMS__, META=__META__;
const KEY='judgews_'+META.corpus+'_'+META.rubric;
let S={}; try{S=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){S={}}
let passB=false;
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}};
const st=n=>S[n]||(S[n]={marks:{},why:{},defects:'',conf:''});
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

function render(){
 const fs=document.getElementById('fsplit').value, fd=document.getElementById('fdone').value;
 let shown=0, done=0;
 document.getElementById('cards').innerHTML=ITEMS.map(it=>{
  const s=st(it.n);
  const complete=it.reqs.every(r=>s.marks[r.id]);
  if(complete)done++;
  if((fs&&it.split!==fs)||(fd==='todo'&&complete))return '';
  shown++;
  const rows=it.reqs.map(r=>{
   const mine=s.marks[r.id]||'', jv=it.judge[r.id]||'';
   const dis=passB&&mine&&jv&&mine!==jv;
   return `<tr><td><span class="rid">${esc(r.id)}</span>
     <div class="rclaim">${esc(r.claim)}</div>
     <span class="sev ${r.sev}">${r.sev}</span>
     ${passB&&jv?`<div class="jv ${dis?'dis':''}">judge: ${esc(jv)}${dis?' &mdash; you disagree':''}
        ${it.judge_ev[r.id]?'<br>'+esc(it.judge_ev[r.id]):''}</div>`:''}
     ${dis?`<div class="why"><select data-n="${it.n}" data-r="${esc(r.id)}" class="whysel">
        <option value="">why do you disagree?</option>
        <option value="scope">requirement should not apply here</option>
        <option value="missing">judge missed something</option>
        <option value="wrong">requirement itself is wrong</option>
        <option value="verdict">right requirement, wrong verdict</option>
      </select></div>`:''}
    </td><td><div class="opts">
     ${['satisfied','violated','not_applicable'].map(v=>
       `<span class="opt ${mine===v?'sel':''}" data-v="${v}" data-n="${it.n}" data-r="${esc(r.id)}"
        >${v==='not_applicable'?'n/a':v}</span>`).join('')}
    </div></td></tr>`}).join('');
  return `<article class="card ${complete?'done':''}">
   <div class="hd"><h2>#${it.n} &middot; ${esc(it.subtask)} &middot; ${esc(it.app)} on ${esc(it.system)}</h2>
    <span class="tag ${it.split==='TEST'?'test':''}">${it.split}</span></div>
   <details><summary>Prompt</summary><pre>${esc(it.prompt)}</pre></details>
   <details open><summary>Answer</summary><pre>${esc(it.answer)}</pre></details>
   ${it.free.length?`<div class="free"><b>Free choice &mdash; never mark violated for:</b>
     ${it.free.map(f=>esc(f.axis)).join(' &middot; ')}</div>`:''}
   <table class="reqs"><thead><tr><th>requirement</th><th style="width:230px">your verdict</th></tr></thead>
    <tbody>${rows}</tbody></table>
   <textarea data-n="${it.n}" class="def" rows="2"
     placeholder="Anything wrong with this answer that no requirement covers?">${esc(s.defects)}</textarea>
   <div class="conf">confidence
    <select data-n="${it.n}" class="conf-sel">
     <option value="">&mdash;</option><option value="3">3 sure</option>
     <option value="2">2 fairly</option><option value="1">1 unsure</option></select></div>
  </article>`}).join('');
 ITEMS.forEach(it=>{const s=st(it.n);
  document.querySelectorAll(`.conf-sel[data-n="${it.n}"]`).forEach(e=>e.value=s.conf||'');
  Object.entries(s.why||{}).forEach(([r,v])=>{
   const e=document.querySelector(`.whysel[data-n="${it.n}"][data-r="${CSS.escape(r)}"]`);
   if(e)e.value=v;});});
 document.getElementById('count').textContent=`${done}/${ITEMS.length} done · ${shown} shown`;
}
document.addEventListener('click',e=>{
 const o=e.target.closest('.opt'); if(!o)return;
 const s=st(+o.dataset.n); s.marks[o.dataset.r]=o.dataset.v; save(); render();});
document.addEventListener('change',e=>{
 if(e.target.classList.contains('whysel')){st(+e.target.dataset.n).why[e.target.dataset.r]=e.target.value;save();}
 if(e.target.classList.contains('conf-sel')){st(+e.target.dataset.n).conf=e.target.value;save();}});
document.addEventListener('input',e=>{
 if(e.target.classList.contains('def')){st(+e.target.dataset.n).defects=e.target.value;save();}});
document.getElementById('pass').addEventListener('click',()=>{
 passB=!passB;const b=document.getElementById('pass');
 b.textContent=passB?'Pass B — judge revealed':'Pass A — blind';
 b.classList.toggle('primary',!passB);render();});
['fsplit','fdone'].forEach(i=>document.getElementById(i).addEventListener('change',render));
document.getElementById('reset').addEventListener('click',()=>{
 if(confirm('Clear all your marks?')){S={};save();render();}});
document.getElementById('export').addEventListener('click',()=>{
 const rows=[['n','split','subtask','app','system','requirement','human','judge','why','confidence','defects']];
 ITEMS.forEach(it=>{const s=st(it.n);
  it.reqs.forEach(r=>rows.push([it.n,it.split,it.subtask,it.app,it.system,r.id,
    s.marks[r.id]||'',it.judge[r.id]||'',(s.why||{})[r.id]||'',s.conf||'',
    r===it.reqs[0]?(s.defects||''):'']));});
 const csv=rows.map(r=>r.map(c=>`"${String(c).replace(/"/g,'""')}"`).join(',')).join('\n');
 const a=document.createElement('a');
 a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv'}));
 a.download=`judge_review_${META.corpus}_${META.rubric}.csv`;a.click();});
render();
</script>
"""

if __name__ == "__main__":
    sys.exit(main())
