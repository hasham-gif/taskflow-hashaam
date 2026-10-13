"""Business logic for TaskFlow."""

from pathlib import Path

from taskflow.models import Task
from taskflow.storage import DATA_FILE, load_tasks, save_tasks


class TaskManager:
    """Manages the collection of tasks."""

    def __init__(self, file_path: Path = DATA_FILE) -> None:
        """Load existing tasks from the storage file."""
        self.file_path = file_path
        self.tasks = load_tasks(file_path)

    def _next_id(self) -> int:
        """Return the next unused task id."""
        return max((task.id for task in self.tasks), default=0) + 1

    def add(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        due_date: str | None = None,
    ) -> Task:
        """Create a new task, save it, and return it."""
        task = Task(
            id=self._next_id(),
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
        )
        self.tasks.append(task)
        save_tasks(self.tasks, self.file_path)
        return task

    def get_all(self) -> list[Task]:
        """Return a copy of all tasks."""
        return list(self.tasks)