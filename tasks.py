# -*- coding: utf-8 -*-
import json
import re
from datetime import datetime
from pathlib import Path

from config import TASKS_FILE


TASKS_PATH = Path(TASKS_FILE)


def _now():
    return datetime.now().strftime("%Y-%m-%d %I:%M %p")


def _load_tasks():
    if not TASKS_PATH.exists():
        return []
    try:
        data = json.loads(TASKS_PATH.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
    except Exception:
        pass
    return []


def _save_tasks(tasks):
    TASKS_PATH.parent.mkdir(parents=True, exist_ok=True)
    TASKS_PATH.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")


def _next_task_id(tasks):
    existing_ids = [task.get("id", 0) for task in tasks if isinstance(task.get("id"), int)]
    return max(existing_ids, default=0) + 1


def _parse_task_id(command):
    match = re.search(r"\btask\s+(\d+)\b|\b(\d+)\b", command)
    if not match:
        return None
    return int(match.group(1) or match.group(2))


def _find_task(tasks, task_id):
    for task in tasks:
        if task.get("id") == task_id:
            return task
    return None


def _format_task(task):
    status = "done" if task.get("completed") else "pending"
    return f"{task['id']}. {task['title']} ({status})"


def _format_tasks(tasks, include_completed=False):
    visible_tasks = [
        task for task in tasks
        if include_completed or not task.get("completed")
    ]
    if not visible_tasks:
        return "You do not have any tasks right now."

    recent_tasks = visible_tasks[-8:]
    return "Your tasks are: " + "; ".join(_format_task(task) for task in recent_tasks)


def _extract_new_task(command):
    prefixes = (
        "add task ",
        "create task ",
        "new task ",
        "add todo ",
        "todo ",
    )
    for prefix in prefixes:
        if command.lower().startswith(prefix):
            return command[len(prefix):].strip()
    return None


def handle_tasks(command):
    original_command = command.strip()
    command = original_command.lower().strip()

    task_title = _extract_new_task(original_command)
    if task_title is not None:
        if not task_title:
            return True, "Please tell me the task title."

        tasks = _load_tasks()
        task = {
            "id": _next_task_id(tasks),
            "title": task_title,
            "completed": False,
            "created_at": _now(),
            "completed_at": None,
        }
        tasks.append(task)
        _save_tasks(tasks)
        return True, f"Task {task['id']} added: {task['title']}."

    if command in ("show tasks", "list tasks", "my tasks", "show todos", "list todos"):
        return True, _format_tasks(_load_tasks())

    if command in ("show completed tasks", "completed tasks", "done tasks"):
        completed_tasks = [task for task in _load_tasks() if task.get("completed")]
        if not completed_tasks:
            return True, "You do not have any completed tasks yet."
        return True, "Completed tasks are: " + "; ".join(_format_task(task) for task in completed_tasks[-8:])

    if command in ("show all tasks", "all tasks"):
        return True, _format_tasks(_load_tasks(), include_completed=True)

    if command.startswith(("complete task ", "finish task ", "done task ", "mark task ")):
        task_id = _parse_task_id(command)
        if task_id is None:
            return True, "Please tell me which task number to complete."

        tasks = _load_tasks()
        task = _find_task(tasks, task_id)
        if task is None:
            return True, f"I could not find task {task_id}."
        if task.get("completed"):
            return True, f"Task {task_id} is already completed."

        task["completed"] = True
        task["completed_at"] = _now()
        _save_tasks(tasks)
        return True, f"Completed task {task_id}: {task['title']}."

    if command.startswith(("reopen task ", "undo task ")):
        task_id = _parse_task_id(command)
        if task_id is None:
            return True, "Please tell me which task number to reopen."

        tasks = _load_tasks()
        task = _find_task(tasks, task_id)
        if task is None:
            return True, f"I could not find task {task_id}."
        if not task.get("completed"):
            return True, f"Task {task_id} is already pending."

        task["completed"] = False
        task["completed_at"] = None
        _save_tasks(tasks)
        return True, f"Reopened task {task_id}: {task['title']}."

    if command.startswith(("delete task ", "remove task ")):
        task_id = _parse_task_id(command)
        if task_id is None:
            return True, "Please tell me which task number to delete."

        tasks = _load_tasks()
        task = _find_task(tasks, task_id)
        if task is None:
            return True, f"I could not find task {task_id}."

        tasks = [item for item in tasks if item.get("id") != task_id]
        _save_tasks(tasks)
        return True, f"Deleted task {task_id}: {task['title']}."

    if command in ("clear tasks", "delete all tasks", "clear todos"):
        _save_tasks([])
        return True, "All tasks cleared."

    return False, None
