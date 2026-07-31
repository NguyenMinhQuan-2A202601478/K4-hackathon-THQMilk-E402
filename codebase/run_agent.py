from __future__ import annotations

import sys
import time
from pathlib import Path

# Fix Windows console UTF-8 encoding
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "codebase"))

from config import init_env
from discord_loader import load_and_group_messages
from discord_summarizer import generate_daily_digest


init_env()


def main():
    start_time = time.time()
    print("=" * 65)
    print("🚀 DISCORD ANNOUNCEMENT SUMMARIZER AGENT - CODEBASE PROTOTYPE")
    print("=" * 65)

    # Step 1: Load Discord Dataset
    print("\n[Step 1/4] Loading messages from data/data-discord/...")
    dataset = load_and_group_messages()
    print(f"✅ Loaded {dataset.get('files_loaded', 0)} files.")
    print(f"📊 Total Raw Messages: {dataset.get('total_messages', 0)}")
    print(f"🎯 Candidate Announcements Detected: {dataset.get('candidate_count', 0)}")

    channels = dataset.get("channels", {})
    for ch_name, msgs in channels.items():
        print(f"   • Channel #{ch_name}: {len(msgs)} messages")

    # Step 2: OpenAI Summarization & Extraction Call
    print("\n[Step 2/4] Executing Real OpenAI API Call for Extraction & Summarization...")
    digest_markdown = generate_daily_digest(channels, model_name="gpt-4o-mini")

    # Step 3: Write Output Artifact
    print("\n[Step 3/4] Saving Daily Important Updates Markdown Report...")
    out_file_codebase = Path(__file__).resolve().parent / "Daily_Important_Updates.md"
    out_file_root = ROOT / "Daily_Important_Updates.md"

    out_file_codebase.write_text(digest_markdown, encoding="utf-8")
    out_file_root.write_text(digest_markdown, encoding="utf-8")

    print(f"💾 Report saved to: {out_file_codebase}")
    print(f"💾 Report saved to: {out_file_root}")

    # Step 4: Summary Logs
    elapsed = time.time() - start_time
    print(f"\n[Step 4/4] Pipeline completed in {elapsed:.2f} seconds.")
    print("=" * 65)
    print("DAILY DIGEST OUTPUT PREVIEW:")
    print("-" * 65)
    print(digest_markdown[:600] + ("\n..." if len(digest_markdown) > 600 else ""))
    print("=" * 65)


if __name__ == "__main__":
    main()
