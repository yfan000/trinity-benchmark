#!/usr/bin/env python3
"""results/trinity_samples.html — a browser for the 90 Trinity benchmark samples.

Ninety samples with ~2,000-character prompts do not read in a terminal. This renders them
filterable by subtask and domain, with each reference answer collapsed behind a toggle so
the page can be read the way an agent sees it — prompt first, answer only on request.

Usage:
    python skills/build_trinity_html.py
"""
from __future__ import annotations
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

SRC = ROOT / "results" / "skills" / "trinity" / "samples.jsonl"
OUT = ROOT / "results" / "trinity_samples.html"


def main() -> int:
    rows = [json.loads(l) for l in SRC.open()]
    rows.sort(key=lambda r: (r["order"], r["domain"]))
    data = [{"id": r["sample_id"], "subtask": r["subtask"], "domain": r["domain"],
             "variation": r["variation"], "order": r["order"],
             "prompt": r["prompt"], "reference": r["reference"]} for r in rows]
    OUT.write_text(TEMPLATE.replace("__DATA__", json.dumps(data, separators=(",", ":"))))
    print(f"{len(rows)} samples, {len({r['subtask'] for r in rows})} subtasks, "
          f"{len({r['domain'] for r in rows})} domains -> {OUT}")
    return 0


TEMPLATE = """<meta charset="utf-8"/>
<title>Trinity Agent Benchmark</title>
<style>
:root{--bg:#F2F4F3;--surface:#FFFFFF;--surface-2:#E9ECEB;--text:#12181B;--text-dim:#55636B;
 --text-faint:#8B979B;--border:#D8DEDD;--accent:#0E7C86;--accent-soft:#D9EEEE;
 --accent-text:#08565D;--warn:#C1432E;--warn-soft:#F7E4E0;
 --shadow:0 1px 2px rgba(18,24,27,.06),0 4px 12px rgba(18,24,27,.05);--radius:8px;
 --font:ui-sans-serif,-apple-system,"Segoe UI",Arial,sans-serif;
 --mono:ui-monospace,"SF Mono","Cascadia Code",Consolas,monospace;}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#10151A;--surface:#161D22;
 --surface-2:#1D262C;--text:#E7EDEC;--text-dim:#93A2A6;--text-faint:#5E6C70;--border:#263136;
 --accent:#34C6C9;--accent-soft:#16363A;--accent-text:#7FE0E2;--warn:#D9634C;--warn-soft:#2A1A16;
 --shadow:0 1px 2px rgba(0,0,0,.3),0 4px 16px rgba(0,0,0,.35);}}
:root[data-theme="dark"]{--bg:#10151A;--surface:#161D22;--surface-2:#1D262C;--text:#E7EDEC;
 --text-dim:#93A2A6;--text-faint:#5E6C70;--border:#263136;--accent:#34C6C9;--accent-soft:#16363A;
 --accent-text:#7FE0E2;--warn:#D9634C;--warn-soft:#2A1A16;
 --shadow:0 1px 2px rgba(0,0,0,.3),0 4px 16px rgba(0,0,0,.35);}
*{box-sizing:border-box;}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--font);font-size:14px;line-height:1.55;}
.wrap{max-width:1080px;margin:0 auto;padding:26px 22px 80px;}
h1{margin:0 0 6px;font-size:21px;font-weight:660;letter-spacing:-.012em;}
.sub{color:var(--text-dim);font-size:13.5px;max-width:86ch;}
.filters{position:sticky;top:0;z-index:5;background:var(--bg);padding:14px 0 12px;
 border-bottom:1px solid var(--border);margin:16px 0 0;}
.frow{display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin-bottom:7px;}
.lbl{font-size:10px;text-transform:uppercase;letter-spacing:.09em;color:var(--text-faint);
 font-weight:680;width:62px;flex:none;}
button.f{background:var(--surface);border:1px solid var(--border);border-radius:20px;
 padding:3px 11px;font:inherit;font-size:12px;color:var(--text-dim);cursor:pointer;}
button.f:hover{border-color:var(--accent);color:var(--text);}
button.f.on{background:var(--accent-soft);border-color:var(--accent);color:var(--accent-text);font-weight:620;}
.count{margin-left:auto;font-size:12px;color:var(--text-faint);font-family:var(--mono);}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
 box-shadow:var(--shadow);padding:16px 18px;margin-top:14px;}
.hd{display:flex;gap:9px;align-items:baseline;flex-wrap:wrap;margin-bottom:10px;}
.id{font-family:var(--mono);font-size:11.5px;color:var(--text-faint);}
.tag{font-size:10.5px;font-weight:680;letter-spacing:.04em;text-transform:uppercase;
 padding:2px 9px;border-radius:20px;background:var(--accent-soft);color:var(--accent-text);}
.dom{font-size:12.5px;color:var(--text-dim);font-weight:600;}
.var{font-size:11.5px;color:var(--text-faint);font-style:italic;margin-left:auto;}
.sec{margin-bottom:9px;}
.sec b{display:block;font-size:10px;text-transform:uppercase;letter-spacing:.09em;
 color:var(--accent);font-weight:700;margin-bottom:3px;}
.sec div{white-space:pre-wrap;font-size:13px;color:var(--text);}
.sec.workload div{color:var(--text-dim);}
pre{margin:6px 0;padding:9px 11px;background:var(--surface-2);border-radius:6px;
 overflow-x:auto;font-family:var(--mono);font-size:11.5px;line-height:1.45;white-space:pre;}
details{margin-top:11px;border-top:1px solid var(--border);padding-top:10px;}
summary{cursor:pointer;font-size:11.5px;color:var(--warn);font-weight:650;list-style:none;}
summary::-webkit-details-marker{display:none;}
summary::before{content:"▸ ";}
details[open] summary::before{content:"▾ ";}
details .body{margin-top:8px;padding:11px 13px;background:var(--warn-soft);border-radius:6px;
 white-space:pre-wrap;font-size:12.5px;color:var(--text-dim);}
.none{padding:40px;text-align:center;color:var(--text-faint);}
</style>
<div class="wrap">
<h1>Trinity agent benchmark &mdash; 90 samples</h1>
<div class="sub">Nine HPC pipeline subtasks &times; ten scientific domains. Each sample is
self-contained: an agent receives only this prompt, never the originating conversation. The
reference answer is stored separately and hidden by default &mdash; every prompt states the
task explicitly while withholding the answer being tested.</div>
<div class="filters">
  <div class="frow"><span class="lbl">Subtask</span><span id="fsub"></span></div>
  <div class="frow"><span class="lbl">Domain</span><span id="fdom"></span><span class="count" id="cnt"></span></div>
</div>
<div id="list"></div>
</div>
<script>
const D = __DATA__;
const SUBS = [...new Set(D.map(d=>d.subtask))];
const DOMS = [...new Set(D.map(d=>d.domain))].sort();
let fs = null, fd = null;

const esc = s => s.replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));

// Split the four-section prompt so each part can be styled; anything that looks like a
// pasted script or log is shown monospaced rather than as prose.
function sections(p){
  const keys=["Task:","Workload:","Instructions:","Output:"];
  const idx=keys.map(k=>({k,i:p.indexOf(k)})).filter(x=>x.i>=0).sort((a,b)=>a.i-b.i);
  return idx.map((x,n)=>({
    name:x.k.replace(':',''),
    body:p.slice(x.i+x.k.length, n+1<idx.length?idx[n+1].i:undefined).trim()
  }));
}
function bodyHtml(t){
  // treat indented / directive-looking blocks as code
  const lines=t.split("\\n");
  let out="", buf=[];
  const flush=()=>{ if(buf.length){ out+=`<pre>${esc(buf.join("\\n"))}</pre>`; buf=[]; } };
  for(const l of lines){
    if(/^\\s*(#PBS|#!|module |mpiexec|qsub|---|\\$ |[A-Z_]+=)/.test(l) || /^\\s{2,}\\S/.test(l)) buf.push(l);
    else { flush(); out+= l.trim()? `<div>${esc(l)}</div>` : ""; }
  }
  flush(); return out;
}
function chips(el, items, cur, set){
  el.innerHTML = `<button class="f${cur===null?' on':''}" data-v="">All</button>` +
    items.map(v=>`<button class="f${cur===v?' on':''}" data-v="${esc(v)}">${esc(v)}</button>`).join("");
  el.querySelectorAll("button").forEach(b=>b.onclick=()=>{set(b.dataset.v||null);render();});
}
function render(){
  chips(document.getElementById("fsub"), SUBS, fs, v=>fs=v);
  chips(document.getElementById("fdom"), DOMS, fd, v=>fd=v);
  const rows = D.filter(d=>(!fs||d.subtask===fs)&&(!fd||d.domain===fd));
  document.getElementById("cnt").textContent = `${rows.length} of ${D.length}`;
  document.getElementById("list").innerHTML = rows.length ? rows.map(d=>`
    <div class="card">
      <div class="hd"><span class="id">${d.id}</span><span class="tag">${esc(d.subtask)}</span>
        <span class="dom">${esc(d.domain)}</span><span class="var">${esc(d.variation)}</span></div>
      ${sections(d.prompt).map(s=>`<div class="sec ${s.name.toLowerCase()}">
         <b>${s.name}</b>${bodyHtml(s.body)}</div>`).join("")}
      <details><summary>Reference answer &mdash; withheld from the agent (${d.reference.length} chars)</summary>
        <div class="body">${esc(d.reference)}</div></details>
    </div>`).join("") : '<div class="none">No samples match that filter.</div>';
}
render();
</script>
"""


if __name__ == "__main__":
    sys.exit(main())
