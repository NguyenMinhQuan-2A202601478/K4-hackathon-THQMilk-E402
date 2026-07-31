from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from codebase.config import init_env

init_env()


DISCORD_SUMMARIZER_PROMPT = """You are a Senior AI Product Engineer & Announcement Summarizer for a Discord Student Community.
Your mission is to inspect raw Discord community messages and extract ONLY important community announcements.

CRITICAL INSTRUCTIONS:
1. ONLY extract information supported by the given messages.
2. NEVER invent or hallucinate deadlines, tasks, dates, or URLs.
3. If evidence is insufficient for any section, write "Not enough evidence."
4. If there are conflicting announcements, display BOTH along with their timestamps and channel names.
5. Filter out casual chat. Focus strictly on:
   - Deadlines
   - Assignments & Homework
   - Schedule Changes & Events
   - Resources & Links
   - Action Required & Logistics
6. Each item MUST include:
   - Short summary
   - Source Discord channel
   - Timestamp
   - Confidence score (0.0 to 1.0)
   - Supporting evidence snippet (exact quote)

Output in EXACTLY this Markdown format:

# Daily Important Updates

## Deadlines
- **Summary**: ...
  - **Channel**: #...
  - **Timestamp**: ...
  - **Confidence**: ...
  - **Evidence**: "..."

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
    """Generate Daily Important Updates markdown using real OpenAI API call."""
    try:
        from openai import OpenAI
    except ImportError:
        return "# Daily Important Updates\n\nError: OpenAI library not installed. Please run `pip install openai`."

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "# Daily Important Updates\n\nError: OPENAI_API_KEY environment variable not set."

    # Build input context for model
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
    client = OpenAI(api_key=api_key)

    resp = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": DISCORD_SUMMARIZER_PROMPT},
            {"role": "user", "content": f"Here are the Discord community messages:\n\n{context_str}\n\nGenerate the Daily Important Updates digest now."},
        ],
        temperature=0.0,
    )

    return resp.choices[0].message.content or "# Daily Important Updates\n\nNot enough evidence."
