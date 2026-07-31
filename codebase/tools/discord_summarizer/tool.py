from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from codebase.providers import make_provider


DISCORD_SUMMARIZER_PROMPT = """You are a Senior AI Product Engineer & Announcement Summarizer for a Discord Student Community.
Your mission is to inspect raw Discord community messages and extract ONLY important community announcements.

CRITICAL EXTRACTION MANDATES:
1. **SOURCE LOCATION**: Every summary MUST state the exact Discord source channel (e.g. `📍 Kênh nguồn: #thông-báo`).
2. **URLS & CREDENTIALS**: If a message contains Zoom links, meeting IDs, or passcodes, you MUST extract them as clickable markdown links and bold credentials. NEVER omit links!
3. **MANDATORY REGULATIONS**: If a message contains regulations, naming rules (e.g. `CÚ PHÁP ĐẶT TÊN CHUẨN: G01 — T001 — Nguyễn Văn An`), or entry guidelines, you MUST include a dedicated `⚠️ Quy định / Lưu ý` section.
4. **ZERO HALLUCINATION**: ONLY extract information explicitly supported by the message text.
5. If evidence for a category is insufficient, write "Not enough evidence."

Output in EXACTLY this Markdown format:

# Daily Important Updates

## Deadlines
- **Summary**: ...
  - **Channel**: #...
  - **Timestamp**: ...
  - **Confidence**: ...
  - **Evidence**: "..."
  - **Links / Passcode**: [Link Zoom / Doc](url) | Meeting ID: ... | Passcode: ...
  - **Quy định / Lưu ý**: ...

## Assignments
...

## Schedule Changes
...

## Resources
...

## Action Required
...
"""


def generate_daily_digest(grouped_channels: dict[str, list[dict[str, Any]]], model_name: str = "gpt-4o-mini") -> str:
    """Generate Daily Important Updates markdown using real OpenAI API call via provider layer."""
    provider = make_provider("openai")

    context_blocks = []
    for channel_name, msgs in grouped_channels.items():
        candidates = [m for m in msgs if m.get("is_candidate", True)]
        for m in candidates[:30]:
            block = (
                f"[Channel: #{channel_name}] [Author: {m.get('author')}] [Time: {m.get('timestamp')}]\n"
                f"Content: {m.get('content')}\n"
            )
            context_blocks.append(block)

    if not context_blocks:
        return """# Daily Important Updates

## Deadlines
Not enough evidence.

## Assignments
Not enough evidence.

## Schedule Changes
Not enough evidence.

## Resources
Not enough evidence.

## Action Required
Not enough evidence.
"""

    context_str = "\n---\n".join(context_blocks)
    messages = [
        {"role": "system", "content": DISCORD_SUMMARIZER_PROMPT},
        {"role": "user", "content": f"Here are the Discord community messages:\n\n{context_str}\n\nGenerate the Daily Important Updates digest now."},
    ]

    response = provider.complete(
        messages=messages,
        tools=None,
        model=model_name or os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.0,
    )

    return response.text or "# Daily Important Updates\n\nNot enough evidence."
