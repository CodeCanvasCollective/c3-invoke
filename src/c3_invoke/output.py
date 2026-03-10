from __future__ import annotations

import json
from typing import Any


def parse_json_output(output: str) -> Any:
    """Parse JSON from AI CLI output, handling markdown fences and embedded JSON."""
    text = (output or "").strip()
    if not text:
        raise ValueError("CLI returned empty output.")

    if text.startswith("```json"):
        text = text[7:].strip()
        if text.endswith("```"):
            text = text[:-3].strip()
    elif text.startswith("```"):
        text = text[3:].strip()
        if text.endswith("```"):
            text = text[:-3].strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        decoder = json.JSONDecoder()
        for index, char in enumerate(text):
            if char not in "[{":
                continue
            try:
                parsed, _ = decoder.raw_decode(text[index:])
                return parsed
            except json.JSONDecodeError:
                continue

    preview = text[:200].replace("\n", " ")
    raise ValueError(f"CLI did not return valid JSON. Output preview: {preview}")
