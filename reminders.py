# -*- coding: utf-8 -*-
import re
import threading
from datetime import datetime, timedelta

active_timers = []


def _schedule(seconds, message):
    def notify():
        from speech import speak

        speak(message)

    timer = threading.Timer(seconds, notify)
    timer.daemon = True
    timer.start()
    active_timers.append(timer)


def _parse_duration(text):
    match = re.search(r"(\d+)\s*(second|seconds|minute|minutes|hour|hours)", text)
    if not match:
        return None

    amount = int(match.group(1))
    unit = match.group(2)
    if unit.startswith("second"):
        return amount
    if unit.startswith("minute"):
        return amount * 60
    if unit.startswith("hour"):
        return amount * 3600
    return None


def _parse_clock_time(text):
    match = re.search(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", text)
    if not match:
        return None

    hour = int(match.group(1))
    minute = int(match.group(2) or 0)
    meridiem = match.group(3)

    if meridiem == "pm" and hour != 12:
        hour += 12
    if meridiem == "am" and hour == 12:
        hour = 0
    if hour > 23 or minute > 59:
        return None

    now = datetime.now()
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    return target


def handle_reminder(command):
    command = command.lower().strip()

    if command.startswith("set timer"):
        seconds = _parse_duration(command)
        if seconds is None:
            return True, "Please tell me a timer duration, like 10 minutes."
        _schedule(seconds, "Timer finished.")
        return True, f"Timer set for {seconds // 60} minutes." if seconds >= 60 else f"Timer set for {seconds} seconds."

    if command.startswith("remind me"):
        reminder_text = command.replace("remind me to", "", 1).replace("remind me", "", 1).strip()

        if " in " in reminder_text:
            task, duration_text = reminder_text.rsplit(" in ", 1)
            seconds = _parse_duration(duration_text)
            if seconds is None:
                return True, "Please tell me when to remind you."
            _schedule(seconds, f"Reminder: {task.strip()}")
            return True, f"Okay, I will remind you to {task.strip()}."

        if " at " in reminder_text:
            task, time_text = reminder_text.rsplit(" at ", 1)
            target = _parse_clock_time(time_text)
            if target is None:
                return True, "Please tell me a valid reminder time."
            seconds = max(1, int((target - datetime.now()).total_seconds()))
            _schedule(seconds, f"Reminder: {task.strip()}")
            return True, f"Okay, I will remind you to {task.strip()} at {target.strftime('%I:%M %p')}."

        return True, "Please tell me when to remind you."

    return False, None
