#!/usr/bin/env python3
"""results/trinity_comparison.html — every prompt, every model's answer, side by side.

The scoreboard says a model scored 2/6; it does not show you *what it wrote* or *why that
was wrong*. This does: one card per sample, the prompt, the catalog's ground truth, and each
model's answer with the judge's specific defects attached.

It is also the fastest way to audit the judge itself, which has not been validated against a
human. Reading a dozen cards tells you whether the defects are real or the rubric is
miscalibrated — which is how the out-of-scope penalties and the impossible-filesystem
instruction were caught.

Usage:
    python skills/build_comparison_html.py
"""
from __future__ import annotations
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

TRIN = ROOT / "results" / "skills" / "trinity"
OUT = ROOT / "results" / "trinity_comparison.html"


def load(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.open()] if p.exists() else []


def build() -> dict:
    samples = {s["sample_id"]: s for s in load(TRIN / "samples.jsonl")}
    answers = defaultdict(dict)
    for a in load(TRIN / "answers.jsonl"):
        if not a["error"]:
            answers[a["sample_id"]][(a["model"], a.get("style", "plain"))] = a["answer"]
    grades = defaultdict(dict)
    for g in load(TRIN / "grades.jsonl"):
        grades[g["sample_id"]][(g["model"], g.get("style", "plain"))] = g

    cards = []
    for sid, s in sorted(samples.items(), key=lambda kv: (kv[1]["order"], kv[1]["domain"])):
        rows = []
        for (model, style), ans in sorted(answers.get(sid, {}).items()):
            g = grades.get(sid, {}).get((model, style), {})
            total = (g.get("correctness", 0) + g.get("completeness", 0)
                     + g.get("usability", 0)) if g else None
            rows.append({
                "model": model, "style": style, "answer": ans,
                "score": total, "fatal": g.get("fatal_error"),
                "c": g.get("correctness"), "p": g.get("completeness"), "u": g.get("usability"),
                "errors": g.get("errors", []), "note": g.get("note", ""),
                "pass": bool(g) and total == 6 and not g.get("fatal_error"),
            })
        if not rows:
            continue
        cards.append({"id": sid, "subtask": s["subtask"], "domain": s["domain"],
                      "app": s["app"], "system": s["system"], "order": s["order"],
                      "prompt": s["prompt"], "key": s["grading_key"], "rows": rows})
    models = sorted({r["model"] for c in cards for r in c["rows"]})
    return {"cards": cards, "models": models,
            "subtasks": sorted({c["subtask"] for c in cards},
                               key=lambda x: next(c["order"] for c in cards if c["subtask"] == x))}


TEMPLATE = """<meta charset="utf-8"/>
<title>Trinity Model Comparison</title>
<style>
:root{--bg:#F2F4F3;--surface:#FFFFFF;--surface-2:#E9ECEB;--text:#12181B;--text-dim:#55636B;
 --text-faint:#8B979B;--border:#D8DEDD;--accent:#0E7C86;--accent-soft:#D9EEEE;
 --accent-text:#08565D;--good:#2E8B6E;--good-soft:#E3F3ED;--warn:#C1432E;--warn-soft:#F9E7E3;
 --shadow:0 1px 2px rgba(18,24,27,.06),0 4px 12px rgba(18,24,27,.05);--radius:8px;
 --font:ui-sans-serif,-apple-system,"Segoe UI",Arial,sans-serif;
 --mono:ui-monospace,"SF Mono","Cascadia Code",Consolas,monospace;}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#10151A;--surface:#161D22;
 --surface-2:#1D262C;--text:#E7EDEC;--text-dim:#93A2A6;--text-faint:#5E6C70;--border:#263136;
 --accent:#34C6C9;--accent-soft:#16363A;--accent-text:#7FE0E2;--good:#4CBF97;--good-soft:#14302A;
 --warn:#D9634C;--warn-soft:#2E1A16;--shadow:0 1px 2px rgba(0,0,0,.3),0 4px 16px rgba(0,0,0,.35);}}
:root[data-theme="dark"]{--bg:#10151A;--surface:#161D22;--surface-2:#1D262C;--text:#E7EDEC;
 --text-dim:#93A2A6;--text-faint:#5E6C70;--border:#263136;--accent:#34C6C9;--accent-soft:#16363A;
 --accent-text:#7FE0E2;--good:#4CBF97;--good-soft:#14302A;--warn:#D9634C;--warn-soft:#2E1A16;
 --shadow:0 1px 2px rgba(0,0,0,.3),0 4px 16px rgba(0,0,0,.35);}
*{box-sizing:border-box;}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--font);font-size:14px;line-height:1.55;}
.wrap{max-width:1280px;margin:0 auto;padding:24px 20px 80px;}
h1{margin:0 0 6px;font-size:21px;font-weight:660;letter-spacing:-.012em;}
.sub{color:var(--text-dim);font-size:13.5px;max-width:90ch;}
.bar{position:sticky;top:0;z-index:9;background:var(--bg);padding:14px 0 12px;border-bottom:1px solid var(--border);margin-top:14px;}
.frow{display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin-bottom:6px;}
.lbl{font-size:10px;text-transform:uppercase;letter-spacing:.09em;color:var(--text-faint);font-weight:680;width:66px;flex:none;}
button.f{background:var(--surface);border:1px solid var(--border);border-radius:20px;padding:3px 11px;
 font:inherit;font-size:12px;color:var(--text-dim);cursor:pointer;}
button.f:hover{border-color:var(--accent);color:var(--text);}
button.f.on{background:var(--accent-soft);border-color:var(--accent);color:var(--accent-text);font-weight:620;}
.count{margin-left:auto;font-size:12px;color:var(--text-faint);font-family:var(--mono);}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
 box-shadow:var(--shadow);margin-top:16px;overflow:hidden;}
.hd{padding:13px 16px;border-bottom:1px solid var(--border);display:flex;gap:9px;align-items:baseline;flex-wrap:wrap;}
.id{font-family:var(--mono);font-size:11.5px;color:var(--text-faint);}
.tag{font-size:10.5px;font-weight:680;letter-spacing:.04em;text-transform:uppercase;padding:2px 9px;
 border-radius:20px;background:var(--accent-soft);color:var(--accent-text);}
.meta{font-size:12.5px;color:var(--text-dim);}
.truth{margin-left:auto;font-family:var(--mono);font-size:12px;color:var(--good);font-weight:650;}
details.pr{border-bottom:1px solid var(--border);}
details.pr>summary{cursor:pointer;padding:9px 16px;font-size:11.5px;color:var(--accent);font-weight:640;list-style:none;}
summary::-webkit-details-marker{display:none;}
summary::before{content:"▸ ";}
details[open]>summary::before{content:"▾ ";}
.prompt{padding:0 16px 14px;white-space:pre-wrap;font-size:12.5px;color:var(--text-dim);}
.ans{border-bottom:1px solid var(--border);}
.ans:last-child{border-bottom:0;}
.ah{display:flex;gap:10px;align-items:center;padding:9px 16px;background:var(--surface-2);}
.mdl{font-weight:650;font-size:13px;min-width:150px;}
.sty{font-size:10px;text-transform:uppercase;letter-spacing:.06em;color:var(--text-faint);font-weight:670;}
.pill{font-family:var(--mono);font-size:11.5px;font-weight:680;padding:2px 9px;border-radius:20px;}
.pill.ok{background:var(--good-soft);color:var(--good);}
.pill.no{background:var(--warn-soft);color:var(--warn);}
.dims{font-family:var(--mono);font-size:11px;color:var(--text-faint);margin-left:auto;}
.body{padding:11px 16px;white-space:pre-wrap;font-family:var(--mono);font-size:11.5px;
 line-height:1.5;color:var(--text);max-height:340px;overflow:auto;background:var(--bg);}
.defects{padding:9px 16px 13px;}
.defects b{font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:var(--warn);font-weight:700;}
.defects li{font-size:12.5px;color:var(--text-dim);margin:4px 0 0 2px;list-style:none;padding-left:14px;position:relative;}
.defects li::before{content:"✗";position:absolute;left:0;color:var(--warn);font-weight:700;}
.note{font-size:12.5px;color:var(--text-dim);font-style:italic;margin-top:7px;}
.none{padding:44px;text-align:center;color:var(--text-faint);}
</style>
<div class="wrap">
<h1>What each model actually answered</h1>
<div class="sub">Every benchmark sample with all models' answers side by side, the correct
answer from Argonne's software catalog, and the specific defects the judge (Opus 5) found in
each. Green means fully correct &mdash; all three dimensions perfect and no fatal error.</div>
<div class="bar">
  <div class="frow"><span class="lbl">Subtask</span><span id="fsub"></span></div>
  <div class="frow"><span class="lbl">Show</span><span id="fres"></span><span class="count" id="cnt"></span></div>
</div>
<div id="list"></div>
</div>
<script>
const D = __DATA__;
let fsub = null, fres = "all";
const esc = s => String(s).replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));

function chips(el, items, cur, set, labels){
  el.innerHTML = items.map((v,i)=>
    `<button class="f${cur===v?' on':''}" data-v="${esc(v)}">${esc(labels?labels[i]:v)}</button>`).join("");
  el.querySelectorAll("button").forEach(b=>b.onclick=()=>{set(b.dataset.v);render();});
}

function render(){
  chips(document.getElementById("fsub"), [""].concat(D.subtasks), fsub===null?"":fsub,
        v=>fsub=(v||null), ["All"].concat(D.subtasks));
  chips(document.getElementById("fres"), ["all","failed","passed"], fres, v=>fres=v,
        ["Everything","Only failures","Only fully correct"]);

  const cards = D.cards.filter(c=>!fsub || c.subtask===fsub);
  let shown = 0;
  const html = cards.map(c=>{
    let rows = c.rows;
    if (fres==="failed") rows = rows.filter(r=>!r.pass);
    if (fres==="passed") rows = rows.filter(r=>r.pass);
    if (!rows.length) return "";
    shown++;
    return `<div class="card">
      <div class="hd"><span class="id">${c.id}</span><span class="tag">${esc(c.subtask)}</span>
        <span class="meta">${esc(c.domain)} &middot; ${esc(c.app)}@${esc(c.system)}</span>
        <span class="truth">correct: ${esc(c.key.app||"—")}</span></div>
      <details class="pr"><summary>Show the prompt the models were given</summary>
        <div class="prompt">${esc(c.prompt)}</div></details>
      ${rows.map(r=>`<div class="ans">
        <div class="ah"><span class="mdl">${esc(r.model)}</span>
          <span class="sty">${esc(r.style)}</span>
          <span class="pill ${r.pass?'ok':'no'}">${r.score===null?'ungraded':(r.pass?'fully correct':r.score+'/6')}</span>
          ${r.fatal?'<span class="pill no">fatal</span>':''}
          <span class="dims">${r.c===undefined?'':'correctness '+r.c+' · completeness '+r.p+' · usability '+r.u}</span></div>
        <div class="body">${esc(r.answer).slice(0,4000)}</div>
        ${(r.errors&&r.errors.length)?`<div class="defects"><b>Judge found</b><ul>${
            r.errors.map(e=>`<li>${esc(e)}</li>`).join("")}</ul>${
            r.note?`<div class="note">${esc(r.note)}</div>`:''}</div>`:''}
      </div>`).join("")}
    </div>`;
  }).join("");
  document.getElementById("cnt").textContent = `${shown} of ${D.cards.length} samples`;
  document.getElementById("list").innerHTML = html || '<div class="none">Nothing matches that filter.</div>';
}
render();
</script>
"""


def main() -> int:
    d = build()
    if not d["cards"]:
        print("no graded answers yet")
        return 1
    OUT.write_text(TEMPLATE.replace("__DATA__", json.dumps(d, separators=(",", ":"))))
    n = sum(len(c["rows"]) for c in d["cards"])
    print(f"{len(d['cards'])} samples, {n} answers, {len(d['models'])} models -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
