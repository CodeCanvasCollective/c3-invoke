"""Tests for the public API surface."""

from unittest.mock import patch

from c3_invoke import (
    GeminiProvider,
    ClaudeProvider,
    CodexProvider,
    get_provider,
    list_providers,
    parse_json_output,
    run_batch,
)


def test_get_provider_gemini():
    provider = get_provider("gemini")
    assert isinstance(provider, GeminiProvider)


def test_get_provider_claude():
    provider = get_provider("claude")
    assert isinstance(provider, ClaudeProvider)


def test_get_provider_codex():
    provider = get_provider("codex")
    assert isinstance(provider, CodexProvider)


def test_get_provider_case_insensitive():
    provider = get_provider("GEMINI")
    assert isinstance(provider, GeminiProvider)


def test_get_provider_unknown():
    import pytest
    with pytest.raises(KeyError, match="Unknown provider"):
        get_provider("unknown")


def test_list_providers():
    with patch("shutil.which", return_value=None):
        infos = list_providers()
    assert len(infos) == 3
    names = {info.name for info in infos}
    assert names == {"gemini", "claude", "codex"}


def test_public_exports():
    """Verify all public names are importable."""
    assert parse_json_output is not None
    assert run_batch is not None
