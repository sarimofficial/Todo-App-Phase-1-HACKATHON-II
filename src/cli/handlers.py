"""CLI handlers for menu options.

This module provides validation functions and handler functions for
all menu options in the todo application.
"""

from src.models.task import Task
from src.services.task_service import TaskService

TITLE_MAX_LENGTH = 200


def validate_title(title: str) -> tuple[str, str | None]:
    """Validate and normalize a task title.

    Args:
        title: The raw title input from user

    Returns:
        Tuple of (normalized_title, error_message or None)
        - If valid: returns (stripped_title, None)
        - If empty/whitespace: returns ("", "Task title cannot be empty")
        - If too long: returns (truncated_title, "Warning: Title truncated to 200 characters")
    """
    stripped = title.strip()
    if not stripped:
        return "", "Task title cannot be empty"
    if len(stripped) > TITLE_MAX_LENGTH:
        return stripped[:TITLE_MAX_LENGTH], "Warning: Title truncated to 200 characters"
    return stripped, None


def validate_id(id_input: str) -> tuple[int | None, str | None]:
    """Validate and parse a task ID input.

    Args:
        id_input: The raw input from user for task ID

    Returns:
        Tuple of (parsed_id or None, error_message or None)
        - If valid integer: returns (int(value), None)
        - If invalid format: returns (None, "Invalid ID format - please enter a number")
    """
    try:
        return int(id_input), None
    except ValueError:
        return None, "Invalid ID format - please enter a number"


def format_task(task: Task) -> str:
    """Format a task for display.

    Args:
        task: The task to format

    Returns:
        Formatted string like "1. [ ] Buy groceries" or "2. [X] Call mom"
    """
    status = "X" if task.completed else " "
    return f"{task.id}. [{status}] {task.title}"


def display_tasks(tasks: list[Task]) -> None:
    """Display all tasks or a message if empty.

    Args:
        tasks: List of tasks to display
    """
    if not tasks:
        print("No tasks found")
    else:
        for task in tasks:
            print(format_task(task))


def handle_view_tasks(task_service: TaskService) -> None:
    """Handle the View Tasks menu option.

    Args:
        task_service: The task service instance
    """
    tasks = task_service.get_all_tasks()
    display_tasks(tasks)


def handle_add_task(task_service: TaskService) -> None:
    """Handle the Add Task menu option.

    Args:
        task_service: The task service instance
    """
    title = input("Enter task title: ")
    normalized_title, error = validate_title(title)

    if error:
        print(error)
        return

    task = task_service.add_task(normalized_title)
    print(f"Task added with ID: {task.id}")


def handle_toggle_complete(task_service: TaskService) -> None:
    """Handle the Toggle Complete menu option.

    Args:
        task_service: The task service instance
    """
    id_input = input("Enter task ID to toggle: ")
    task_id, error = validate_id(id_input)

    if error:
        print(error)
        return

    success = task_service.toggle_complete(task_id)
    if not success:
        print(f"Task not found: ID {task_id}")
        return

    task = task_service.get_task(task_id)
    if task:
        status = "complete" if task.completed else "incomplete"
        print(f"Task {task_id} marked as {status}")


def handle_update_task(task_service: TaskService) -> None:
    """Handle the Update Task menu option.

    Args:
        task_service: The task service instance
    """
    id_input = input("Enter task ID to update: ")
    task_id, error = validate_id(id_input)

    if error:
        print(error)
        return

    task = task_service.get_task(task_id)
    if task is None:
        print(f"Task not found: ID {task_id}")
        return

    new_title = input("Enter new title: ")
    normalized_title, error = validate_title(new_title)

    if error:
        print(error)
        return

    success = task_service.update_task(task_id, normalized_title)
    if success:
        print(f"Task {task_id} updated")


def handle_delete_task(task_service: TaskService) -> None:
    """Handle the Delete Task menu option.

    Args:
        task_service: The task service instance
    """
    id_input = input("Enter task ID to delete: ")
    task_id, error = validate_id(id_input)

    if error:
        print(error)
        return

    success = task_service.delete_task(task_id)
    if success:
        print(f"Task {task_id} deleted")
    else:
        print(f"Task not found: ID {task_id}")
