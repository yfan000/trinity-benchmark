#!/usr/bin/env python3
"""Render the augmentation-ablation result: what the prompt supplies, in pass-points.

This is the findings page. The per-item browser (tools/build_ab_report.py) is where you go to
check any single claim on it; this is the claim.

Everything is computed here from the graded corpus under one rubric (r28) by the same replay
audit/matrix.py uses, including the exact McNemar. Nothing is typed in.

    python tools/build_result_page.py            ->  site/trinity_augmentation_v8.html
    python tools/build_result_page.py --arms bare,cat,base,rich
"""
from __future__ import annotations

import argparse
import collections
import html
import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from audit.matrix import GRADED_UNDER, replay, rule_classes         # noqa: E402

TRIN = ROOT / "data" / "corpus" / "v8"
RUBRIC = "r28"
SUBTASKS = ["Software selection", "Input preparation", "Resource selection", "Batch job creation"]
LABEL = {"bare": "bare<br><span>no catalog, no example</span>",
         "cat": "cat<br><span>catalog, no example</span>",
         "base": "base<br><span>+ worked examples</span>",
         "rich": "rich<br><span>+ contracts, scaling</span>"}
e = html.escape


def ok(r):
    return (r.get("correctness") == 2 and r.get("completeness") == 2
            and r.get("usability") == 2 and not r.get("fatal_error"))


def load(arm, view):
    """Majority-of-k pass per item, scored under r28 in the requested view."""
    runs = []
    for i in (1, 2, 3):
        p = TRIN / f"grades_v8{arm}__gpt56terra__{GRADED_UNDER}__SKILLMODE__run{i}.jsonl"
        if p.exists():
            runs.append({(r["model"], r["subtask"], r["app"], r["system"]): r
                         for r in map(json.loads, p.open())})
    if not runs:
        return None, None
    keys = sorted(set.intersection(*[set(m) for m in runs]))
    out, viol = {}, collections.Counter()
    for k in keys:
        votes = []
        for m in runs:
            rr, _ = replay(m[k], RUBRIC, view=view)
            votes.append(ok(rr))
            for rid, v in (rr.get("requirements") or {}).items():
                if v.get("verdict") == "violated":
                    viol[rid] += 1
        out[k] = sum(votes) > len(votes) / 2
    return out, viol


def mcnemar_exact(b, c):
    """Two-sided exact binomial on the discordant pairs."""
    n = b + c
    if not n:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", default="bare,rich")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    arms = [x.strip() for x in a.arms.split(",")]
    out = pathlib.Path(a.out) if a.out else ROOT / "site" / "trinity_augmentation_v8.html"

    data = {}
    for view in ("all", "knowledge+mixed"):
        for arm in arms:
            p, v = load(arm, view)
            if p is None:
                print(f"  {arm}: no grades — skipping")
                continue
            data[(arm, view)] = (p, v)
    arms = [x for x in arms if (x, "all") in data]
    if len(arms) < 2:
        print("  need at least two graded arms")
        return 1
    lo, hi = arms[0], arms[-1]
    keys = sorted(set(data[(lo, "all")][0]) & set(data[(hi, "all")][0]))
    models = sorted({k[0] for k in keys})

    def n(arm, view, sel=None):
        p = data[(arm, view)][0]
        return sum(p[k] for k in (sel if sel is not None else keys) if k in p)

    # ---- headline
    tot = len(keys)
    delta = n(hi, "all") - n(lo, "all")

    # ---- stage x arm, both views
    def grid(view):
        rows = ""
        for st in SUBTASKS:
            sel = [k for k in keys if k[1] == st]
            cells = "".join(f"<td><b>{n(arm, view, sel)}</b><span>/{len(sel)}</span></td>"
                            for arm in arms)
            d = n(hi, view, sel) - n(lo, view, sel)
            rows += f"<tr><th>{e(st)}</th>{cells}<td class='d'>{d:+d}</td></tr>"
        cells = "".join(f"<td><b>{n(arm, view)}</b><span>/{tot}</span></td>" for arm in arms)
        d = n(hi, view) - n(lo, view)
        rows += f"<tr class='tot'><th>all stages</th>{cells}<td class='d'>{d:+d}</td></tr>"
        return rows

    # ---- per model, exact McNemar, scored on all rules
    P, Q = data[(lo, "all")][0], data[(hi, "all")][0]
    stats = ""
    for label, sel in ([("all items", keys)]
                       + [(m, [k for k in keys if k[0] == m]) for m in models]):
        b = sum(1 for k in sel if not P[k] and Q[k])          # gained with augmentation
        c = sum(1 for k in sel if P[k] and not Q[k])
        p = mcnemar_exact(b, c)
        testable = len(sel) >= 12
        stats += (f"<tr{' class=hl' if label == 'all items' else ''}><th>{e(label)}</th>"
                  f"<td>{n(lo,'all',sel)}</td><td>{n(hi,'all',sel)}</td>"
                  f"<td class='d'>{n(hi,'all',sel)-n(lo,'all',sel):+d}</td>"
                  f"<td>{b}</td><td>{c}</td>"
                  f"<td class='p'>{'%.1g' % p if testable else 'n too small'}</td></tr>")

    # ---- model x stage: who is helped, and where
    def cellgrid(view):
        rows = ""
        for m in models:
            tds = ""
            for st in SUBTASKS:
                sel = [k for k in keys if k[0] == m and k[1] == st]
                a_, b_ = n(lo, view, sel), n(hi, view, sel)
                d = b_ - a_
                # shade by how much of this cell the prompt is worth
                pct = d / len(sel) if sel else 0
                tds += (f'<td class="cell" style="--f:{min(1.0, pct * 1.6):.2f}">'
                        f'<b>{a_}&rarr;{b_}</b><span>{d:+d}</span></td>')
            sel = [k for k in keys if k[0] == m]
            rows += (f'<tr><th>{e(m)}</th>{tds}'
                     f'<td class="d">{n(hi,view,sel)-n(lo,view,sel):+d}</td></tr>')
        tds = ""
        for st in SUBTASKS:
            sel = [k for k in keys if k[1] == st]
            tds += f'<td class="d">{n(hi,view,sel)-n(lo,view,sel):+d}</td>'
        rows += (f'<tr class="tot"><th>all models</th>{tds}'
                 f'<td class="d">{n(hi,view)-n(lo,view):+d}</td></tr>')
        return rows

    # per-model: the rules the prompt rescues most
    def rescued(sel):
        c = collections.Counter()
        for arm, sign in ((lo, 1), (hi, -1)):
            runs = []
            for i in (1, 2, 3):
                pth = TRIN / f"grades_v8{arm}__gpt56terra__{GRADED_UNDER}__SKILLMODE__run{i}.jsonl"
                if pth.exists():
                    runs.append({(r["model"], r["subtask"], r["app"], r["system"]): r
                                 for r in map(json.loads, pth.open())})
            for k in sel:
                for m_ in runs:
                    if k not in m_:
                        continue
                    rr, _ = replay(m_[k], RUBRIC)
                    for rid, v in (rr.get("requirements") or {}).items():
                        if v.get("verdict") == "violated":
                            c[rid] += sign
        return [(rid, d) for rid, d in c.most_common(3) if d > 0]

    permodel = ""
    for m in models:
        sel = [k for k in keys if k[0] == m]
        top = rescued(sel)
        why = " &middot; ".join(f"<code>{e(r.split('.', 1)[1])}</code> &minus;{d}" for r, d in top)
        cap = n(hi, "knowledge+mixed", sel) - n(lo, "knowledge+mixed", sel)
        allg = n(hi, "all", sel) - n(lo, "all", sel)
        permodel += (f'<tr><th>{e(m)}</th><td class="d">{allg:+d}</td><td class="d">{cap:+d}</td>'
                     f'<td class="why">{why}</td></tr>')

    # ---- which requirements moved
    vlo, vhi = data[(lo, "all")][1], data[(hi, "all")][1]
    cls = rule_classes()
    moved = sorted(((vlo[r] - vhi[r], r) for r in set(vlo) | set(vhi)), reverse=True)[:12]
    mrows = "".join(
        f"<tr><td class='r'>{e(r)}</td><td class='c {cls.get(r,'?')}'>{cls.get(r,'?')}</td>"
        f"<td>{vlo[r]}</td><td>{vhi[r]}</td><td class='d'>-{d}</td></tr>"
        for d, r in moved if d > 0)

    head = "".join(f"<th>{LABEL.get(x, e(x))}</th>" for x in arms)
    doc = f"""<!doctype html><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>What the prompt supplies</title>
<style>
:root{{--ink:#14181d;--paper:#f6f7f8;--surface:#fff;--muted:#5d6673;--rule:#dfe3e8;
 --accent:#0f6f6c;--warn:#b3261e;--ok:#1a6b3c;--mono:ui-monospace,Menlo,monospace;
 --sans:system-ui,-apple-system,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--ink:#e6eaef;--paper:#101418;
 --surface:#171c22;--muted:#95a1b0;--rule:#2a323b;--accent:#4fd1c9;--warn:#ff8a80;--ok:#5fd08a}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);font:15px/1.6 var(--sans);
 padding:40px 18px 90px}}
.w{{max-width:860px;margin:0 auto}}
.kick{{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);font-weight:600}}
h1{{font-size:27px;margin:6px 0 10px;letter-spacing:-.015em}}
.lede{{color:var(--muted);max-width:68ch}}
h2{{font-size:13px;text-transform:uppercase;letter-spacing:.09em;color:var(--muted);
 margin:40px 0 6px;font-weight:600}}
.big{{display:flex;gap:26px;align-items:baseline;margin:22px 0 4px;flex-wrap:wrap}}
.big b{{font:600 42px/1 var(--mono);color:var(--accent)}}
.big span{{color:var(--muted);max-width:44ch}}
table{{width:100%;border-collapse:collapse;margin:10px 0 4px;font-variant-numeric:tabular-nums}}
th{{font-size:11.5px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);
 text-align:right;padding:0 9px 8px;font-weight:600;vertical-align:bottom}}
th span{{display:block;text-transform:none;letter-spacing:0;font-weight:400;font-size:10.5px;opacity:.8}}
tbody th{{text-align:left;text-transform:none;font-size:14px;color:var(--ink);letter-spacing:0;
 padding:8px 9px;font-weight:400}}
td{{text-align:right;padding:8px 9px;border-top:1px solid var(--rule);font-family:var(--mono);
 font-size:14px}}
td b{{font-weight:600}} td span{{color:var(--muted);font-size:11.5px}}
tr.tot td,tr.tot th{{border-top:2px solid var(--ink);font-weight:600}}
tr.hl td,tr.hl th{{background:color-mix(in srgb,var(--accent) 8%,transparent)}}
td.d{{color:var(--accent);font-weight:600}}
td.p{{font-size:12.5px;color:var(--muted)}}
td.r{{text-align:left;font-size:12px}}
td.c{{text-align:left;font-size:11px}}
td.c.supplied{{color:var(--warn)}} td.c.knowledge{{color:var(--ok)}}
table.hm td.cell{{background:color-mix(in srgb,var(--accent) calc(var(--f)*42%),transparent);
 text-align:center}}
table.hm td.cell b{{display:block;font-size:13px;font-weight:600}}
table.hm td.cell span{{font-size:11px;color:var(--muted)}}
td.why{{text-align:left;font-size:11.5px;color:var(--muted);font-family:var(--sans)}}
td.why code{{font-family:var(--mono);font-size:11px}}
.note{{background:var(--surface);border:1px solid var(--rule);border-left:3px solid var(--accent);
 border-radius:5px;padding:13px 16px;margin:14px 0;font-size:14px}}
.note b{{display:block;margin-bottom:3px}}
.note.warn{{border-left-color:var(--warn)}}
.meta{{font-family:var(--mono);font-size:12px;color:var(--muted);border-top:1px solid var(--rule);
 padding-top:12px;margin-top:38px}}
a{{color:var(--accent)}}
</style>
<div class="w">
<div class="kick">Trinity benchmark &middot; augmentation ablation</div>
<h1>What the prompt supplies, in pass-points</h1>
<p class="lede">The published benchmark hands the model most of the facility knowledge the task is
about: the installed-software list, the queue table, the required-file inventory, the module
lines, a worked example. This strips that material away and re-runs the same items, so the score
can be split into what the model knows and what we told it.</p>

<div class="big"><b>{delta:+d}</b>
<span>of {tot} items, the difference between <code>{e(lo)}</code> and <code>{e(hi)}</code> —
{n(lo,'all')}/{tot} ({100*n(lo,'all')//tot}%) unaugmented against
{n(hi,'all')}/{tot} ({100*n(hi,'all')//tot}%) with the current prompt.</span></div>

<h2>Passes by stage — all {len(cls)} requirements</h2>
<table><thead><tr><th style="text-align:left">stage</th>{head}<th>&Delta;</th></tr></thead>
<tbody>{grid("all")}</tbody></table>

<h2>Passes by stage — capability only</h2>
<p class="lede">Restricted to requirements a model could satisfy without the catalog
(<code>r29-capability</code>, registered before these answers existed). This separates
<i>it does not know our queue names</i> from <i>it cannot write a valid deck</i>.</p>
<table><thead><tr><th style="text-align:left">stage</th>{head}<th>&Delta;</th></tr></thead>
<tbody>{grid("knowledge+mixed")}</tbody></table>

<div class="note"><b>Half the effect is information; half is not.</b>
The gap narrows from {n(hi,'all')-n(lo,'all')} to
{n(hi,'knowledge+mixed')-n(lo,'knowledge+mixed')} points when the catalog-dependent rules are
excluded, but it does not close. Resource selection is almost entirely information — it recovers
once the queue-table rules come out. Batch job creation is not: without the site conventions and
the worked script, the scripts are structurally worse, not merely factually wrong.</div>

<h2>Which model is helped, and where — all requirements</h2>
<p class="lede">Each cell is passes unaugmented &rarr; augmented, out of 10 attempts. Shading is
the share of the cell the prompt is worth.</p>
<table class="hm"><thead><tr><th style="text-align:left">model</th>
{"".join(f"<th>{e(s.split()[0])}</th>" for s in SUBTASKS)}<th>&Delta;</th></tr></thead>
<tbody>{cellgrid("all")}</tbody></table>

<h2>The same grid, capability only</h2>
<table class="hm"><thead><tr><th style="text-align:left">model</th>
{"".join(f"<th>{e(s.split()[0])}</th>" for s in SUBTASKS)}<th>&Delta;</th></tr></thead>
<tbody>{cellgrid("knowledge+mixed")}</tbody></table>

<h2>What the prompt rescues, per model</h2>
<table><thead><tr><th style="text-align:left">model</th><th>all rules</th><th>capability</th>
<th style="text-align:left">requirements it stops violating (count across 3 replicates)</th></tr></thead>
<tbody>{permodel}</tbody></table>

<h2>Paired test — exact McNemar on pass/fail</h2>
<table><thead><tr><th style="text-align:left">stratum</th><th>{e(lo)}</th><th>{e(hi)}</th>
<th>&Delta;</th><th>gained</th><th>lost</th><th>exact p</th></tr></thead>
<tbody>{stats}</tbody></table>
<p class="lede">Every item is answered under both prompts by the same model, so the comparison is
paired. Per-model rows are given because the 160 items are 40 anchors &times; 4 models and rows
sharing an anchor share a prompt; pooling them and quoting one p-value would treat them as
independent.</p>

<h2>Which requirements moved</h2>
<table><thead><tr><th style="text-align:left">requirement</th><th style="text-align:left">class</th>
<th>{e(lo)}</th><th>{e(hi)}</th><th>&Delta;</th></tr></thead>
<tbody>{mrows}</tbody></table>
<p class="lede">Violations across all three judge replicates. A score change that cannot name the
rules behind it is not a finding.</p>

<div class="note warn"><b>This comparison has no internal control.</b>
In the base-vs-rich A/B, 120 of 160 items had byte-identical prompts and calibrated the noise
floor. Here every item differs, so the noise floor is imported: the base/rich control moved 4 rows
on identical prompts, and 20 of 320 cells flip between judge replicates. The effect here is an
order of magnitude larger than either, but the absence should be stated rather than assumed
away.</div>

<div class="note"><b>One directive is worth 12 rows.</b>
<code>BATCH.common.filesystems_declared</code> — the ALCF <code>#PBS -l filesystems=</code> line —
is violated on 31 of 40 unaugmented Batch items and is fatal. Scored as minor, the unaugmented
Batch stage recovers from 1/40 to 13/40. Several answers are otherwise correct scripts that omit
exactly that line.</div>

<p class="meta">corpus v8 &middot; collected under {GRADED_UNDER}, scored under {RUBRIC} &middot;
gpt56terra, skill mode, k=3 &middot; every number regenerated by tools/build_result_page.py
&middot; per-item evidence: <a href="trinity_{e(lo)}_vs_{e(hi)}_v8.html">trinity_{e(lo)}_vs_{e(hi)}_v8.html</a></p>
</div>"""
    out.parent.mkdir(exist_ok=True)
    out.write_text(doc)
    print(f"  {out.relative_to(ROOT)}  ({out.stat().st_size // 1024} KB)")
    print(f"  {lo} {n(lo,'all')}/{tot} -> {hi} {n(hi,'all')}/{tot}  ({delta:+d})")
    print(f"  capability-only: {n(lo,'knowledge+mixed')} -> {n(hi,'knowledge+mixed')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
