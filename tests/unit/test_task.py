"""Unit tests for the Task model."""

from src.models.task import Task


class TestTask:
    """Test cases for the Task dataclass."""

    def test_task_creation(self) -> None:
        """Test creating a basic task."""
        task = Task(id=1, title="Test task", completed=False)
        assert task.id == 1
        assert task.title == "Test task"
        assert task.completed is False

    def test_task_creation_default_completed(self) -> None:
        """Test that completed defaults to False."""
        task = Task(id=1, title="Test task")
        assert task.completed is False

    def test_task_with_completed_true(self) -> None:
        """Test creating a completed task."""
        task = Task(id=1, title="Test task", completed=True)
        assert task.completed is True

    def test_task_equality(self) -> None:
        """Test task equality comparison."""
        task1 = Task(id=1, title="Test task", completed=False)
        task2 = Task(id=1, title="Test task", completed=False)
        assert task1 == task2

    def test_task_inequality(self) -> None:
        """Test task inequality comparison."""
        task1 = Task(id=1, title="Test task")
        task2 = Task(id=2, title="Test task")
        assert task1 != task2

    def test_task_repr(self) -> None:
        """Test task string representation."""
        task = Task(id=1, title="Test task")
        assert "Task" in repr(task)
        assert "id=1" in repr(task)
        assert "Test task" in repr(task)

    def test_task_with_long_title(self) -> None:
        """Test task with 200 character title."""
        title = "x" * 200
        task = Task(id=1, title=title)
        assert len(task.title) == 200

    def test_task_with_special_characters(self) -> None:
        """Test task with special characters in title."""
        task = Task(id=1, title="Task with special chars: @#$%^&*()")
        assert task.title == "Task with special chars: @#$%^&*()"
