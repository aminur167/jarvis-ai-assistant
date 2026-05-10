# -*- coding: utf-8 -*-
from datetime import datetime
from pathlib import Path

from config import NOTES_FILE


NOTES_PATH = Path(NOTES_FILE)


def handle_notes(command):
    command = command.strip()
    lower_command = command.lower()

    if lower_command in ("take note", "add note", "note"):
        return True, "What should I write in the note?"

    if lower_command.startswith(("take note ", "add note ", "note ")):
        note = command.split(" ", 2)[-1].strip()
        if not note:
            return True, "What should I write in the note?"
        NOTES_PATH.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        with NOTES_PATH.open("a", encoding="utf-8") as file:
            file.write(f"[{timestamp}] {note}\n")
        return True, "Note saved."

    if lower_command in ("show notes", "read notes", "my notes"):
        if not NOTES_PATH.exists() or not NOTES_PATH.read_text(encoding="utf-8").strip():
            return True, "You do not have any notes yet."
        lines = NOTES_PATH.read_text(encoding="utf-8").strip().splitlines()
        recent_notes = lines[-5:]
        return True, "Here are your recent notes. " + " ".join(recent_notes)

    if lower_command in ("clear notes", "delete notes"):
        NOTES_PATH.write_text("", encoding="utf-8")
        return True, "All notes cleared."

    return False, None
