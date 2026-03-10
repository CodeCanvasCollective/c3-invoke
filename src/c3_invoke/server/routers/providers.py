from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter, HTTPException

from ... import get_provider, list_providers

router = APIRouter(prefix="/providers", tags=["providers"])


@router.get("")
def get_providers() -> list[dict]:
    return [asdict(info) for info in list_providers()]


@router.get("/{name}/test")
def test_provider(name: str) -> dict:
    try:
        provider = get_provider(name)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Unknown provider: {name}")
    info = provider.info()
    return {
        "name": info.name,
        "display_name": info.display_name,
        "available": info.available,
        "binary": info.binary,
        "version": info.version,
    }
