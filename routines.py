# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

from config import ROUTINES_FILE


ROUTINES_PATH = Path(ROUTINES_FILE)


def _load_routines():
    if not ROUTINES_PATH.exists():
        return {}
    try:
        data = json.loads(ROUTINES_PATH.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return {}


def _save_routines(routines):
    ROUTINES_PATH.write_text(json.dumps(routines, ensure_ascii=False, indent=2), encoding="utf-8")


def _clean_name(name):
    return re.sub(r"\s+", " ", name.strip().lower())


def _split_commands(commands_text):
    return [item.strip() for item in re.split(r"\s*(?:;|\|)\s*", commands_text) if item.strip()]


def get_routine_commands(command):
    command = command.lower().strip()
    prefixes = ("run routine ", "start routine ", "routine ")
    for prefix in prefixes:
        if command.startswith(prefix):
            name = _clean_name(command.replace(prefix, "", 1))
            routines = _load_routines()
            return name, routines.get(name)
    return None, None


def handle_routines(command):
    original_command = command.strip()
    command = original_command.lower().strip()

    if command in ("list routines", "show routines", "my routines"):
        routines = _load_routines()
        if not routines:
            return True, "You do not have any routines yet."
        names = ", ".join(sorted(routines))
        return True, f"Your routines are: {names}."

    if command.startswith(("delete routine ", "remove routine ")):
        name = _clean_name(command.split("routine ", 1)[1])
        routines = _load_routines()
        if name not in routines:
            return True, f"I could not find a routine named {name}."
        del routines[name]
        _save_routines(routines)
        return True, f"Deleted routine {name}."

    create_prefixes = ("create routine ", "add routine ", "save routine ")
    if command.startswith(create_prefixes):
        routine_index = command.find("routine ")
        payload = original_command[routine_index + len("routine "):]
        if ":" not in payload:
            return True, "Please use this format: create routine study mode: open vs code; play focus music."
        name, commands_text = payload.split(":", 1)
        name = _clean_name(name)
        commands = _split_commands(commands_text)
        if not name or not commands:
            return True, "Please give me a routine name and at least one command."

        routines = _load_routines()
        routines[name] = commands
        _save_routines(routines)
        return True, f"Saved routine {name} with {len(commands)} commands."

    name, commands = get_routine_commands(command)
    if name and commands is None:
        return True, f"I could not find a routine named {name}."

    return False, None
