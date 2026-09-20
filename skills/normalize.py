"""Per-benchmark normalizers: raw load_items() dicts -> {question, answer, category, difficulty}.

Every benchmark module returns its dataset's native field names, which differ everywhere
(`problem` vs `question` vs `input` vs `prompt`, `Answer` vs `final_answer` vs `target`).
The skill classifier needs one shape, so each benchmark gets one small function here.

`question` is the substantive content a reader needs to judge what skills the item exercises
— stem plus answer options where the options carry signal — but not the answer-format
boilerplate the runner appends ("Answer with only the letter."), which is identical across
thousands of items and tells the classifier nothing.
"""
from __future__ import annotations

LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
           "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"]


def _mcq(stem: str, options: list[str], labels: list[str] | None = None) -> str:
    labels = labels or LETTERS[:len(options)]
    body = "\n".join(f"{lab}) {opt}" for lab, opt in zip(labels, options))
    return f"{stem}\n{body}"


def _mmlu(it):
    return _mcq(it["question"], list(it["choices"])), LETTERS[it["answer"]], it["_subject"], None


def _mmlu_pro(it):
    return _mcq(it["question"], list(it["options"])), it["answer"], it["category"], None


def _gpqa(it):
    return _mcq(it["question"], it["options"]), it["answer"], it["category"], None


def _gsm8k(it):
    ans = it["answer"]
    return it["question"], (ans.split("####")[-1].strip() if "####" in ans else ans.strip()), None, None


def _gsm1k(it):
    return it["question"], it["answer"].strip(), None, None


def _aime(it):
    return it["Problem"], str(it["Answer"]), None, None


def _olympiad(it):
    return it["question"], str(it.get("final_answer")), it.get("subfield"), it.get("difficulty")


def _math(it):
    return it["problem"], it["solution"], it.get("type"), it.get("level")


def _humaneval(it):
    return it["prompt"], it["canonical_solution"], None, None


def _bigcodebench(it):
    return it["complete_prompt"], it["canonical_solution"], None, None


def _arc(it):
    labels = list(it["choices"]["label"])
    texts = list(it["choices"]["text"])
    return _mcq(it["question"], texts, labels), it["answerKey"], None, None


def _hellaswag(it):
    return _mcq(it["ctx"], list(it["endings"])), LETTERS[int(it["label"])], it.get("activity_label"), None


def _winogrande(it):
    return _mcq(it["sentence"], [it["option1"], it["option2"]]), LETTERS[int(it["answer"]) - 1], None, None


def _truthfulqa(it):
    choices = list(it["mc1_targets"]["choices"])
    labels = list(it["mc1_targets"]["labels"])
    return _mcq(it["question"], choices), LETTERS[labels.index(1)], None, None


def _longbench(it):
    # The source document runs to tens of thousands of chars. Its *length* is the skill-relevant
    # signal (this is a long-context task); its contents would dwarf every other sample in the
    # corpus and blow the classifier's input budget, so record the size and drop the body.
    stem = (f"[Long-context task: {len(it['context']):,} chars of source document, omitted here]\n\n"
            f"{it['question']}")
    opts = [it["choice_A"], it["choice_B"], it["choice_C"], it["choice_D"]]
    return _mcq(stem, opts), it["answer"], it.get("domain"), it.get("difficulty")


def _bbh(it):
    return it["input"], it["target"], it["_task"], None


def _ifeval(it):
    return it["prompt"], None, ", ".join(it["instruction_id_list"]), None


def _mt_bench(it):
    turns = "\n\n".join(f"Turn {i + 1}: {t}" for i, t in enumerate(it["turns"]))
    return turns, None, it.get("category"), None


def _hle(it):
    return it["question"], it["answer"], it.get("category"), None


def _infobench(it):
    stem = it["instruction"]
    if it.get("input"):
        stem = f"{stem}\n\nInput:\n{it['input']}"
    labels = it.get("question_label") or []
    flat = [lab for sub in labels for lab in (sub if isinstance(sub, list) else [sub])]
    return stem, "; ".join(it.get("decomposed_questions") or []), (flat[0] if flat else "Unlabeled"), it.get("subset")


def _followbench(it):
    return it["instruction"], it.get("target"), it["_bucket"], f"level_{it['level']}"


def _sealqa(it):
    return it["question"], it["answer"], it.get("topic") or "Unlabeled", it["_difficulty"]


def _clutrr(it):
    return it["question"], it["answer"], it["category"], f"{it['hops']}_hops"


def _labbench(it):
    return _mcq(it["question"], list(it["options"]), list(it["letters"])), it["answer"], it.get("subtask"), None


def _matscibench(it):
    return it["question"], str(it.get("answer")), it.get("category"), it.get("difficulty")


NORMALIZERS = {
    "mmlu": _mmlu, "mmlu_pro": _mmlu_pro, "gpqa": _gpqa, "gpqa_main": _gpqa,
    "gsm8k": _gsm8k, "gsm1k": _gsm1k, "aime2024": _aime, "olympiadbench": _olympiad,
    "math": _math, "humaneval": _humaneval, "bigcodebench": _bigcodebench, "arc": _arc,
    "hellaswag": _hellaswag, "winogrande": _winogrande, "truthfulqa": _truthfulqa,
    "longbench_v2": _longbench, "bbh": _bbh, "ifeval": _ifeval, "mt_bench": _mt_bench,
    "hle": _hle, "infobench": _infobench, "followbench": _followbench, "sealqa": _sealqa,
    "clutrr_regen": _clutrr, "labbench": _labbench, "matscibench": _matscibench,
}
