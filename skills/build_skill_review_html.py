#!/usr/bin/env python3
"""results/judging_skill_review.html — the judging skill, laid out for a human review pass.

The skill is 50 requirements across four subtasks, and the question a reviewer needs to answer
per requirement is always the same: should this rule exist, and is it decided the right way?
Two columns carry the evidence for that:

  FP      how often it flagged a real Polaris run that actually executed. Should be 0.
  recall  how often it caught a deliberately broken script.

Requirements with no calibration data show blank — nothing tested them, which is not the same
as passing, and the page says so rather than leaving a reader to assume.
"""
from __future__ import annotations
import html, json, sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REQ = ROOT / "skills" / "judging" / "requirements"
OUT = ROOT / "results" / "judging_skill_review.html"
CAL = ROOT / "results" / "skills" / "trinity" / "calibration.json"

ORDER = [("software_selection", "Software selection"), ("input_preparation", "Input preparation"),
         ("resource_selection", "Resource selection"), ("batch_job_creation", "Batch job creation")]


def esc(s) -> str:
    return html.escape(str(s or ""))


def main() -> int:
    cal = json.loads(CAL.read_text()) if CAL.exists() else []
    fp = Counter(v for r in cal if r["kind"] == "positive" and "error" not in r
                 for v in r["violated"])
    rec = {}
    for r in cal:
        if r["kind"] == "negative" and "error" not in r and r.get("expect"):
            a, b = rec.get(r["expect"], (0, 0))
            rec[r["expect"]] = (a + bool(r["caught"]), b + 1)

    cards, counts = "", Counter()
    for d, title in ORDER:
        rows, fcs = "", ""
        for f in sorted((REQ / d).glob("*.yaml")):
            doc = yaml.safe_load(f.read_text()) or {}
            for r in doc.get("requirements") or []:
                rid = r["id"]
                det = r.get("decided_by") == "deterministic"
                counts["deterministic" if det else "judge"] += 1
                c, n = rec.get(rid, (None, None))
                nfp = fp.get(rid, 0)
                counts["fp"] += 1 if nfp else 0
                flag = ("bad" if nfp else "good" if n else "none")
                rows += (
                  f'<tr class="r" data-dec="{"det" if det else "judge"}" '
                  f'data-ev="{"fp" if nfp else "tested" if n else "untested"}">'
                  f'<td><code>{esc(rid)}</code><div class="claim">'
                  f'{esc(" ".join(str(r["claim"]).split()))}</div>'
                  + (f'<div class="why">{esc(" ".join(str(r["rationale"]).split()))}</div>'
                     if r.get("rationale") else "")
                  + f'</td><td><span class="pill {"det" if det else "jud"}">'
                  f'{"code" if det else "judge"}</span></td>'
                  f'<td><span class="sev {esc(r.get("severity","major"))}">'
                  f'{esc(r.get("severity","major"))}</span></td>'
                  f'<td class="dim">{esc(r.get("dimension"))}</td>'
                  f'<td class="src">{esc(r.get("source",""))}</td>'
                  f'<td class="r n {flag}">{nfp or ""}</td>'
                  f'<td class="r n">{f"{c}/{n}" if n else ""}</td></tr>')
            for x in doc.get("free_choice") or []:
                counts["free"] += 1
                fcs += (f'<li><b>{esc(x["axis"])}</b> — '
                        f'{esc(" ".join(str(x["note"]).split()))}'
                        f'<span class="src"> [{esc(x.get("source",""))}]</span></li>')
        cards += (f'<section data-sub="{esc(title)}"><h2>{esc(title)}</h2>'
                  f'<table><thead><tr><th>requirement</th><th>decided</th><th>sev</th>'
                  f'<th>dim</th><th>source</th><th class="r">FP</th><th class="r">recall</th>'
                  f'</tr></thead><tbody>{rows}</tbody></table>'
                  + (f'<h3>Free choice — never deduct</h3><ul class="fc">{fcs}</ul>'
                     if fcs else "") + "</section>")

    OUT.write_text(PAGE.format(cards=cards, det=counts["deterministic"], jud=counts["judge"],
                               free=counts["free"], fp=counts["fp"],
                               tot=counts["deterministic"] + counts["judge"]))
    print(f"{OUT}  ({OUT.stat().st_size//1024} KB)")
    return 0


PAGE = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Judging Skill Review</title>
<style>
:root{{--bg:#F5F3F0;--panel:#fff;--sunk:#EEEAE5;--ink:#15120F;--ink2:#5D554C;--ink3:#948B80;
 --line:#DFD8CF;--acc:#2F6F5E;--accs:#DDEEE8;--acct:#1C4A3E;--bad:#B3402F;--bads:#F8E4E0;
 --good:#2F7D5B;--goods:#E2F0E9;--warn:#A9761A;--warns:#F7EBD6;
 --mono:ui-monospace,"SF Mono",Menlo,monospace;--sans:ui-sans-serif,-apple-system,"Segoe UI",Arial,sans-serif;}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#111110;--panel:#1A1917;
 --sunk:#222120;--ink:#EDEAE5;--ink2:#A9A197;--ink3:#6E665C;--line:#2C2A27;--acc:#4FB396;
 --accs:#12302A;--acct:#7FD6BD;--bad:#E0705C;--bads:#2E1815;--good:#5FBE92;--goods:#12291F;
 --warn:#D6A44E;--warns:#2C2113;}}}}
:root[data-theme="dark"]{{--bg:#111110;--panel:#1A1917;--sunk:#222120;--ink:#EDEAE5;--ink2:#A9A197;
 --ink3:#6E665C;--line:#2C2A27;--acc:#4FB396;--accs:#12302A;--acct:#7FD6BD;--bad:#E0705C;
 --bads:#2E1815;--good:#5FBE92;--goods:#12291F;--warn:#D6A44E;--warns:#2C2113;}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:14px;line-height:1.5}}
.wrap{{max-width:1180px;margin:0 auto;padding:30px 20px 80px}}
h1{{font-size:clamp(23px,3.4vw,33px);letter-spacing:-.02em;margin:12px 0 6px;font-weight:660}}
.sub{{color:var(--ink2);max-width:74ch;margin:0 0 20px}}
.stats{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:18px}}
.stat{{background:var(--panel);border:1px solid var(--line);border-radius:9px;padding:9px 14px}}
.stat b{{display:block;font-family:var(--mono);font-size:19px;font-weight:660}}
.stat span{{font-size:10px;text-transform:uppercase;letter-spacing:.07em;color:var(--ink3);font-weight:670}}
.bar{{position:sticky;top:0;z-index:9;background:var(--bg);padding:10px 0;border-bottom:1px solid var(--line);
 display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}}
select{{font:inherit;font-size:12.5px;background:var(--panel);color:var(--ink);border:1px solid var(--line);
 border-radius:7px;padding:6px 9px;cursor:pointer}}
select:hover{{border-color:var(--acc)}}
section{{background:var(--panel);border:1px solid var(--line);border-radius:11px;padding:16px 18px;margin-bottom:14px}}
h2{{font-size:17px;margin:0 0 10px;font-weight:660;letter-spacing:-.01em}}
h3{{font-size:11px;text-transform:uppercase;letter-spacing:.09em;color:var(--ink3);margin:16px 0 7px;font-weight:700}}
table{{width:100%;border-collapse:collapse}}
th{{font-size:9.5px;text-transform:uppercase;letter-spacing:.06em;color:var(--ink3);font-weight:700;
 text-align:left;padding:0 8px 6px 0;border-bottom:1px solid var(--line)}}
td{{padding:9px 8px 9px 0;border-bottom:1px solid var(--line);vertical-align:top;color:var(--ink2);font-size:12.5px}}
td code{{font-family:var(--mono);font-size:11.5px;color:var(--ink);font-weight:600}}
.claim{{margin-top:3px;color:var(--ink2);max-width:62ch}}
.why{{margin-top:4px;font-size:11.5px;color:var(--ink3);border-left:2px solid var(--line);padding-left:8px;max-width:62ch}}
.pill{{font-size:10px;font-weight:700;padding:2px 8px;border-radius:20px;text-transform:uppercase;letter-spacing:.05em}}
.pill.det{{background:var(--accs);color:var(--acct)}}
.pill.jud{{background:var(--warns);color:var(--warn)}}
.sev{{font-size:10px;font-weight:660}}
.sev.fatal{{color:var(--bad)}}.sev.major{{color:var(--warn)}}.sev.minor{{color:var(--ink3)}}
.dim,.src{{font-size:11px;color:var(--ink3)}}
.src{{font-family:var(--mono);font-size:10.5px}}
td.r{{text-align:right}}
td.n{{font-family:var(--mono);font-weight:660}}
td.n.bad{{color:var(--bad);background:var(--bads)}}
td.n.good{{color:var(--good)}}
.fc li{{font-size:12.5px;color:var(--ink2);margin-bottom:7px;line-height:1.5}}
.fc b{{color:var(--ink)}}
.note{{background:var(--warns);border-left:3px solid var(--warn);border-radius:0 8px 8px 0;
 padding:11px 14px;margin-bottom:18px;font-size:12.5px;color:var(--ink2);line-height:1.55}}
.note b{{color:var(--ink)}}
.hide{{display:none!important}}
footer{{margin-top:26px;padding-top:14px;border-top:1px solid var(--line);font-size:11.5px;color:var(--ink3);line-height:1.6}}
</style>
<div class="wrap">
<h1>Judging skill — review copy</h1>
<p class="sub">Rubric <b>r2</b>. The requirements <i>are</i> the skill: the judge rules on each one
separately and the 0&ndash;2 scores are computed from those verdicts in code. For each rule the
question is the same &mdash; should it exist, and is it decided the right way?</p>

<div class="stats">
 <div class="stat"><b>{tot}</b><span>requirements</span></div>
 <div class="stat"><b>{det}</b><span>decided in code</span></div>
 <div class="stat"><b>{jud}</b><span>decided by judge</span></div>
 <div class="stat"><b>{free}</b><span>free-choice axes</span></div>
 <div class="stat"><b>{fp}</b><span>with false positives</span></div>
</div>

<div class="note"><b>Calibration evidence.</b> <b>FP</b> counts how often a rule flagged a real
Polaris job script that actually ran &mdash; it should be 0. <b>recall</b> counts how often it
caught a deliberately broken script. Only 1 of 8 real scripts came back clean, and every false
positive belongs to a rule decided by the judge or whose code check is unimplemented; every
rule backed by mined runs scored 8/8 recall with no false positives. A <b>blank</b> means
nothing tested that rule &mdash; not that it passed. Input preparation and Resource selection
have no calibration data at all yet.</div>

<div class="bar">
 <select id="fsub"><option value="">All subtasks</option>
  <option>Software selection</option><option>Input preparation</option>
  <option>Resource selection</option><option>Batch job creation</option></select>
 <select id="fdec"><option value="">Decided by: any</option>
  <option value="det">code</option><option value="judge">judge</option></select>
 <select id="fev"><option value="">Evidence: any</option>
  <option value="fp">has false positives</option><option value="tested">tested, clean</option>
  <option value="untested">untested</option></select>
</div>

{cards}

<footer>Generated from <code>skills/judging/requirements/</code> and
<code>results/skills/trinity/calibration.json</code>. Every rule's <code>source</code> says what
backs it: <code>run:N/M</code> is mined from real runs, <code>catalog:</code> from the facility
YAML, <code>format:</code> from a format spec, and <code>model</code> means an LLM asserted it
and nothing has confirmed it &mdash; the first thing to doubt.</footer>
</div>
<script>
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
function apply(){{
 const s=$('#fsub').value,d=$('#fdec').value,e=$('#fev').value;
 $$('section').forEach(x=>x.classList.toggle('hide',!!s&&x.dataset.sub!==s));
 $$('tr.r').forEach(r=>r.classList.toggle('hide',
   (d&&r.dataset.dec!==d)||(e&&r.dataset.ev!==e)));
}}
['fsub','fdec','fev'].forEach(i=>$('#'+i).addEventListener('change',apply));apply();
</script>
"""

if __name__ == "__main__":
    sys.exit(main())
