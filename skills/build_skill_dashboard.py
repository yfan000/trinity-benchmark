#!/usr/bin/env python3
"""Skill-first dashboard: results/skill_breakdown.html

category_breakdown.html is organized by benchmark, with one skills tab bolted on. This is
the transpose — one tab per skill, and within it a benchmark x model heatmap showing where
each skill's evidence actually comes from.

That decomposition is the point. "Numerical reasoning 71.8%" pools GSM8K word problems with
MatSciBench derivations; a model can be strong on one and weak on the other, and the pooled
number hides it. Every skill row here also carries an "All benchmarks" summary so the pooled
figure and its parts sit side by side.

Usage:
    python skills/build_skill_dashboard.py
"""
from __future__ import annotations
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from skills.join_correctness import join, load_labels  # noqa: E402

OUT = ROOT / "results" / "skill_breakdown.html"
SPARSE_BELOW = 30  # items; below this a skill's numbers are too thin to read as a result

BENCH_LABEL = {
    "mmlu": "MMLU", "mmlu_pro": "MMLU-Pro", "gpqa": "GPQA-Diamond", "gpqa_main": "GPQA-Main",
    "gsm8k": "GSM8K", "gsm1k": "GSM1K", "math": "MATH", "aime2024": "AIME 2024",
    "olympiadbench": "OlympiadBench", "bbh": "BBH", "humaneval": "HumanEval",
    "bigcodebench": "BigCodeBench", "ifeval": "IFEval", "infobench": "InfoBench",
    "followbench": "FollowBench", "truthfulqa": "TruthfulQA", "winogrande": "WinoGrande",
    "mt_bench": "MT-Bench", "longbench_v2": "LongBench-v2", "hle": "HLE", "sealqa": "SealQA",
    "clutrr_regen": "CLUTRR", "arc": "ARC", "hellaswag": "HellaSwag",
}
MODEL_ORDER = ["Llama-3.1-8B", "gemma-4-E4B", "Llama-3.1-70B", "gpt-oss-20b", "gpt-oss-120b",
               "gemma-4-31B", "nemotron-3-ultra", "inkling-bf16", "gemini25pro", "gpt41nano",
               "gpt5", "claudehaiku45", "gemini35flash", "gpto3", "claudesonnet5",
               "gpt56terra", "claudeopus48"]
PROVIDER = ({m: "sophia" for m in MODEL_ORDER[:6]} |
            {m: "minerva" for m in MODEL_ORDER[6:8]} |
            {m: "argo" for m in MODEL_ORDER[8:]})
ALL = "All benchmarks"


def build() -> dict:
    labels = load_labels()
    rows = join(labels)

    n_items = defaultdict(set)
    for r in labels.values():
        for s in r["fundamental_skills"]:
            n_items[s].add(r["sample_id"])

    acc: dict[str, dict[str, dict[str, list]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for r in rows:
        for skill in r["skills"]:
            acc[skill][BENCH_LABEL.get(r["benchmark"], r["benchmark"])][r["model"]].append(r["score"])
            acc[skill][ALL][r["model"]].append(r["score"])

    def cell(v):
        return {"pct": round(100 * sum(v) / len(v), 1), "n": len(v)}

    skills = {}
    for skill, benches in acc.items():
        skills[skill] = {
            "items": len(n_items[skill]),
            "sparse": len(n_items[skill]) < SPARSE_BELOW,
            "rows": {b: {m: cell(v) for m, v in sorted(models.items())}
                     for b, models in sorted(benches.items(), key=lambda kv: (kv[0] != ALL, kv[0]))},
        }
    order = sorted(skills, key=lambda s: (skills[s]["sparse"], -skills[s]["items"]))
    return {"model_order": MODEL_ORDER, "provider": PROVIDER, "skill_order": order,
            "skills": skills, "all_label": ALL}


TEMPLATE = """<meta charset="utf-8"/>
<title>ALCF Skill Sources</title>
<style>
:root {
  --bg:#F2F4F3; --surface:#FFFFFF; --surface-2:#E9ECEB; --text:#12181B; --text-dim:#55636B;
  --text-faint:#8B979B; --border:#D8DEDD; --border-strong:#BFC8C7; --accent:#0E7C86;
  --accent-soft:#D9EEEE; --accent-text:#08565D; --heat-low:#C1432E; --heat-mid:#E9DFC6;
  --heat-high:#0E7C86; --sophia-tag:#7A5CC2; --argo-tag:#C2724A; --minerva-tag:#2E8B6E;
  --shadow:0 1px 2px rgba(18,24,27,.06),0 4px 12px rgba(18,24,27,.05); --radius:6px;
  --font-body:ui-sans-serif,-apple-system,"Segoe UI",Arial,sans-serif;
  --font-mono:ui-monospace,"SF Mono","Cascadia Code",Consolas,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#10151A; --surface:#161D22; --surface-2:#1D262C; --text:#E7EDEC; --text-dim:#93A2A6;
  --text-faint:#5E6C70; --border:#263136; --border-strong:#33413A; --accent:#34C6C9;
  --accent-soft:#16363A; --accent-text:#7FE0E2; --heat-low:#D9634C; --heat-mid:#3A362A;
  --heat-high:#34C6C9; --sophia-tag:#A891E8; --argo-tag:#E39468; --minerva-tag:#4CBF97;
  --shadow:0 1px 2px rgba(0,0,0,.3),0 4px 16px rgba(0,0,0,.35);}}
:root[data-theme="dark"]{
  --bg:#10151A; --surface:#161D22; --surface-2:#1D262C; --text:#E7EDEC; --text-dim:#93A2A6;
  --text-faint:#5E6C70; --border:#263136; --border-strong:#33413A; --accent:#34C6C9;
  --accent-soft:#16363A; --accent-text:#7FE0E2; --heat-low:#D9634C; --heat-mid:#3A362A;
  --heat-high:#34C6C9; --sophia-tag:#A891E8; --argo-tag:#E39468; --minerva-tag:#4CBF97;
  --shadow:0 1px 2px rgba(0,0,0,.3),0 4px 16px rgba(0,0,0,.35);}
*{box-sizing:border-box;}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--font-body);font-size:14px;line-height:1.5;}
header{padding:22px 28px 16px;border-bottom:1px solid var(--border);background:var(--surface);}
h1{margin:0 0 6px;font-size:19px;font-weight:650;letter-spacing:-.01em;}
.sub{color:var(--text-dim);font-size:13px;max-width:80ch;}
.layout{display:grid;grid-template-columns:250px 1fr;gap:0;align-items:start;}
@media (max-width:820px){.layout{grid-template-columns:1fr;}nav{position:static!important;max-height:none!important;border-right:0!important;border-bottom:1px solid var(--border);}}
nav{position:sticky;top:0;max-height:100vh;overflow-y:auto;border-right:1px solid var(--border);padding:14px 10px 28px;background:var(--surface);}
.navhead{font-size:10.5px;text-transform:uppercase;letter-spacing:.09em;color:var(--text-faint);padding:10px 10px 6px;font-weight:650;}
button.tab{display:flex;justify-content:space-between;align-items:center;gap:8px;width:100%;text-align:left;
  background:none;border:0;border-radius:var(--radius);padding:6px 10px;font:inherit;font-size:13px;
  color:var(--text-dim);cursor:pointer;}
button.tab:hover{background:var(--surface-2);color:var(--text);}
button.tab.on{background:var(--accent-soft);color:var(--accent-text);font-weight:600;}
button.tab .n{font-family:var(--font-mono);font-size:11px;color:var(--text-faint);font-variant-numeric:tabular-nums;}
button.tab.on .n{color:var(--accent-text);}
main{padding:22px 28px 60px;min-width:0;}
h2{margin:0 0 4px;font-size:17px;font-weight:650;}
.meta{color:var(--text-dim);font-size:12.5px;margin-bottom:14px;}
.insight{background:var(--surface);border:1px solid var(--border);border-left:3px solid var(--accent);
  border-radius:var(--radius);padding:11px 14px;margin-bottom:16px;font-size:13px;color:var(--text-dim);}
.insight b{color:var(--text);font-weight:600;}
.warn{border-left-color:var(--heat-low);}
.scroll{overflow-x:auto;border:1px solid var(--border);border-radius:var(--radius);background:var(--surface);box-shadow:var(--shadow);}
table{border-collapse:separate;border-spacing:0;font-size:12.5px;width:100%;}
th,td{padding:6px 9px;text-align:center;white-space:nowrap;border-bottom:1px solid var(--border);}
thead th{position:sticky;top:0;background:var(--surface);z-index:2;font-weight:600;font-size:11.5px;}
.grp th{font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;padding-bottom:2px;border-bottom:0;}
.grp .sophia{color:var(--sophia-tag);} .grp .argo{color:var(--argo-tag);} .grp .minerva{color:var(--minerva-tag);}
th.rowhead,td.rowhead{position:sticky;left:0;z-index:1;background:var(--surface);text-align:left;
  font-weight:500;border-right:1px solid var(--border-strong);max-width:190px;overflow:hidden;text-overflow:ellipsis;}
thead th.rowhead{z-index:3;}
tr.total td,tr.total th{font-weight:650;background:var(--surface-2);}
td.cell{font-family:var(--font-mono);font-variant-numeric:tabular-nums;}
td.cell .n{display:block;font-size:9.5px;opacity:.62;line-height:1.1;}
td.empty{color:var(--text-faint);}
td.lown{outline:1px dashed var(--border-strong);outline-offset:-3px;}
footer{padding:0 28px 40px;color:var(--text-faint);font-size:12px;max-width:95ch;}
</style>
<header>
  <h1>Fundamental skill breakdown</h1>
  <div class="sub">Each of 3,604 benchmark questions was labeled with the skills it requires,
  then joined back to every model's per-question correctness. Pick a skill to see which
  benchmarks supply its evidence &mdash; a pooled skill score can hide a model that is strong
  on one source and weak on another.</div>
</header>
<div class="layout">
  <nav id="nav"></nav>
  <main>
    <h2 id="title"></h2>
    <div class="meta" id="meta"></div>
    <div id="insight"></div>
    <div class="scroll"><table id="tbl"></table></div>
  </main>
</div>
<footer>Cells show accuracy % with item count beneath; dashed outline marks n&lt;10.
&ldquo;All benchmarks&rdquo; is the pooled figure reported in Table 2 of BENCHMARK_REPORT.md.
Generated by <code>skills/build_skill_dashboard.py</code>.</footer>
<script>
const D = __DATA__;
let current = D.skill_order[0];

function heat(p){
  const t = Math.max(0, Math.min(1, p/100));
  const mix = (a,b,k)=>a.map((v,i)=>Math.round(v+(b[i]-v)*k));
  const lo=[193,67,46], mid=[233,223,198], hi=[14,124,134];
  const dark = matchMedia('(prefers-color-scheme: dark)').matches
            && document.documentElement.dataset.theme !== 'light'
            || document.documentElement.dataset.theme === 'dark';
  const L = dark?[217,99,76]:lo, M = dark?[58,54,42]:mid, H = dark?[52,198,201]:hi;
  const c = t<0.5 ? mix(L,M,t*2) : mix(M,H,(t-0.5)*2);
  return `rgb(${c[0]} ${c[1]} ${c[2]} / ${dark?0.55:0.8})`;
}
function ink(p){
  const dark = matchMedia('(prefers-color-scheme: dark)').matches
            && document.documentElement.dataset.theme !== 'light'
            || document.documentElement.dataset.theme === 'dark';
  if (dark) return 'var(--text)';
  return (p>72||p<26) ? '#fff' : 'var(--text)';
}

function renderNav(){
  const nav = document.getElementById('nav');
  const dense = D.skill_order.filter(s=>!D.skills[s].sparse);
  const thin  = D.skill_order.filter(s=>D.skills[s].sparse);
  const group = (label, list) => list.length ? `<div class="navhead">${label}</div>` +
    list.map(s=>`<button class="tab${s===current?' on':''}" data-s="${s}">
      <span>${s}</span><span class="n">${D.skills[s].items}</span></button>`).join('') : '';
  nav.innerHTML = group('Skills', dense) + group('Too sparse to read', thin);
  nav.querySelectorAll('button').forEach(b=>b.onclick=()=>{current=b.dataset.s;render();});
}

function render(){
  renderNav();
  const sk = D.skills[current];
  const benches = Object.keys(sk.rows);
  document.getElementById('title').textContent = current;
  document.getElementById('meta').textContent =
    `${sk.items.toLocaleString()} questions carry this skill, drawn from ${benches.length-1} benchmark${benches.length===2?'':'s'}.`;

  const pooled = sk.rows[D.all_label];
  const ranked = Object.entries(pooled).sort((a,b)=>b[1].pct-a[1].pct);
  let note = '';
  if (sk.sparse){
    note = `<div class="insight warn">Only <b>${sk.items}</b> question${sk.items===1?'':'s'} carry this
      skill &mdash; too few to compare models. Its near-absence is the finding: nothing in this
      corpus exercises it.</div>`;
  } else if (ranked.length){
    const [bn,bv] = ranked[0], [wn,wv] = ranked[ranked.length-1];
    // Widest spread across the benchmarks feeding this skill, for the top model.
    let sprBench='', spr=0;
    const per = benches.filter(b=>b!==D.all_label).map(b=>[b, sk.rows[b][bn]]).filter(x=>x[1]);
    if (per.length>1){
      const hi=per.reduce((a,c)=>c[1].pct>a[1].pct?c:a), lo=per.reduce((a,c)=>c[1].pct<a[1].pct?c:a);
      spr = hi[1].pct-lo[1].pct; sprBench = `${hi[0]} ${hi[1].pct.toFixed(1)}% vs ${lo[0]} ${lo[1].pct.toFixed(1)}%`;
    }
    note = `<div class="insight">Best: <b>${bn}</b> ${bv.pct.toFixed(1)}% &middot;
      weakest: <b>${wn}</b> ${wv.pct.toFixed(1)}% &middot; spread ${(bv.pct-wv.pct).toFixed(1)} pts.
      ${spr>15?`Even <b>${bn}</b> varies by ${spr.toFixed(0)} pts across sources (${sprBench}) &mdash;
      the pooled score averages over real differences.`:''}</div>`;
  }
  document.getElementById('insight').innerHTML = note;

  const t = document.getElementById('tbl');
  const grp = D.model_order.map(m=>`<th class="${D.provider[m]}">${D.provider[m]}</th>`).join('');
  const hdr = D.model_order.map(m=>`<th>${m}</th>`).join('');
  const body = benches.map(b=>{
    const cells = D.model_order.map(m=>{
      const c = sk.rows[b][m];
      if(!c) return '<td class="empty">&mdash;</td>';
      return `<td class="cell${c.n<10?' lown':''}" style="background:${heat(c.pct)};color:${ink(c.pct)}"
        title="${b} × ${m}: ${c.pct.toFixed(1)}% over ${c.n} items">${c.pct.toFixed(1)}<span class="n">n=${c.n}</span></td>`;
    }).join('');
    return `<tr class="${b===D.all_label?'total':''}"><th class="rowhead" title="${b}">${b}</th>${cells}</tr>`;
  }).join('');
  t.innerHTML = `<thead><tr class="grp"><th class="rowhead"></th>${grp}</tr>
    <tr><th class="rowhead">Benchmark</th>${hdr}</tr></thead><tbody>${body}</tbody>`;
}
render();
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', render);
</script>
"""


def main() -> int:
    data = build()
    OUT.write_text(TEMPLATE.replace("__DATA__", json.dumps(data, separators=(",", ":"))))
    dense = [s for s in data["skill_order"] if not data["skills"][s]["sparse"]]
    print(f"{len(data['skill_order'])} skills ({len(dense)} well-populated) -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
