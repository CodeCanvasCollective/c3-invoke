from __future__ import annotations

import shutil
import subprocess
import time
from abc import ABC, abstractmethod

from ..types import PromptRequest, PromptResponse, ProviderInfo


class BaseProvider(ABC):
    """Abstract base class for AI CLI providers."""

    @abstractmethod
    def info(self) -> ProviderInfo:
        """Return provider metadata (name, binary path, availability)."""

    @abstractmethod
    def build_command(self, request: PromptRequest) -> list[str]:
        """Build the CLI command arguments for the given request."""

    def is_available(self) -> bool:
        """Check if the CLI binary is installed and accessible."""
        return self.info().available

    def run(self, request: PromptRequest) -> PromptResponse:
        """Execute a prompt via the CLI subprocess."""
        info = self.info()
        if not info.available:
            return PromptResponse(
                raw_output="",
                provider=info.name,
                is_error=True,
                error_message=f"{info.display_name} not found in PATH.",
            )

        command = self.build_command(request)
        start = time.monotonic()
        try:
            result = self._execute(command, request)
            elapsed = time.monotonic() - start
            output = (result.stdout or "").strip()
            return PromptResponse(
                raw_output=output,
                provider=info.name,
                elapsed_seconds=round(elapsed, 3),
            )
        except subprocess.CalledProcessError as exc:
            elapsed = time.monotonic() - start
            fallback = self._handle_fallback(exc, request)
            if fallback is not None:
                total_elapsed = time.monotonic() - start
                return PromptResponse(
                    raw_output=(fallback.stdout or "").strip(),
                    provider=info.name,
                    elapsed_seconds=round(total_elapsed, 3),
                )
            stderr = (exc.stderr or "").strip()
            error_msg = stderr[:300] if stderr else f"CLI exited with code {exc.returncode}."
            return PromptResponse(
                raw_output="",
                provider=info.name,
                elapsed_seconds=round(elapsed, 3),
                is_error=True,
                error_message=error_msg,
            )
        except subprocess.TimeoutExpired:
            elapsed = time.monotonic() - start
            return PromptResponse(
                raw_output="",
                provider=info.name,
                elapsed_seconds=round(elapsed, 3),
                is_error=True,
                error_message=f"CLI timed out after {request.timeout}s.",
            )
        except Exception as exc:
            elapsed = time.monotonic() - start
            return PromptResponse(
                raw_output="",
                provider=info.name,
                elapsed_seconds=round(elapsed, 3),
                is_error=True,
                error_message=str(exc),
            )

    def _execute(
        self, command: list[str], request: PromptRequest
    ) -> subprocess.CompletedProcess[str]:
        """Run the subprocess command."""
        return subprocess.run(
            command,
            input=request.prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
            cwd=request.cwd,
            timeout=request.timeout,
        )

    def _handle_fallback(
        self,
        exc: subprocess.CalledProcessError,
        request: PromptRequest,
    ) -> subprocess.CompletedProcess[str] | None:
        """Override to provide fallback behavior on specific errors. Return None to propagate."""
        return None

    def _resolve_binary(self, *names: str) -> str:
        """Find the first available binary from the given names."""
        for name in names:
            path = shutil.which(name)
            if path:
                return path
        return ""
