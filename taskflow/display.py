"""Table formatting for TaskFlow."""

from taskflow.models import Task

HEADERS = ("ID", "Title", "Priority", "Due", "Status")
EMPTY_VALUE = "-"
COLUMN_GAP = "  "


def _task_to_row(task: Task) -> tuple[str, ...]:
    """Convert a task into a row of display strings."""
    return (
        str(task.id),
        task.title,
        task.priority,
        task.due_date or EMPTY_VALUE,
        task.status,
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