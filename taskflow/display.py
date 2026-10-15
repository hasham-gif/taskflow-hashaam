"""Table formatting for TaskFlow."""

from datetime import date

from taskflow.manager import STATUS_PENDING
from taskflow.models import Task

HEADERS = ("ID", "Title", "Priority", "Due", "Status")
EMPTY_VALUE = "-"
COLUMN_GAP = "  "
STATUS_OVERDUE = "OVERDUE"


def is_overdue(task: Task, today: date | None = None) -> bool:
    """Return True if the task is pending and its due date has passed."""
    if task.status != STATUS_PENDING or task.due_date is None:
        return False
    today = today or date.today()
    return task.due_date < today.isoformat()


def _task_to_row(task: Task) -> tuple[str, ...]:
    """Convert a task into a row of display strings."""
    return (
        str(task.id),
        task.title,
        task.priority,
        task.due_date or EMPTY_VALUE,
        STATUS_OVERDUE if is_overdue(task) else task.status,
    )


def _format_row(row: tuple[str, ...], widths: list[int]) -> str:
    """Pad each cell to its column width and join them into one line."""
    return COLUMN_GAP.join(cell.ljust(width) for cell, width in zip(row, widths))


def format_table(tasks: list[Task]) -> str:
    """Return the tasks formatted as a text table."""
    if not tasks:
        return "No tasks found."

    rows = [_task_to_row(task) for task in tasks]
    all_rows = [HEADERS] + rows
    widths = [max(len(row[i]) for row in all_rows) for i in range(len(HEADERS))]
    separator = tuple("-" * width for width in widths)

    lines = [_format_row(HEADERS, widths), _format_row(separator, widths)]
    lines += [_format_row(row, widths) for row in rows]
    return "\n".join(lines)