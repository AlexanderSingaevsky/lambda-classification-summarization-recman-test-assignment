from __future__ import annotations

from typing import List, Literal, Protocol, TypedDict, Optional

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from src.settings import get_settings


class ChatMessage(TypedDict):
    role: Literal["system", "human", "assistant"]
    content: str


class LLMClient(Protocol):
    def generate(self, messages: List[ChatMessage]) -> str:  # returns assistant content
        ...


class OpenAIClient:
    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        temperature: float = 0.0,
    ) -> None:
        settings = get_settings()
        model_to_use = model or settings.llm_model_name or "gpt-4o-mini"
        api_key_to_use = api_key or settings.llm_api_key or None
        self.llm = ChatOpenAI(model=model_to_use, temperature=temperature, api_key=api_key_to_use)

    def generate(self, messages: List[ChatMessage]) -> str:
        response = self.llm.invoke(messages)
        return response.content if hasattr(response, "content") else str(response)


class AnthropicClient:
    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        temperature: float = 0.0,
    ) -> None:
        settings = get_settings()
        model_to_use = model or settings.llm_model_name or "claude-3-5-sonnet-latest"
        api_key_to_use = api_key or settings.llm_api_key or None
        self.llm = ChatAnthropic(model=model_to_use, temperature=temperature, api_key=api_key_to_use)

    def generate(self, messages: List[ChatMessage]) -> str:
        response = self.llm.invoke(messages)
        return response.content if hasattr(response, "content") else str(response)
