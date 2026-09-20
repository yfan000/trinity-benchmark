#!/usr/bin/env python3
"""One completion interface, several judges, so they can be compared on frozen answers.

The Claude judge is NOT being replaced. Two reasons, both specific to this project:

  1. Every graded version v2-v6 was produced by `claudeopus5`. Swapping it out would mean
     none of those results could be compared to anything produced afterwards.
  2. `TARGETS` includes `gpt-oss-120b`. A GPT judge is same-family with one of the graded
     models — a self-preference risk that does not exist today. Running both judges on the
     same frozen answers measures that bias instead of absorbing it.

So: add `gpt56terra`, keep `claudeopus5`, report the per-model delta.

`gpt56terra` is the strongest GPT on the Argo roster and the best-scoring model on this very
benchmark (61% answer-correct, 46% fully correct over 156 samples — ahead of every other model
tested), which is the relevant evidence for judging competence.

Everything here was verified against the live endpoint before being wired in: all three Argo
auth shapes return 200, and `gpt56terra` answers correctly through `config.argo_auth()`.

Usage:
    python skills/judge_client.py --smoke
"""
from __future__ import annotations
import argparse
import json
import re
import sys
import time
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import config  # noqa: E402
import judge as judge_mod  # noqa: E402

# Per-model, because these differ in ways that silently break a run:
#   - reasoning models spend the budget thinking BEFORE emitting text. A 6000 cap returns
#     empty text with finish_reason="length" — exactly what produced 10 zero-character
#     nemotron answers and 13/40 truncations before REASONING_MAX_TOKENS was introduced.
#   - Opus 5 rejects `temperature` as deprecated; so do OpenAI reasoning models. A global
#     default would fail on one or the other.
JUDGES = {
    "claudeopus5": {"provider": "anthropic", "model": "claudeopus5",
                    "max_tokens": 6000, "temperature": None, "reasoning": True},
    "gpt56terra":  {"provider": "argo", "model": "gpt56terra",
                    "max_tokens": 16384, "temperature": None, "reasoning": True},
    "gpt5":        {"provider": "argo", "model": "gpt5",
                    "max_tokens": 16384, "temperature": None, "reasoning": True},
    "gpto3":       {"provider": "argo", "model": "gpto3",
                    "max_tokens": 16384, "temperature": None, "reasoning": True},
    "gpt41nano":   {"provider": "argo", "model": "gpt41nano",
                    "max_tokens": 4096, "temperature": 0.0, "reasoning": False},
}


class JudgeError(RuntimeError):
    """A judge failed to answer. Never scored as a model failure."""


def complete(judge_id: str, prompt: str, *, max_tokens: int | None = None,
             timeout: float = 600.0, attempts: int = 3) -> tuple[str, dict]:
    """Return (text, meta). meta carries enough to diagnose a failure after the fact."""
    if judge_id not in JUDGES:
        raise JudgeError(f"unknown judge {judge_id!r}; have {sorted(JUDGES)}")
    spec = JUDGES[judge_id]
    mt = max_tokens or spec["max_tokens"]
    t0 = time.perf_counter()

    for attempt in range(1, attempts + 1):
        try:
            if spec["provider"] == "anthropic":
                kw = {}
                if spec["temperature"] is not None:
                    kw["temperature"] = spec["temperature"]
                msg = judge_mod._get_client().with_options(timeout=timeout).messages.create(
                    model=spec["model"], max_tokens=mt,
                    messages=[{"role": "user", "content": prompt}], **kw)
                text = judge_mod._text_of(msg)
                meta = {"finish_reason": msg.stop_reason,
                        "output_tokens": msg.usage.output_tokens,
                        "blocks": [b.type for b in msg.content]}
            else:
                hdr, body_extra = config.argo_auth()
                body = {"model": spec["model"], "max_tokens": mt,
                        "messages": [{"role": "user", "content": prompt}], **body_extra}
                if spec["temperature"] is not None:
                    body["temperature"] = spec["temperature"]
                r = httpx.post(config.ARGO_URL.rstrip("/") + "/chat/completions",
                               headers=hdr, json=body, timeout=timeout)
                if r.status_code != 200:
                    raise JudgeError(f"HTTP {r.status_code}: {r.text[:120]}")
                d = r.json()
                ch = (d.get("choices") or [{}])[0]
                m = ch.get("message") or {}
                text = (m.get("content") or m.get("reasoning_content") or "").strip()
                meta = {"finish_reason": ch.get("finish_reason"),
                        "output_tokens": (d.get("usage") or {}).get("completion_tokens"),
                        "blocks": None}

            meta |= {"judge": judge_id, "provider": spec["provider"], "model": spec["model"],
                     "max_tokens": mt, "temperature": spec["temperature"],
                     "latency_s": round(time.perf_counter() - t0, 1), "attempt": attempt}

            # A truncated judgement is a judge failure, never a zero for the model. This is
            # the same rule that kept a Minerva outage out of the scoreboard.
            if meta["finish_reason"] == "length":
                if attempt < attempts:
                    time.sleep(3 * attempt)
                    continue
                raise JudgeError(f"budget exhausted at {mt} tokens with no complete reply")
            if not text:
                if attempt < attempts:
                    time.sleep(3 * attempt)
                    continue
                raise JudgeError(f"empty reply (finish_reason={meta['finish_reason']})")
            return text, meta

        except JudgeError:
            if attempt >= attempts:
                raise
            time.sleep(3 * attempt)
        except Exception as e:
            if attempt >= attempts:
                raise JudgeError(f"{type(e).__name__}: {str(e)[:120]}") from e
            time.sleep(3 * attempt)
    raise JudgeError("attempts exhausted")


def parse_json(text: str, require: str | None = None) -> dict | None:
    """Extract the judge's JSON object, which is NESTED.

    judge.py's `_last_json_object` finds the last *flat* `{...}`, which was right for the old
    verdict shape but silently wrong for this one: a reply whose `requirements` array holds
    objects returns the last inner requirement instead of the document. Every reply parsed as
    "unparseable" on the first run of this judge was that.

    So: brace-match from each `{`, respecting string literals and escapes, and take the first
    complete object that has the field we need.
    """
    if not text:
        return None
    body = text.strip()
    if body.startswith("```"):                       # fenced replies are common
        body = re.sub(r"^```[a-zA-Z]*\n|\n```\s*$", "", body).strip()

    for start in (m.start() for m in re.finditer(r"\{", body)):
        depth, in_str, esc = 0, False, False
        for i in range(start, len(body)):
            c = body[i]
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
                continue
            if c == '"':
                in_str = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    try:
                        obj = json.loads(body[start:i + 1])
                    except json.JSONDecodeError:
                        break                        # malformed; try the next `{`
                    if isinstance(obj, dict) and (require is None or require in obj):
                        return obj
                    break
    # last resort: the old parser, for a reply that is flat after all
    return judge_mod._last_json_object(text)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--judges", default="claudeopus5,gpt56terra")
    a = ap.parse_args()
    if not a.smoke:
        print(json.dumps({k: {x: y for x, y in v.items()} for k, v in JUDGES.items()}, indent=1))
        return 0
    probe = ('Reply with ONLY this JSON and nothing else: '
             '{"ok": true, "n": 7}')
    for j in a.judges.split(","):
        try:
            text, meta = complete(j, probe, max_tokens=JUDGES[j]["max_tokens"])
            print(f"  {j:<14} {meta['finish_reason']:<10} "
                  f"{str(meta['output_tokens']):>6} tok  {meta['latency_s']:>5}s  "
                  f"parsed={parse_json(text)}")
        except JudgeError as e:
            print(f"  {j:<14} FAILED  {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
