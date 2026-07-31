from __future__ import annotations

from typing import Any

from codebase.providers.base import Provider
from codebase.providers.openai_provider import OpenAIProvider


def make_provider(name: str = "openai", **kwargs: Any) -> Provider:
    name_lower = name.lower()
    if name_lower == "openai":
        return OpenAIProvider(**kwargs)
    # Default fallback to OpenAIProvider
    return OpenAIProvider(**kwargs)
