# -*- coding: utf-8 -*-
import os
import subprocess


APP_COMMANDS = {
    "notepad": ["notepad"],
    "calculator": ["calc"],
    "calc": ["calc"],
    "paint": ["mspaint"],
    "chrome": ["cmd", "/c", "start", "chrome"],
    "edge": ["cmd", "/c", "start", "msedge"],
    "command prompt": ["cmd"],
    "cmd": ["cmd"],
    "powershell": ["powershell"],
    "vs code": ["cmd", "/c", "code"],
    "vscode": ["cmd", "/c", "code"],
}


def handle_app(command):
    command = command.lower().strip()
    if not command.startswith("open "):
        return False, None

    app_name = command.replace("open ", "", 1).strip()
    if app_name not in APP_COMMANDS:
        return False, None

    try:
        if os.name == "nt":
            subprocess.Popen(APP_COMMANDS[app_name], shell=False)
        else:
            subprocess.Popen(APP_COMMANDS[app_name])
        return True, f"Opening {app_name}"
    except Exception:
        return True, f"Sorry, I could not open {app_name}."
