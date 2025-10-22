import json
from typing import Any, Dict, List

from src.schemas import ClassificationInput, ClassificationOutputItem, EmailItem
from src.classification import EmailClassifier
from src.llm import OpenAIClient


def _normalize_items(event: Any) -> List[EmailItem]:
    if isinstance(event, list):
        raw_items = event
    elif isinstance(event, dict):
        if "items" in event and isinstance(event["items"], list):
            raw_items = event["items"]
        elif "body" in event:
            try:
                body = event["body"] if isinstance(event["body"], str) else json.dumps(event["body"])
                raw_items = json.loads(body)
                if isinstance(raw_items, dict) and "items" in raw_items:
                    raw_items = raw_items["items"]
            except Exception:
                raw_items = []
        else:
            raw_items = []
    else:
        raw_items = []

    items: List[EmailItem] = []
    for r in raw_items:
        try:
            items.append(EmailItem(**r))
        except Exception:
            # skip malformed items
            continue
    return items


def handler(event: Any, context: Any) -> Dict[str, Any]:
    mode = None
    if isinstance(event, dict):
        mode = event.get("mode")
        if not mode and "queryStringParameters" in event:
            q = event.get("queryStringParameters") or {}
            mode = q.get("mode")
    mode = (mode or "classify").strip().lower()

    if mode == "classify":
        items = _normalize_items(event)
        request = ClassificationInput(items=items)
        client = OpenAIClient()
        classifier = EmailClassifier(client)
        outputs: List[ClassificationOutputItem] = classifier.classify(request)
        body = [o.model_dump() for o in outputs]
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(body),
        }

    if mode == "summarize":
        # Placeholder for summarization implementation
        return {
            "statusCode": 501,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "summarization_not_implemented"}),
        }

    return {
        "statusCode": 400,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"error": "invalid_mode"}),
    }
