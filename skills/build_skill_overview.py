#!/usr/bin/env python3
"""Skill overview: results/skill_overview.html — one heatmap, nothing else.

skill_breakdown.html decomposes each skill by source benchmark, which is the right tool for
auditing a number but too much detail for reading the shape of the results. This pools every
benchmark into a single skills x models matrix — the same figures as Table 2 of
BENCHMARK_REPORT.md, arranged so patterns across skills are visible at a glance.

Usage:
    python skills/build_skill_overview.py
"""
from __future__ import annotations
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from skills.join_correctness import join, load_labels  # noqa: E402

OUT = ROOT / "results" / "skill_overview.html"
SPARSE_BELOW = 30

MODEL_ORDER = ["Llama-3.1-8B", "gemma-4-E4B", "Llama-3.1-70B", "gpt-oss-20b", "gpt-oss-120b",
               "gemma-4-31B", "nemotron-3-ultra", "inkling-bf16", "gemini25pro", "gpt41nano",
               "gpt5", "claudehaiku45", "gemini35flash", "gpto3", "claudesonnet5",
               "gpt56terra", "claudeopus48"]
PROVIDER = ({m: "sophia" for m in MODEL_ORDER[:6]} |
            {m: "minerva" for m in MODEL_ORDER[6:8]} |
            {m: "argo" for m in MODEL_ORDER[8:]})
ONPREM = set(MODEL_ORDER[:8])


def build() -> dict:
    labels = load_labels()
    rows = join(labels)

    items = defaultdict(set)
    for r in labels.values():
        for s in r["fundamental_skills"]:
            items[s].add(r["sample_id"])

    acc: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    benches: dict[str, set] = defaultdict(set)
    for r in rows:
        for s in r["skills"]:
            acc[s][r["model"]].append(r["score"])
            benches[s].add(r["benchmark"])

    skills = {}
    for s, models in acc.items():
        cells = {m: {"pct": round(100 * sum(v) / len(v), 1), "n": len(v)} for m, v in models.items()}
        onp = [(m, c["pct"]) for m, c in cells.items() if m in ONPREM]
        com = [(m, c["pct"]) for m, c in cells.items() if m not in ONPREM]
        # Break ties by name, not dict order — Ethical/normative judgment has two commercial
        # models at exactly 90.5%, and an unstable pick makes this table disagree with the
        # report for no real reason.
        best = lambda g: max(g, key=lambda kv: (kv[1], [-ord(c) for c in kv[0]])) if g else None  # noqa: E731
        best_on, best_com = best(onp), best(com)
        tied_com = sorted(m for m, p in com if best_com and p == best_com[1])
        skills[s] = {
            "items": len(items[s]),
            "benchmarks": len(benches[s]),
            "sparse": len(items[s]) < SPARSE_BELOW,
            "cells": cells,
            "best_onprem": best_on,
            "best_commercial": best_com,
            "tied_commercial": tied_com if len(tied_com) > 1 else None,
            "gap": round(best_com[1] - best_on[1], 1) if best_on and best_com else None,
        }
    return {"model_order": MODEL_ORDER, "provider": PROVIDER, "skills": skills,
            "onprem": sorted(ONPREM)}


TEMPLATE = """<meta charset="utf-8"/>
<title>ALCF Skill Matrix</title>
<style>
:root{--bg:#F2F4F3;--surface:#FFFFFF;--surface-2:#E9ECEB;--text:#12181B;--text-dim:#55636B;
 --text-faint:#8B979B;--border:#D8DEDD;--border-strong:#BFC8C7;--accent:#0E7C86;
 --accent-soft:#D9EEEE;--accent-text:#08565D;--sophia-tag:#7A5CC2;--argo-tag:#C2724A;
 --minerva-tag:#2E8B6E;--shadow:0 1px 2px rgba(18,24,27,.06),0 4px 12px rgba(18,24,27,.05);
 --radius:6px;--font-body:ui-sans-serif,-apple-system,"Segoe UI",Arial,sans-serif;
 --font-mono:ui-monospace,"SF Mono","Cascadia Code",Consolas,monospace;}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#10151A;--surface:#161D22;
 --surface-2:#1D262C;--text:#E7EDEC;--text-dim:#93A2A6;--text-faint:#5E6C70;--border:#263136;
 --border-strong:#33413A;--accent:#34C6C9;--accent-soft:#16363A;--accent-text:#7FE0E2;
 --sophia-tag:#A891E8;--argo-tag:#E39468;--minerva-tag:#4CBF97;
 --shadow:0 1px 2px rgba(0,0,0,.3),0 4px 16px rgba(0,0,0,.35);}}
:root[data-theme="dark"]{--bg:#10151A;--surface:#161D22;--surface-2:#1D262C;--text:#E7EDEC;
 --text-dim:#93A2A6;--text-faint:#5E6C70;--border:#263136;--border-strong:#33413A;--accent:#34C6C9;
 --accent-soft:#16363A;--accent-text:#7FE0E2;--sophia-tag:#A891E8;--argo-tag:#E39468;
 --minerva-tag:#4CBF97;--shadow:0 1px 2px rgba(0,0,0,.3),0 4px 16px rgba(0,0,0,.35);}
*{box-sizing:border-box;}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--font-body);font-size:14px;line-height:1.5;}
.wrap{max-width:1500px;margin:0 auto;padding:26px 24px 60px;}
h1{margin:0 0 6px;font-size:20px;font-weight:650;letter-spacing:-.01em;}
.sub{color:var(--text-dim);font-size:13px;max-width:82ch;margin-bottom:18px;}
.bar{display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin-bottom:12px;}
.seg{display:inline-flex;border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;background:var(--surface);}
.seg button{background:none;border:0;padding:6px 13px;font:inherit;font-size:12.5px;color:var(--text-dim);cursor:pointer;}
.seg button+button{border-left:1px solid var(--border);}
.seg button:hover{background:var(--surface-2);color:var(--text);}
.seg button.on{background:var(--accent-soft);color:var(--accent-text);font-weight:600;}
.lbl{font-size:10.5px;text-transform:uppercase;letter-spacing:.09em;color:var(--text-faint);font-weight:650;}
.scroll{overflow-x:auto;border:1px solid var(--border);border-radius:var(--radius);background:var(--surface);box-shadow:var(--shadow);}
table{border-collapse:separate;border-spacing:0;font-size:12.5px;width:100%;}
th,td{padding:6px 8px;text-align:center;white-space:nowrap;border-bottom:1px solid var(--border);}
thead th{position:sticky;top:0;background:var(--surface);z-index:2;font-weight:600;font-size:11.5px;}
.grp th{font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;padding-bottom:2px;border-bottom:0;}
.grp .sophia{color:var(--sophia-tag);}.grp .argo{color:var(--argo-tag);}.grp .minerva{color:var(--minerva-tag);}
th.rh,td.rh{position:sticky;left:0;z-index:1;background:var(--surface);text-align:left;font-weight:500;
 border-right:1px solid var(--border-strong);}
thead th.rh{z-index:3;}
td.rh .nm{display:block;}
td.rh .sz{display:block;font-size:10px;color:var(--text-faint);font-family:var(--font-mono);font-variant-numeric:tabular-nums;}
td.c{font-family:var(--font-mono);font-variant-numeric:tabular-nums;}
td.c .n{display:block;font-size:9.5px;opacity:.6;line-height:1.1;}
td.gap{font-family:var(--font-mono);font-variant-numeric:tabular-nums;font-weight:600;
 border-left:1px solid var(--border-strong);}
td.gap.neg{color:var(--minerva-tag);}
tr.thin td.rh .nm{color:var(--text-faint);font-style:italic;}
td.empty{color:var(--text-faint);}
.note{margin-top:14px;color:var(--text-dim);font-size:12.5px;max-width:95ch;}
.note b{color:var(--text);}
.prov{margin-top:20px;padding-top:14px;border-top:1px solid var(--border);color:var(--text-faint);
 font-size:11.5px;line-height:1.65;max-width:95ch;}
.prov b{color:var(--text-dim);font-weight:650;}
</style>
<div class="wrap">
  <h1>Fundamental skills &times; models</h1>
  <div class="sub">All 3,604 benchmark questions labeled by the skills they require, pooled
  across every benchmark. Each cell is one model's accuracy on the questions carrying that
  skill. Columns run weakest&rarr;strongest within each provider.</div>
  <div class="bar">
    <span class="lbl">Sort</span>
    <div class="seg" id="sort">
      <button data-k="items" class="on">Question count</button>
      <button data-k="gap">Commercial advantage</button>
      <button data-k="spread">Model spread</button>
      <button data-k="name">Name</button>
    </div>
  </div>
  <div class="scroll"><table id="t"></table></div>
  <div class="note" id="note"></div>
  <div class="prov">
    <b>Argonne Leadership Computing Facility</b> &middot; 17 models across 26 public benchmarks,
    August 2026. Sophia and Minerva are ALCF's own clusters; Argo is the gateway to commercial
    APIs.<br>
    <b>How the skill labels were made.</b> Each of the 3,604 benchmark questions was classified
    by an LLM (<code>claude-sonnet-4-6</code>, temperature 0) against a 29-tag taxonomy, then
    joined to every model's per-question correctness. The taxonomy was derived from the
    benchmarks' own category vocabularies and refined on a 388-question discovery pass, not
    fixed in advance.<br>
    <b>Read the numbers with this caveat.</b> Labels are machine-generated. They passed 21
    construct-validity checks (WinoGrande&rarr;coreference 99%, HumanEval&rarr;code generation
    99%, and so on) and the classifier agrees with itself at 0.974, but measured agreement with
    a human labeller was <b>0.893 and should be treated as an upper bound</b> &mdash; the review
    interface pre-checked the classifier's labels, which anchors the reviewer. Full method,
    per-tag precision and recall, and the remaining caveats are in
    <code>BENCHMARK_REPORT.md</code>.
  </div>
</div>
<script>
const D = __DATA__;
let sortKey = 'items';
const dark = () => (matchMedia('(prefers-color-scheme: dark)').matches
    && document.documentElement.dataset.theme !== 'light')
    || document.documentElement.dataset.theme === 'dark';

function heat(p){
  const t=Math.max(0,Math.min(1,p/100)), mix=(a,b,k)=>a.map((v,i)=>Math.round(v+(b[i]-v)*k));
  const L=dark()?[217,99,76]:[193,67,46], M=dark()?[58,54,42]:[233,223,198], H=dark()?[52,198,201]:[14,124,134];
  const c = t<.5 ? mix(L,M,t*2) : mix(M,H,(t-.5)*2);
  return `rgb(${c[0]} ${c[1]} ${c[2]} / ${dark()?.55:.8})`;
}
const ink = p => dark() ? 'var(--text)' : ((p>72||p<26)?'#fff':'var(--text)');

function spread(s){
  const v=Object.values(D.skills[s].cells).map(c=>c.pct);
  return v.length ? Math.max(...v)-Math.min(...v) : 0;
}
function order(){
  const keys=Object.keys(D.skills);
  const cmp={
    items:(a,b)=>D.skills[b].items-D.skills[a].items,
    gap:(a,b)=>(D.skills[b].gap??-99)-(D.skills[a].gap??-99),
    spread:(a,b)=>spread(b)-spread(a),
    name:(a,b)=>a.localeCompare(b),
  }[sortKey];
  // sparse skills always sink to the bottom: their ordering is noise whatever the key
  return keys.sort((a,b)=>(D.skills[a].sparse-D.skills[b].sparse)||cmp(a,b));
}

function render(){
  const t=document.getElementById('t');
  const grp=D.model_order.map(m=>`<th class="${D.provider[m]}">${D.provider[m]}</th>`).join('');
  const hdr=D.model_order.map(m=>`<th>${m}</th>`).join('');
  const body=order().map(s=>{
    const sk=D.skills[s];
    const cells=D.model_order.map(m=>{
      const c=sk.cells[m];
      if(!c) return '<td class="empty">&mdash;</td>';
      return `<td class="c" style="background:${heat(c.pct)};color:${ink(c.pct)}"
        title="${s} × ${m}: ${c.pct.toFixed(1)}% over ${c.n} observations">${c.pct.toFixed(1)}<span class="n">${c.n}</span></td>`;
    }).join('');
    const g=sk.gap;
    const gapCell=g===null?'<td class="gap empty">&mdash;</td>'
      :`<td class="gap${g<=0?' neg':''}" title="best commercial ${sk.tied_commercial?sk.tied_commercial.join(' / ')+' (tied)':sk.best_commercial[0]} ${sk.best_commercial[1]}% − best ALCF-hosted ${sk.best_onprem[0]} ${sk.best_onprem[1]}%">${g>0?'+':''}${g.toFixed(1)}</td>`;
    return `<tr class="${sk.sparse?'thin':''}">
      <td class="rh"><span class="nm">${s}</span><span class="sz">${sk.items} q · ${sk.benchmarks} bench</span></td>
      ${cells}${gapCell}</tr>`;
  }).join('');
  t.innerHTML=`<thead><tr class="grp"><th class="rh"></th>${grp}<th></th></tr>
    <tr><th class="rh">Skill</th>${hdr}<th title="best commercial − best ALCF-hosted">Gap</th></tr></thead>
    <tbody>${body}</tbody>`;

  const thin=Object.keys(D.skills).filter(s=>D.skills[s].sparse);
  document.getElementById('note').innerHTML =
    `Cells show accuracy % with observation count beneath &mdash; one observation is a
     (question &times; model) pair, so counts exceed question counts. <b>Gap</b> is the best
     commercial (Argo) model minus the best ALCF-hosted (Sophia or Minerva) one;
     <span style="color:var(--minerva-tag);font-weight:600">negative</span> means the on-prem
     option wins. Italic rows (${thin.join(', ')}) carry too few questions to compare models &mdash;
     their near-absence is the finding, not their scores.`;
}
document.querySelectorAll('#sort button').forEach(b=>b.onclick=()=>{
  sortKey=b.dataset.k;
  document.querySelectorAll('#sort button').forEach(x=>x.classList.toggle('on',x===b));
  render();
});
render();
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', render);
</script>
"""


def main() -> int:
    data = build()
    OUT.write_text(TEMPLATE.replace("__DATA__", json.dumps(data, separators=(",", ":"))))
    print(f"{len(data['skills'])} skills x {len(data['model_order'])} models -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
