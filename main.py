"""Command-line entry point for TaskFlow."""

import argparse

from taskflow.display import format_table
from taskflow.manager import TaskManager


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

    subparsers.add_parser("list", help="List all tasks")
    return parser


def main() -> None:
    """Read the command from the terminal and run it."""
    args = build_parser().parse_args()
    manager = TaskManager()

    if args.command == "add":
        task = manager.add(args.title, args.description, args.priority, args.due)
        print(f"Task {task.id} added: {task.title}")
    elif args.command == "list":
        print(format_table(manager.get_all()))


if __name__ == "__main__":
    main()