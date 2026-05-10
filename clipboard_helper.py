# -*- coding: utf-8 -*-
def _with_clipboard(action):
    import tkinter as tk

    root = tk.Tk()
    root.withdraw()
    try:
        return action(root)
    finally:
        root.destroy()


def _read_clipboard():
    def action(root):
        import tkinter as tk

        try:
            return root.clipboard_get()
        except tk.TclError:
            return ""

    return _with_clipboard(action)


def _write_clipboard(text):
    def action(root):
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()

    _with_clipboard(action)


def handle_clipboard(command):
    command = command.strip()
    lower_command = command.lower()

    if lower_command in ("read clipboard", "clipboard read", "what is in clipboard"):
        text = _read_clipboard()
        if not text:
            return True, "Clipboard is empty."
        return True, f"Clipboard says: {text}"

    if lower_command in ("clear clipboard", "clipboard clear"):
        _write_clipboard("")
        return True, "Clipboard cleared."

    if lower_command.startswith(("copy ", "copy this ", "copy text ")):
        text = command
        for prefix in ("copy this ", "copy text ", "copy "):
            if lower_command.startswith(prefix):
                text = command[len(prefix):].strip()
                break
        if not text:
            return True, "What should I copy?"
        try:
            _write_clipboard(text)
            return True, "Copied to clipboard."
        except Exception:
            return True, "Sorry, I could not access the clipboard."

    return False, None
