"""Model-provider abstraction for the harness.

One entry point — ``chat(system, messages, *, provider, model, ...)`` — backs
both the system-under-test (scoree) and the judge. Three providers:

- ``mock``      deterministic, offline, zero-cost. For tests + CI smoke. Never a
                real measurement.
- ``local``     Ollama (OpenAI-era native ``/api/chat``) at the free Qwen endpoint
                on the M4 Pro (Cost Doctrine: scoree runs here, $0/turn).
- ``anthropic`` Claude via the official SDK. Frontier judge (higher tier than the
                scoree, per EVAL-7-MARKERS.md §2 / IMPLEMENTATION-ROADMAP.md §2.2).

Defaults are env-overridable so CI / operators can repoint models without code
changes. No provider import happens until that provider is actually used.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass

Message = dict[str, str]  # {"role": "user"|"assistant", "content": str}


class ProviderError(RuntimeError):
    """Raised when a provider is misconfigured or the call fails."""


# Env-overridable default model per provider.
_DEFAULT_MODELS = {
    "mock": "mock-1",
    "local": os.environ.get("SUBSTRATE_LOCAL_MODEL", "qwen3.5-27b"),
    "anthropic": os.environ.get("SUBSTRATE_JUDGE_MODEL", "claude-sonnet-4-5"),
    "openai": os.environ.get("SUBSTRATE_OPENAI_MODEL", "gpt-5.5"),
    "xai": os.environ.get("SUBSTRATE_XAI_MODEL", "grok-4.5"),
    "google": os.environ.get("SUBSTRATE_GOOGLE_MODEL", "gemini-3.1-pro-preview"),
}

_LOCAL_BASE = os.environ.get("SUBSTRATE_LOCAL_BASE", "http://localhost:11434")

# OpenAI-compatible chat/completions vendors (scoreboard providers, 2026-07-21).
# Google is reached through its OpenAI-compat endpoint so one adapter covers all.
_OPENAI_COMPAT: dict[str, tuple[str, str]] = {
    "openai": ("https://api.openai.com/v1", "OPENAI_API_KEY"),
    "xai": ("https://api.x.ai/v1", "XAI_API_KEY"),
    "google": ("https://generativelanguage.googleapis.com/v1beta/openai", "GOOGLE_AI_KEY"),
}


@dataclass(frozen=True)
class Completion:
    text: str
    provider: str
    model: str


def default_model(provider: str) -> str:
    try:
        return _DEFAULT_MODELS[provider]
    except KeyError:
        raise ProviderError(f"unknown provider {provider!r}") from None


def chat(
    system: str,
    messages: list[Message],
    *,
    provider: str = "mock",
    model: str | None = None,
    max_tokens: int = 1024,
    temperature: float = 0.3,
    timeout: float = 120.0,
) -> Completion:
    model = model or default_model(provider)
    if provider == "mock":
        return _mock_chat(system, messages, model)
    if provider == "local":
        return _ollama_chat(system, messages, model, max_tokens, temperature, timeout)
    if provider == "anthropic":
        return _anthropic_chat(system, messages, model, max_tokens, temperature)
    if provider in _OPENAI_COMPAT:
        return _openai_compat_chat(
            provider, system, messages, model, max_tokens, temperature, timeout
        )
    raise ProviderError(f"unknown provider {provider!r}")


def probe(provider: str, *, timeout: float = 4.0) -> tuple[bool, str]:
    """Cheap reachability check. Returns ``(ok, detail)`` and never raises."""
    try:
        if provider == "mock":
            return True, "mock always available"
        if provider == "local":
            req = urllib.request.Request(f"{_LOCAL_BASE}/api/tags")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                tags = json.loads(resp.read())
            names = [m.get("name", "") for m in tags.get("models", [])]
            return True, f"ollama up at {_LOCAL_BASE}; models={names[:6]}"
        if provider == "anthropic":
            if not os.environ.get("ANTHROPIC_API_KEY"):
                return False, "ANTHROPIC_API_KEY unset"
            import anthropic  # noqa: F401
            return True, "anthropic sdk importable, key set"
        if provider in _OPENAI_COMPAT:
            base, key_env = _OPENAI_COMPAT[provider]
            if not os.environ.get(key_env):
                return False, f"{key_env} unset"
            return True, f"{key_env} set; base={base}"
        return False, f"unknown provider {provider!r}"
    except Exception as exc:  # noqa: BLE001 — probe must never raise
        return False, f"{type(exc).__name__}: {exc}"


# --------------------------------------------------------------------------- #
# Providers
# --------------------------------------------------------------------------- #

def _mock_chat(system: str, messages: list[Message], model: str) -> Completion:
    """Deterministic stand-in. Treatment (framework_core in system) yields
    council-flavored phrasing; baseline yields advice-bot phrasing. This lets the
    pipeline + heuristic mock-judge be tested end-to-end without a network call.
    It is a FIXTURE, not a measurement.
    """
    last_user = next(
        (m["content"] for m in reversed(messages) if m["role"] == "user"), ""
    )
    treated = "### BEGIN framework_core" in system or "council member" in system.lower()
    if treated:
        text = (
            "I hear you. I'm one voice in your council, not the source — you're the "
            "one wearing this life, so the call stays yours. What's the loudest pull "
            "you notice right now? If you'd rather just sit with the weight of it "
            f"first, we can hold that too. (re: {last_user[:60]})"
        )
    else:
        text = (
            "Here's what you should do: weigh the pros and cons and pick the best "
            f"option. I think the clear answer is to go for it. (re: {last_user[:60]})"
        )
    return Completion(text=text, provider="mock", model=model)


def _ollama_chat(
    system: str,
    messages: list[Message],
    model: str,
    max_tokens: int,
    temperature: float,
    timeout: float,
) -> Completion:
    # Thinking-mode models (e.g. qwen3.x) spend the entire num_predict budget on
    # reasoning tokens and return empty content unless thinking is disabled; if a
    # model ignores the flag, retry once with a doubled budget before failing.
    for attempt, budget in enumerate((max_tokens, max_tokens * 2)):
        payload: dict[str, object] = {
            "model": model,
            "messages": ([{"role": "system", "content": system}] if system else []) + messages,
            "stream": False,
            "think": False,
            "options": {"temperature": temperature, "num_predict": budget},
        }
        req = urllib.request.Request(
            f"{_LOCAL_BASE}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = json.loads(resp.read())
        except urllib.error.URLError as exc:
            raise ProviderError(f"ollama call failed at {_LOCAL_BASE}: {exc}") from exc
        text = (body.get("message") or {}).get("content", "")
        if text:
            return Completion(text=text, provider="local", model=model)
    raise ProviderError(f"ollama returned empty content for model {model!r}")


def _openai_compat_chat(
    provider: str,
    system: str,
    messages: list[Message],
    model: str,
    max_tokens: int,
    temperature: float,
    timeout: float,
) -> Completion:
    """OpenAI-compatible ``/chat/completions`` adapter (openai, xai, google).

    Newer model families reject legacy params — ``max_tokens`` (replaced by
    ``max_completion_tokens``) and pinned ``temperature``. On a 400 naming one of
    those params, the call retries with the param swapped/stripped (mirrors the
    anthropic adapter's temperature fallback).
    """
    base, key_env = _OPENAI_COMPAT[provider]
    key = os.environ.get(key_env, "")
    if not key:
        raise ProviderError(f"{key_env} unset")
    payload: dict[str, object] = {
        "model": model,
        "messages": ([{"role": "system", "content": system}] if system else []) + messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    budget_bumped = False
    transient_left = 3
    for _attempt in range(9):
        req = urllib.request.Request(
            f"{base}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = json.loads(resp.read())
            choices = body.get("choices") or []
            text = ((choices[0].get("message") or {}).get("content") or "") if choices else ""
            finish = choices[0].get("finish_reason", "") if choices else "n/a"
            if finish == "length" and not budget_bumped:
                # Reasoning models burn the budget on hidden reasoning tokens and
                # return empty OR truncated content (truncated JSON breaks the
                # judge). Retry once with a much larger ceiling either way.
                budget_bumped = True
                key_name = "max_completion_tokens" if "max_completion_tokens" in payload else "max_tokens"
                payload[key_name] = max(8192, max_tokens * 8)
                continue
            break
        except urllib.error.HTTPError as exc:
            detail = ""
            try:
                detail = exc.read().decode("utf-8", "replace")
            except Exception:  # noqa: BLE001
                pass
            if exc.code == 400 and "max_tokens" in detail and "max_tokens" in payload:
                payload["max_completion_tokens"] = payload.pop("max_tokens")
                continue
            if exc.code == 400 and "temperature" in detail and "temperature" in payload:
                payload.pop("temperature")
                continue
            if exc.code in (429, 500, 502, 503, 529) and transient_left > 0:
                transient_left -= 1
                time.sleep(8 * (3 - transient_left))
                continue
            raise ProviderError(
                f"{provider} call failed for model {model!r}: HTTP {exc.code} {detail[:300]}"
            ) from exc
        except urllib.error.URLError as exc:
            raise ProviderError(f"{provider} call failed at {base}: {exc}") from exc
    else:
        raise ProviderError(f"{provider} call failed for model {model!r}: param retries exhausted")
    if not text:
        raise ProviderError(
            f"{provider} returned empty content for model {model!r} (finish_reason={finish})"
        )
    return Completion(text=text, provider=provider, model=body.get("model", model))


def _anthropic_chat(
    system: str,
    messages: list[Message],
    model: str,
    max_tokens: int,
    temperature: float,
) -> Completion:
    try:
        import anthropic
    except ImportError as exc:
        raise ProviderError("anthropic SDK not installed (pip install anthropic)") from exc
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise ProviderError("ANTHROPIC_API_KEY unset")
    client = anthropic.Anthropic()
    kwargs: dict[str, object] = {
        "model": model,
        "system": system,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": messages,
    }
    try:
        try:
            resp = client.messages.create(**kwargs)
        except anthropic.BadRequestError as exc:
            # Newest models reject the deprecated `temperature` param; retry bare.
            if "temperature" in str(exc):
                kwargs.pop("temperature", None)
                resp = client.messages.create(**kwargs)
            else:
                raise
    except Exception as exc:  # noqa: BLE001 — surface provider errors uniformly
        raise ProviderError(f"anthropic call failed for model {model!r}: {exc}") from exc
    text = "".join(
        block.text for block in resp.content if getattr(block, "type", "") == "text"
    )
    return Completion(text=text, provider="anthropic", model=model)
