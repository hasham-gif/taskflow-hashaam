"""Tests for the TaskManager."""

import pytest

from taskflow.manager import TaskManager


@pytest.fixture
def manager(tmp_path):
    """Create a manager that stores its tasks in a temporary file."""
    return TaskManager(tmp_path / "tasks.json")


def test_add_task_creates_unique_ids(manager):
    t1 = manager.add("Task A")
    t2 = manager.add("Task B")
    assert t1.id != t2.id


def test_invalid_priority_is_rejected(manager):
    with pytest.raises(ValueError):
        manager.add("Task", priority="urgent")


def test_empty_title_is_rejected(manager):
    with pytest.raises(ValueError):
        manager.add("   ")


def test_update_changes_only_given_fields(manager):
    task = manager.add("Old title", priority="low")
    manager.update(task.id, title="New title")
    updated = manager.get_all()[0]
    assert updated.title == "New title"
    assert updated.priority == "low"


def test_complete_marks_task_done(manager):
    task = manager.add("Task")
    manager.complete(task.id)
    assert manager.get_all()[0].status == "done"


def test_delete_removes_task(manager):
    task = manager.add("Task")
    manager.delete(task.id)
    assert manager.get_all() == []


def test_missing_id_is_rejected(manager):
    with pytest.raises(ValueError):
        manager.complete(99)


def test_tasks_persist_between_runs(manager):
    manager.add("Saved task")
    reloaded = TaskManager(manager.file_path)
    assert reloaded.get_all()[0].title == "Saved task"


def test_corrupted_json_file_gives_empty_list(tmp_path):
    bad_file = tmp_path / "tasks.json"
    bad_file.write_text("this is not json", encoding="utf-8")
    assert TaskManager(bad_file).get_all() == []


def test_missing_json_file_gives_empty_list(tmp_path):
    assert TaskManager(tmp_path / "does_not_exist.json").get_all() == []


def test_filter_by_status(manager):
    first = manager.add("A")
    manager.add("B")
    manager.complete(first.id)
    done = manager.get_tasks(status="done")
    assert [task.title for task in done] == ["A"]


def test_search_by_keyword_ignores_case(manager):
    manager.add("Write report")
    manager.add("Buy milk")
    results = manager.get_tasks(keyword="REPORT")
    assert [task.title for task in results] == ["Write report"]


def test_sort_by_priority_puts_high_first(manager):
    manager.add("Low task", priority="low")
    manager.add("High task", priority="high")
    titles = [task.title for task in manager.get_tasks(sort_by="priority")]
    assert titles == ["High task", "Low task"]