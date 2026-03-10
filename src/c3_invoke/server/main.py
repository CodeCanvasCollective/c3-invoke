from __future__ import annotations

import sys


def main() -> None:
    try:
        import uvicorn
    except ImportError:
        print("Error: uvicorn not installed. Run: pip install c3-invoke[server]", file=sys.stderr)
        sys.exit(1)

    uvicorn.run(
        "c3_invoke.server.app:create_app",
        factory=True,
        host="0.0.0.0",
        port=8766,
        reload=False,
    )


if __name__ == "__main__":
    main()
