"""JSON file storage for TaskFlow."""

import json
from pathlib import Path

from taskflow.models import Task

DATA_FILE = Path("data") / "tasks.json"


def load_tasks(file_path: Path = DATA_FILE) -> list[Task]:
    """Load tasks from the JSON file, or return an empty list on any problem."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return [Task(**item) for item in data]
    except (FileNotFoundError, json.JSONDecodeError, TypeError):
        return []


def save_tasks(tasks: list[Task], file_path: Path = DATA_FILE) -> None:
    """Save the list of tasks to the JSON file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump([task.to_dict() for task in tasks], file, indent=4)