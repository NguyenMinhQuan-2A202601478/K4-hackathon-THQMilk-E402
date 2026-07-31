from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None

from codebase.tools.clarify.tool import ask_user
from codebase.tools.format.tool import render_digest
from codebase.tools.discord_loader import load_and_group_messages
from codebase.tools.discord_summarizer import generate_daily_digest


TOOL_FUNCTIONS = {
    "clarify": ask_user,
    "format": render_digest,
    "load_discord_messages": load_and_group_messages,
    "generate_discord_digest": generate_daily_digest,
}


def load_tool_declarations(path: Path) -> list[dict[str, Any]]:
    if yaml is not None and path.exists():
        return yaml.safe_load(Path(path).read_text(encoding="utf-8")).get("tools", [])
    return []


def to_openai_tools(declarations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{
        "type": "function",
        "function": {
            "name": item["name"],
            "description": item.get("description", ""),
            "parameters": item.get("parameters", {"type": "object", "properties": {}}),
        },
    } for item in declarations]
