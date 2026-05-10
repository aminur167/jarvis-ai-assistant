# -*- coding: utf-8 -*-
import json
from datetime import datetime
from pathlib import Path

from config import HISTORY_FILE


HISTORY_PATH = Path(HISTORY_FILE)
MAX_HISTORY = 100


def _load_history():
    if not HISTORY_PATH.exists():
        return []
    try:
        return json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
    except Exception:
        return []


def _save_history(history):
    HISTORY_PATH.write_text(json.dumps(history[-MAX_HISTORY:], ensure_ascii=False, indent=2), encoding="utf-8")


def record_command(command, normalized_command=None):
    history = _load_history()
    history.append(
        {
            "time": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
            "command": command,
            "normalized": normalized_command or command,
        }
    )
    _save_history(history)


def handle_history(command):
    command = command.lower().strip()
    if command not in ("what did i ask last", "last command", "command history", "show history", "clear history"):
        return False, None

    if command == "clear history":
        _save_history([])
        return True, "Command history cleared."

    history = _load_history()
    if not history:
        return True, "Command history is empty."

    if command in ("what did i ask last", "last command"):
        last = history[-1]
        return True, f"Last command was: {last['command']}."

    recent = history[-5:]
    summary = "; ".join(f"{item['time']}: {item['command']}" for item in recent)
    return True, f"Recent commands: {summary}"
