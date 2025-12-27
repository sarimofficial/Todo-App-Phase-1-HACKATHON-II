"""Unit tests for the TaskService."""

from src.services.task_service import TaskService


class TestTaskService:
    """Test cases for the TaskService class."""

    def test_initial_state(self) -> None:
        """Test that a new TaskService has empty tasks."""
        service = TaskService()
        assert service.get_all_tasks() == []

    def test_add_task(self) -> None:
        """Test adding a task."""
        service = TaskService()
        task = service.add_task("Buy groceries")
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.completed is False

    def test_add_multiple_tasks(self) -> None:
        """Test adding multiple tasks gets sequential IDs."""
        service = TaskService()
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        task3 = service.add_task("Task 3")
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_get_all_tasks(self) -> None:
        """Test getting all tasks."""
        service = TaskService()
        service.add_task("Task 1")
        service.add_task("Task 2")
        tasks = service.get_all_tasks()
        assert len(tasks) == 2
        assert tasks[0].id == 1
        assert tasks[1].id == 2

    def test_get_task_found(self) -> None:
        """Test getting an existing task by ID."""
        service = TaskService()
        service.add_task("Task 1")
        task = service.get_task(1)
        assert task is not None
        assert task.title == "Task 1"

    def test_get_task_not_found(self) -> None:
        """Test getting a non-existent task returns None."""
        service = TaskService()
        task = service.get_task(999)
        assert task is None

    def test_update_task_success(self) -> None:
        """Test updating a task's title."""
        service = TaskService()
        service.add_task("Original title")
        success = service.update_task(1, "New title")
        assert success is True
        task = service.get_task(1)
        assert task is not None
        assert task.title == "New title"

    def test_update_task_not_found(self) -> None:
        """Test updating a non-existent task returns False."""
        service = TaskService()
        success = service.update_task(999, "New title")
        assert success is False

    def test_delete_task_success(self) -> None:
        """Test deleting a task."""
        service = TaskService()
        service.add_task("Task to delete")
        success = service.delete_task(1)
        assert success is True
        assert service.get_task(1) is None

    def test_delete_task_not_found(self) -> None:
        """Test deleting a non-existent task returns False."""
        service = TaskService()
        success = service.delete_task(999)
        assert success is False

    def test_toggle_complete_false_to_true(self) -> None:
        """Test toggling task from incomplete to complete."""
        service = TaskService()
        service.add_task("Task")
        success = service.toggle_complete(1)
        assert success is True
        task = service.get_task(1)
        assert task is not None
        assert task.completed is True

    def test_toggle_complete_true_to_false(self) -> None:
        """Test toggling task from complete to incomplete."""
        service = TaskService()
        service.add_task("Task")
        service.toggle_complete(1)  # Complete it
        service.toggle_complete(1)  # Toggle again
        task = service.get_task(1)
        assert task is not None
        assert task.completed is False

    def test_toggle_complete_not_found(self) -> None:
        """Test toggling a non-existent task returns False."""
        service = TaskService()
        success = service.toggle_complete(999)
        assert success is False

    def test_ids_not_reused_after_delete(self) -> None:
        """Test that deleted task IDs are not reused."""
        service = TaskService()
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.delete_task(1)
        new_task = service.add_task("Task 3")
        assert new_task.id == 3  # Should be 3, not 1

    def test_get_all_tasks_after_deletions(self) -> None:
        """Test that get_all_tasks returns remaining tasks sorted by ID."""
        service = TaskService()
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.add_task("Task 3")
        service.delete_task(2)
        tasks = service.get_all_tasks()
        assert len(tasks) == 2
        assert tasks[0].id == 1
        assert tasks[1].id == 3
