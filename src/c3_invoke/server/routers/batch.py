from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ... import get_provider
from ...pool import run_batch
from ...types import OutputFormat, PromptRequest

router = APIRouter(tags=["batch"])


class BatchPromptItem(BaseModel):
    prompt: str
    timeout: int = Field(default=90, ge=1, le=600)
    output_format: str = Field(default="text")
    model: str | None = Field(default=None)
    extra_flags: list[str] = Field(default_factory=list)
    cwd: str | None = Field(default=None)


class BatchBody(BaseModel):
    provider: str = Field(description="Provider name: gemini, claude, or codex")
    prompts: list[BatchPromptItem] = Field(min_length=1, max_length=20)
    max_workers: int = Field(default=4, ge=1, le=10)


@router.post("/batch")
def run_batch_prompts(body: BatchBody) -> list[dict]:
    try:
        provider = get_provider(body.provider)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Unknown provider: {body.provider}")

    requests = []
    for item in body.prompts:
        try:
            fmt = OutputFormat(item.output_format)
        except ValueError:
            fmt = OutputFormat.TEXT
        requests.append(
            PromptRequest(
                prompt=item.prompt,
                timeout=item.timeout,
                output_format=fmt,
                model=item.model,
                extra_flags=item.extra_flags,
                cwd=item.cwd,
            )
        )

    responses = run_batch(provider, requests, max_workers=body.max_workers)
    return [asdict(r) for r in responses]
