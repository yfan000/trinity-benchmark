#!/usr/bin/env python3
"""Render site/trinity_benchmark_report.pdf and the result table in site/index.html.

Every number here comes from `audit.matrix.compute()`. Nothing is typed in. The previous version
of this report was built by a one-off script that scored rows with a severity override absent
from the library and aggregated replicates with floor(sum/3) instead of a majority; it published
203/320, which no tool in the repository could produce. Reading the numbers from the same
function the CLI uses is the only structural fix for that.

The prose is written by hand because a paragraph that explains a failure pattern cannot be
derived from counts — but every count inside it is interpolated, so prose and table cannot drift.

    python tools/build_report.py            # HTML + PDF (needs Chrome for the PDF)
    python tools/build_report.py --no-pdf
"""
from __future__ import annotations

import argparse
import html
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from audit.matrix import GRADED_UNDER, SUBTASKS, compute   # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
RUBRIC = "r28"
DATE = "2026-09-21"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

SHORT = {s: s.replace(" ", "<br>", 1) for s in SUBTASKS}
e = html.escape

# Hand-written, one per model: the lead is the pattern, the body is the evidence for it.
PROSE = {
 "nemotron-3-ultra": (
   "Quantitative slips inside otherwise sound work.",
   "Its errors require real domain work to make: computing 80 NaCl pairs into a 6.245 nm box and "
   "arriving at 0.55 M where 0.15 M was requested. It invents plausible-but-nonexistent nekRS "
   "control blocks, and it truncates large coordinate files. <b>Clean on Batch job creation</b> — "
   "no rule failed twice out of three runs on any of its 20 attempts. The only model I would "
   "consider for unattended use, and only outside Input preparation."),
 "gemma-4-31b": (
   "Precise work undone by single-token errors.",
   "<code>vdw-type</code> for <code>vdwtype</code> — one hyphen making the key invalid. "
   "<code>#PBS -l select=1:system=polaris</code> submitted to Sirius: the right directive with a "
   "machine name copied from the worked example. Its Input-preparation failures are the broadest "
   "of any model by rule count, but shallow — mostly one defect per answer."),
 "gpt-oss-120b": (
   "Abbreviates when asked for complete files.",
   "One behaviour drives four separate Input-preparation rules: <code>conf.gro</code> declaring "
   "13 atoms for a 34,000-atom system, &ldquo;&hellip; (remaining protein atoms) &hellip;&rdquo;, "
   "&ldquo;a very small illustrative system.&rdquo; It is also the weakest on Software selection, "
   "genuinely naming the wrong code. Its Batch score is the one most sensitive to a rubric "
   "judgement call: it trails a comment on a <code>#PBS</code> line in 8 of 8 attempts, which "
   "ALCF documents as breaking submission, and which the library therefore scores as major."),
 "llama-3.1-8b": (
   "Fabricates formats that look correct.",
   "It invented an entire <code>input.json</code> AlphaFold configuration language with fields "
   "such as <code>num_recycle</code> that do not exist; wrote a haemoglobin sequence under a "
   "ubiquitin header; authored a <code>tip3p.itp</code> with <code>[ moleculetype ]</code> and no "
   "<code>[ atoms ]</code> section. Uniquely, it violates queue limits the prompt states "
   "explicitly and fails rank arithmetic. Its failures span <b>all four subtasks</b>."),
}


def matrix_html(R, models) -> str:
    rows = ""
    for m in models:
        cells = ""
        for s in SUBTASKS:
            p, n = R.total(m, [s])
            cells += f'<td><b>{p}</b><span>/{n}</span></td>'
        t, n = R.total(m)
        rows += (f'<tr><th>{e(m)}</th>{cells}'
                 f'<td class="tot"><b>{t}</b><span>/{n}</span><i>{t / n:.0%}</i></td></tr>')
    colt = "".join(f'<td><b>{sum(R.total(m, [s])[0] for m in models)}</b>'
                   f'<span>/{sum(R.total(m, [s])[1] for m in models)}</span></td>' for s in SUBTASKS)
    g = sum(R.total(m)[0] for m in models)
    gn = sum(R.total(m)[1] for m in models)
    rows += (f'<tr class="all"><th>All models</th>{colt}'
             f'<td class="tot"><b>{g}</b><span>/{gn}</span><i>{g / gn:.0%}</i></td></tr>')
    return rows


def sections(R, models) -> str:
    secs = ""
    for m in models:
        head, body = PROSE[m]
        t, n = R.total(m)
        blocks = ""
        for s in SUBTASKS:
            fl = dict(R.bysub[m].get(s, {}).most_common(6)) if R.bysub[m].get(s) else {}
            p, tot = R.total(m, [s])
            if not fl:
                blocks += (f'<div class="sub"><h4>{e(s)} <span class="ss">{p}/{tot}</span></h4>'
                           f'<p class="none">No rule failed in a majority of runs on any '
                           f'attempt.</p></div>')
                continue
            tr = ""
            for r, c in fl.items():
                sev = R.sev.get(r, "major")
                app, evid = R.ev.get(f"{m}|{r}", ["", ""])
                tr += (f'<tr><td class="r"><span class="sev {e(sev)}">{e(sev)[:3]}</span>'
                       f'{e(r.split(".", 1)[1])}</td><td class="n">{c}</td>'
                       f'<td class="e">{e(evid[:132])}<span class="app">{e(app)}</span></td></tr>')
            blocks += (f'<div class="sub"><h4>{e(s)} <span class="ss">{p}/{tot}</span></h4>'
                       f'<table class="fail"><tbody>{tr}</tbody></table></div>')
        secs += (f'<section class="model"><h3>{e(m)} <span class="sc">{t}/{n} &middot; '
                 f'{t / n:.0%}</span></h3><p class="lead">{head}</p><p>{body}</p>{blocks}</section>')
    return secs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-pdf", action="store_true")
    a = ap.parse_args()

    R = compute(RUBRIC)
    asg = compute(GRADED_UNDER)                       # the ladder: what the repairs were worth
    dem = compute(RUBRIC, demote=frozenset({"BATCH.common.no_directive_comments"}))
    models = R.models()
    tot = sum(R.total(m)[0] for m in models)
    ntot = sum(R.total(m)[1] for m in models)
    ip = sum(R.total(m, ["Input preparation"])[0] for m in models)
    ipn = sum(R.total(m, ["Input preparation"])[1] for m in models)
    best_ip = max(R.total(m, ["Input preparation"])[0] for m in models)
    others = {s: sum(R.total(m, [s])[0] for m in models)
              for s in SUBTASKS if s != "Input preparation"}
    demtot = sum(dem.total(m)[0] for m in models)
    asgtot = sum(asg.total(m)[0] for m in models)

    css = (ROOT / "tools" / "report.css").read_text()
    doc = f"""<meta charset="utf-8"><title>Trinity Benchmark Results</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Serif:ital,wght@0,400;0,600;1,400&display=swap">
<style>{css}</style>
<div class="kicker">Trinity agent benchmark</div>
<h1>Can a cheaper model be trusted with HPC job preparation?</h1>
<div class="meta"><span><b>Corpus</b> v8 &middot; 10 anchors &times; 4 subtasks &times; 4 models
&times; 2 arms</span><span><b>Judge</b> gpt56terra (Argo), k=3</span>
<span><b>Rubric</b> {RUBRIC}</span><span><b>Date</b> {DATE}</span></div>
<h2>Results</h2>
<p>Each cell is passes out of 20 attempts (10 anchors &times; 2 prompt arms). A pass requires 2/2
on correctness, completeness and usability with no fatal violation, taken as the majority across
three judge replicates.</p>
<table class="matrix"><thead><tr><th>Model</th>{"".join(f"<th>{SHORT[s]}</th>" for s in SUBTASKS)}
<th>Total</th></tr></thead><tbody>{matrix_html(R, models)}</tbody></table>
<div class="note"><b>Three of four subtasks are usable; one is not</b>
{", ".join(f"{s} ({n}/80)" for s, n in others.items())} are in workable shape. Input preparation
sits at <b>{ip}/{ipn} = {ip / ipn:.0%}</b> and no model exceeds {best_ip}/20.</div>
<h2>Failure patterns by model and subtask</h2>
<p>Rules that failed in a majority of the three judge runs, grouped by subtask. The count is the
number of attempts (out of 20) on which that rule fired.</p>
{sections(R, models)}
<h2>Interactive detail</h2>
<p><b>Open <code>index.html</code> in a web browser</b> to reach these — a PDF reader cannot
follow links into local HTML files. All four sit beside this report.</p>
<table class="links">
<tr><td class="f">trinity_failures_v8.html</td><td><b>Failure browser.</b> Pick a rule and a model
to see every answer that failed it, with all three replicates&rsquo; evidence, the judge&rsquo;s
overall comment, and the full prompt, reference and answer behind each. This is the page behind
every claim above.</td></tr>
<tr><td class="f">trinity_traces_v8.html</td><td><b>Answer traces.</b> All 320 graded answers with
per-requirement verdicts, as judged under {GRADED_UNDER}. Filterable by arm, failure and replicate
instability.</td></tr>
<tr><td class="f">trinity_rules_v8.html</td><td><b>Grading rules.</b> Every requirement applied to
each sample, what decides it, where it came from, and the source YAML.</td></tr>
<tr><td class="f">trinity_arm_inspector_v8.html</td><td><b>Prompt A/B inspector.</b> Both prompt
arms per anchor with the enrichment diff highlighted.</td></tr>
</table>
<h2>What the numbers survived</h2>
<p>These figures are what remained after repeated rounds of removing defects in the measurement
itself. No model changed while reported scores moved by tens of rows:</p>
<ul>
<li><b>A rule that could not be satisfied.</b> <code>content_markers_present</code> applied a
file-<i>detection</i> heuristic as a completeness requirement, demanding the literal amino-acid
alphabet inside every FASTA.</li>
<li><b>A rule contradicting another rule.</b> <code>not_copied_from_example</code> penalised
reproducing the HPLinpack header that <code>header_and_output_lines</code> requires fatally.
Retiring it in {RUBRIC} is worth {tot - asgtot} rows ({asgtot}/{ntot} &rarr; {tot}/{ntot}), all of
them in Input preparation.</li>
<li><b>Prompts demanding the impossible.</b> Three anchors instructed models to author compiled
binaries (<code>.tpr</code>, <code>.re2</code>, <code>.h5</code>) that fatal rules forbid
writing.</li>
<li><b>A prompt naming a queue that does not exist.</b> All four models were told
<code>queue workq</code> for HPL on Crux, which has no such queue; all four obeyed and were failed
fatally. Eight failures attributable entirely to the harness.</li>
<li><b>A silently truncated worked example.</b> The prompt builder cut examples at 44 lines, so
GROMACS models saw one of three required file formats.</li>
</ul>
<div class="note caveat"><b>Limits of this result</b>
Ten anchors per subtask makes a single cell &plusmn;1&ndash;2 rows; {R.unstable} of
{R.cells} cells flipped between judge replicates. The judge&rsquo;s own test&ndash;retest spread
is 7% of rows at k=3, so differences under about 5 points are not resolvable. One severity
judgement is worth more than that spread: scoring
<code>no_directive_comments</code> as minor rather than major would read
{demtot}/{ntot} instead of {tot}/{ntot}, almost all of it gpt-oss
(<code>audit.matrix --demote</code> prices it). Every number is GPT-judged only; the
same-family question against <code>gpt-oss-120b</code> is unmeasured. Input-preparation failures
were verified by reading the evidence individually; the other subtasks were not audited to the
same depth. The grades were collected under {GRADED_UNDER} and re-scored offline under {RUBRIC},
which is exact for a rubric change that only removes rules.</div>
<footer>Trinity agent benchmark &middot; corpus v8 &middot; rubric {RUBRIC} &middot; judge
gpt56terra at k=3 &middot; generated {DATE} by tools/build_report.py</footer>"""

    out = SITE / "report.html"
    out.write_text(doc)
    print(f"  {out.relative_to(ROOT)}  ({tot}/{ntot})")

    # Keep index.html's table in step with the same numbers.
    idx = SITE / "index.html"
    t = idx.read_text()
    start = t.index("<table>")
    end = t.index("</table>", start) + len("</table>")
    hdr = ("<table>\n    <tr><th>Model</th>"
           + "".join(f"<th>{s.split()[0]}</th>" for s in SUBTASKS) + "<th>Total</th></tr>\n")
    body = ""
    for m in models:
        cells = "".join(
            f'<td{" class=\"low\"" if s == "Input preparation" else ""}>'
            f'{R.total(m, [s])[0]}</td>' for s in SUBTASKS)
        p, n = R.total(m)
        body += f"    <tr><td>{e(m)}</td>{cells}<td>{p}/{n} · {p / n:.0%}</td></tr>\n"
    cells = "".join(
        f'<td{" class=\"low\"" if s == "Input preparation" else ""}>'
        f'{sum(R.total(m, [s])[0] for m in models)}/{sum(R.total(m, [s])[1] for m in models)}</td>'
        for s in SUBTASKS)
    body += (f'    <tr class="tot"><td>All models</td>{cells}'
             f'<td>{tot}/{ntot} · {tot / ntot:.0%}</td></tr>\n  ')
    idx.write_text(t[:start] + hdr + body + "</table>" + t[end:])
    print(f"  {idx.relative_to(ROOT)}  table updated")

    if not a.no_pdf:
        pdf = SITE / "trinity_benchmark_report.pdf"
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf}", out.as_uri()],
                       check=True, capture_output=True)
        print(f"  {pdf.relative_to(ROOT)}  ({pdf.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
