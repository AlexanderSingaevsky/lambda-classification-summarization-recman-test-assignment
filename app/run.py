from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any, Dict

from src.handler import handler


def _configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run classifier/summarizer locally")
    parser.add_argument("--input", required=True, help="Path to JSON file with items (array or {items: [...]})")
    parser.add_argument("--mode", choices=["classify", "summarize"], default="classify")
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()

    _configure_logging(args.log_level)

    input_path = Path(args.input)
    data: Any
    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    event: Dict[str, Any]
    if isinstance(data, dict):
        event = {"mode": args.mode, "items": data.get("items", [])}
    else:
        event = {"mode": args.mode, "items": data}

    result = handler(event, context=None)

    # Print body as pretty JSON for local run
    body = result.get("body")
    try:
        parsed = json.loads(body) if isinstance(body, str) else body
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
    except Exception:
        print(body)


if __name__ == "__main__":
    main()
