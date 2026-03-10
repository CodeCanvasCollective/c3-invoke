from __future__ import annotations

import subprocess

from ..types import PromptRequest, ProviderInfo
from .base import BaseProvider


class GeminiProvider(BaseProvider):
    """Provider for the Gemini CLI (Google AI)."""

    def info(self) -> ProviderInfo:
        binary = self._resolve_binary("gemini")
        return ProviderInfo(
            name="gemini",
            display_name="Gemini CLI",
            binary=binary,
            available=bool(binary),
        )

    def build_command(self, request: PromptRequest) -> list[str]:
        binary = self.info().binary
        if not binary:
            binary = "gemini"
        cmd = [binary, "-p", "", "-o", "text", "--allowed-mcp-server-names", ""]
        cmd.extend(request.extra_flags)
        return cmd

    def _handle_fallback(
        self,
        exc: subprocess.CalledProcessError,
        request: PromptRequest,
    ) -> subprocess.CompletedProcess[str] | None:
        """Fall back to command without --allowed-mcp-server-names if unsupported."""
        stderr = (exc.stderr or "").lower()
        if any(
            token in stderr
            for token in ("unknown option", "unknown argument", "not recognized")
        ):
            binary = self.info().binary or "gemini"
            fallback_cmd = [binary, "-p", "", "-o", "text"]
            fallback_cmd.extend(request.extra_flags)
            return subprocess.run(
                fallback_cmd,
                input=request.prompt,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
                cwd=request.cwd,
                timeout=request.timeout,
            )
        return None
