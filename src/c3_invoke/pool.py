from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

    from .providers.base import BaseProvider
    from .types import PromptRequest, PromptResponse


def run_batch(
    provider: BaseProvider,
    requests: Sequence[PromptRequest],
    max_workers: int = 4,
) -> list[PromptResponse]:
    """Run multiple prompts in parallel using a thread pool."""
    if not requests:
        return []

    if len(requests) == 1:
        try:
            return [provider.run(requests[0])]
        except Exception as exc:
            from .types import PromptResponse as PR

            return [PR(
                raw_output="",
                provider=provider.info().name,
                is_error=True,
                error_message=str(exc),
            )]

    results: list[tuple[int, PromptResponse]] = []
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(provider.run, req): idx
            for idx, req in enumerate(requests)
        }
        for future in as_completed(futures):
            idx = futures[future]
            try:
                response = future.result()
            except Exception as exc:
                from .types import PromptResponse as PR

                response = PR(
                    raw_output="",
                    provider=provider.info().name,
                    is_error=True,
                    error_message=str(exc),
                )
            results.append((idx, response))

    results.sort(key=lambda item: item[0])
    return [resp for _, resp in results]
