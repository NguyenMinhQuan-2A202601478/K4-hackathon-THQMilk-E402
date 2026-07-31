from __future__ import annotations

import os
from pathlib import Path


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if key and key not in os.environ:
            os.environ[key] = value


def init_env() -> Path:
    """Initialize environment variables from root or local .env file."""
    root_dir = Path(__file__).resolve().parent.parent
    local_env = Path(__file__).resolve().parent / ".env"
    root_env = root_dir / ".env"
    starter_env = root_dir / "starter_v0" / ".env"

    if local_env.exists():
        load_dotenv(local_env)
    elif root_env.exists():
        load_dotenv(root_env)
    elif starter_env.exists():
        load_dotenv(starter_env)

    return root_dir
