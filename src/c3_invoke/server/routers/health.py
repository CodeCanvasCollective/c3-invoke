from __future__ import annotations

from fastapi import APIRouter

from ...providers import GeminiProvider, ClaudeProvider, CodexProvider

router = APIRouter()

_PROVIDERS = [GeminiProvider(), ClaudeProvider(), CodexProvider()]


@router.get("/health")
def health() -> dict:
    available = [p.info().name for p in _PROVIDERS if p.is_available()]
    return {
        "status": "ok",
        "version": "0.1.0",
        "providers_available": available,
    }
