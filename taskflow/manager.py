"""Business logic for TaskFlow."""

from pathlib import Path

from taskflow.models import Task
from taskflow.storage import DATA_FILE, load_tasks, save_tasks
from taskflow.validators import validate_due_date, validate_priority, validate_title

STATUS_DONE = "done"


class TaskManager:
    """Manages the collection of tasks."""

    def __init__(self, file_path: Path = DATA_FILE) -> None:
        """Load existing tasks from the storage file."""
        self.file_path = file_path
        self.tasks = load_tasks(file_path)

    def _next_id(self) -> int:
        """Return the next unused task id."""
        return max((task.id for task in self.tasks), default=0) + 1

    def _find(self, task_id: int) -> Task:
        """Return the task with the given id, or raise ValueError if missing."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise ValueError(f"Task with id {task_id} does not exist.")

    def add(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        due_date: str | None = None,
    ) -> Task:
        """Validate the input, create a new task, save it, and return it."""
        task = Task(
            id=self._next_id(),
            title=validate_title(title),
            description=description.strip(),
            priority=validate_priority(priority),
            due_date=validate_due_date(due_date),
        )
        self.tasks.append(task)
        save_tasks(self.tasks, self.file_path)
        return task

    def get_all(self) -> list[Task]:
        """Return a copy of all tasks."""
        return list(self.tasks)

    def update(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
        priority: str | None = None,
        due_date: str | None = None,
    ) -> Task:
        """Update the given fields of a task, save it, and return it."""
        task = self._find(task_id)
        new_title = validate_title(title) if title is not None else task.title
        new_description = (
            description.strip() if description is not None else task.description
        )
        new_priority = (
            validate_priority(priority) if priority is not None else task.priority
        )
        new_due_date = (
            validate_due_date(due_date) if due_date is not None else task.due_date
        )

        task.title = new_title
        task.description = new_description
        task.priority = new_priority
        task.due_date = new_due_date
        save_tasks(self.tasks, self.file_path)
        return task

    def complete(self, task_id: int) -> Task:
        """Mark a task as done, save it, and return it."""
        task = self._find(task_id)
        task.status = STATUS_DONE
        save_tasks(self.tasks, self.file_path)
        return task

    def delete(self, task_id: int) -> Task:
        """Remove a task, save the list, and return the removed task."""
        task = self._find(task_id)
        self.tasks.remove(task)
        save_tasks(self.tasks, self.file_path)
        return task