"""Command-line entry point for TaskFlow."""

import argparse
import sys

from taskflow.display import format_table
from taskflow.manager import SORT_OPTIONS, TaskManager

def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser with all supported commands."""
    parser = argparse.ArgumentParser(
        prog="taskflow", description="A command-line task manager."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Short task name")
    add_parser.add_argument("-d", "--description", default="", help="Optional details")
    add_parser.add_argument(
        "-p", "--priority", default="medium", help="low, medium or high"
    )
    add_parser.add_argument("--due", default=None, help="Due date (YYYY-MM-DD)")

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--status", default=None, help="pending or done")
    list_parser.add_argument(
        "-p", "--priority", default=None, help="low, medium or high"
    )
    list_parser.add_argument(
        "--sort", default=None, choices=SORT_OPTIONS, help="Sort by due or priority"
    )

    search_parser = subparsers.add_parser("search", help="Search tasks by keyword")
    search_parser.add_argument("keyword", help="Word to look for in title or description")

    update_parser = subparsers.add_parser("update", help="Update an existing task")
    update_parser.add_argument("id", type=int, help="ID of the task to update")
    update_parser.add_argument("--title", default=None, help="New title")
    update_parser.add_argument("-d", "--description", default=None, help="New details")
    update_parser.add_argument(
        "-p", "--priority", default=None, help="low, medium or high"
    )
    update_parser.add_argument("--due", default=None, help="New due date (YYYY-MM-DD)")

    done_parser = subparsers.add_parser("done", help="Mark a task as done")
    done_parser.add_argument("id", type=int, help="ID of the task to complete")

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="ID of the task to delete")
    return parser


def run_command(args: argparse.Namespace, manager: TaskManager) -> str:
    """Run the chosen command and return the message to show the user."""
    if args.command == "add":
        task = manager.add(args.title, args.description, args.priority, args.due)
        return f"Task {task.id} added: {task.title}"
    if args.command == "list":
        tasks = manager.get_tasks(
            status=args.status, priority=args.priority, sort_by=args.sort
        )
        return format_table(tasks)
    if args.command == "search":
        return format_table(manager.get_tasks(keyword=args.keyword))
    if args.command == "update":
        task = manager.update(
            args.id, args.title, args.description, args.priority, args.due
        )
        return f"Task {task.id} updated: {task.title}"
    if args.command == "done":
        task = manager.complete(args.id)
        return f"Task {task.id} marked as done: {task.title}"
    task = manager.delete(args.id)
    return f"Task {task.id} deleted: {task.title}"


def main() -> None:
    """Read the command from the terminal, run it, and report any error."""
    args = build_parser().parse_args()
    manager = TaskManager()
    try:
        print(run_command(args, manager))
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()