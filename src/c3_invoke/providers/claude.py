from __future__ import annotations

from ..types import PromptRequest, ProviderInfo
from .base import BaseProvider


class ClaudeProvider(BaseProvider):
    """Provider for the Claude CLI (Anthropic)."""

    def info(self) -> ProviderInfo:
        binary = self._resolve_binary("claude")
        return ProviderInfo(
            name="claude",
            display_name="Claude CLI",
            binary=binary,
            available=bool(binary),
        )

    def build_command(self, request: PromptRequest) -> list[str]:
        binary = self.info().binary
        if not binary:
            binary = "claude"
        cmd = [binary, "--print", "--output-format", "text"]
        if request.model:
            cmd.extend(["--model", request.model])
        cmd.extend(request.extra_flags)
        return cmd
