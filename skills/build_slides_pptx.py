#!/usr/bin/env python3
"""Generate results/ALCF_skill_taxonomy.pptx — a 4-slide progress deck.

Hyperlinks point at the local dashboards via file:// URLs, so they open on this machine.
Sending the .pptx alone breaks them; send results/ alongside it, or host the HTML.

Usage:
    python skills/build_slides_pptx.py
"""
from __future__ import annotations
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu, Pt

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
OUT = RESULTS / "ALCF_skill_taxonomy.pptx"

INK, DIM, FAINT = RGBColor(0x12, 0x18, 0x1B), RGBColor(0x55, 0x63, 0x6B), RGBColor(0x8B, 0x97, 0x9B)
ACCENT, ACCENT_BG = RGBColor(0x0E, 0x7C, 0x86), RGBColor(0xD9, 0xEE, 0xEE)
WARN, WARN_BG = RGBColor(0xC1, 0x43, 0x2E), RGBColor(0xF7, 0xE4, 0xE0)
PANEL, LINE, WHITE = RGBColor(0xF2, 0xF4, 0xF3), RGBColor(0xD8, 0xDE, 0xDD), RGBColor(0xFF, 0xFF, 0xFF)
FONT, MONO = "Aptos", "Consolas"

W, H = Emu(12192000), Emu(6858000)          # 13.33 x 7.5 in, 16:9
M = Emu(640080)                              # 0.7 in margin


def inches(v):
    return Emu(int(v * 914400))


def textbox(slide, x, y, w, h):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    return tf


def para(tf, text="", size=14, color=DIM, bold=False, space_after=4, font=FONT,
         first=False, align=None, line=None):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.space_after = Pt(space_after)
    if align:
        p.alignment = align
    if line:
        p.line_spacing = line
    if text:
        r = p.add_run()
        r.text = text
        r.font.size, r.font.bold, r.font.name = Pt(size), bold, font
        r.font.color.rgb = color
    return p


def rich(p, parts, size=13, line=1.25):
    """parts = [(text, color, bold, font|None), ...]"""
    p.line_spacing = line
    for text, color, bold, *rest in parts:
        r = p.add_run()
        r.text = text
        r.font.size, r.font.bold = Pt(size), bold
        r.font.name = rest[0] if rest else FONT
        r.font.color.rgb = color


def box(slide, x, y, w, h, fill, line_color=None):
    from pptx.enum.shapes import MSO_SHAPE
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    sh.adjustments[0] = 0.06
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    if line_color:
        sh.line.color.rgb = line_color
        sh.line.width = Pt(0.75)
    else:
        sh.line.fill.background()
    sh.shadow.inherit = False
    sh.text_frame.word_wrap = True
    return sh


def blank(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.background.fill
    bg.solid()
    bg.fore_color.rgb = WHITE
    return s


def eyebrow(slide, text):
    sh = box(slide, M, inches(0.42), inches(3.1), inches(0.3), ACCENT_BG)
    tf = sh.text_frame
    tf.margin_left = tf.margin_right = Emu(91440)
    para(tf, text.upper(), 10, ACCENT, True, 0, first=True)
    return sh


def title(slide, text, y=0.84, size=30):
    tf = textbox(slide, M, inches(y), W - 2 * M, inches(0.9))
    para(tf, text, size, INK, True, 0, first=True, line=1.05)


def deck(slide, text, y=1.62, w=None, size=13):
    tf = textbox(slide, M, inches(y), w or (W - 2 * M - inches(0.4)), inches(0.8))
    para(tf, text, size, DIM, False, 0, first=True, line=1.3)


def footer(slide, left, page):
    tf = textbox(slide, M, H - inches(0.52), W - 2 * M, inches(0.28))
    p = para(tf, "", 9.5, FAINT, False, 0, first=True)
    r = p.add_run(); r.text = left
    r.font.size, r.font.name, r.font.color.rgb = Pt(9.5), FONT, FAINT
    r2 = p.add_run(); r2.text = "        " + page
    r2.font.size, r2.font.name, r2.font.bold, r2.font.color.rgb = Pt(9.5), MONO, True, FAINT


def link_bar(slide, y, label, filename, note):
    """A hyperlink chip pointing at a local dashboard.

    The link is attached twice on purpose: to the shape (so the whole box is a click
    target, not just the small text run) and to the text run itself. PowerPoint only
    activates hyperlinks in slideshow mode, so the full path is also printed as selectable
    text — that stays usable when the deck is read in edit mode or the file:// link is
    blocked by sandboxing.
    """
    url = (RESULTS / filename).as_uri()
    sh = box(slide, M, inches(y), W - 2 * M, inches(0.78), PANEL, LINE)
    sh.click_action.hyperlink.address = url          # whole box clickable
    tf = sh.text_frame
    tf.margin_left = tf.margin_right = inches(0.16)
    tf.margin_top = inches(0.08)
    p = tf.paragraphs[0]
    p.line_spacing = 1.12
    r = p.add_run(); r.text = label
    r.font.size, r.font.bold, r.font.name = Pt(12.5), True, FONT
    r.font.color.rgb = ACCENT
    r.hyperlink.address = url                        # text also clickable
    r2 = p.add_run(); r2.text = "   " + note
    r2.font.size, r2.font.name, r2.font.color.rgb = Pt(10), FONT, DIM
    p2 = tf.add_paragraph()
    p2.space_before = Pt(3)
    r3 = p2.add_run(); r3.text = str(RESULTS / filename)
    r3.font.size, r3.font.name, r3.font.color.rgb = Pt(9), MONO, FAINT
    return sh


def stat_row(slide, y, stats, cols=None):
    cols = cols or len(stats)
    gap = inches(0.16)
    total = W - 2 * M
    w = Emu(int((total - gap * (cols - 1)) / cols))
    for i, (val, lab) in enumerate(stats):
        x = M + Emu(int(i * (w + gap)))
        sh = box(slide, x, inches(y), w, inches(0.78), PANEL, LINE)
        tf = sh.text_frame
        tf.margin_left = inches(0.14); tf.margin_top = inches(0.1)
        para(tf, val, 20, INK, True, 0, font=MONO, first=True)
        para(tf, lab.upper(), 8.5, FAINT, True, 0)


def bullets(slide, x, y, w, items, size=12, gap=7, h=2.1):
    tf = textbox(slide, x, inches(y), w, inches(h))
    for i, parts in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap)
        r = p.add_run(); r.text = "•  "
        r.font.size, r.font.color.rgb, r.font.name = Pt(size), ACCENT, FONT
        rich(p, parts, size=size, line=1.22)


def heading(slide, x, y, text, w=None):
    tf = textbox(slide, x, inches(y), w or inches(5.0), inches(0.26))
    para(tf, text.upper(), 9.5, FAINT, True, 0, first=True)


# ─────────────────────────────────────────────────────────────────────────────
BENCH_GROUPS = [
    ("Knowledge & science MCQ", "MMLU 200 · MMLU-Pro 100 · GPQA-Diamond 100 · GPQA-Main 100 · ARC 100 · HLE 100"),
    ("Mathematics", "GSM8K 100 · GSM1K 100 · MATH 100 · AIME 2024 30 · OlympiadBench 50"),
    ("Code generation", "HumanEval 164 · BigCodeBench 50"),
    ("Instruction & format following", "IFEval 100 · InfoBench 2,250 · FollowBench 409"),
    ("Commonsense & truthfulness", "HellaSwag 100 · WinoGrande 100 · TruthfulQA 100"),
    ("Long-context & fact-seeking", "LongBench-v2 21 · SealQA 365"),
    ("Reasoning & dialogue", "BBH 135 · CLUTRR-regen 100 · MT-Bench 80"),
]


def slide1(prs):
    s = blank(prs)
    eyebrow(s, "Project goal")
    title(s, "Which LLM should Trinity call — at what quality, at what cost?", size=27)
    tf = textbox(s, M, inches(1.66), W - 2 * M - inches(0.4), inches(0.72))
    para(tf, "Trinity agents will make LLM calls continuously, so the model choice is a standing "
             "quality-versus-cost decision. Benchmark leaderboards answer neither question well: "
             "they score whole benchmarks rather than the skills an agent call actually needs, and "
             "they ignore cost entirely. This project measures both sides on the same 17 models.",
         12.5, DIM, False, 0, first=True, line=1.3)

    heading(s, M, 2.58, "Two questions, measured separately")
    bullets(s, M, 2.88, inches(6.15), h=2.0, items=[
        [("Quality — for the skills agent calls need. ", INK, True),
         ("Every benchmark question relabelled by the underlying skill it exercises, so 17 models "
          "can be compared on one axis instead of 24 incomparable scoreboards.", DIM, False)],
        [("Cost — tokens now, dollars and GPU-hours next. ", INK, True),
         ("Output tokens per answer are measured for all 17. On-prem models on Sophia and Minerva "
          "carry no per-token charge at all, which is the larger cost lever.", DIM, False)],
    ], size=12, gap=9)

    heading(s, M, 4.98, "Where the frontier sits today")
    rows = [("Model", "Quality", "Tokens", "Hosting", True),
            ("claudeopus48", "77.7", "298", "commercial API", False),
            ("gpt56terra", "74.4", "416", "commercial API", False),
            ("gemma-4-31B", "63.0", "123", "ALCF on-prem", False),
            ("gpt-oss-120b", "62.7", "470", "ALCF on-prem", False)]
    y = 5.28
    for name, q, t, host, is_head in rows:
        tf = textbox(s, M, inches(y), inches(6.15), inches(0.26))
        p = tf.paragraphs[0]
        sz = 9.5 if is_head else 11.5
        col = FAINT if is_head else INK
        r = p.add_run(); r.text = name.ljust(17)
        r.font.size, r.font.bold, r.font.name, r.font.color.rgb = Pt(sz), is_head, FONT, col
        for val, cw in ((q, 9), (t, 9)):
            rv = p.add_run(); rv.text = val.rjust(cw)
            rv.font.size, rv.font.name, rv.font.bold = Pt(sz), MONO, False
            rv.font.color.rgb = FAINT if is_head else DIM
        rh = p.add_run(); rh.text = "   " + host
        rh.font.size, rh.font.name = Pt(sz), FONT
        rh.font.color.rgb = FAINT if is_head else (ACCENT if "on-prem" in host else DIM)
        y += 0.3 if is_head else 0.32

    sh = box(s, M + inches(6.62), inches(2.88), inches(4.62), inches(2.62), ACCENT_BG)
    tfb = sh.text_frame
    tfb.margin_left = tfb.margin_right = inches(0.17); tfb.margin_top = inches(0.14)
    para(tfb, "EMERGING ANSWER", 9.5, ACCENT, True, 6, first=True)
    p = tfb.add_paragraph(); p.space_after = Pt(7)
    rich(p, [("gemma-4-31B", INK, True, MONO),
             (" reaches 81% of the best commercial model's quality on 41% of its output tokens — "
              "and runs on ALCF hardware, so those tokens are free.", DIM, False)], size=11.5, line=1.25)
    p = tfb.add_paragraph()
    rich(p, [("It also beats every commercial model at instruction-following", INK, True),
             (" (76.9%), which the HPC mapping shows is required by ", DIM, False),
             ("98%", ACCENT, True, MONO),
             (" of agent-style tasks — the single most-demanded skill for an agent that acts "
              "rather than advises.", DIM, False)], size=11.5, line=1.25)

    sh2 = box(s, M + inches(6.62), inches(5.62), inches(4.62), inches(0.84), WARN_BG)
    tf2 = sh2.text_frame
    tf2.margin_left = tf2.margin_right = inches(0.17); tf2.margin_top = inches(0.1)
    p = tf2.paragraphs[0]
    rich(p, [("Not yet costed. ", INK, True),
             ("Tokens are a proxy; dollars-per-call and GPU-hours are not measured, and "
              "readiness for agent tasks is projected, not observed.", DIM, False)], size=10, line=1.2)

    footer(s, "Quality = mean over 24 benchmarks  ·  Tokens = mean output tokens per answer", "1 / 4")


def slide2(prs):
    s = blank(prs)
    eyebrow(s, "Benchmarks used")
    title(s, "24 public benchmarks, seven capability groups", size=28)
    tf = textbox(s, M, inches(1.62), W - 2 * M - inches(0.4), inches(0.56))
    para(tf, "Every benchmark runs against all 17 models at full scale — 6 open-weight on Sophia, "
             "2 on Minerva, 9 commercial via Argo. Counts below are questions per benchmark.",
         12.5, DIM, False, 0, first=True, line=1.3)

    y = 2.30
    for name, items in BENCH_GROUPS:
        sh = box(s, M, inches(y), W - 2 * M, inches(0.46), PANEL, LINE)
        tf = sh.text_frame
        tf.margin_left = inches(0.16); tf.margin_top = inches(0.1)
        p = tf.paragraphs[0]
        rich(p, [(f"{name}   ", INK, True), (items, DIM, False, MONO)], size=11)
        y += 0.50

    tf = textbox(s, M, inches(y + 0.02), W - 2 * M, inches(0.38))
    para(tf, "Also run as small pilots, not at full scale and excluded from the analysis: "
             "LAB-Bench (24) and MatSciBench (20). SWE-bench Verified was run but withdrawn — "
             "its 20,000-character file limit skipped most instances.",
         10, FAINT, False, 0, first=True, line=1.25)

    link_bar(s, y + 0.44, "▶  Open the per-benchmark dashboard", "category_breakdown.html",
             "23 tabs — each benchmark by its own topic and difficulty categories.")

    footer(s, "Full scores in BENCHMARK_REPORT.pdf, Table 1", "2 / 4")


def slide3(prs):
    s = blank(prs)
    eyebrow(s, "Phase 1 · complete")
    title(s, "Every question relabelled by the skill it requires", size=28)
    tf = textbox(s, M, inches(1.62), W - 2 * M - inches(0.4), inches(0.78))
    para(tf, "How the labelling works: each question is shown to an LLM classifier "
             "(claude-sonnet-4-6, temperature 0) together with all 29 skill definitions, and it "
             "returns every skill that question requires — multi-label, since most questions need "
             "several. The taxonomy itself was derived from the benchmarks' own category "
             "vocabularies, then refined on a 388-question discovery pass, not imposed up front.",
         12, DIM, False, 0, first=True, line=1.28)

    stat_row(s, 2.62, [("3,604", "Questions"), ("29", "Skills"), ("17", "Models"),
                       ("135,796", "Observations"), ("21/21", "Validity checks")])

    heading(s, M, 3.62, "What it revealed")
    bullets(s, M, 3.88, inches(7.0), h=2.0, items=[
        [("The open/closed gap is a reasoning gap. ", INK, True),
         ("Best commercial leads best ALCF-hosted by ", DIM, False),
         ("13.2", ACCENT, True, MONO), (" points on reasoning — and ", DIM, False),
         ("0.3", ACCENT, True, MONO), (" on style and format. A ", DIM, False),
         ("49×", ACCENT, True, MONO), (" difference.", DIM, False)],
        [("gemma-4-31B beats every commercial model at instruction-following ", INK, True),
         ("— 76.9% vs claudeopus48's 75.6%, over 891 questions.", DIM, False)],
        [("Temporal reasoning defeats everyone ", INK, True),
         ("— best score 47.9%, the only well-populated skill where no model clears half.", DIM, False)],
    ], size=12)

    heading(s, M + inches(7.4), 3.62, "Validation", w=inches(3.9))
    tf = textbox(s, M + inches(7.4), inches(3.88), inches(3.9), inches(1.24))
    for i, (k, v) in enumerate([("Construct validity", "21/21"), ("Self-consistency", "0.974"),
                                ("Human agreement", "0.893"), ("Per-tag precision", "1.00")]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(5)
        rich(p, [(f"{k}   ", DIM, False), (v, INK, True, MONO)], size=11.5)

    sh = box(s, M + inches(7.4), inches(5.22), inches(3.9), inches(0.74), WARN_BG)
    tfb = sh.text_frame
    tfb.margin_left = tfb.margin_right = inches(0.13); tfb.margin_top = inches(0.08)
    p = tfb.paragraphs[0]
    rich(p, [("0.893 is an upper bound. ", INK, True),
             ("The review page pre-checked the classifier's labels, so it partly measures "
              "whether the reviewer objected.", DIM, False)], size=9.5, line=1.18)

    link_bar(s, 6.08, "▶  Open the skill matrix", "skill_overview.html",
             "29 skills × 17 models, all benchmarks pooled.")
    footer(s, "skill_overview.html · skill_breakdown.html", "3 / 4")


def slide4(prs):
    s = blank(prs)
    eyebrow(s, "Phase 2 · in progress")
    title(s, "Mapping those skills onto real HPC tasks", size=28)
    tf = textbox(s, M, inches(1.62), W - 2 * M - inches(0.4), inches(0.72))
    para(tf, "592 realistic ALCF task instances across six operational tasks, generated from 25 "
             "pages of Argonne's documentation and labelled with the same classifier. Each cell "
             "is the share of that task's instances requiring that skill — counted from the "
             "labels, not asserted.", 12.5, DIM, False, 0, first=True, line=1.3)

    # skill rows x task columns, matching the dashboard's orientation
    cols = ["Failure\ndiag.", "Job\nmonitor", "Job\nsubmit", "Perf.\nanalysis",
            "Resource\nselect", "Workflow\nmgmt"]
    rows = [
        ("Expert domain knowledge", ["82%", "62%", "91%", "91%", "93%", "82%"], False),
        ("Factual recall",          ["73%", "78%", "72%", "73%", "73%", "40%"], False),
        ("Diagnosis",               ["89%", "42%", "61%", "53%", "31%", "49%"], True),
        ("Instruction/format following", ["44%", "42%", "39%", "44%", "44%", "44%"], False),
        ("Code generation",         ["34%", "33%", "33%", "36%", "38%", "60%"], False),
        ("Causal reasoning",        ["45%", "27%", "20%", "51%", "24%", "22%"], False),
    ]
    heading(s, M, 2.56, "Fundamental skill  ×  HPC task   ·   n = 62 / 45 / 54 / 45 / 45 / 45")

    # column headers, two lines each
    x0, colw = M + inches(2.60), inches(0.72)
    for i, c in enumerate(cols):
        tfh = textbox(s, x0 + Emu(int(i * colw)), inches(2.84), colw, inches(0.44))
        for j, line in enumerate(c.split("\n")):
            para(tfh, line, 9, FAINT, True, 0, first=(j == 0), align=PP_ALIGN.CENTER)

    y = 3.30
    for name, vals, unmeasured in rows:
        tfr = textbox(s, M, inches(y), inches(2.55), inches(0.26))
        p = tfr.paragraphs[0]
        r = p.add_run(); r.text = name
        r.font.size, r.font.name = Pt(11), FONT
        r.font.color.rgb = WARN if unmeasured else INK
        r.font.bold = unmeasured
        for i, v in enumerate(vals):
            tfc = textbox(s, x0 + Emu(int(i * colw)), inches(y), colw, inches(0.26))
            para(tfc, v, 10.5, INK if int(v[:-1]) >= 60 else DIM, int(v[:-1]) >= 60, 0,
                 font=MONO, first=True, align=PP_ALIGN.CENTER)
        y += 0.31

    sh = box(s, M, inches(y + 0.12), inches(6.85), inches(0.82), ACCENT_BG)
    tfb = sh.text_frame
    tfb.margin_left = tfb.margin_right = inches(0.15); tfb.margin_top = inches(0.1)
    p = tfb.paragraphs[0]
    rich(p, [("Diagnosis is the gap. ", INK, True),
             ("The only skill required by all six tasks — 89% of failure-diagnosis instances — "
              "and our corpus contains just 26 questions that exercise it. That row is the "
              "specification for the benchmark to build next.", DIM, False)], size=10.5, line=1.22)

    heading(s, M + inches(7.15), 2.56, "Still open", w=inches(4.6))
    bullets(s, M + inches(7.15), 2.84, inches(4.6), h=3.1, items=[
        [("Instances are synthetic ", INK, True),
         ("— documentation-grounded, but real ALCF tickets would be better evidence.", DIM, False)],
        [("One model wrote and labelled them, ", INK, True),
         ("so their agreement is not fully independent.", DIM, False)],
        [("Task categories are soft. ", INK, True),
         ("A blind re-check agreed 79% overall, only 33% for Job submission.", DIM, False)],
        [("Next: ", INK, True),
         ("blind human validation (~60 instances), then fold into the report.", DIM, False)],
    ], size=11, gap=8)

    link_bar(s, 6.18, "▶  Open the HPC skill map", "hpc_mapping.html",
             "20 skills × 6 tasks, plus projected readiness and its coverage gate.")
    footer(s, "Mapping built · validation pending", "4 / 4")


def main() -> int:
    prs = Presentation()
    prs.slide_width, prs.slide_height = W, H
    for fn in (slide1, slide2, slide3, slide4):
        fn(prs)
    prs.save(OUT)
    print(f"{len(prs.slides.__iter__.__self__._sldIdLst)} slides -> {OUT}")
    print("Hyperlinks use file:// paths into results/ — they resolve on this machine only.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
