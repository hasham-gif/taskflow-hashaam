"""Input validation functions for TaskFlow."""

from datetime import datetime

VALID_PRIORITIES = ("low", "medium", "high")
MAX_TITLE_LENGTH = 100
DATE_FORMAT = "%Y-%m-%d"


def validate_title(title: str) -> str:
    """Return the cleaned title, or raise ValueError if it is invalid."""
    cleaned = title.strip()
    if not cleaned:
        raise ValueError("Title cannot be empty.")
    if len(cleaned) > MAX_TITLE_LENGTH:
        raise ValueError(f"Title cannot be longer than {MAX_TITLE_LENGTH} characters.")
    return cleaned


def validate_priority(priority: str) -> str:
    """Return the cleaned priority, or raise ValueError if it is invalid."""
    cleaned = priority.strip().lower()
    if cleaned not in VALID_PRIORITIES:
        raise ValueError("Priority must be one of: low, medium, high.")
    return cleaned


def validate_due_date(due_date: str | None) -> str | None:
    """Return the due date in YYYY-MM-DD form, or raise ValueError if invalid."""
    if due_date is None:
        return None
    try:
        parsed = datetime.strptime(due_date, DATE_FORMAT)
    except ValueError:
        raise ValueError("Due date must be a real date in YYYY-MM-DD format.") from None
    return parsed.strftime(DATE_FORMAT)