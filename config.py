"""Benchmark configuration: models, endpoint, auth."""
from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from repo root
load_dotenv(Path(__file__).parent.parent.parent / ".env")

_DEFAULT_SOPHIA_URL = "https://inference-api.alcf.anl.gov/resource_server/sophia/vllm/v1"
SOPHIA_URL = os.getenv("VLLM_ENDPOINT", _DEFAULT_SOPHIA_URL)
ALCF_TOKEN = os.getenv("ALCF_INFERENCE_TOKEN", "")

# Argo — ANL's gateway to closed-source commercial models (OpenAI/Anthropic/Google).
# OpenAI-compatible chat/completions, same SSE streaming shape as Sophia's vLLM endpoint.
# Auth is your ANL username, not a secret token (confirmed against the live endpoint).
_DEFAULT_ARGO_URL = "https://apps.inside.anl.gov/argoapi/v1"
ARGO_URL = os.getenv("ARGO_URL", _DEFAULT_ARGO_URL)
ARGO_USER = os.getenv("ARGO_USER", os.getenv("USER", ""))

# judge.py reaches Opus 5 by pointing the Anthropic SDK at Argo's Anthropic-shaped bridge.
# It lives in the shell environment rather than .env, so the pipeline runs on this machine and
# fails on a clean checkout with no error that names the cause. Surfaced here so it is at
# least discoverable, and so a missing value is reported rather than guessed at.
ANTHROPIC_BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "")


def argo_auth() -> tuple[dict, dict]:
    """(headers, body_extras) for an Argo call — the single definition.

    Three call sites had drifted apart: client.py and probe_tools.py sent
    `Authorization: Bearer $ARGO_USER`, while trinity_run.ask() sent no header and put the
    username in the body's `user` field. Both reach the endpoint, which is why the divergence
    survived, but it means a change to how Argo identifies callers has to be made in three
    places and one of them will be missed. Send both forms: the header is what client.py has
    always used, the body field is what the Trinity runs were actually measured with.
    """
    if not ARGO_USER:
        raise RuntimeError(
            "ARGO_USER is unset and $USER is empty. Argo identifies callers by ANL username; "
            "without it requests fail in ways that look like the model returning nothing.")
    return ({"Authorization": f"Bearer {ARGO_USER}", "Content-Type": "application/json"},
            {"user": ARGO_USER})

# Minerva — ALCF's third inference cluster (NVIDIA B200), separate from Sophia (A100) and
# Metis (SambaNova). Both models here are "Always Hot" per ALCF's docs (never cold/down),
# unlike most of Sophia's roster. Same OpenAI-compatible chat/completions shape and the
# same Globus bearer token as Sophia — only the base URL and model IDs differ.
_DEFAULT_MINERVA_URL = "https://inference-api.alcf.anl.gov/resource_server/minerva/api/v1"
MINERVA_URL = os.getenv("MINERVA_ENDPOINT", _DEFAULT_MINERVA_URL)
MINERVA_MODELS = [
    "nemotron-3-ultra",
    "inkling-bf16",
]

# Closed-source models available via Argo, picked to span provider x capability tier.
# IDs are Argo's own "internal_id" strings (verified via GET /v1/models), not display names.
ARGO_MODELS = [
    "claudesonnet5",
    "claudeopus48",
    "claudehaiku45",
    "gpt56terra",
    "gpt5",
    "gpt41nano",
    "gpto3",
    "gemini25pro",
    "gemini35flash",
]

# Models currently confirmed working on Sophia (503s excluded at runtime)
CANDIDATE_MODELS = [
    "meta-llama/Llama-4-Scout-17B-16E-Instruct",
    "meta-llama/Llama-4-Maverick-17B-128E-Instruct",
    "meta-llama/Meta-Llama-3.1-405B-Instruct",
    "meta-llama/Meta-Llama-3.1-70B-Instruct",
    "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "meta-llama/Llama-3.3-70B-Instruct",
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "mistralai/Mixtral-8x22B-Instruct-v0.1",
    "mistralai/Mistral-Large-Instruct-2407",
    "mistralai/Devstral-2-123B-Instruct-2512",
    "google/gemma-3-27b-it",
    "google/gemma-4-26B-A4B-it",
    "google/gemma-4-31B-it",
    "google/gemma-4-E4B-it",
    "argonne/AuroraGPT-DPO-UFB-0225",
    "argonne/AuroraGPT-IT-v4-0125",
    "argonne/AuroraGPT-Tulu3-SFT-0125",
    "allenai/Llama-3.1-Tulu-3-405B",
    "AstroMLab/AstroSage-70B-20251009",
    "nvidia/nemotron-3-super-120b",
]

# Short display name for plots
def short_name(model: str) -> str:
    return model.split("/")[-1]

# Models observed emitting a chain-of-thought preamble before (or instead of) a direct
# answer. On short-budget prompts (MCQ letter/short-numeric benchmarks), that preamble
# consumes max_tokens before the model ever reaches the answer, producing a truncated
# fragment like "We need to compute..." rather than a wrong answer — the model isn't
# failing the question, it never got to answer it. Confirmed directly on gpt-oss-120b/20b
# and Llama-4-Maverick this session (see BENCHMARK_REPORT.md finding 2); Llama-4-Scout is
# included on the strength of the same behavior documented in the original ALCF paper
# (paper/paper.tex, Section 5.2) even though it wasn't live to re-confirm this session.
REASONING_MODELS = {
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "meta-llama/Llama-4-Maverick-17B-128E-Instruct",
    "meta-llama/Llama-4-Scout-17B-16E-Instruct",
    # Argo (closed-source) models — empirically tested at max_tokens=16 on MMLU: these 7
    # returned mostly/entirely empty responses (silent, no error), while claudehaiku45 and
    # gpt41nano answered normally with no empty responses — consistent with "thinking"/
    # reasoning mode being on by default for the flagship tier and off for the cheap tier.
    "claudesonnet5",
    "claudeopus48",
    "gpt5",
    "gpto3",
    "gpt56terra",
    "gemini25pro",
    "gemini35flash",
    # Minerva models — both emit a visible chain-of-thought preamble before the final
    # answer (confirmed live: inkling-bf16 got cut off mid-reasoning at max_tokens=32
    # with an empty final `text`; nemotron-3-ultra answered correctly at 32 but also
    # emits reasoning content, so the same floor is applied for harder questions).
    "nemotron-3-ultra",
    "inkling-bf16",
}


def resolve_max_tokens(model: str, default_max_tokens: int, reasoning_min: int = 1024) -> int:
    """Give REASONING_MODELS a floor high enough to get through their CoT preamble on
    short-budget benchmarks, while leaving every other model's (usually deliberately
    small, for speed/cost) max_tokens untouched."""
    if model in REASONING_MODELS:
        return max(default_max_tokens, reasoning_min)
    return default_max_tokens
