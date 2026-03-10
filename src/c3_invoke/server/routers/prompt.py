from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ... import get_provider
from ...types import OutputFormat, PromptRequest

router = APIRouter(tags=["prompt"])


class PromptBody(BaseModel):
    provider: str = Field(description="Provider name: gemini, claude, or codex")
    prompt: str = Field(description="The prompt text to send")
    timeout: int = Field(default=90, ge=1, le=600)
    output_format: str = Field(default="text")
    model: str | None = Field(default=None)
    extra_flags: list[str] = Field(default_factory=list)
    cwd: str | None = Field(default=None)


@router.post("/prompt")
def run_prompt(body: PromptBody) -> dict:
    try:
        provider = get_provider(body.provider)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Unknown provider: {body.provider}")

    try:
        fmt = OutputFormat(body.output_format)
    except ValueError:
        fmt = OutputFormat.TEXT

    request = PromptRequest(
        prompt=body.prompt,
        timeout=body.timeout,
        output_format=fmt,
        model=body.model,
        extra_flags=body.extra_flags,
        cwd=body.cwd,
    )
    response = provider.run(request)
    return asdict(response)
