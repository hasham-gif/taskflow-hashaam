"""Data model for TaskFlow."""

from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Task:
    """Represents a single task."""

    id: int
    title: str
    description: str = ""
    priority: str = "medium"
    due_date: str | None = None
    status: str = "pending"
    created_at: str = ""

    def __post_init__(self) -> None:
        """Set the creation timestamp automatically if not provided."""
        if not self.created_at:
            self.created_at = datetime.now().isoformat(timespec="seconds")

    def to_dict(self) -> dict:
        """Convert the task to a dictionary for saving to JSON."""
        return asdict(self)