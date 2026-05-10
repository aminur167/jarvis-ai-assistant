# -*- coding: utf-8 -*-
import os
from pathlib import Path


BASE_DIR = Path.cwd()
HOME = Path.home()

FOLDERS = {
    "desktop": HOME / "Desktop",
    "downloads": HOME / "Downloads",
    "documents": HOME / "Documents",
    "pictures": HOME / "Pictures",
    "music": HOME / "Music",
    "videos": HOME / "Videos",
    "project": BASE_DIR,
    "my project": BASE_DIR,
    "jarvis project": BASE_DIR,
}


def handle_file_opener(command):
    command = command.lower().strip()
    if not command.startswith("open "):
        return False, None

    target_name = command.replace("open ", "", 1).strip()
    if target_name not in FOLDERS:
        return False, None

    target = FOLDERS[target_name]
    if not target.exists():
        return True, f"Sorry, I could not find {target_name}."

    try:
        os.startfile(target)
        return True, f"Opening {target_name}."
    except Exception:
        return True, f"Sorry, I could not open {target_name}."
