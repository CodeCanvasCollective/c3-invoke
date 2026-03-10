from __future__ import annotations

from fastapi import FastAPI

from .routers import batch, health, prompt, providers


def create_app() -> FastAPI:
    app = FastAPI(
        title="C3 Invoke",
        description="Unified HTTP API for AI CLI providers",
        version="0.1.0",
    )
    app.include_router(health.router)
    app.include_router(providers.router)
    app.include_router(prompt.router)
    app.include_router(batch.router)
    return app
