# Changelog - Discord Announcement Summarizer Agent

All notable changes to the Discord Announcement Summarizer Agent project will be documented in this file.

---

## [v1.1.0] - 2026-07-30 (Hackathon Release)

### Added
- **Discord Message Data Loader (`starter_v0/tools/discord_loader/tool.py`)**:
  - Robust multi-path finder for `data/data-discord/`.
  - JSON parser handling guild, channel, author roles, timestamps, attachments, and embeds.
  - Noise filtering engine excluding casual chatter, short greetings ("hi", "dạ", "cảm ơn"), and spam.
  - Candidate announcement detector searching for official roles (Lab Coach, BTC, Teacher, Admin) and critical keywords.
- **Discord Summarizer Tool (`starter_v0/tools/discord_summarizer/tool.py`)**:
  - OpenAI API integration (`gpt-4o-mini` / `gpt-4o`).
  - Zero-hallucination prompt enforcement with strict evidence grounding rules.
  - Categorized extraction: Deadlines, Assignments, Schedule Changes, Resources, Action Required.
  - Structured Markdown output schema generation.
- **End-to-End Pipeline Script (`starter_v0/run_discord_summarizer.py`)**:
  - Standalone runner executing 10-step pipeline.
  - Comprehensive step logging (loaded files, raw messages, candidate counts, execution time).
  - Output artifact generation saved to `Daily_Important_Updates.md`.
- **Evaluation Engine (`eval/`)**:
  - `eval/golden_set.json`: 20 test cases covering Easy (5), Medium (5), Hard (5), and Adversarial (5).
  - `eval/run_eval_discord.py`: Automated evaluation script.
  - `eval/evaluation_result.csv`: CSV export of test case outputs.
  - `eval/evaluation_summary.md`: Summary report documenting overall pass rate (> 85%).
- **Validation Engine (`validation/`)**:
  - `validation/feedback_log.md`: 5 user validation entries.
- **Interactive UI Artifacts**:
  - `index.html` & `agent_workflow.html`: High-end interactive Discord simulator and SVG workflow graph visualization.

---

## [v1.0.0] - 2026-07-30 (Starter Code Baseline)

### Added
- `starter_v0/` base framework with Provider abstractions, environment loading, tool declarations, CLI chat loop, and Streamlit app.
