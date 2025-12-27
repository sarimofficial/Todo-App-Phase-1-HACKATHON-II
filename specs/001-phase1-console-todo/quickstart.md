# Quickstart: Phase I - Console Todo Application

**Feature**: 001-phase1-console-todo
**Date**: 2025-12-28

## Prerequisites

- Python 3.11 or higher
- No additional packages required (standard library only)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd TodoApp
```

### 2. Verify Python Version

```bash
python --version
# Should output: Python 3.11.x or higher
```

### 3. (Optional) Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 4. Install Development Dependencies

```bash
pip install pytest pytest-cov ruff
```

## Running the Application

```bash
python -m src.main
```

Or:

```bash
python src/main.py
```

## Usage

### Main Menu

```
=== Todo Application ===

1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Complete
6. Exit

Select option: _
```

### Example Session

```
=== Todo Application ===

1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Complete
6. Exit

Select option: 1
Enter task title: Buy groceries
Task added with ID: 1

Select option: 1
Enter task title: Call mom
Task added with ID: 2

Select option: 2
=== Your Tasks ===
1. [ ] Buy groceries
2. [ ] Call mom

Select option: 5
Enter task ID to toggle: 2
Task 2 marked as complete

Select option: 2
=== Your Tasks ===
1. [ ] Buy groceries
2. [X] Call mom

Select option: 4
Enter task ID to delete: 1
Task 1 deleted

Select option: 2
=== Your Tasks ===
2. [X] Call mom

Select option: 6
Goodbye!
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=src --cov-report=term-missing
```

### Run Specific Test File

```bash
pytest tests/unit/test_task_service.py
```

## Linting

### Check Code

```bash
ruff check src/ tests/
```

### Auto-fix Issues

```bash
ruff check --fix src/ tests/
```

### Format Code

```bash
ruff format src/ tests/
```

## Project Structure

```
TodoApp/
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Task dataclass
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py  # Business logic
│   └── cli/
│       ├── __init__.py
│       ├── menu.py          # Menu display
│       └── handlers.py      # Menu handlers
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_task.py
│   │   └── test_task_service.py
│   └── integration/
│       ├── __init__.py
│       └── test_cli_flow.py
└── specs/
    └── 001-phase1-console-todo/
        ├── spec.md
        ├── plan.md
        ├── research.md
        ├── data-model.md
        └── quickstart.md    # This file
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'src'"

Run from the repository root directory:

```bash
cd TodoApp
python -m src.main
```

### "python: command not found"

Try using `python3` instead:

```bash
python3 -m src.main
```

### Tests Not Found

Ensure you have `__init__.py` files in all test directories:

```bash
touch tests/__init__.py tests/unit/__init__.py tests/integration/__init__.py
```

## Limitations (Phase I)

- **No persistence**: All tasks are lost when you exit the application
- **Single user**: No authentication or multi-user support
- **No search/filter**: View shows all tasks; no filtering capability
- **No priorities/dates**: Tasks have only title and completion status

These limitations are intentional for Phase I. They will be addressed in subsequent phases.
