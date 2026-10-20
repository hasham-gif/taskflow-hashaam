# TaskFlow

TaskFlow is a command-line task manager written in Python. You can add, view,
update, complete, delete, filter, search and sort tasks directly from the
terminal. Tasks are saved in a JSON file, so they are still there the next time
you run the program.

## Features

- Add tasks with a title, description, priority and due date
- List tasks in a clean table
- Update, complete and delete tasks
- Filter tasks by status or priority
- Search tasks by keyword in the title or description
- Sort tasks by due date or priority
- Overdue tasks are marked as `OVERDUE`
- Input validation with friendly error messages (no raw tracebacks)
- Automatic saving to `data/tasks.json`

## Installation

Requirements: Python 3.10 or newer and Git.

```bash
git clone https://github.com/hasham-gif/taskflow-hashaam.git
cd taskflow-hashaam
python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows (CMD)
.venv\Scripts\activate.bat

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Mac / Linux
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Add a task:

```bash
python main.py add "Finish report" -d "Quarterly summary" -p high --due 2026-11-15
```

List tasks, with optional filters and sorting:

```bash
python main.py list
python main.py list --status pending
python main.py list -p high
python main.py list --status pending -p high --sort due
```

Search tasks by keyword:

```bash
python main.py search "report"
```

Update, complete and delete a task by its ID:

```bash
python main.py update 3 --title "Finish final report" -p medium
python main.py done 3
python main.py delete 3
```

Example output:

```
ID  Title                Priority  Due         Status
--  -------------------  --------  ----------  -------
1   Finish final report  medium    2026-11-15  pending
2   Buy groceries        low       -           done
3   Study for exam       high      2026-10-01  OVERDUE
```

Valid priorities are `low`, `medium` and `high`. Dates use the `YYYY-MM-DD`
format. Sort options are `due` and `priority`.

## Project Structure

```
taskflow-hashaam/
|-- main.py              # Entry point, command-line parsing (argparse)
|-- taskflow/
|   |-- __init__.py
|   |-- models.py        # Task class
|   |-- storage.py       # Load/save the JSON file
|   |-- manager.py       # Business logic (add, update, delete, filter...)
|   |-- validators.py    # Input validation functions
|   `-- display.py       # Table formatting
|-- tests/
|   |-- test_models.py
|   |-- test_manager.py
|   `-- test_validators.py
|-- data/
|   `-- tasks.json       # Created automatically
|-- requirements.txt
|-- .gitignore
`-- README.md
```

## Running the Tests

```bash
python -m pytest -v
```

## Author

Hashaam