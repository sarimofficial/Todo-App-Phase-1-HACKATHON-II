"""Menu display and user input handling.

This module provides functions to display the main menu and get user choices.
"""


def display_menu() -> None:
    """Display the main menu options."""
    print()
    print("=== Todo Application ===")
    print()
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Toggle Complete")
    print("6. Exit")
    print()


def get_user_choice() -> int:
    """Get and validate user menu choice.

    Returns:
        The validated menu choice as an integer

    Note:
        This function does not handle invalid input gracefully for TDD.
        The caller should handle ValueError if needed.
    """
    choice = input("Select option: ")
    return int(choice)
