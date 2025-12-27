"""Main entry point for the todo application.

This module provides the main application loop and orchestrates
all menu options.
"""

from src.cli.handlers import (
    handle_add_task,
    handle_delete_task,
    handle_toggle_complete,
    handle_update_task,
    handle_view_tasks,
)
from src.cli.menu import display_menu, get_user_choice
from src.services.task_service import TaskService


def main() -> None:
    """Run the todo application."""
    task_service = TaskService()

    while True:
        display_menu()
        try:
            choice = get_user_choice()
        except ValueError:
            print("Invalid option")
            continue

        if choice == 1:
            handle_add_task(task_service)
        elif choice == 2:
            handle_view_tasks(task_service)
        elif choice == 3:
            handle_update_task(task_service)
        elif choice == 4:
            handle_delete_task(task_service)
        elif choice == 5:
            handle_toggle_complete(task_service)
        elif choice == 6:
            print("Goodbye!")
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
