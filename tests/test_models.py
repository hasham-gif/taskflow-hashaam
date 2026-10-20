"""Tests for the Task model."""

from taskflow.models import Task


def test_task_gets_default_values():
    task = Task(1, "Buy milk")
    assert task.priority == "medium"
    assert task.status == "pending"
    assert task.due_date is None


def test_created_at_is_set_automatically():
    task = Task(1, "Buy milk")
    assert task.created_at != ""


def test_to_dict_contains_all_fields():
    data = Task(1, "Buy milk").to_dict()
    assert data["id"] == 1
    assert data["title"] == "Buy milk"
    assert set(data) == {
        "id", "title", "description", "priority", "due_date", "status", "created_at"
    }