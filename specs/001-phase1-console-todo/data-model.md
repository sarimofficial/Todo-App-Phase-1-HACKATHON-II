# Data Model: Phase I - Console Todo Application

**Feature**: 001-phase1-console-todo
**Date**: 2025-12-28
**Source**: [spec.md](./spec.md) Key Entities section

## Entities

### Task

Represents a single todo item in the application.

**Source**: FR-002, FR-003, FR-004, FR-008, FR-009 from spec.md

#### Fields

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| `id` | `int` | Unique, sequential, ≥1, auto-assigned | N/A (auto) | Unique identifier for the task |
| `title` | `str` | Non-empty, 1-200 characters, stripped | N/A (required) | Description of the task |
| `completed` | `bool` | - | `False` | Whether the task is marked complete |

#### Validation Rules

| Rule | Field | Condition | Error Message |
|------|-------|-----------|---------------|
| Non-empty | `title` | `len(title.strip()) > 0` | "Task title cannot be empty" |
| Max length | `title` | `len(title) <= 200` | Warning + truncate to 200 |
| No whitespace-only | `title` | `title.strip() != ""` | "Task title cannot be empty" |

#### State Transitions

```
                    toggle_complete()
    ┌─────────────────────────────────────────┐
    │                                         │
    ▼                                         │
┌─────────┐     toggle_complete()      ┌──────┴────┐
│ created │ ─────────────────────────► │ completed │
│ (False) │ ◄───────────────────────── │  (True)   │
└─────────┘     toggle_complete()      └───────────┘
```

- Task is created with `completed=False`
- `toggle_complete()` flips between `True` and `False`
- No other state transitions exist

#### Python Implementation

```python
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
```

## Storage Model

### TaskStore (In-Memory)

The `TaskService` class manages task storage internally.

#### Structure

```python
class TaskService:
    _tasks: dict[int, Task]  # ID -> Task mapping
    _next_id: int            # Auto-increment counter (starts at 1)
```

#### Invariants

1. `_next_id` is always greater than any key in `_tasks`
2. All keys in `_tasks` are unique positive integers
3. `_tasks[id].id == id` for all entries (key matches Task.id)
4. Deleted IDs are never reused

#### Operations

| Operation | Input | Output | Side Effects |
|-----------|-------|--------|--------------|
| `add_task` | `title: str` | `Task` | Increments `_next_id`, adds to `_tasks` |
| `get_all_tasks` | - | `list[Task]` | None (read-only) |
| `get_task` | `task_id: int` | `Task \| None` | None (read-only) |
| `update_task` | `task_id: int, title: str` | `bool` | Modifies `_tasks[task_id].title` |
| `delete_task` | `task_id: int` | `bool` | Removes from `_tasks` |
| `toggle_complete` | `task_id: int` | `bool` | Flips `_tasks[task_id].completed` |

## Relationships

Phase I has only one entity (Task) with no relationships. Future phases may introduce:
- User → Task (ownership)
- Category → Task (classification)
- Project → Task (grouping)

These are out of scope for Phase I per spec constraints.

## Display Format

Per FR-008 and spec CLI examples:

```
{id}. [{status}] {title}
```

Where:
- `{id}` = Task ID (integer)
- `{status}` = "X" if completed, " " (space) if not
- `{title}` = Task title (truncated display if needed)

**Examples**:
```
1. [ ] Buy groceries
2. [X] Call mom
3. [ ] Finish report
```
