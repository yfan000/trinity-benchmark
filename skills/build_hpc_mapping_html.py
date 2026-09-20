#!/usr/bin/env python3
"""results/hpc_mapping.html — the fundamental-skill → HPC-task mapping.

Three views: the mapping matrix, the advisory-vs-execution shift, and projected model
readiness with its coverage gate. Self-contained and theme-aware, matching the other
dashboards.

The matrix puts skills on rows and tasks on columns. With six tasks the column headers fit
horizontally, so long skill names ("Reading comprehension (long-context)") are readable
instead of rotated and clipped. Advisory and execution instances are pooled per task; the
shift table below keeps the comparison between them.

Usage:
    python skills/build_hpc_mapping_html.py
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

HPC = ROOT / "results" / "skills" / "hpc"
OUT = ROOT / "results" / "hpc_mapping.html"


def build() -> dict:
    m = json.loads((HPC / "mapping.json").read_text())
    r = json.loads((HPC / "readiness.json").read_text())
    taxonomy = m["taxonomy"]

    combined = m["framings"]["combined"]
    # Keep only skills this corpus actually uses — the rest would be empty rows.
    used = [s for s in taxonomy if any(t["shares"].get(s, 0) > 0 for t in combined.values())]
    # Order rows by total demand so the important skills sit at the top.
    used.sort(key=lambda s: -sum(t["shares"].get(s, 0) * t["n_instances"] for t in combined.values()))

    shift = []
    if "advisory" in m["framings"] and "execution" in m["framings"]:
        a, e = m["framings"]["advisory"], m["framings"]["execution"]
        wm = lambda f, s: (sum(t["shares"].get(s, 0) * t["n_instances"] for t in f.values())  # noqa: E731
                           / sum(t["n_instances"] for t in f.values()))
        shift = sorted(((s, wm(a, s), wm(e, s)) for s in used),
                       key=lambda x: -abs(x[2] - x[1]))

    return {"tasks": combined, "skills": used, "measurable": m["measurable"],
            "bench_counts": m["bench_counts"], "shift": shift,
            "readiness": r["framings"]["combined"], "model_order": r["model_order"],
            "min_coverage": r["min_coverage"], "min_share": m["min_share"]}


TEMPLATE = """<meta charset="utf-8"/>
<title>ALCF HPC Skill Map</title>
<style>
:root{--bg:#F2F4F3;--surface:#FFFFFF;--surface-2:#E9ECEB;--text:#12181B;--text-dim:#55636B;
 --text-faint:#8B979B;--border:#D8DEDD;--border-strong:#BFC8C7;--accent:#0E7C86;
 --accent-soft:#D9EEEE;--accent-text:#08565D;--warn:#C1432E;--good:#2E8B6E;
 --shadow:0 1px 2px rgba(18,24,27,.06),0 4px 12px rgba(18,24,27,.05);--radius:6px;
 --font-body:ui-sans-serif,-apple-system,"Segoe UI",Arial,sans-serif;
 --font-mono:ui-monospace,"SF Mono","Cascadia Code",Consolas,monospace;}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#10151A;--surface:#161D22;
 --surface-2:#1D262C;--text:#E7EDEC;--text-dim:#93A2A6;--text-faint:#5E6C70;--border:#263136;
 --border-strong:#33413A;--accent:#34C6C9;--accent-soft:#16363A;--accent-text:#7FE0E2;
 --warn:#D9634C;--good:#4CBF97;--shadow:0 1px 2px rgba(0,0,0,.3),0 4px 16px rgba(0,0,0,.35);}}
:root[data-theme="dark"]{--bg:#10151A;--surface:#161D22;--surface-2:#1D262C;--text:#E7EDEC;
 --text-dim:#93A2A6;--text-faint:#5E6C70;--border:#263136;--border-strong:#33413A;--accent:#34C6C9;
 --accent-soft:#16363A;--accent-text:#7FE0E2;--warn:#D9634C;--good:#4CBF97;
 --shadow:0 1px 2px rgba(0,0,0,.3),0 4px 16px rgba(0,0,0,.35);}
*{box-sizing:border-box;}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--font-body);font-size:14px;line-height:1.55;}
.wrap{max-width:1520px;margin:0 auto;padding:26px 24px 70px;}
h1{margin:0 0 6px;font-size:21px;font-weight:660;letter-spacing:-.012em;}
.sub{color:var(--text-dim);font-size:13.5px;max-width:88ch;margin-bottom:6px;}
h2{font-size:12px;text-transform:uppercase;letter-spacing:.09em;color:var(--text-faint);font-weight:680;margin:34px 0 10px;}
.bar{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin:16px 0 12px;}
.seg{display:inline-flex;border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;background:var(--surface);}
.seg button{background:none;border:0;padding:6px 15px;font:inherit;font-size:12.5px;color:var(--text-dim);cursor:pointer;}
.seg button+button{border-left:1px solid var(--border);}
.seg button:hover{background:var(--surface-2);color:var(--text);}
.seg button.on{background:var(--accent-soft);color:var(--accent-text);font-weight:600;}
.lbl{font-size:10.5px;text-transform:uppercase;letter-spacing:.09em;color:var(--text-faint);font-weight:680;}
.scroll{overflow-x:auto;border:1px solid var(--border);border-radius:var(--radius);background:var(--surface);box-shadow:var(--shadow);}
table{border-collapse:separate;border-spacing:0;font-size:12.5px;width:100%;}
th,td{padding:6px 8px;text-align:center;white-space:nowrap;border-bottom:1px solid var(--border);}
thead th{position:sticky;top:0;background:var(--surface);z-index:2;font-weight:600;font-size:11px;}
th.rh,td.rh{position:sticky;left:0;z-index:1;background:var(--surface);text-align:left;font-weight:500;
 border-right:1px solid var(--border-strong);min-width:270px;white-space:normal;}
td.rh .bn{display:block;font-size:10px;color:var(--text-faint);font-family:var(--font-mono);}
thead th.task{white-space:normal;min-width:104px;max-width:126px;line-height:1.25;vertical-align:bottom;}
tr.tot td{background:var(--surface-2);font-weight:650;}
thead th.rh{z-index:3;}
td.rh .sz{display:block;font-size:10px;color:var(--text-faint);font-family:var(--font-mono);}
td.c{font-family:var(--font-mono);font-variant-numeric:tabular-nums;}
td.zero{color:var(--text-faint);}
td.edge{outline:2px solid var(--accent);outline-offset:-2px;font-weight:650;}
.unmeas{color:var(--warn);font-weight:650;}
.note{margin-top:12px;color:var(--text-dim);font-size:12.5px;max-width:96ch;}
.note b{color:var(--text);}
.cov{display:inline-block;width:56px;height:7px;border-radius:4px;background:var(--surface-2);overflow:hidden;vertical-align:middle;margin-right:6px;}
.cov i{display:block;height:100%;background:var(--good);}
.cov.low i{background:var(--warn);}
.notest{color:var(--warn);font-style:italic;}
.shift td.up{color:var(--good);font-weight:650;}
.shift td.down{color:var(--warn);font-weight:650;}
.prov{margin-top:26px;padding-top:14px;border-top:1px solid var(--border);color:var(--text-faint);
 font-size:11.5px;line-height:1.65;max-width:96ch;}
.prov b{color:var(--text-dim);font-weight:650;}
</style>
<div class="wrap">
<h1>What HPC work demands of a model</h1>
<div class="sub">592 realistic ALCF task instances across six operational tasks &mdash; generated
from Argonne's own documentation, then labeled with the same 29-tag fundamental-skill
classifier used on the 3,604-question benchmark corpus. The mapping below is
<b>measured from those labels</b>, not asserted.</div>
<div class="sub">Each task pools both ways it can arrive: a user asking the help desk for
advice, and an agent being told to carry the work out.</div>

<h2>Mapping — share of a task's instances requiring each skill</h2>
<div class="scroll"><table id="matrix"></table></div>
<div class="note" id="mnote"></div>

<h2>Within that total: what changes when an agent acts instead of advises</h2>
<div class="scroll"><table id="shift" class="shift"></table></div>

<h2>Projected model readiness</h2>
<div class="note" style="margin:0 0 10px">These are <b>projections</b>, not measurements: no
model was run against an HPC task. Each is that task's skill profile weighted against the
model's measured accuracy on those skills elsewhere. Where too much of a task's demand rests
on skills our corpus cannot measure, the row is withheld rather than guessed.</div>
<div class="scroll"><table id="ready"></table></div>

<div class="prov" id="prov"></div>
</div>
<script>
const D = __DATA__;
const TASKS = Object.keys(D.tasks).sort();
const dark = () => (matchMedia('(prefers-color-scheme: dark)').matches
  && document.documentElement.dataset.theme !== 'light') || document.documentElement.dataset.theme === 'dark';
function heat(v){
  if(!v) return 'transparent';
  const t=Math.max(0,Math.min(1,v));
  return dark() ? `rgb(52 198 201 / ${0.10+t*0.5})` : `rgb(14 124 134 / ${0.07+t*0.55})`;
}
const pct = v => (v*100).toFixed(0)+'%';

// Skills are rows and tasks are columns: with only six tasks the column headers fit
// horizontally, so long skill names no longer have to be rotated and clipped.
function matrix(){
  const head=TASKS.map(t=>`<th class="task">${t}<br><span style="font-weight:400;opacity:.6">n=${D.tasks[t].n_instances}</span></th>`).join('');
  const body=D.skills.map(s=>{
    const cells=TASKS.map(t=>{
      const d=D.tasks[t], v=d.shares[s]||0, edge=d.edges[s]!==undefined;
      if(!v) return '<td class="c zero">&middot;</td>';
      return `<td class="c${edge?' edge':''}" style="background:${heat(v)}"
        title="${t} × ${s}: ${pct(v)} of ${d.n_instances} instances${edge?' (edge)':''}">${pct(v)}</td>`;
    }).join('');
    const un = !D.measurable[s];
    return `<tr><td class="rh"><span class="${un?'unmeas':''}">${s}</span>
      <span class="bn">${(D.bench_counts[s]||0).toLocaleString()} benchmark questions${un?' — not measurable':''}</span></td>${cells}</tr>`;
  }).join('');
  document.getElementById('matrix').innerHTML=
    `<thead><tr><th class="rh">Fundamental skill</th>${head}</tr></thead><tbody>${body}</tbody>`;
  document.getElementById('mnote').innerHTML=
    `Outlined cells are <b>edges</b> &mdash; the skill appears on at least ${pct(D.min_share)} of
     that task's instances (and at least 5 of them), so a stray label can't create one.
     Skills in <span class="unmeas">red</span> have too few benchmark questions behind them to
     support a model score. ${D.skills.length} of 29 skills appear on HPC work at all; the rest
     are omitted as empty rows.`;
}

function shiftTable(){
  const rows=D.shift.slice(0,12).map(([s,a,e])=>{
    const d=e-a, cls=d>0.02?'up':(d<-0.02?'down':'');
    return `<tr><td class="rh">${s}</td><td class="c">${pct(a)}</td><td class="c">${pct(e)}</td>
      <td class="c ${cls}">${d>0?'+':''}${pct(d)}</td></tr>`;
  }).join('');
  document.getElementById('shift').innerHTML=
    `<thead><tr><th class="rh">Fundamental skill</th><th>Advisory</th><th>Execution</th><th>Shift</th></tr></thead>
     <tbody>${rows}</tbody>`;
}

function ready(){
  const head=D.model_order.map(m=>`<th>${m}</th>`).join('');
  const body=TASKS.map(t=>{
    const d=D.readiness[t], low=d.coverage<D.min_coverage;
    const cov=`<span class="cov ${low?'low':''}"><i style="width:${(d.coverage*100).toFixed(0)}%"></i></span>${pct(d.coverage)}`;
    if(!d.estimable){
      const miss=d.unmeasured.slice(0,2).map(([s,w])=>`${s} ${pct(w)}`).join(', ');
      return `<tr><td class="rh">${t}<span class="bn">${cov}</span></td>
        <td class="notest" colspan="${D.model_order.length}">not estimable &mdash; weight on unmeasured skills: ${miss}</td></tr>`;
    }
    const vals=D.model_order.map(m=>d.readiness[m]).filter(v=>v!==null);
    const lo=Math.min(...vals), hi=Math.max(...vals);
    const cells=D.model_order.map(m=>{
      const v=d.readiness[m];
      if(v===null) return '<td class="c zero">&mdash;</td>';
      return `<td class="c" style="background:${heat(0.15+((v-lo)/Math.max(hi-lo,1e-9))*0.85)}"
        title="${t} × ${m}: projected ${v.toFixed(1)}%">${v.toFixed(0)}</td>`;
    }).join('');
    return `<tr><td class="rh">${t}<span class="bn">${cov}</span></td>${cells}</tr>`;
  }).join('');
  document.getElementById('ready').innerHTML=
    `<thead><tr><th class="rh">HPC task &middot; coverage</th>${head}</tr></thead><tbody>${body}</tbody>`;
}

function render(){matrix();shiftTable();ready();}
document.getElementById('prov').innerHTML=
  `<b>Argonne Leadership Computing Facility</b> &middot; September 2026.
   <b>Method.</b> 592 task instances were generated by an LLM from 25 cached pages of
   docs.alcf.anl.gov (PBS Pro, queue policy, Globus, filesystems, debugging and performance
   tools), then classified against the locked 29-tag fundamental-skill taxonomy by
   <code>claude-sonnet-4-6</code> at temperature 0 &mdash; the same classifier and taxonomy used
   on the benchmark corpus. Each task pools its advisory and execution instances.<br>
   <b>Read with these caveats.</b> The instances are <i>synthetic though documentation-grounded</i>;
   real user tickets would be better evidence and the pipeline accepts them as a drop-in
   replacement. The same model wrote and labelled them, so their agreement is not fully
   independent, and a blind re-check agreed with only 79% of the task labels. Readiness figures
   are projections from fundamental-skill scores, never direct measurements. Even the execution
   instances ask a model to <i>produce</i> a command rather than run one and read its output, so
   genuine tool use remains unmeasured. Full method in <code>BENCHMARK_REPORT.md</code>.`;
render();
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', render);
</script>
"""


def main() -> int:
    data = build()
    OUT.write_text(TEMPLATE.replace("__DATA__", json.dumps(data, separators=(",", ":"))))
    n = sum(t["n_instances"] for t in data["tasks"].values())
    print(f"{len(data['skills'])} skills x {len(data['tasks'])} tasks, "
          f"{n} instances (advisory + execution combined) -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
