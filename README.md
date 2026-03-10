# C3 Invoke

Unified interface to AI CLIs (Gemini, Claude, Codex) from Python or HTTP.

## Installation

```bash
pip install c3-invoke            # Core library (zero dependencies)
pip install c3-invoke[server]    # With FastAPI HTTP server
```

## Quick Start

```python
from c3_invoke import GeminiProvider, ClaudeProvider, parse_json_output
from c3_invoke.types import PromptRequest

# Call any AI CLI with a unified interface
gemini = GeminiProvider()
response = gemini.run(PromptRequest(prompt="Explain Python decorators"))
print(response.raw_output)

# Parse JSON from CLI output (handles markdown fences, embedded JSON)
data = parse_json_output(response.raw_output)

# Run multiple prompts in parallel
from c3_invoke import run_batch
responses = run_batch(gemini, [
    PromptRequest(prompt="Explain decorators"),
    PromptRequest(prompt="Explain generators"),
], max_workers=4)
```

## Providers

| Provider | CLI Binary | Status |
|----------|-----------|--------|
| `GeminiProvider` | `gemini` | Fully implemented |
| `ClaudeProvider` | `claude` | Fully implemented |
| `CodexProvider` | `codex` | Fully implemented |

```python
from c3_invoke import get_provider, list_providers

# Get a specific provider
provider = get_provider("claude")

# List all providers with availability status
for info in list_providers():
    print(f"{info.display_name}: {'available' if info.available else 'not found'}")
```

## HTTP Server

```bash
pip install c3-invoke[server]
c3-invoke-server    # Starts on port 8766
```

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Server status + available providers |
| `/providers` | GET | List all providers with availability |
| `/providers/{name}/test` | GET | Test specific provider |
| `/prompt` | POST | Send a single prompt to a provider |
| `/batch` | POST | Send multiple prompts in parallel |

### Example

```bash
# Single prompt
curl -X POST http://localhost:8766/prompt \
  -H "Content-Type: application/json" \
  -d '{"provider": "gemini", "prompt": "What is Python?"}'

# Batch prompts
curl -X POST http://localhost:8766/batch \
  -H "Content-Type: application/json" \
  -d '{"provider": "gemini", "prompts": [{"prompt": "Q1"}, {"prompt": "Q2"}]}'
```

## Development

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

## Architecture

```
src/c3_invoke/
├── __init__.py             # Public API: get_provider(), list_providers()
├── types.py                # PromptRequest, PromptResponse, ProviderInfo
├── output.py               # parse_json_output()
├── pool.py                 # run_batch() — parallel execution
├── providers/
│   ├── base.py             # BaseProvider ABC
│   ├── gemini.py           # GeminiProvider
│   ├── claude.py           # ClaudeProvider
│   └── codex.py            # CodexProvider
└── server/                 # Optional FastAPI server
    ├── app.py
    ├── main.py
    └── routers/
```

## Part of C3 Ecosystem

C3 Invoke is a standalone package in the [C3 organization](https://github.com/C3) ecosystem. See the [C3 Architecture Overview](https://github.com/C3/job-compass/blob/main/docs/C3-ORGANIZATION.md) for how it fits with Job Compass and C3 CLI Desktop.
