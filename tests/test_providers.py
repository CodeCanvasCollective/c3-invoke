"""Tests for AI CLI providers."""

import subprocess
from unittest.mock import MagicMock, patch

import pytest

from c3_invoke.providers.gemini import GeminiProvider
from c3_invoke.providers.claude import ClaudeProvider
from c3_invoke.providers.codex import CodexProvider
from c3_invoke.types import PromptRequest, PromptResponse


class TestGeminiProvider:
    def test_info_when_available(self):
        provider = GeminiProvider()
        with patch("shutil.which", return_value="/usr/bin/gemini"):
            info = provider.info()
        assert info.name == "gemini"
        assert info.display_name == "Gemini CLI"
        assert info.available is True
        assert info.binary == "/usr/bin/gemini"

    def test_info_when_not_available(self):
        provider = GeminiProvider()
        with patch("shutil.which", return_value=None):
            info = provider.info()
        assert info.available is False
        assert info.binary == ""

    def test_build_command(self):
        provider = GeminiProvider()
        with patch("shutil.which", return_value="/usr/bin/gemini"):
            cmd = provider.build_command(PromptRequest(prompt="test"))
        assert cmd[0] == "/usr/bin/gemini"
        assert "-p" in cmd
        assert "-o" in cmd
        assert "text" in cmd
        assert "--allowed-mcp-server-names" in cmd

    def test_build_command_with_extra_flags(self):
        provider = GeminiProvider()
        with patch("shutil.which", return_value="/usr/bin/gemini"):
            cmd = provider.build_command(PromptRequest(prompt="test", extra_flags=["--debug"]))
        assert "--debug" in cmd

    def test_run_success(self):
        provider = GeminiProvider()
        mock_result = MagicMock()
        mock_result.stdout = "Hello from Gemini"
        mock_result.returncode = 0

        with patch("shutil.which", return_value="/usr/bin/gemini"), \
             patch("subprocess.run", return_value=mock_result):
            response = provider.run(PromptRequest(prompt="test"))

        assert response.raw_output == "Hello from Gemini"
        assert response.provider == "gemini"
        assert response.is_error is False

    def test_run_not_available(self):
        provider = GeminiProvider()
        with patch("shutil.which", return_value=None):
            response = provider.run(PromptRequest(prompt="test"))

        assert response.is_error is True
        assert "not found" in response.error_message

    def test_run_with_fallback(self):
        provider = GeminiProvider()

        # First call raises with "unknown option", second call succeeds
        error = subprocess.CalledProcessError(1, "gemini")
        error.stderr = "unknown option: --allowed-mcp-server-names"

        mock_fallback = MagicMock()
        mock_fallback.stdout = "Fallback response"

        call_count = 0

        def mock_run(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise error
            return mock_fallback

        with patch("shutil.which", return_value="/usr/bin/gemini"), \
             patch("subprocess.run", side_effect=mock_run):
            response = provider.run(PromptRequest(prompt="test"))

        assert response.raw_output == "Fallback response"
        assert response.is_error is False

    def test_run_timeout(self):
        provider = GeminiProvider()

        with patch("shutil.which", return_value="/usr/bin/gemini"), \
             patch("subprocess.run", side_effect=subprocess.TimeoutExpired("gemini", 90)):
            response = provider.run(PromptRequest(prompt="test", timeout=90))

        assert response.is_error is True
        assert "timed out" in response.error_message


class TestClaudeProvider:
    def test_info(self):
        provider = ClaudeProvider()
        with patch("shutil.which", return_value="/usr/bin/claude"):
            info = provider.info()
        assert info.name == "claude"
        assert info.display_name == "Claude CLI"
        assert info.available is True

    def test_build_command(self):
        provider = ClaudeProvider()
        with patch("shutil.which", return_value="/usr/bin/claude"):
            cmd = provider.build_command(PromptRequest(prompt="test"))
        assert cmd[0] == "/usr/bin/claude"
        assert "--print" in cmd
        assert "--output-format" in cmd

    def test_build_command_with_model(self):
        provider = ClaudeProvider()
        with patch("shutil.which", return_value="/usr/bin/claude"):
            cmd = provider.build_command(PromptRequest(prompt="test", model="sonnet"))
        assert "--model" in cmd
        assert "sonnet" in cmd


class TestCodexProvider:
    def test_info(self):
        provider = CodexProvider()
        with patch("shutil.which", return_value="/usr/bin/codex"):
            info = provider.info()
        assert info.name == "codex"
        assert info.display_name == "Codex CLI"

    def test_build_command(self):
        provider = CodexProvider()
        with patch("shutil.which", return_value="/usr/bin/codex"):
            cmd = provider.build_command(PromptRequest(prompt="test"))
        assert cmd[0] == "/usr/bin/codex"
        assert "--quiet" in cmd
