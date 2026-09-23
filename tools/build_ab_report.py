#!/usr/bin/env python3
"""Build a paired base-vs-rich report: same items, both arms, side by side.

The A/B is the paper's null result, and a null is only readable if you can see what moved. This
page pairs every item by (model, subtask, app, system) and shows, for each: whether the prompt
differed at all, whether the outcome flipped, which requirement verdicts changed, the prompt diff,
both answers, and the judge's evidence on both sides.

The strata matter more than the total. 30 of 40 anchors are byte-identical across arms — the
enrichment only touches Input preparation — so those rows are a control: any movement there is
sampling noise, and it calibrates how large the treated movement has to be before it means
anything. Within the treated stage, two anchors (vllm@frontier, pytorch@sophia) are too sparse in
the catalog to receive a format contract, so they act as a placebo.

Scored under r28 by the same replay audit/matrix.py uses, so this page and the published table
cannot disagree.

    python tools/build_ab_report.py          ->  site/trinity_ab_compare_v8.html
"""
from __future__ import annotations

import argparse
import collections
import difflib
import html
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from audit.matrix import GRADED_UNDER, replay, rule_classes        # noqa: E402

TRIN = ROOT / "data" / "corpus" / "v8"
RUBRIC = "r28"
ARMS = ("base", "rich")          # overridden by --arms; the published pair by default
SPARSE = {("vllm", "frontier"), ("pytorch", "sophia")}   # no format contract: the placebo stratum
SUBTASKS = ["Software selection", "Input preparation", "Resource selection", "Batch job creation"]
e = html.escape


def rows(name):
    p = TRIN / name
    return [json.loads(l) for l in p.open()] if p.exists() else []


def key(r):
    return (r["model"], r["subtask"], r["app"], r["system"])


def load(arms):
    S, A, G = {}, {}, collections.defaultdict(list)
    for arm in arms:
        for r in rows(f"samples_v8{arm}.jsonl"):
            S[(arm, r["subtask"], r["app"], r["system"])] = r
        for r in rows(f"answers_v8{arm}.jsonl"):
            A[(arm, *key(r))] = r
        for i in (1, 2, 3):
            for r in rows(f"grades_v8{arm}__gpt56terra__{GRADED_UNDER}__SKILLMODE__run{i}.jsonl"):
                G[(arm, *key(r))].append(r)
    return S, A, G


def consensus(grades):
    """Majority pass/fail and per-rule majority verdict, scored under r28."""
    reps = [replay(g, RUBRIC)[0] for g in grades]
    ok = lambda r: (r.get("correctness") == 2 and r.get("completeness") == 2
                    and r.get("usability") == 2 and not r.get("fatal_error"))
    votes = [ok(r) for r in reps]
    verdicts, evidence = {}, {}
    ids = set().union(*[set(r.get("requirements") or {}) for r in reps]) if reps else set()
    for rid in ids:
        vs = [(r.get("requirements") or {}).get(rid, {}) for r in reps]
        got = [v.get("verdict") for v in vs if v.get("verdict")]
        if not got:
            continue
        top = collections.Counter(got).most_common(1)[0][0]
        verdicts[rid] = top
        evidence[rid] = next((v.get("evidence", "") for v in vs if v.get("verdict") == top), "")
    return {"pass": sum(votes) > 1, "votes": votes,
            "nviol": sum(1 for v in verdicts.values() if v == "violated"),
            "verdicts": verdicts, "evidence": evidence,
            "unstable": len(set(votes)) > 1}


LO, HI = ["base"], ["rich"]          # set by main(); the arm names used in panel labels


def prompt_block(it: dict) -> str:
    """Always show the prompt. When the arms differ, show the diff AND both full texts.

    An identical-prompt row is the control, and the control is only interpretable if you can read
    what was actually asked — "prompts are byte-identical" tells you nothing about whether the
    task was reasonable.
    """
    if it["same"]:
        return (f'<h4>Prompt <span class="q">identical in both arms</span></h4>'
                f'<pre>{e(it["pb"])}</pre>')
    return (f'<h4>Prompt difference ({e(LO[0])} &rarr; {e(HI[0])})</h4>'
            f'<div class="diff">{diff_html(it["pb"], it["pr"])}</div>'
            f'<h4>Full prompts</h4>'
            f'<div class="two"><div><b>{e(LO[0])}</b><pre>{e(it["pb"])}</pre></div>'
            f'<div><b>{e(HI[0])}</b><pre>{e(it["pr"])}</pre></div></div>')


def diff_html(a: str, b: str) -> str:
    out = []
    for ln in difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm="", n=2):
        cls = ("add" if ln.startswith("+") and not ln.startswith("+++")
               else "del" if ln.startswith("-") and not ln.startswith("---")
               else "hunk" if ln.startswith("@@") else "ctx")
        out.append(f'<div class="dl {cls}">{e(ln) or "&nbsp;"}</div>')
    return "".join(out) or '<div class="dl ctx">prompts are byte-identical</div>'


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", default=",".join(ARMS),
                    help="the two arms to pair, least-augmented first (e.g. bare,rich)")
    ap.add_argument("--out", default=None)
    a_ = ap.parse_args()
    lo, hi = [x.strip() for x in a_.arms.split(",")][:2]
    out = pathlib.Path(a_.out) if a_.out else ROOT / "site" / f"trinity_{lo}_vs_{hi}_v8.html"

    LO[0], HI[0] = lo, hi
    S, A, G = load((lo, hi))
    missing = [arm for arm in (lo, hi) if not any(k[0] == arm for k in G)]
    if missing:
        print(f"  no grades for {', '.join(missing)} — answer and judge that arm first")
        return 1

    items, strata = [], collections.defaultdict(lambda: {"b": 0, "r": 0, "n": 0})
    for k in sorted({k[1:] for k in G}, key=lambda x: (SUBTASKS.index(x[1]), x[2], x[3], x[0])):
        model, st, app, sysname = k
        if (lo, *k) not in G or (hi, *k) not in G:
            continue
        b, r = consensus(G[(lo, *k)]), consensus(G[(hi, *k)])
        pb = S[(lo, st, app, sysname)]["prompt"]
        pr = S[(hi, st, app, sysname)]["prompt"]
        same = pb == pr
        moved = {rid: (b["verdicts"].get(rid), r["verdicts"].get(rid))
                 for rid in set(b["verdicts"]) | set(r["verdicts"])
                 if b["verdicts"].get(rid) != r["verdicts"].get(rid)}
        # The base/rich placebo split is meaningless when every prompt differs; fall back to the
        # stage, which is what varies in that case.
        if same:
            stratum = "control — prompt identical"
        elif {LO[0], HI[0]} == {"base", "rich"}:
            stratum = ("placebo — no format contract" if (app, sysname) in SPARSE
                       else "treated — enrichment supplied")
        else:
            stratum = st
        s = strata[stratum]
        s["b"] += b["pass"]; s["r"] += r["pass"]; s["n"] += 1
        items.append({"model": model, "subtask": st, "app": app, "system": sysname,
                      "same": same, "stratum": stratum, "base": b, "rich": r, "moved": moved,
                      "pb": pb, "pr": pr,
                      "ab": (A.get((lo, *k)) or {}).get("answer", ""),
                      "ar": (A.get(("rich", *k)) or {}).get("answer", "")})

    flips = [i for i in items if i["base"]["pass"] != i["rich"]["pass"]]
    nb = sum(i["base"]["pass"] for i in items)
    nr = sum(i["rich"]["pass"] for i in items)

    n_same = sum(1 for i in items if i["same"])
    lede = (
        f"Every item answered under both prompt arms, scored under rubric {RUBRIC} by the same "
        f"replay the results table uses. The enrichment touches Input preparation only, so "
        f"{n_same} of {len(items)} items are byte-identical across arms and act as a control: "
        f"movement there is sampling noise and sets the bar the treated movement has to clear. "
        f"Two treated anchors are too sparse in the catalog to receive a format contract and act "
        f"as a placebo." if n_same else
        f"Every item answered under both prompt arms, scored under rubric {RUBRIC} by the same "
        f"replay the results table uses. <b>{e(lo)}</b> strips the catalog material the prompt "
        f"normally supplies \u2014 the installed-software list, the queue table, the required-file "
        f"inventory, the module lines and the worked example \u2014 keeping the task, the workload "
        f"and the output contract. Every item differs between these arms, so unlike the base/rich "
        f"comparison there is <b>no byte-identical control stratum here</b>: the noise floor is "
        f"imported (the base/rich control moved 4 rows on identical prompts, and 20 of 320 cells "
        f"flip between judge replicates).")

    cards = "".join(
        f'<div class="stat"><b>{v["b"]} &rarr; {v["r"]}</b>'
        f'<span>{e(k)}</span><i>{v["n"]} items</i></div>'
        for k, v in sorted(strata.items()))

    body = []
    for n, it in enumerate(items):
        pb_, pr_ = it["base"]["pass"], it["rich"]["pass"]
        badge = lambda ok: f'<span class="p {"y" if ok else "n"}">{"pass" if ok else "fail"}</span>'
        flip = ("same" if pb_ == pr_ else "gain" if pr_ else "loss")
        # The judge's full decision on BOTH arms, not only what moved: a reader checking a claim
        # needs to see the rules that held as well as the ones that broke.
        cls = rule_classes()
        vb, vr = it["base"]["verdicts"], it["rich"]["verdicts"]
        cell = lambda v, ev: (f'<div class="vd {v or "—"}">{e(str(v or "—"))}</div>'
                              f'<div class="ev">{e((ev or "")[:260])}</div>')
        allrows = "".join(
            f'<tr class="{"chg" if vb.get(rid) != vr.get(rid) else ""}">'
            f'<td class="r">{e(rid)}<span class="cl {cls.get(rid, "")}">{cls.get(rid, "")}</span></td>'
            f'<td class="half">{cell(vb.get(rid), it["base"]["evidence"].get(rid))}</td>'
            f'<td class="half">{cell(vr.get(rid), it["rich"]["evidence"].get(rid))}</td></tr>'
            for rid in sorted(set(vb) | set(vr)))
        moved = allrows
        body.append(f"""
<details class="it" data-flip="{flip}" data-same="{str(it['same']).lower()}"
  data-model="{e(it['model'])}" data-sub="{e(it['subtask'])}">
 <summary>
  <span class="mono">{e(it['app'])}@{e(it['system'])}</span>
  <span class="sub">{e(it['subtask'])}</span>
  <span class="mdl">{e(it['model'])}</span>
  <span class="arms">{badge(pb_)}<span class="arrow">&rarr;</span>{badge(pr_)}</span>
  <span class="v">{it['base']['nviol']} &rarr; {it['rich']['nviol']} viol</span>
  {'<span class="tag">identical prompt</span>' if it['same'] else ''}
  {'<span class="tag warn">replicates disagree</span>' if it['base']['unstable'] or it['rich']['unstable'] else ''}
 </summary>
 <div class="panel">
  {prompt_block(it)}
  <h4>Judge decision — every requirement, both arms
      <span class="q">{len(it['moved'])} changed, highlighted</span></h4>
  <table class="mv"><thead><tr><th>requirement</th><th>{e(LO[0])}</th><th>{e(HI[0])}</th></tr></thead>
  {moved}</table>
  <h4>Answers</h4>
  <div class="two">
   <div><b>{e(lo)}</b><pre>{e(it['ab'][:4000])}</pre></div>
   <div><b>{e(hi)}</b><pre>{e(it['ar'][:4000])}</pre></div>
  </div>
 </div>
</details>""")

    doc = f"""<!doctype html><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Base vs rich — paired</title>
<style>
:root{{--ink:#14181d;--paper:#f6f7f8;--surface:#fff;--muted:#5d6673;--rule:#dfe3e8;
 --accent:#0f6f6c;--ok:#1a6b3c;--bad:#b3261e;--add:#e7f5ec;--del:#fdecea;
 --mono:ui-monospace,Menlo,monospace;--sans:system-ui,-apple-system,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--ink:#e6eaef;--paper:#101418;
 --surface:#171c22;--muted:#95a1b0;--rule:#2a323b;--accent:#4fd1c9;--ok:#5fd08a;--bad:#ff8a80;
 --add:#123021;--del:#33191a}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);font:14px/1.5 var(--sans);padding:28px 16px 80px}}
.wrap{{max-width:1080px;margin:0 auto}}
h1{{font-size:21px;margin:0 0 4px}}
.lede{{color:var(--muted);max-width:74ch;margin:0 0 18px}}
.stats{{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0 6px}}
.stat{{background:var(--surface);border:1px solid var(--rule);border-left:3px solid var(--accent);
 border-radius:5px;padding:9px 13px;min-width:190px}}
.stat b{{display:block;font:600 17px var(--mono)}}
.stat span{{display:block;font-size:12px;color:var(--muted)}}
.stat i{{font-size:11px;color:var(--muted);font-style:normal}}
.bar{{position:sticky;top:0;background:var(--paper);padding:10px 0;border-bottom:1px solid var(--rule);
 margin-bottom:8px;display:flex;gap:8px;flex-wrap:wrap;z-index:5}}
select,button{{font:13px var(--sans);padding:5px 9px;border:1px solid var(--rule);border-radius:5px;
 background:var(--surface);color:var(--ink)}}
.it{{background:var(--surface);border:1px solid var(--rule);border-radius:6px;margin-bottom:6px}}
summary{{cursor:pointer;padding:9px 12px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}}
summary::-webkit-details-marker{{display:none}}
.mono{{font-family:var(--mono);font-size:12.5px;min-width:160px}}
.sub{{font-size:12px;color:var(--muted);min-width:118px}}
.mdl{{font-family:var(--mono);font-size:11.5px;color:var(--muted);min-width:130px}}
.p{{font-size:11px;padding:1px 7px;border-radius:9px;font-weight:600}}
.p.y{{background:var(--add);color:var(--ok)}} .p.n{{background:var(--del);color:var(--bad)}}
.arrow{{margin:0 5px;color:var(--muted)}}
.v{{font-family:var(--mono);font-size:11.5px;color:var(--muted)}}
.tag{{font-size:10.5px;color:var(--muted);border:1px solid var(--rule);border-radius:9px;padding:1px 7px}}
.tag.warn{{color:#b06a00;border-color:#b06a00}}
.panel{{padding:4px 14px 14px;border-top:1px solid var(--rule)}}
h4{{font-size:11.5px;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);margin:14px 0 6px}}
.diff{{font-family:var(--mono);font-size:11.5px;max-height:320px;overflow:auto;
 border:1px solid var(--rule);border-radius:5px}}
.dl{{padding:1px 8px;white-space:pre-wrap}}
.dl.add{{background:var(--add)}} .dl.del{{background:var(--del)}}
.dl.hunk{{color:var(--muted);background:var(--paper)}} .dl.ctx{{color:var(--muted)}}
table.mv{{width:100%;border-collapse:collapse;font-size:12.5px}}
table.mv td{{border-top:1px solid var(--rule);padding:5px 7px;vertical-align:top}}
td.r{{font-family:var(--mono);font-size:11.5px;width:230px}}
td.ev{{color:var(--muted);font-size:11.5px}}
table.mv thead th{{font-size:10.5px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);
 text-align:left;padding:4px 7px;border-bottom:1px solid var(--rule)}}
td.half{{width:36%;vertical-align:top}}
tr.chg{{background:color-mix(in srgb,var(--accent) 7%,transparent)}}
.vd{{font-family:var(--mono);font-size:11px;font-weight:600}}
.vd.violated{{color:var(--bad)}} .vd.satisfied{{color:var(--ok)}}
.vd.not_applicable,.vd.not_evaluated{{color:var(--muted);font-weight:400}}
.ev{{color:var(--muted);font-size:11px;margin-top:2px}}
.cl{{display:block;font-size:9.5px;text-transform:uppercase;letter-spacing:.05em;opacity:.7}}
.cl.supplied{{color:var(--bad)}} .cl.knowledge{{color:var(--ok)}}
.none{{color:var(--muted);font-size:12.5px}}
h4 .q{{text-transform:none;letter-spacing:0;font-weight:400;opacity:.75}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
@media(max-width:820px){{.two{{grid-template-columns:1fr}}}}
pre{{font-family:var(--mono);font-size:11px;white-space:pre-wrap;background:var(--paper);
 border:1px solid var(--rule);border-radius:5px;padding:8px;max-height:340px;overflow:auto;margin:4px 0 0}}
</style>
<div class="wrap">
<h1>{e(lo)} vs {e(hi)}, paired on the same items</h1>
<p class="lede">{lede}</p>

<div class="stats">
 <div class="stat"><b>{nb} &rarr; {nr}</b><span>items passing, of {len(items)}</span><i>{e(lo)} &rarr; {e(hi)}</i></div>
 {cards}
 <div class="stat"><b>{len(flips)}</b><span>items whose outcome flipped</span>
   <i>{sum(1 for i in flips if i['rich']['pass'])} gained, {sum(1 for i in flips if i['base']['pass'])} lost</i></div>
</div>

<div class="bar">
 <select id="f-flip"><option value="">all outcomes</option><option value="gain">gained under rich</option>
  <option value="loss">lost under rich</option><option value="same">unchanged</option></select>
 <select id="f-same"><option value="">all strata</option><option value="false">prompt differed</option>
  <option value="true">prompt identical (control)</option></select>
 <select id="f-sub"><option value="">all stages</option>{"".join(f'<option>{e(s)}</option>' for s in SUBTASKS)}</select>
 <select id="f-model"><option value="">all models</option>{"".join(f'<option>{e(m)}</option>' for m in sorted({i["model"] for i in items}))}</select>
 <button id="x">expand visible</button><span id="count" class="v"></span>
</div>
{"".join(body)}
</div>
<script>
const $=s=>document.querySelector(s), items=[...document.querySelectorAll('.it')];
function apply(){{
  const f=$('#f-flip').value, s=$('#f-same').value, t=$('#f-sub').value, m=$('#f-model').value;
  let n=0;
  for(const it of items){{
    const ok=(!f||it.dataset.flip===f)&&(!s||it.dataset.same===s)
           &&(!t||it.dataset.sub===t)&&(!m||it.dataset.model===m);
    it.style.display=ok?'':'none'; if(ok)n++;
  }}
  $('#count').textContent=n+' of '+items.length+' shown';
}}
['f-flip','f-same','f-sub','f-model'].forEach(i=>$('#'+i).addEventListener('change',apply));
$('#x').addEventListener('click',()=>{{
  const vis=items.filter(i=>i.style.display!=='none'), open=vis.some(i=>i.open);
  vis.forEach(i=>i.open=!open);
}});
apply();
</script>"""
    out.parent.mkdir(exist_ok=True)
    out.write_text(doc)
    print(f"  {out.relative_to(ROOT)}  ({out.stat().st_size // 1024} KB)")
    print(f"  {len(items)} paired items, base {nb} -> rich {nr}, {len(flips)} flipped")
    for k, v in sorted(strata.items()):
        print(f"    {k:<32}{v['b']:>3} -> {v['r']:<3} of {v['n']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
