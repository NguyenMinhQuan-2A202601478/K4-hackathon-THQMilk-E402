from __future__ import annotations

from typing import Any


def render_digest(content: str) -> dict[str, Any]:
    return {
        "status": "success",
        "formatted_content": content,
    }
