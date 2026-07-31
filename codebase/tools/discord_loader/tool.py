from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def find_data_discord_path() -> Path:
    candidates = [
        Path("data/data-discord"),
        Path("../data/data-discord"),
        Path(__file__).resolve().parent.parent.parent.parent / "data" / "data-discord",
        Path("c:/AI Thuc Chien/Mini Hackathon/K4-hackathon-THQMilk-E402/data/data-discord"),
    ]
    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            return candidate.resolve()
    
    fallback = Path("data/data-discord").resolve()
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback


def is_noise_message(text: str) -> bool:
    if not text or len(text.strip()) < 5:
        return True
    
    noise_patterns = [
        r"^(hi|hello|cảm ơn|cam on|tks|thanks|dạ|da|ok|okay|thả tim|vâng|chuẩn|hay quá|👍|❤️|😃)$",
        r"^có 1 bạn quên sạc",
        r"^cho em hỏi",
    ]
    cleaned = text.strip().lower()
    for pattern in noise_patterns:
        if re.search(pattern, cleaned):
            return True
    return False


def is_candidate_announcement(msg: dict[str, Any]) -> bool:
    author = msg.get("author", {})
    nickname = author.get("nickname", "") or ""
    roles = [r.get("name", "").lower() for r in author.get("roles", [])]
    content = msg.get("content", "") or ""

    is_official = (
        author.get("isBot", False)
        or any(role in ["lab coach", "coach", "btc", "teacher", "giảng viên", "trợ giảng", "admin"] for role in roles)
        or any(k in nickname.lower() for k in ["coach", "btc", "teacher", "giảng viên", "trợ giảng", "admin"])
    )

    keywords = [
        "thông báo", "hạn", "nộp", "bài tập", "lịch", "zoom", "deadline", 
        "quy định", "bắt buộc", "slide", "slides", "codelab", "codelabs", 
        "link", "meeting", "workshop", "kick-off", "xác nhận", "nộp bài",
        "hạn cuối", "bài lab", "spec", "checkpoint", "cp1", "cp2", "cp3", "cp4", "cp5", "cp6"
    ]
    has_keyword = any(kw in content.lower() for kw in keywords)

    return is_official or has_keyword


def load_and_group_messages(custom_dir: Path | None = None) -> dict[str, Any]:
    data_dir = custom_dir or find_data_discord_path()
    json_files = list(data_dir.glob("*.json"))
    if not json_files:
        return {
            "status": "empty",
            "message": f"No Discord JSON export files found in {data_dir}",
            "channels": {},
            "total_messages": 0,
            "candidate_count": 0,
        }

    grouped: dict[str, list[dict[str, Any]]] = {}
    total_messages = 0
    candidate_count = 0

    for file_path in json_files:
        try:
            raw_data = json.loads(file_path.read_text(encoding="utf-8"))
            channel_name = raw_data.get("channel", {}).get("name", "unknown-channel")
            messages = raw_data.get("messages", [])
            total_messages += len(messages)

            cleaned_list = []
            for msg in messages:
                content = msg.get("content", "")
                if is_noise_message(content):
                    continue

                author = msg.get("author", {})
                author_name = author.get("nickname") or author.get("name") or "User"
                
                item = {
                    "id": msg.get("id"),
                    "timestamp": msg.get("timestamp"),
                    "author": author_name,
                    "content": content,
                    "is_candidate": is_candidate_announcement(msg),
                }
                cleaned_list.append(item)
                if item["is_candidate"]:
                    candidate_count += 1

            if channel_name not in grouped:
                grouped[channel_name] = []
            grouped[channel_name].extend(cleaned_list)

        except Exception as exc:
            print(f"⚠️ Error parsing file {file_path.name}: {exc}")

    return {
        "status": "success",
        "data_dir": str(data_dir),
        "files_loaded": len(json_files),
        "total_messages": total_messages,
        "candidate_count": candidate_count,
        "channels": grouped,
    }
