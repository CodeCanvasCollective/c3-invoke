from __future__ import annotations

from ..types import PromptRequest, ProviderInfo
from .base import BaseProvider


class CodexProvider(BaseProvider):
    """Provider for the Codex CLI (OpenAI)."""

    def info(self) -> ProviderInfo:
        binary = self._resolve_binary("codex")
        return ProviderInfo(
            name="codex",
            display_name="Codex CLI",
            binary=binary,
            available=bool(binary),
        )

    def build_command(self, request: PromptRequest) -> list[str]:
        binary = self.info().binary
        if not binary:
            binary = "codex"
        cmd = [binary, "--quiet"]
        if request.model:
            cmd.extend(["--model", request.model])
        cmd.extend(request.extra_flags)
        return cmd
