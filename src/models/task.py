"""Task data model for the todo application.

This module defines the Task class representing a single todo item.
"""


from dataclasses import dataclass


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique sequential identifier (auto-assigned, starts at 1)
        title: Description of the task (1-200 characters)
        completed: Whether the task is marked complete (default: False)
    """

    id: int
    title: str
    completed: bool = False
