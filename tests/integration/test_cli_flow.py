"""Integration tests for CLI flow."""

from unittest.mock import patch

from src.cli.handlers import (
    format_task,
    handle_add_task,
    handle_delete_task,
    handle_toggle_complete,
    handle_update_task,
    handle_view_tasks,
    validate_id,
    validate_title,
)
from src.models.task import Task
from src.services.task_service import TaskService


class TestValidateTitle:
    """Test cases for validate_title function."""

    def test_valid_title(self) -> None:
        """Test that a valid title returns (title, None)."""
        result = validate_title("Buy groceries")
        assert result == ("Buy groceries", None)

    def test_empty_title(self) -> None:
        """Test that empty title returns error."""
        result = validate_title("")
        assert result == ("", "Task title cannot be empty")

    def test_whitespace_only_title(self) -> None:
        """Test that whitespace-only title returns error."""
        result = validate_title("   ")
        assert result == ("", "Task title cannot be empty")

    def test_title_truncation(self) -> None:
        """Test that titles over 200 chars are truncated."""
        long_title = "x" * 250
        result = validate_title(long_title)
        assert len(result[0]) == 200
        assert result[1] == "Warning: Title truncated to 200 characters"

    def test_title_with_leading_whitespace(self) -> None:
        """Test that leading whitespace is stripped."""
        result = validate_title("  Buy groceries")
        assert result == ("Buy groceries", None)

    def test_title_with_trailing_whitespace(self) -> None:
        """Test that trailing whitespace is stripped."""
        result = validate_title("Buy groceries  ")
        assert result == ("Buy groceries", None)

    def test_title_with_special_characters(self) -> None:
        """Test that special characters are preserved."""
        result = validate_title("Task @#$%^&*()")
        assert result == ("Task @#$%^&*()", None)


class TestValidateId:
    """Test cases for validate_id function."""

    def test_valid_id(self) -> None:
        """Test that a valid ID returns (int, None)."""
        result = validate_id("42")
        assert result == (42, None)

    def test_negative_id(self) -> None:
        """Test that negative IDs are accepted."""
        result = validate_id("-1")
        assert result == (-1, None)

    def test_invalid_id_non_numeric(self) -> None:
        """Test that non-numeric input returns error."""
        result = validate_id("abc")
        assert result == (None, "Invalid ID format - please enter a number")

    def test_invalid_id_float_string(self) -> None:
        """Test that float string returns error."""
        result = validate_id("3.14")
        assert result == (None, "Invalid ID format - please enter a number")


class TestFormatTask:
    """Test cases for format_task function."""

    def test_incomplete_task(self) -> None:
        """Test formatting an incomplete task."""
        task = Task(id=1, title="Buy groceries", completed=False)
        result = format_task(task)
        assert result == "1. [ ] Buy groceries"

    def test_completed_task(self) -> None:
        """Test formatting a completed task."""
        task = Task(id=2, title="Call mom", completed=True)
        result = format_task(task)
        assert result == "2. [X] Call mom"


class TestHandlerViewTasks:
    """Test cases for handle_view_tasks function."""

    @patch("builtins.print")
    def test_view_empty_tasks(self, mock_print) -> None:
        """Test viewing when no tasks exist."""
        service = TaskService()
        handle_view_tasks(service)
        mock_print.assert_called_once_with("No tasks found")

    @patch("builtins.print")
    def test_view_with_tasks(self, mock_print) -> None:
        """Test viewing with tasks."""
        service = TaskService()
        service.add_task("Task 1")
        service.add_task("Task 2")
        handle_view_tasks(service)
        # Should print each task formatted
        calls = mock_print.call_args_list
        assert len(calls) == 2
        assert "1. [ ] Task 1" in str(calls[0])
        assert "2. [ ] Task 2" in str(calls[1])


class TestHandlerAddTask:
    """Test cases for handle_add_task function."""

    @patch("builtins.input", return_value="Buy groceries")
    @patch("builtins.print")
    def test_add_task_success(self, mock_print, mock_input) -> None:
        """Test adding a task successfully."""
        service = TaskService()
        handle_add_task(service)
        mock_print.assert_called_with("Task added with ID: 1")
        assert service.get_task(1) is not None

    @patch("builtins.input", return_value="")
    @patch("builtins.print")
    def test_add_task_empty_title(self, mock_print, mock_input) -> None:
        """Test adding a task with empty title."""
        service = TaskService()
        handle_add_task(service)
        mock_print.assert_called_with("Task title cannot be empty")
        assert len(service.get_all_tasks()) == 0


class TestHandlerToggleComplete:
    """Test cases for handle_toggle_complete function."""

    @patch("builtins.input", return_value="abc")
    @patch("builtins.print")
    def test_toggle_invalid_id(self, mock_print, mock_input) -> None:
        """Test toggling with invalid ID format."""
        service = TaskService()
        handle_toggle_complete(service)
        mock_print.assert_called_with("Invalid ID format - please enter a number")

    @patch("builtins.input", return_value="999")
    @patch("builtins.print")
    def test_toggle_not_found(self, mock_print, mock_input) -> None:
        """Test toggling a non-existent task."""
        service = TaskService()
        handle_toggle_complete(service)
        mock_print.assert_called_with("Task not found: ID 999")


class TestHandlerUpdateTask:
    """Test cases for handle_update_task function."""

    @patch("builtins.input", side_effect=["1", "Updated title"])
    @patch("builtins.print")
    def test_update_success(self, mock_print, mock_input) -> None:
        """Test updating a task successfully."""
        service = TaskService()
        service.add_task("Original title")
        handle_update_task(service)
        mock_print.assert_called_with("Task 1 updated")
        assert service.get_task(1).title == "Updated title"


class TestHandlerDeleteTask:
    """Test cases for handle_delete_task function."""

    @patch("builtins.input", return_value="999")
    @patch("builtins.print")
    def test_delete_not_found(self, mock_print, mock_input) -> None:
        """Test deleting a non-existent task."""
        service = TaskService()
        handle_delete_task(service)
        mock_print.assert_called_with("Task not found: ID 999")
