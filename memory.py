# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

from config import MEMORY_FILE


MEMORY_PATH = Path(MEMORY_FILE)


def _load_memory():
    if not MEMORY_PATH.exists():
        return {}
    try:
        return json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_memory(memory):
    MEMORY_PATH.write_text(json.dumps(memory, ensure_ascii=False, indent=2), encoding="utf-8")


def get_memory_context():
    memory = _load_memory()
    if not memory:
        return ""
    facts = [f"{key}: {value}" for key, value in memory.items()]
    return "User memory:\n" + "\n".join(facts)


def handle_memory(command):
    command = command.strip()
    lower_command = command.lower()
    memory = _load_memory()

    name_match = re.match(r"my name is (.+)", lower_command)
    if name_match:
        name = command[len("my name is "):].strip()
        memory["name"] = name
        _save_memory(memory)
        return True, f"Nice to meet you, {name}."

    remember_match = re.match(r"remember (?:that )?(.+?) is (.+)", lower_command)
    if remember_match:
        key = remember_match.group(1).strip().replace(" ", "_")
        value_start = lower_command.find(" is ") + 4
        value = command[value_start:].strip()
        memory[key] = value
        _save_memory(memory)
        return True, f"Okay, I will remember your {key.replace('_', ' ')}."

    if lower_command in ("what is my name", "who am i"):
        if "name" not in memory:
            return True, "I do not know your name yet."
        return True, f"Your name is {memory['name']}."

    if lower_command.startswith("what is my "):
        key = lower_command.replace("what is my ", "", 1).strip().replace(" ", "_")
        if key in memory:
            return True, f"Your {key.replace('_', ' ')} is {memory[key]}."
        return True, f"I do not know your {key.replace('_', ' ')} yet."

    if lower_command in ("show memory", "what do you remember"):
        if not memory:
            return True, "I do not remember anything yet."
        return True, "I remember: " + ", ".join(f"{key.replace('_', ' ')} is {value}" for key, value in memory.items())

    if lower_command in ("clear memory", "forget everything"):
        _save_memory({})
        return True, "Memory cleared."

    return False, None
