"""Task service for managing todo items.

This module provides the TaskService class which handles all task CRUD operations
using in-memory storage.
"""

from typing import Self

from src.models.task import Task


class TaskService:
    """Service for managing tasks in memory.

    Provides CRUD operations for tasks with sequential ID generation.
    All data is stored in memory and lost when the application exits.
    """

    def __init__(self: Self) -> None:
        """Initialize the task service with empty storage."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self: Self, title: str) -> Task:
        """Create and store a new task.

        Args:
            title: The task title (1-200 characters, non-empty)

        Returns:
            The created Task with assigned ID
        """
        task = Task(id=self._next_id, title=title, completed=False)
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get_all_tasks(self: Self) -> list[Task]:
        """Retrieve all tasks sorted by ID.

        Returns:
            List of all tasks in ID order
        """
        return [self._tasks[task_id] for task_id in sorted(self._tasks.keys())]

    def get_task(self: Self, task_id: int) -> Task | None:
        """Retrieve a task by ID.

        Args:
            task_id: The unique task identifier

        Returns:
            The Task if found, None otherwise
        """
        return self._tasks.get(task_id)

    def update_task(self: Self, task_id: int, title: str) -> bool:
        """Update a task's title.

        Args:
            task_id: The unique task identifier
            title: The new task title (1-200 characters, non-empty)

        Returns:
            True if task was updated, False if not found
        """
        if task_id not in self._tasks:
            return False
        self._tasks[task_id].title = title
        return True

    def delete_task(self: Self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: The unique task identifier

        Returns:
            True if task was deleted, False if not found
        """
        if task_id not in self._tasks:
            return False
        del self._tasks[task_id]
        return True

    def toggle_complete(self: Self, task_id: int) -> bool:
        """Toggle a task's completion status.

        Args:
            task_id: The unique task identifier

        Returns:
            True if task was toggled, False if not found
        """
        if task_id not in self._tasks:
            return False
        self._tasks[task_id].completed = not self._tasks[task_id].completed
        return True
