#!/usr/bin/env python3
"""Phase 2a — produce the worksheet a human fills in to validate the taxonomy.

Writes three files:
  human_validation.csv  — the worksheet. Fill in `human_skills` with `|`-separated tag
                          names; leave `llm_skills` untouched.
  taxonomy_v1.md        — the cheat-sheet of valid tag names to label from. A typo'd tag
                          silently scores as a disagreement, so label from this list.
  validation_review.html — optional checkbox UI over the same rows; its export produces the
                          identical CSV format, so either route feeds compute_agreement.py.

Rows are grouped by benchmark so a reviewer can work through one domain at a time.

Usage:
    python skills/build_validation_worksheet.py --n 250
"""
from __future__ import annotations
import argparse
import csv
import html
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "results" / "skills"
LABELS_PATH = OUT_DIR / "labels_final.jsonl"
DISCOVERY_PATH = OUT_DIR / "discovery_results.jsonl"
SAMPLES_PATH = OUT_DIR / "samples.jsonl"
TAXONOMY_PATH = OUT_DIR / "taxonomy_v1.json"


def load_labeled() -> list[dict]:
    """Prefer final labels (fixed taxonomy); fall back to the discovery pass."""
    samples = {json.loads(l)["sample_id"]: json.loads(l) for l in SAMPLES_PATH.open()}
    if LABELS_PATH.exists():
        rows = [json.loads(l) for l in LABELS_PATH.open()]
        key = "fundamental_skills"
    else:
        rows = [json.loads(l) for l in DISCOVERY_PATH.open()]
        key = "proposed_skills"
    out = []
    for r in rows:
        s = samples.get(r["sample_id"])
        if s:
            out.append({**s, "llm_skills": r.get(key, [])})
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=250)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--blind", action="store_true",
                    help="hide the LLM's labels so the reviewer starts from nothing. Costs "
                         "more effort per item but is the only way to measure agreement "
                         "without anchoring the reviewer on what the classifier already said.")
    args = ap.parse_args()

    if not TAXONOMY_PATH.exists():
        print(f"missing {TAXONOMY_PATH} — lock the taxonomy from the discovery review first")
        return 1
    taxonomy = json.loads(TAXONOMY_PATH.read_text())

    rows = load_labeled()
    by_bench = defaultdict(list)
    for r in rows:
        by_bench[r["benchmark"]].append(r)

    if len(rows) <= args.n:
        # The labeled set is already the validation subset (label_full_corpus.py
        # --stratified) — take it whole rather than re-sampling it into a mismatch.
        picked = rows
    else:
        rng = random.Random(args.seed)
        per_bench = max(1, args.n // max(len(by_bench), 1))
        picked = []
        for bench in sorted(by_bench):
            pool = by_bench[bench]
            picked.extend(rng.sample(pool, min(per_bench, len(pool))))
    picked.sort(key=lambda r: (r["benchmark"], r["sample_id"]))

    csv_path = OUT_DIR / "human_validation.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["sample_id", "benchmark", "original_category", "question",
                    "llm_skills", "human_skills", "notes"])
        for r in picked:
            w.writerow([r["sample_id"], r["benchmark"], r["original_category"] or "",
                        r["question"][:1500], "|".join(r["llm_skills"]), "", ""])

    md_path = OUT_DIR / "taxonomy_v1.md"
    md_path.write_text(
        "# Fundamental skills — valid tag names\n\n"
        "Label `human_skills` using these names exactly, `|`-separated.\n\n"
        + "\n".join(f"- **{t['name']}** — {t['description']}" for t in taxonomy) + "\n")

    html_path = OUT_DIR / "validation_review.html"
    html_path.write_text(_render_html(picked, taxonomy, blind=args.blind))

    print(f"{len(picked)} rows across {len(by_bench)} benchmarks")
    print(f"  worksheet   {csv_path}")
    print(f"  cheat-sheet {md_path}")
    print(f"  review UI   {html_path}")
    return 0


def _render_html(rows: list[dict], taxonomy: list[dict], blind: bool = False) -> str:
    data = json.dumps([{"sample_id": r["sample_id"], "benchmark": r["benchmark"],
                        "original_category": r["original_category"] or "",
                        "question": r["question"][:4000],
                        # In blind mode the page never receives the LLM's labels, so they
                        # cannot anchor the reviewer. They are re-attached afterwards by
                        # compute_agreement.py reading labels_final.jsonl.
                        "llm_skills": [] if blind else r["llm_skills"]}
                       for r in rows])
    tags = json.dumps([t["name"] for t in taxonomy])
    descs = json.dumps({t["name"]: t["description"] for t in taxonomy})
    return (_HTML_TEMPLATE.replace("__DATA__", data).replace("__TAGS__", tags)
            .replace("__DESCS__", descs).replace("__BLIND__", "true" if blind else "false"))


_HTML_TEMPLATE = """<!doctype html>
<html><head><meta charset="utf-8"/>
<title>Skill taxonomy — human validation</title>
<style>
 :root { --bg:#faf9f7; --fg:#1c1b19; --muted:#6b6862; --line:#e2ded7; --card:#fff; --accent:#8a5a2b; }
 @media (prefers-color-scheme: dark) {
   :root { --bg:#161513; --fg:#eceae6; --muted:#9a958c; --line:#2e2c28; --card:#1e1d1a; --accent:#d9a066; } }
 * { box-sizing:border-box; }
 body { margin:0; background:var(--bg); color:var(--fg); font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }
 header { position:sticky; top:0; background:var(--bg); border-bottom:1px solid var(--line);
          padding:14px 24px; display:flex; gap:16px; align-items:center; flex-wrap:wrap; z-index:5; }
 h1 { font-size:17px; margin:0; font-weight:600; }
 .count { color:var(--muted); font-size:13px; }
 button { background:var(--accent); color:#fff; border:0; border-radius:6px; padding:8px 16px;
          font-size:14px; cursor:pointer; font-weight:500; }
 main { padding:24px; max-width:980px; margin:0 auto; display:flex; flex-direction:column; gap:18px; }
 .card { background:var(--card); border:1px solid var(--line); border-radius:10px; padding:18px; }
 .meta { color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.04em; margin-bottom:8px; }
 pre.q { white-space:pre-wrap; word-break:break-word; margin:0 0 14px; font:13px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;
         max-height:260px; overflow:auto; background:var(--bg); border:1px solid var(--line); border-radius:6px; padding:12px; }
 .tags { display:flex; flex-wrap:wrap; gap:6px; }
 label.tag { display:inline-flex; align-items:center; gap:5px; border:1px solid var(--line); border-radius:20px;
             padding:4px 11px; font-size:13px; cursor:pointer; user-select:none; }
 label.tag.on { background:var(--accent); color:#fff; border-color:var(--accent); }
 label.tag.llm { border-color:var(--accent); border-style:dashed; }
 .notes { width:100%; margin-top:10px; padding:7px 10px; font-size:13px; border:1px solid var(--line);
          border-radius:6px; background:var(--bg); color:var(--fg); }
</style></head><body>
<header>
 <h1>Skill taxonomy — human validation</h1>
 <span class="count" id="count"></span>
 <button onclick="exportCsv()">Export CSV</button>
 <span class="count" id="mode-note"></span>
</header>
<main id="main"></main>
<script>
const DATA = __DATA__, TAGS = __TAGS__, DESCS = __DESCS__, BLIND = __BLIND__;
document.getElementById('mode-note').textContent = BLIND
  ? "Blind mode: nothing is pre-selected. Tag each question from scratch."
  : "Dashed outline = what the LLM proposed. Click to set your own labels.";
const human = DATA.map(r => new Set(r.llm_skills));
const notes = DATA.map(() => "");
function updateCount() {
  document.getElementById('count').textContent = `${DATA.length} items`;
}
function render() {
  document.getElementById('main').innerHTML = DATA.map((r, i) => `
    <div class="card">
      <div class="meta">${r.sample_id} · ${r.benchmark}${r.original_category ? ' · ' + r.original_category : ''}</div>
      <pre class="q">${r.question.replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}</pre>
      <div class="tags">${TAGS.map(t => `
        <label class="tag ${human[i].has(t) ? 'on' : ''} ${r.llm_skills.includes(t) ? 'llm' : ''}"
               title="${DESCS[t].replace(/"/g, '&quot;')}">
          <input type="checkbox" ${human[i].has(t) ? 'checked' : ''}
                 onchange="toggle(${i}, this.checked, '${t.replace(/'/g, "\\\\'")}', this)"> ${t}
        </label>`).join('')}</div>
      <input class="notes" placeholder="notes (optional)" oninput="notes[${i}]=this.value">
    </div>`).join('');
  updateCount();
}
function toggle(i, on, tag, el) {
  on ? human[i].add(tag) : human[i].delete(tag);
  el.parentElement.classList.toggle('on', on);
}
function exportCsv() {
  const esc = v => `"${String(v).replace(/"/g, '""')}"`;
  const lines = [['sample_id','benchmark','original_category','question','llm_skills','human_skills','notes'].join(',')];
  DATA.forEach((r, i) => lines.push([r.sample_id, r.benchmark, r.original_category, r.question,
    r.llm_skills.join('|'), [...human[i]].join('|'), notes[i]].map(esc).join(',')));
  const url = URL.createObjectURL(new Blob([lines.join('\\n')], {type:'text/csv'}));
  const a = document.createElement('a');
  a.href = url; a.download = 'human_validation.csv'; a.click();
  URL.revokeObjectURL(url);
}
render();
</script></body></html>
"""


if __name__ == "__main__":
    sys.exit(main())
