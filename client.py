"""Async streaming client for ALCF Sophia vLLM endpoint, and Argo (closed-source models)."""
from __future__ import annotations
import json
import time
from dataclasses import dataclass, field
from typing import AsyncIterator

import httpx
from config import (SOPHIA_URL, ALCF_TOKEN, ARGO_URL, ARGO_USER, ARGO_MODELS,
                     MINERVA_URL, MINERVA_MODELS, argo_auth)

CONNECT_TIMEOUT = 15.0
READ_TIMEOUT = 90.0


@dataclass
class StreamResult:
    text: str = ""
    reasoning: str = ""
    ttft_s: float | None = None
    total_s: float | None = None
    server_completion_tokens: int = 0
    error: str | None = None

    @property
    def all_text(self) -> str:
        return self.text + self.reasoning

    @property
    def output_tokens(self) -> int:
        if self.server_completion_tokens:
            return self.server_completion_tokens
        return max(1, len(self.all_text.split())) if self.all_text else 0

    @property
    def throughput_tps(self) -> float | None:
        if self.total_s and self.output_tokens:
            return self.output_tokens / self.total_s
        return None


async def chat_stream(
    client: httpx.AsyncClient,
    model: str,
    messages: list[dict],
    max_tokens: int = 256,
    temperature: float | None = None,
    seed: int | None = None,
) -> StreamResult:
    """Single streaming chat completion, returns StreamResult. Routes to Argo (closed-source
    models), Minerva (Always-Hot ALCF cluster), or Sophia (default open-weight models) based
    on which candidate list `model` is in — all three speak the same OpenAI-compatible SSE
    format, only the base URL/auth differ (Minerva reuses Sophia's ALCF_TOKEN).

    temperature/seed are omitted from the payload entirely when left as None, so existing
    callers keep the previous server-default behaviour byte-for-byte. Set them explicitly
    for experiments that need repeated samples to be a controlled, reportable condition —
    without them, "independent samples" are drawn at an unknown, provider-chosen
    temperature, which is not a documentable experimental parameter."""
    result = StreamResult()
    if model in ARGO_MODELS:
        base_url, headers = ARGO_URL, argo_auth()[0]
    elif model in MINERVA_MODELS:
        base_url, headers = MINERVA_URL, {
            "Authorization": f"Bearer {ALCF_TOKEN}",
            "Content-Type": "application/json",
        }
    else:
        base_url, headers = SOPHIA_URL, {
            "Authorization": f"Bearer {ALCF_TOKEN}",
            "Content-Type": "application/json",
        }
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "stream": True,
    }
    if temperature is not None:
        payload["temperature"] = temperature
    if seed is not None:
        payload["seed"] = seed
    t0 = time.perf_counter()
    first_token = False
    try:
        async with client.stream(
            "POST",
            f"{base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=httpx.Timeout(connect=CONNECT_TIMEOUT, read=READ_TIMEOUT,
                                  write=10.0, pool=10.0),
        ) as resp:
            resp.raise_for_status()
            async for raw in resp.aiter_lines():
                if not raw.startswith("data:"):
                    continue
                data = raw[5:].strip()
                if data == "[DONE]":
                    break
                try:
                    chunk = json.loads(data)
                except json.JSONDecodeError:
                    continue
                choices = chunk.get("choices", [])
                if choices:
                    delta = choices[0].get("delta", {})
                    content = delta.get("content") or ""
                    reasoning = delta.get("reasoning") or ""
                    token_text = content + reasoning
                    if token_text:
                        result.text += content
                        result.reasoning += reasoning
                        if not first_token:
                            result.ttft_s = time.perf_counter() - t0
                            first_token = True
                usage = chunk.get("usage")
                if usage and usage.get("completion_tokens"):
                    result.server_completion_tokens = usage["completion_tokens"]
        result.total_s = time.perf_counter() - t0
    except httpx.HTTPStatusError as e:
        result.error = f"HTTP {e.response.status_code}"
        result.total_s = time.perf_counter() - t0
    except Exception as e:
        result.error = str(e)[:120]
        result.total_s = time.perf_counter() - t0
    return result


def make_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(limits=httpx.Limits(max_connections=10))


async def chat_stream_retry(
    client: httpx.AsyncClient,
    model: str,
    messages: list[dict],
    max_tokens: int = 256,
    retries: int = 2,
    temperature: float | None = None,
    seed: int | None = None,
) -> StreamResult:
    """chat_stream() swallows HTTP errors/exceptions into StreamResult.error instead of
    raising, so a transient failure (rate limit, outage) silently looks like an empty
    response to callers that don't check .error — which then gets scored as flat 0%/wrong
    instead of being retried or surfaced. Use this wrapper anywhere a silent all-zero
    benchmark result would otherwise go unnoticed."""
    import asyncio

    async def _attempt() -> StreamResult:
        try:
            # Extra watchdog on top of chat_stream's own httpx timeouts — a streaming
            # response that trickles data just under the per-chunk read timeout can
            # otherwise stall far longer than any single call should reasonably take.
            return await asyncio.wait_for(
                chat_stream(client, model, messages, max_tokens=max_tokens,
                            temperature=temperature, seed=seed), timeout=150.0
            )
        except asyncio.TimeoutError:
            r = StreamResult()
            r.error = "watchdog timeout after 150s"
            return r

    r = await _attempt()
    attempt = 0
    while r.error and attempt < retries:
        attempt += 1
        await asyncio.sleep(5 * attempt)
        r = await _attempt()
    if r.error:
        print(f"    WARNING: {model} request failed after {retries} retries: {r.error}")
    return r
