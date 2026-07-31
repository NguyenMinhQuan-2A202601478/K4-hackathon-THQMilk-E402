from __future__ import annotations

from typing import Any


def ask_user(question: str, response_type: str = "text", options: list[str] | None = None) -> dict[str, Any]:
    return {
        "awaiting_user": True,
        "question": question,
        "response_type": response_type,
        "options": options or [],
    }
