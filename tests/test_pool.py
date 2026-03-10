"""Tests for c3_invoke.pool — parallel prompt execution."""

from unittest.mock import MagicMock, patch

from c3_invoke.pool import run_batch
from c3_invoke.types import PromptRequest, PromptResponse, ProviderInfo


class TestRunBatch:
    def _make_provider(self, responses: list[str]):
        """Create a mock provider that returns predefined responses."""
        provider = MagicMock()
        provider.info.return_value = ProviderInfo(
            name="mock", display_name="Mock", binary="/mock", available=True
        )

        call_idx = 0

        def mock_run(request):
            nonlocal call_idx
            idx = call_idx
            call_idx += 1
            return PromptResponse(
                raw_output=responses[idx] if idx < len(responses) else "",
                provider="mock",
            )

        provider.run.side_effect = mock_run
        return provider

    def test_empty_requests(self):
        provider = MagicMock()
        result = run_batch(provider, [])
        assert result == []

    def test_single_request(self):
        provider = self._make_provider(["response 1"])
        requests = [PromptRequest(prompt="test 1")]
        results = run_batch(provider, requests)
        assert len(results) == 1
        assert results[0].raw_output == "response 1"

    def test_multiple_requests_preserves_order(self):
        responses = ["a", "b", "c"]
        provider = MagicMock()
        provider.info.return_value = ProviderInfo(
            name="mock", display_name="Mock", binary="/mock", available=True
        )

        # Each call returns a unique response based on prompt content
        def mock_run(request):
            idx = int(request.prompt.split()[-1])
            return PromptResponse(raw_output=f"response {idx}", provider="mock")

        provider.run.side_effect = mock_run

        requests = [PromptRequest(prompt=f"test {i}") for i in range(3)]
        results = run_batch(provider, requests, max_workers=2)

        assert len(results) == 3
        # Results should be in original order
        for i, result in enumerate(results):
            assert result.raw_output == f"response {i}"

    def test_error_handling(self):
        provider = MagicMock()
        provider.info.return_value = ProviderInfo(
            name="mock", display_name="Mock", binary="/mock", available=True
        )
        provider.run.side_effect = RuntimeError("CLI crashed")

        requests = [PromptRequest(prompt="test")]
        results = run_batch(provider, requests)
        assert len(results) == 1
        assert results[0].is_error is True
        assert "CLI crashed" in results[0].error_message
