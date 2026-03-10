from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class OutputFormat(Enum):
    TEXT = "text"
    JSON = "json"
    MARKDOWN = "markdown"


@dataclass(frozen=True)
class PromptRequest:
    """A request to send a prompt to an AI CLI provider."""

    prompt: str
    timeout: int = 90
    output_format: OutputFormat = OutputFormat.TEXT
    model: str | None = None
    extra_flags: list[str] = field(default_factory=list)
    cwd: str | None = None


@dataclass(frozen=True)
class PromptResponse:
    """The response from an AI CLI provider."""

    raw_output: str
    parsed: Any = None
    provider: str = ""
    model: str = ""
    elapsed_seconds: float = 0.0
    is_error: bool = False
    error_message: str = ""


@dataclass(frozen=True)
class ProviderInfo:
    """Metadata about an AI CLI provider."""

    name: str
    display_name: str
    binary: str
    available: bool
    version: str = ""
