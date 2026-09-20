"""LLM-as-judge using Claude-sonnet-4-6 via Anthropic API."""
from __future__ import annotations
import ast
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

_SCORE_PROMPT = """\
You are an impartial evaluator scoring an AI model's response.

Task given to the model:
{task}

Model's response:
{response}

Evaluation criteria:
{criteria}

Score the response from 1 to 5:
1 = Wrong / completely fails the task
2 = Partially correct but major issues
3 = Acceptable, meets basic requirements
4 = Good, minor issues only
5 = Excellent, fully correct and well-reasoned

Respond with ONLY a JSON object:
{{"score": <1-5>, "reason": "<one sentence>"}}"""


def score(task: str, response: str, criteria: str) -> dict:
    """Return {score: int, reason: str} using Claude as judge."""
    if not response or not response.strip():
        return {"score": 1, "reason": "Empty response"}
    prompt = _SCORE_PROMPT.format(task=task, response=response[:2000], criteria=criteria)
    try:
        msg = _get_client().messages.create(
            model=JUDGE_MODEL,
            max_tokens=128,
            messages=[{"role": "user", "content": prompt}],
        )
        text = msg.content[0].text.strip()
        # Extract JSON even if wrapped in markdown
        m = re.search(r'\{.*\}', text, re.DOTALL)
        if m:
            return json.loads(m.group())
    except Exception as e:
        return {"score": 1, "reason": f"Judge error: {e}"}
    return {"score": 1, "reason": "Could not parse judge response"}


# Verbatim from centerforaisafety/hle's hle_eval/run_judge_results.py, so our grading
# matches the benchmark's own official methodology rather than inventing a new one.
_HLE_JUDGE_PROMPT = """\
Judge whether the following [response] to [question] is correct or not based on the precise and unambiguous [correct_answer] below.

[question]: {question}

[response]: {response}

Your judgement must be in the format and criteria specified below:

extracted_final_answer: The final exact answer extracted from the [response]. Put the extracted answer as 'None' if there is no exact, final answer to extract from the response.

[correct_answer]: {correct_answer}

reasoning: Explain why the extracted_final_answer is correct or incorrect based on [correct_answer], focusing only on if there are meaningful differences between [correct_answer] and the extracted_final_answer. Do not comment on any background to the problem, do not attempt to solve the problem, do not argue for any answer different than [correct_answer], focus only on whether the answers match.

correct: Answer 'yes' if extracted_final_answer matches the [correct_answer] given above, or is within a small margin of error for numerical problems. Answer 'no' otherwise, i.e. if there if there is any inconsistency, ambiguity, non-equivalency, or if the extracted answer is incorrect.

Respond with ONLY a JSON object in this exact form:
{{"extracted_final_answer": "...", "reasoning": "...", "correct": "yes" or "no"}}"""


def judge_hle(question: str, correct_answer: str, response: str) -> dict:
    """Return {extracted_final_answer, reasoning, correct: 'yes'/'no'} per HLE's own
    official grading prompt (see module docstring above the prompt)."""
    if not response or not response.strip():
        return {"extracted_final_answer": "None", "reasoning": "Empty response", "correct": "no"}
    prompt = _HLE_JUDGE_PROMPT.format(question=question, correct_answer=correct_answer, response=response[:4000])
    try:
        msg = _get_client().messages.create(
            model=JUDGE_MODEL,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
        text = msg.content[0].text.strip()
        m = re.search(r'\{.*\}', text, re.DOTALL)
        if m:
            result = json.loads(m.group())
            result.setdefault("correct", "no")
            return result
    except Exception as e:
        return {"extracted_final_answer": "None", "reasoning": f"Judge error: {e}", "correct": "no"}
    return {"extracted_final_answer": "None", "reasoning": "Could not parse judge response", "correct": "no"}


# Verbatim from qinyiwei/InfoBench's evaluation.py SYS_MSG, so grading matches the
# benchmark's own official yes/no-per-decomposed-question methodology.
_INFOBENCH_SYS_MSG = (
    "Based on the provided Input (if any) and Generated Text, answer the ensuing Questions "
    "with either a YES or NO choice. Your selection should be based on your judgment as well "
    "as the following rules:\n\n"
    "- YES: Select 'YES' if the generated text entirely fulfills the condition specified in "
    "the question. However, note that even minor inaccuracies exclude the text from receiving "
    "a 'YES' rating. As an illustration, consider a question that asks, \"Does each sentence "
    "in the generated text use a second person?” If even one sentence does not use the second "
    "person, the answer should NOT be 'YES'. To qualify for a 'YES' rating, the generated text "
    "must be entirely accurate and relevant to the question\n\n"
    "- NO: Opt for 'NO' if the generated text fails to meet the question's requirements or "
    "provides no information that could be utilized to answer the question. For instance, if "
    "the question asks, \"Is the second sentence in the generated text a compound sentence?\" "
    "and the generated text only has one sentence, it offers no relevant information to answer "
    "the question. Consequently, the answer should be 'NO'."
)


def judge_infobench(input_text: str, output_text: str, decomposed_questions: list[str]) -> list[bool | None]:
    """Ask each decomposed question as a turn in one growing conversation, exactly matching
    InfoBench's official evaluation.py protocol (ported below, GPT-4 swapped for Claude).
    Returns one bool (or None if unparseable) per question, in order."""
    if not output_text or not output_text.strip():
        return [False] * len(decomposed_questions)

    messages: list[dict] = []
    results: list[bool | None] = []
    for i, question in enumerate(decomposed_questions):
        if i == 0:
            if input_text:
                content = f'{_INFOBENCH_SYS_MSG}\n\nInput:\n"{input_text}"\n\nGenerated Text:\n"{output_text}"\n\nQuestion:\n{question}\n'
            else:
                content = f'{_INFOBENCH_SYS_MSG}\n\nGenerated Text:\n"{output_text}"\n\nQuestion:\n{question}\n'
        else:
            content = f"{question}\n"
        messages.append({"role": "user", "content": content})
        try:
            msg = _get_client().messages.create(
                model=JUDGE_MODEL, max_tokens=64, messages=messages,
            )
            generation = msg.content[0].text.strip()
            messages.append({"role": "assistant", "content": generation})
            gen_lower = generation.lower()
            if gen_lower.startswith("yes"):
                results.append(True)
            elif gen_lower.startswith("no"):
                results.append(False)
            elif "YES" in generation and "NO" not in generation:
                results.append(True)
            elif "NO" in generation and "YES" not in generation:
                results.append(False)
            else:
                results.append(None)
        except Exception:
            results.append(None)
    return results


# Generic across content/situation/style/format/mixed constraint types — only the noun
# phrase describing the added constraint changes, matching FollowBench's official
# code/gpt4_based_evaluation.py {type}_evaluation_prompt() functions verbatim.
_FOLLOWBENCH_CONSTRAINT_DESC = {
    "content": "content constraint",
    "situation": "situation constraint (information to describe a specific situation/background)",
    "style": "style constraint",
    "format": "format constraint",
    "example": "constraint",
    "mixed": "constraint",
}


def _followbench_prompt(constraint_type: str, evolve_instructions: list[str], answer: str) -> str:
    desc = _FOLLOWBENCH_CONSTRAINT_DESC.get(constraint_type, "constraint")
    level = len(evolve_instructions) - 1
    if level == 1:
        prompt = (
            f"Given an initial instruction, we add one {desc} and obtain the final "
            "instruction with 1 additional constraint.\n\n"
            f"#Initial Instruction#\n{evolve_instructions[0]}\n\n"
            f"#Initial Instruction + 1 constraint#\n{evolve_instructions[1]}\n\n"
            f"#Answer of Initial Instruction + 1 constraint#\n{answer}\n\n"
            "#System#\n1) Please identify the 1 added constraint.\n"
            "2) Please descriminate if the #Answer of Initial Instruction + 1 constraint# "
            "satisfies the 1 added constraint.\n"
            "3) In the final line, only output a Python LIST with 1 element ('YES' or 'NO') "
            "indicating whether the answer satisfies the 1 added constraint."
        )
    else:
        prompt = (
            f"Given an initial instruction, we add one {desc} per time and obtain the final "
            f"instruction with {level} additional constraints.\n\n"
            f"#Initial Instruction#\n{evolve_instructions[0]}\n\n"
            f"#Initial Instruction + 1 constraint#\n{evolve_instructions[1]}\n\n"
        )
        for i in range(2, level + 1):
            prompt += f"#Initial Instruction + {i} constraints#\n{evolve_instructions[i]}\n\n"
        prompt += (
            f"#Answer of Initial Instruction + {level} constraints#\n{answer}\n\n"
            f"#System#\n1) Please identify all {level} added constraints.\n"
            f"2) For the {level} added constraints, discriminate if the #Answer of Initial "
            f"Instruction + {level} constraints# satisfies each constraint.\n"
            f"3) In the final line, only output a Python LIST with {level} elements "
            "('YES' or 'NO') indicating whether the answer satisfies each constraint."
        )
    return prompt


def judge_followbench(constraint_type: str, evolve_instructions: list[str], answer: str) -> dict:
    """Return {hard_satisfy: bool, soft_satisfy: float}. hard_satisfy requires every added
    constraint at this level to be satisfied; soft_satisfy is the fraction satisfied. Mirrors
    FollowBench's official paring_discriminative_generation() parsing logic."""
    level = len(evolve_instructions) - 1
    if not answer or not answer.strip():
        return {"hard_satisfy": False, "soft_satisfy": 0.0}
    prompt = _followbench_prompt(constraint_type, evolve_instructions, answer[:4000])
    try:
        msg = _get_client().messages.create(
            model=JUDGE_MODEL, max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
        text = msg.content[0].text.strip()
        tail = text.strip("`").strip().split("\n")[-1]
        if level == 1:
            if "YES" in tail:
                return {"hard_satisfy": True, "soft_satisfy": 1.0}
            elif "NO" in tail:
                return {"hard_satisfy": False, "soft_satisfy": 0.0}
            return {"hard_satisfy": False, "soft_satisfy": 0.0}
        m = re.search(r'\[.*\]', tail)
        if m:
            items = ast.literal_eval(m.group())
            if isinstance(items, list) and len(items) == level:
                num_true = sum(1 for x in items if isinstance(x, str) and "YES" in x.upper())
                return {"hard_satisfy": num_true == level, "soft_satisfy": num_true / level}
    except Exception:
        pass
    return {"hard_satisfy": False, "soft_satisfy": 0.0}


# --- Fundamental-skills taxonomy classification ------------------------------------------
# Labels the benchmark *question*, not a model's answer to it — so results can be
# re-aggregated across benchmarks by skill instead of by each benchmark's own category.


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

_SKILLS_DISCOVERY_PROMPT = """\
You are helping build a taxonomy of the fundamental skills that benchmark questions require,
so LLM evaluation results can be aggregated by skill rather than by benchmark.

Question (benchmark "{benchmark}", its own category: "{original_category}"):
{question}

Reference answer: {answer}

Candidate skills (apply the ones that genuinely fit — do not force a fit):
{seed_skills}

Identify every fundamental skill *this specific question* requires. Judge the question
itself, not the benchmark it came from — benchmarks are heterogeneous. Questions are often
compositional, so multiple skills is normal; but only list skills the question actually
exercises. If a required skill is missing from the candidate list, name it in
novel_tag_suggested (short, general enough to recur across benchmarks).

Respond with ONLY a JSON object:
{{"proposed_skills": ["<skill>", ...], "reasoning": "<one sentence>", "novel_tag_suggested": <"name" or null>}}"""


def judge_skills_discovery(question: str, answer: str, benchmark: str,
                           original_category: str, seed_skills: list[str]) -> dict:
    """Open-vocabulary pass for taxonomy discovery: apply seed skills where they fit, or
    propose a new tag. Returns {proposed_skills, reasoning, novel_tag_suggested}."""
    prompt = _SKILLS_DISCOVERY_PROMPT.format(
        benchmark=benchmark, original_category=original_category or "none",
        question=question[:3000], answer=str(answer)[:500],
        seed_skills="\n".join(f"- {s}" for s in seed_skills))
    try:
        msg = _get_client().messages.create(
            model=JUDGE_MODEL, max_tokens=400,
            messages=[{"role": "user", "content": prompt}],
        )
        result = _last_json_object(msg.content[0].text)
        if result is not None:
            result.setdefault("proposed_skills", [])
            result.setdefault("reasoning", "")
            result.setdefault("novel_tag_suggested", None)
            return result
    except Exception as e:
        return {"proposed_skills": [], "reasoning": f"Judge error: {e}", "novel_tag_suggested": None}
    return {"proposed_skills": [], "reasoning": "Could not parse judge response", "novel_tag_suggested": None}


_HPC_GEN_PROMPT = """\
You are writing realistic HPC user-support material for Argonne Leadership Computing Facility
(ALCF), to be used as evaluation content.

Below is an extract of ALCF's own documentation. Use it for concrete, accurate specifics —
real queue names, real PBS directive syntax, real filesystem names, real command flags.

--- ALCF DOCUMENTATION EXTRACT ---
{doc}
--- END EXTRACT ---

Write {n} DISTINCT items of this kind:
  Task category: {category}
  Specific variation to cover: {variation}

Each item must read like something a real ALCF user actually wrote to the help desk, or a
real request a facility-support agent was handed. Concretely:
  - Write in the user's own voice, first person, with the mess of a real request: a pasted
    error message, a partial qsub line, a wrong assumption, missing detail.
  - NOT textbook questions. "What does the qsub -A flag do?" is useless. "My job has been
    queued for 6 hours in prod while shorter jobs jump ahead — here's my qsub line, what am
    I doing wrong?" is what we want.
  - Ground every item in real ALCF specifics from the extract above. Invent plausible
    project names, paths, and job IDs, but never invent flags, queue names, or filesystems.
  - ALCF runs PBS Pro, not Slurm. Use qsub/qstat/qdel/#PBS/$PBS_NODEFILE and mpiexec.
    Never write srun, sbatch, squeue, #SBATCH or $SLURM_* — those are wrong for this site
    and make the item useless as ALCF content.
  - Make the {n} items genuinely different from each other in situation and detail, not one
    template with the numbers changed.

For each item also give the answer a knowledgeable ALCF support engineer would give — brief
(1-3 sentences), correct, and specific.

Respond with ONLY a JSON array, no prose before or after:
[{{"question": "<the user's request, verbatim as they'd write it>", "answer": "<the support answer>"}}, ...]"""


_HPC_EXEC_PROMPT = """\
You are writing realistic HPC *agent* tasks for Argonne Leadership Computing Facility (ALCF),
to be used as evaluation content.

Below is an extract of ALCF's own documentation. Use it for concrete, accurate specifics —
real queue names, real PBS directive syntax, real filesystem names, real command flags.

--- ALCF DOCUMENTATION EXTRACT ---
{doc}
--- END EXTRACT ---

Write {n} DISTINCT tasks of this kind:
  Task category: {category}
  Specific variation to cover: {variation}

These are tasks an autonomous agent operating the machine on a user's behalf must CARRY OUT —
not questions to answer or advice to give. The difference is essential:
  - WRONG (advisory): "Why is my job stuck in the queue?"
  - RIGHT (execution): "Write the PBS script to run this 40-node job on Polaris for 2 hours
    against project X, with 4 ranks per node bound to the 4 GPUs. Output only the script."

So each task must require the agent to PRODUCE something concrete or ACT: emit a job script,
construct an exact mpiexec invocation, issue the right qstat/qdel command, parse command
output and decide what to do next, edit a broken directive, or drive a multi-step sequence.
  - State a specific deliverable and any output constraints ("output only the script, no
    commentary", "reply with just the command", "give the three commands in order").
  - Give the agent the context it needs — paths, project names, node counts, error text —
    the way a real invocation would.
  - ALCF runs PBS Pro, not Slurm. Use qsub/qstat/qdel/#PBS/$PBS_NODEFILE and mpiexec.
    Never write srun, sbatch, squeue, #SBATCH or $SLURM_*.
  - Make the {n} tasks genuinely different in situation and deliverable.

For each task also give the correct result a competent HPC engineer would produce — the
actual script, command, or decision. Keep it concise but real.

Respond with ONLY a JSON array, no prose before or after:
[{{"question": "<the task given to the agent>", "answer": "<the correct output>"}}, ...]"""


def generate_hpc_tasks(category: str, doc: str, variation: str, n: int = 5,
                       framing: str = "advisory") -> list[dict]:
    """Generate `n` realistic ALCF task instances for one (category, variation) pair.

    framing="advisory"  — a user asking the help desk a question (measures advisory skill).
    framing="execution" — a task an agent operating the machine must carry out. The two
    exercise different skills: advisory instances never invoke a tool or obey an output
    constraint, so Tool use and Instruction/format following come back at 0% for them.

    Returns [{"question": str, "answer": str}, ...] — empty list on any failure, so one bad
    generation can't halt a sweep.
    """
    template = _HPC_EXEC_PROMPT if framing == "execution" else _HPC_GEN_PROMPT
    prompt = template.format(doc=doc[:6000], category=category,
                             variation=variation, n=n)
    try:
        msg = _get_client().messages.create(
            model=JUDGE_MODEL, max_tokens=4096, temperature=1.0,
            messages=[{"role": "user", "content": prompt}],
        )
        text = msg.content[0].text
        m = re.search(r'\[.*\]', text, re.DOTALL)
        if not m:
            return []
        items = json.loads(m.group())
        return [{"question": str(it["question"]).strip(), "answer": str(it.get("answer", "")).strip()}
                for it in items
                if isinstance(it, dict) and str(it.get("question", "")).strip()]
    except Exception:
        return []


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
    # alphabet into a FASTA. See skills/format_contracts.yaml.
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
        # No clip here: skills.catalog.render_* already emits labelled sections with per-section
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


# --- Trinity agent benchmark: grading a model's attempt at a subtask ---------------------
# Opus 5 via Argo, chosen deliberately over the sonnet judge used elsewhere: these answers
# are job scripts and input decks where a wrong flag matters, and the grading key carries
# exact strings (module lines, run commands, content markers) to check against.
TRINITY_JUDGE_MODEL = "claudeopus5"

_TRINITY_JUDGE_PROMPT = """\
You are grading one attempt at an HPC agent subtask. Be strict and concrete: this decides
whether a cheaper model can be trusted with this step of a real pipeline.

Subtask: {subtask} — {goal}
Target system: {system} (scheduler: {scheduler})

--- THE PROMPT THE MODEL WAS GIVEN ---
{prompt}
--- THE MODEL'S ANSWER ---
{answer}
--- GROUND TRUTH from the facility's software catalog ---
{key}
--- END ---

The model answered through a plain chat API. It has no filesystem, no shell and no access to
the machine, so never penalise it for not creating files, not running anything, or not
verifying that a path exists — emitting correct file contents as text is a complete answer.

{grading_note}Grade ONLY what this subtask asked for. The sample's own Output line is the contract:

    {output_spec}

Anything outside that contract is out of scope and must not cost marks. If the subtask asks
only which application to use, the absence of a module line, a run command or a job script
is NOT a defect — do not deduct for it or list it under errors. Judge the answer the task
requested, not the fuller answer a complete HPC workflow would eventually need.

Within that scope, be strict: an unsupported claim, an invented module name, a fabricated
version or benchmark, or a wrong technical assertion IS a defect even when the headline
answer is right, because a downstream step may copy it.

Grade against the ground truth, not against your own preferences. Where the catalog gives an
exact string — module lines, a run command, required input extensions, content markers that
must appear inside a file — an answer that differs in substance is wrong even if it looks
plausible. Equivalent phrasing or ordering is fine; a different module, a wrong launcher, a
missing required file, or the wrong scheduler's directives is not.

Score each dimension 0-2 (0 absent/wrong, 1 partially right, 2 correct):
  correctness   — does it match the ground truth?
  completeness  — is everything the subtask asked for present?
  usability     — could this be run as-is on that system without repair?

Also decide `fatal_error`: true if the answer would fail immediately on that machine (wrong
scheduler directives, a nonexistent module or binary, a launcher the site does not use, a
resource request outside the queue's limits).

Respond with ONLY a JSON object:
{{"correctness": <0-2>, "completeness": <0-2>, "usability": <0-2>, "fatal_error": <true|false>,
  "errors": ["<specific defect>", ...], "note": "<one sentence>"}}"""


def _output_spec(prompt: str) -> str:
    """The sample's own Output line — the contract the answer is held to."""
    i = prompt.rfind("Output:")
    return " ".join(prompt[i + len("Output:"):].split())[:400] if i >= 0 else "(not stated)"


def judge_trinity(subtask: str, goal: str, system: str, scheduler: str, prompt: str,
                  answer: str, key: dict, grading_note: str = "") -> dict:
    """Grade one attempt. Returns the three scores, a fatal flag, and specific defects."""
    if not answer or not answer.strip():
        return {"correctness": 0, "completeness": 0, "usability": 0, "fatal_error": True,
                "errors": ["empty response"], "note": "Model returned nothing."}
    p = _TRINITY_JUDGE_PROMPT.format(
        subtask=subtask, goal=goal, system=system, scheduler=scheduler,
        prompt=prompt[:4000], answer=answer[:8000],
        output_spec=_output_spec(prompt), key=json.dumps(key, indent=1)[:3000],
        grading_note=(grading_note.strip() + "\n\n") if grading_note else "")
    try:
        # No temperature: Opus 5 rejects it as deprecated ("`temperature` is deprecated
        # for this model"). Determinism comes from the rubric and the explicit ground truth.
        # 3000, not 1400: Opus 5 emits a thinking block before the JSON and was landing
        # around 1200 output tokens, close enough to the cap that the object occasionally
        # truncated mid-string.
        msg = _get_client().messages.create(
            # A long answer (an 8-file GROMACS deck ran to 8,700 chars) draws a long
            # defect list, and the reply used to run out of budget mid-JSON — which
            # surfaced as an unparseable response that retried forever.
            model=TRINITY_JUDGE_MODEL, max_tokens=6000,
            messages=[{"role": "user", "content": p}])
        raw = _text_of(msg)
        # Recorded so a failure is diagnosable instead of guessed. A previous "unparseable"
        # failure was attributed to truncation on no evidence; stop_reason distinguishes a
        # budget overrun (max_tokens, usually with no text block at all because thinking
        # consumed it) from the judge simply answering in prose (end_turn with text).
        diag = {"stop_reason": getattr(msg, "stop_reason", "?"),
                "out_tokens": getattr(getattr(msg, "usage", None), "output_tokens", None),
                "blocks": [type(b).__name__ for b in msg.content],
                "text_chars": len(raw)}
        r = _last_json_object(raw)
        if r is None:
            m = re.search(r'\{.*\}', raw, re.DOTALL)
            r = json.loads(m.group()) if m else None
        if isinstance(r, dict) and "correctness" in r:
            for k in ("correctness", "completeness", "usability"):
                r[k] = max(0, min(2, int(r.get(k, 0))))
            r["fatal_error"] = bool(r.get("fatal_error", False))
            r.setdefault("errors", [])
            return r
    except Exception as e:
        return {"judge_failed": True, "errors": [f"judge error: {type(e).__name__}"],
                "note": str(e)[:140]}
    # Distinguished from a zero score on purpose. A judge that fails to answer says nothing
    # about the model, and silently recording 0/0/0 fatal would understate it — which is
    # exactly what happened to gpt-oss-120b on the first smoke test.
    return {"judge_failed": True, "errors": ["unparseable judge response"],
            "note": json.dumps(diag), "diag": diag}


_SKILLS_FINAL_PROMPT = """\
Label this benchmark question with every skill it requires, from the fixed taxonomy below.
Judge the question itself, not the benchmark it came from. Questions are often
compositional, so multiple labels is normal — but only apply a label the question actually
exercises. Do not invent labels outside the taxonomy.

Taxonomy:
{taxonomy}

Question (benchmark "{benchmark}", its own category: "{original_category}"):
{question}

Reference answer: {answer}

Do NOT attempt to answer or solve the question. Do not show any working. Classifying is the
only task — emit the JSON object immediately as the first thing you write.

Respond with ONLY a JSON object:
{{"fundamental_skills": ["<label>", ...], "confidence": <0.0-1.0>}}"""


def judge_skills_final(question: str, answer: str, benchmark: str,
                       original_category: str, taxonomy: list[dict]) -> dict:
    """Fixed-taxonomy multi-label pass. `taxonomy` is [{"name","description"}, ...].
    Returns {fundamental_skills, confidence}."""
    prompt = _SKILLS_FINAL_PROMPT.format(
        taxonomy="\n".join(f"- {t['name']}: {t['description']}" for t in taxonomy),
        benchmark=benchmark, original_category=original_category or "none",
        question=question[:3000], answer=str(answer)[:500])
    try:
        # 900, not 300: dense physics/chemistry stems pull the model into solving the
        # problem first, and 13/242 items hit max_tokens before emitting any JSON on the
        # first validation run. (Assistant prefill would be the tighter fix, but this
        # model rejects it — the conversation must end with a user message.)
        msg = _get_client().messages.create(
            # temperature=0: at the API default of 1.0 this classifier agreed with itself
            # only 0.907 (Jaccard) across two runs of the same 242 items — noise large
            # enough to swamp any real signal when comparing models on a skill.
            model=JUDGE_MODEL, max_tokens=900, temperature=0,
            messages=[{"role": "user", "content": prompt}],
        )
        result = _last_json_object(msg.content[0].text)
        if result is not None:
            # Canonicalize case before filtering: the discovery pass returned lowercase
            # variants ("state tracking" for "State tracking") on ~5% of items, and an
            # exact-match filter would silently drop those as if no skill applied.
            # Anything still unmatched is a genuine hallucination and is dropped.
            canon = {t["name"].lower(): t["name"] for t in taxonomy}
            labels = [canon[s.lower()] for s in result.get("fundamental_skills", [])
                      if isinstance(s, str) and s.lower() in canon]
            return {
                "fundamental_skills": sorted(set(labels), key=labels.index),
                "confidence": float(result.get("confidence", 0.5)),
            }
    except Exception:
        pass
    return {"fundamental_skills": [], "confidence": 0.0}
