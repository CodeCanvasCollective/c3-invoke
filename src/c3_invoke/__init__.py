"""C3 Invoke — Unified interface to AI CLIs (Gemini, Claude, Codex)."""

from __future__ import annotations

from .output import parse_json_output
from .pool import run_batch
from .providers.base import BaseProvider
from .providers.claude import ClaudeProvider
from .providers.codex import CodexProvider
from .providers.gemini import GeminiProvider
from .types import OutputFormat, PromptRequest, PromptResponse, ProviderInfo

__all__ = [
    "BaseProvider",
    "ClaudeProvider",
    "CodexProvider",
    "GeminiProvider",
    "OutputFormat",
    "PromptRequest",
    "PromptResponse",
    "ProviderInfo",
    "get_provider",
    "list_providers",
    "parse_json_output",
    "run_batch",
]

_PROVIDERS: dict[str, BaseProvider] = {
    "gemini": GeminiProvider(),
    "claude": ClaudeProvider(),
    "codex": CodexProvider(),
}


def get_provider(name: str) -> BaseProvider:
    """Get a provider instance by name."""
    try:
        return _PROVIDERS[name.lower()]
    except KeyError:
        raise KeyError(f"Unknown provider: {name!r}. Available: {list(_PROVIDERS)}")


def list_providers() -> list[ProviderInfo]:
    """List all registered providers with their availability status."""
    return [p.info() for p in _PROVIDERS.values()]
