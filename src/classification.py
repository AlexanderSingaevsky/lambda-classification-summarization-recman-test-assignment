from __future__ import annotations

from typing import List

from langchain_core.prompts import ChatPromptTemplate

from src.schemas import (
    ClassificationInput,
    ClassificationOutputItem,
    EmailItem,
    ClassificationTopics,
)
from src.llm import LLMClient


class EmailClassifier:
    def __init__(self, client: LLMClient) -> None:
        self.client = client
        self.allowed_topics = ", ".join(t.value for t in ClassificationTopics)
        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a precise assistant that classifies short emails into predefined topics. "
                "Only choose topics from the allowed set. If content is empty or meaningless, return an empty list.",
            ),
            (
                "system",
                "Allowed topics: {allowed_topics}",
            ),
            (
                "human",
                "Classify the following email. Respond ONLY with a JSON array of topics.\n"
                "Subject: {subject}\n\nBody: {body}",
            ),
        ])

    def _parse_topics(self, content: str) -> List[str]:
        import json

        try:
            parsed = json.loads(content)
            if isinstance(parsed, list):
                normalized = []
                allowed = {t.value for t in ClassificationTopics}
                for item in parsed:
                    if isinstance(item, str):
                        v = item.strip().lower()
                        if v in allowed:
                            normalized.append(v)
                return normalized
        except Exception:
            pass
        return []

    def _classify_item(self, item: EmailItem) -> ClassificationOutputItem:
        subject = (item.subject or "").strip()
        body = (item.body or "").strip()
        if not subject and not body:
            return ClassificationOutputItem(id=item.id, error="empty_input")

        messages = self.prompt.format_messages(
            allowed_topics=self.allowed_topics,
            subject=subject,
            body=body,
        )
        content = self.client.generate([
            {"role": m.type, "content": m.content} for m in messages
        ])
        topics = self._parse_topics(content)
        return ClassificationOutputItem(id=item.id, topics=topics)

    def classify(self, request: ClassificationInput) -> List[ClassificationOutputItem]:
        results: List[ClassificationOutputItem] = []
        for item in request.items:
            results.append(self._classify_item(item))
        return results