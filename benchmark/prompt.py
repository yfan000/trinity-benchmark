"""Generate one Trinity benchmark sample: the prompt a model sees, plus a reference answer.

Extracted from the parent repo's `judge.py`, which was 863 lines serving five unrelated
benchmarks (HLE, InfoBench, FollowBench, skills discovery, HPC task generation). Only the
Trinity half came across.

Deliberately NOT carried over: `judge_trinity` and `_TRINITY_JUDGE_PROMPT`, the original
grading path. `judge/grade.py` replaced it, and the original still serialised the grading key
with `json.dumps(key)[:3000]` — a blind tail cut that always landed on the reference answer,
because the reference sorted last. Measured on v6: 16 of 40 samples lost part of their
reference, as little as 43% retained. Shipping it would invite someone to call it.
"""
from __future__ import annotations
import json
import os
import re

import anthropic

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_HELPER", "huihuo.zheng")
        base_url = os.getenv("ANTHROPIC_BASE_URL")
        # No explicit timeout previously — the SDK's default can hang far longer than any
        # single judge call should ever take, silently stalling the whole benchmark run.
        kwargs: dict = {"api_key": api_key, "timeout": 60.0, "max_retries": 1}
        if base_url:
            kwargs["base_url"] = base_url
        _client = anthropic.Anthropic(**kwargs)
    return _client


JUDGE_MODEL = "claude-sonnet-4-6"


def _text_of(msg) -> str:
    """First text block of a response.

    Reasoning models put a ThinkingBlock at content[0], which has no `.text` — indexing
    blindly raises AttributeError and every grade comes back zero.
    """
    for block in msg.content:
        t = getattr(block, "text", None)
        if t:
            return t
    return ""


def _last_json_object(text: str) -> dict | None:
    """Parse the LAST flat JSON object in `text`.

    The classifier sometimes second-guesses itself and emits two objects
    ("...} Wait, let me reconsider. {..."). A greedy r'\\{.*\\}' spans both and fails to
    parse, silently dropping the item — so match each object individually and prefer the
    model's final answer.
    """
    for candidate in reversed(re.findall(r'\{[^{}]*\}', text, re.DOTALL)):
        try:
            parsed = json.loads(candidate)
        except Exception:
            continue
        if isinstance(parsed, dict):
            return parsed
    return None


_TRINITY_PROMPT = """\
You are writing one sample for a benchmark that evaluates HPC *agents* — agents that carry
out real work on a supercomputer for a scientist.

Each sample is a self-contained subtask handed to an agent in isolation. It never sees any
prior conversation, so the sample must carry everything needed to attempt the work.

  Subtask:   {subtask} — {goal}
  Domain:    {domain}
  System:    {system}
  Variation: {variation}

--- TARGET SYSTEM CONFIGURATION (real, from the facility catalog) ---
{system_cfg}
--- APPLICATIONS INSTALLED ON THIS SYSTEM ---
{app_list}
--- THE CORRECT APPLICATION FOR THIS WORKLOAD, AND ITS CATALOG ENTRY ---
{app_cfg}
--- END ---

THE RULE THAT MATTERS MOST: state the task explicitly, but never reveal the answer.
This subtask tests whether the agent can determine {withhold}. If the prompt contains that,
the sample tests nothing. Indirect giveaways count too:
  - never name the application, or a file format/extension that identifies it
  - never give numbers the agent must derive (nodes, ranks, walltime) when those are tested
  - never quote module lines or the launch command when those are tested
  - describe artefacts by what they hold, not by which tool wrote them
{prior}{extra}

Write the sample as exactly four labelled sections. Keep it LEAN — these subtasks are meant
to be solvable by small, cheap models, and every extra sentence is cost paid on every call
and one more place for the answer to hide.

  Task:         one sentence naming what must be done.
  Workload:     the minimum an agent needs, as compact labelled facts, not prose. Aim for
                4-6 short lines, under 400 characters. Include only:
                  - the scientific problem, stated EXACTLY as specified here so the output
                    can be checked against it:{phys}
                    Reproduce those numbers and names faithfully — they are the grading key.
                    A vague problem ("a molecular dynamics benchmark") makes the sample
                    ungradeable.
                  - the target system, named
                  - the working directory, exactly: {workdir}
                  - any prior measurement that genuinely constrains the answer
                EXCLUDE, deliberately:
                  - THE ACCOUNT OR PROJECT ALLOCATION. Never state it. Determining that a
                    charge account is required, and how to supply it, is part of what the
                    Batch job creation subtask tests. Do not invent one either.
                  - queue limits, node counts per system, GPUs per node, walltime ceilings.
                    The agent is expected to know or look up the target system's policy;
                    stating it here removes the capability being tested.
                  - narrative about teams, deadlines, frustration or backstory
                  - filler lines that carry no information ("Prior context: none")
                  - any sentence that concludes something the agent should conclude
                    ("a single node is sufficient", "the debug queue is the right choice")
{mach_block}{def_block}{cat_block}{inp_block}{contract_block}{sysctx_block}{setup_block}{conv_block}  Instructions: {instructions}
  Output:       {output}

This system's scheduler is {sched}. Use that scheduler's directives and launcher —
never the other one's. (ALCF runs PBS Pro; OLCF and NERSC run Slurm.){sched_line}

Then give the reference answer, which is graded against the catalog entry above and must
agree with it — the real module lines, run command, input types, queue and defaults.

Before responding, check the prompt contains ALL FOUR labelled sections in order — Task,
Workload, Instructions, Output — plus any supplied blocks. Dropping the Output section is
the most common mistake when supplied blocks are present; the sample is invalid without it.

Respond with ONLY a JSON object:
{{"prompt": "<the four-section sample>", "reference": "<the reference answer>"}}"""


def generate_trinity_sample(subtask: str, goal: str, domain: str, system: str,
                            variation: str, instructions: str, output: str, withhold: str,
                            system_cfg: str, app_list: str, app_cfg: str,
                            prior: str = "", retry_terms: list[str] | None = None,
                            sched: str = "PBS Pro", workdir: str = "",
                            phys: str = "", mach: str = "",
                            gives_sched: bool = False,
                            show_catalog: bool = False, input_spec: str = "",
                            app_setup: str = "", build_defaults: str = "",
                            conventions: str = "",
                            example: str = "", example_kind: str = "script",
                            account: str = "", format_contract: str = "",
                            system_context: str = "", input_scaling: str = "") -> dict:
    """Generate one Trinity agent-benchmark sample, grounded in the real facility catalog.

    `app_cfg` is the catalog entry for the correct application. It is shown to the generator
    so the reference answer matches reality, and kept out of the prompt by the leak rule.
    `prior` carries earlier pipeline stages' outputs for subtasks that need them — Resource
    selection may name the chosen application, because choosing it was the previous
    subtask's job, not this one's.

    Returns {"prompt": str, "reference": str}; empty strings on failure.
    """
    extra = ""
    if retry_terms:
        extra = ("\nA previous attempt leaked these exact terms. They must not appear "
                 "anywhere in the prompt: " + ", ".join(retry_terms))
    mach_block = ""
    if mach:
        indented = "\n".join("                  " + ln for ln in mach.splitlines())
        mach_block = (
            "  Target system: reproduce this machine specification verbatim as its own\n"
            "                labelled section, so the agent has the hardware and queue limits\n"
            "                it needs and is judged on the allocation it chooses, not on\n"
            "                recalling the machine:\n" + indented + "\n")
    def_block = ""
    if build_defaults:
        lines = "\n".join("                  " + ln for ln in build_defaults.splitlines())
        def_block = (
            "  Build defaults: reproduce verbatim as its own labelled section. The subtask's\n"
            "                own instructions tell the agent to take ranks-per-node and\n"
            "                GPUs-per-rank from these, so withholding them asks it to obey a\n"
            "                rule against a number it was never given — which is exactly what\n"
            "                one model did, inventing 'one MPI rank per GPU' and calling it\n"
            "                standard build behaviour when the recorded default was 8:\n"
            + lines + "\n")
    cat_block = ""
    if show_catalog:
        listing = "\n".join("                  " + ln for ln in app_list.splitlines())
        cat_block = ("  Installed software: reproduce this catalog verbatim as its own labelled\n"
                     "                section. The agent has no tools and cannot look it up, so\n"
                     "                withholding it would test recall of what ALCF installed\n"
                     "                rather than the ability to match a workload to it:\n"
                     + listing + "\n")
    inp_block = ""
    if input_spec:
        inp_block = ("  Required input files: reproduce verbatim as its own labelled section.\n"
                     "                This is the file INVENTORY only — never state what goes\n"
                     "                inside them, which is what the subtask tests:\n"
                     f"                  {input_spec}\n")
    # RICH-arm blocks. The contract states what must appear INSIDE each file; the values stay
    # the test. Deliberately NOT built from input_detection.content_markers — that field is a
    # file-TYPE heuristic and supplying it would instruct the model to write the amino-acid
    # alphabet into a FASTA. See judge/skills/format_contracts.yaml.
    contract_block = ""
    if format_contract:
        lines = "\n".join("                  " + ln for ln in format_contract.splitlines())
        contract_block = ("  Input format contract: reproduce verbatim as its own labelled\n"
                          "                section. This is the FORMAT each file must take —\n"
                          "                which sections must appear inside it. It does NOT\n"
                          "                give the values, which are what the subtask tests:\n"
                          + lines + "\n")
    sysctx_block = ""
    if system_context or input_scaling:
        body = "\n".join(x for x in (system_context, input_scaling) if x)
        lines = "\n".join("                  " + ln for ln in body.splitlines())
        sysctx_block = ("  System context: reproduce verbatim as its own labelled section.\n"
                        "                Hardware and sizing guidance the agent cannot discover\n"
                        "                without tools. HPL cannot size N without the memory\n"
                        "                figure; withholding it made the deck unanswerable:\n"
                        + lines + "\n")
    setup_block = ""
    if app_setup:
        lines = "\n".join("                  " + ln for ln in app_setup.splitlines())
        setup_block = ("  Software environment: reproduce verbatim as its own labelled section.\n"
                       "                The agent has no tools and cannot discover the site's\n"
                       "                module stack; withholding it tests recall rather than\n"
                       "                the ability to assemble a correct script:\n"
                       + lines + "\n")
    conv_block = ""
    if conventions:
        conv = "\n".join("                  " + ln for ln in conventions.splitlines())
        conv_block = ("  Scheduler conventions: reproduce verbatim as its own labelled section.\n"
                      "                These are site rules the agent cannot discover without\n"
                      "                tools; the subtask is assembling a correct script, not\n"
                      "                recalling them:\n" + conv + "\n")
    # The worked example stands on its own: Input preparation supplies a real input deck with
    # no conventions block alongside it.
    if example:
        # Budget PER FILE, not across the whole example, and say so when it clips.
        #
        # This was `example.splitlines()[:44]` — a blind tail-cut. A multi-file example is 100+
        # lines, so the cut silently dropped every file after the first: GROMACS must write
        # .mdp, .gro and .top, and the prompt showed only the .mdp while the rubric still
        # required all three. nekRS lost the body of its .udf the same way. Exactly the defect
        # the catalog renderer was rewritten to remove, in a second place.
        _blocks, _cur = [], []
        for _ln in example.splitlines():
            if _ln.startswith("# ===== ") and _cur:
                _blocks.append(_cur)
                _cur = []
            _cur.append(_ln)
        _blocks.append(_cur)
        _per = 44 if len(_blocks) == 1 else 40
        _out = []
        for _b in _blocks:
            if len(_b) > _per:
                _b = _b[:_per] + [f"[... {len(_b) - _per} more lines of this file omitted —"
                                  f" the form above is what matters]"]
            _out += _b
        ex = "\n".join("                  " + ln for ln in _out)
        what = ("a script for a DIFFERENT application whose resources"
                if example_kind == "script" else
                "a real input deck for a DIFFERENT physical system, taken from the\n"
                "                application's own repository, whose values, species and\n"
                "                comment header")
        conv_block += ("  Worked example: include verbatim as a labelled section, clearly\n"
                       f"                marked as {what} must NOT be\n"
                       "                copied — it demonstrates the required form only:\n"
                       + ex + "\n")
    if account:
        conv_block += (f"  Account: state in the Workload that the project allocation to charge\n"
                       f"                is `{account}`. Withholding it forces a placeholder into\n"
                       f"                an otherwise correct script, which is not what this\n"
                       f"                subtask measures.\n")
    p = _TRINITY_PROMPT.format(
        subtask=subtask, goal=goal, domain=domain, system=system, variation=variation,
        instructions=instructions, output=output, withhold=withhold,
        # No clip here: benchmark.catalog.render_* already emits labelled sections with per-section
        # budgets and an explicit "[... clipped, N chars omitted]" marker where it trims. A blind
        # tail-cut at this point is what silently removed `hardware` and `job_defaults` from the
        # generator's view on 6 of 9 systems.
        system_cfg=system_cfg, app_list=app_list, app_cfg=app_cfg,
        prior=prior, extra=extra, sched=sched, workdir=workdir, mach_block=mach_block,
        def_block=def_block, cat_block=cat_block, inp_block=inp_block, setup_block=setup_block,
        contract_block=contract_block, sysctx_block=sysctx_block,
        conv_block=conv_block,
        sched_line=("\nState plainly in the Workload that this system uses " + sched +
                    ", so the agent is judged on the script it writes rather than on "
                    "recalling which scheduler the facility runs." if gives_sched else ""),
        phys=(f"\n                      {phys}" if phys else " the scale that drives the answer"))
    try:
        # 9000: an Input-preparation reference can be a complete multi-file input deck
        # (nekRS needs .par + .re2 + .udf + .oudf), which truncated mid-JSON at 5000 and
        # returned an empty sample on every retry.
        msg = _get_client().messages.create(
            model=JUDGE_MODEL, max_tokens=9000, temperature=1.0,
            messages=[{"role": "user", "content": p}])
        r = _last_json_object(msg.content[0].text)
        if r is None:
            m = re.search(r'\{.*\}', msg.content[0].text, re.DOTALL)
            r = json.loads(m.group()) if m else None
        if isinstance(r, dict) and r.get("prompt"):
            return {"prompt": str(r["prompt"]).strip(),
                    "reference": str(r.get("reference", "")).strip()}
    except Exception:
        pass
    return {"prompt": "", "reference": ""}
