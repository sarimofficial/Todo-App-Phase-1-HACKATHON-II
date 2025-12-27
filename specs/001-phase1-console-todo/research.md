# Research: Phase I - Console Todo Application

**Feature**: 001-phase1-console-todo
**Date**: 2025-12-28
**Status**: Complete

## Overview

This document consolidates research findings for Phase I implementation decisions. Given the simplicity of Phase I (in-memory console application with no external dependencies), research focused on Python best practices and design patterns appropriate for the scope.

## Research Topics

### 1. Python Data Model: dataclass vs TypedDict vs namedtuple

**Decision**: Use `@dataclass` for the Task model

**Rationale**:
- Dataclasses provide mutable instances (needed for toggling completion)
- Built-in `__init__`, `__repr__`, and `__eq__` reduce boilerplate
- Type hints are first-class citizens
- Available in Python 3.7+ (well within our 3.11+ requirement)

**Alternatives Considered**:

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| `@dataclass` | Mutable, type-hinted, minimal boilerplate | Slightly more memory than namedtuple | ✅ Selected |
| `TypedDict` | Dict-like access | Mutable in ways that break immutability expectations | ❌ Rejected |
| `namedtuple` | Immutable, memory efficient | Requires creating new instance on every update | ❌ Rejected |
| Plain class | Full control | Unnecessary boilerplate for simple model | ❌ Rejected |

### 2. In-Memory Storage: dict vs list

**Decision**: Use `dict[int, Task]` with ID as key

**Rationale**:
- O(1) lookup by ID for get, update, delete, and toggle operations
- ID-based operations are the primary access pattern (spec requires ID input)
- Natural fit for sparse ID space (deleted IDs leave gaps)

**Alternatives Considered**:

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| `dict[int, Task]` | O(1) ID lookup | Slightly more memory | ✅ Selected |
| `list[Task]` | Sequential access, memory efficient | O(n) ID lookup, index != ID after deletions | ❌ Rejected |
| `OrderedDict` | Maintains insertion order | Unnecessary complexity, dict is ordered in Python 3.7+ | ❌ Rejected |

### 3. CLI Input Handling: input() vs argparse vs click

**Decision**: Use built-in `input()` function

**Rationale**:
- Spec requires interactive menu-based interface, not command-line arguments
- No external dependencies allowed (per spec constraints)
- Simple and sufficient for the use case

**Alternatives Considered**:

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| `input()` | Built-in, no dependencies | Basic, no auto-completion | ✅ Selected |
| `argparse` | Structured CLI | Wrong paradigm (args vs interactive menu) | ❌ Rejected |
| `click` | Rich CLI features | External dependency, overkill for Phase I | ❌ Rejected |
| `prompt_toolkit` | Advanced interactive prompts | External dependency | ❌ Rejected |

### 4. Project Structure: Flat vs Layered

**Decision**: Layered structure with models/, services/, cli/

**Rationale**:
- Supports constitution's clean architecture principle
- Separates concerns: data (models), logic (services), presentation (cli)
- Prepares codebase for Phase II expansion (services can be reused with API)
- Not over-engineered: only 3 layers, each with clear purpose

**Structure**:
```
src/
├── models/      # Pure data structures
├── services/    # Business logic
└── cli/         # User interface
```

### 5. Error Handling: Exceptions vs Return Values

**Decision**: Mixed approach - return values for expected cases, exceptions for unexpected

**Rationale**:
- "Task not found" is expected user behavior → return `None` or `False`
- Input validation failures are expected → return error messages
- True exceptions (file system errors, etc.) are not applicable in Phase I
- User sees friendly messages, never stack traces (per SC-004)

**Implementation Pattern**:
```python
# Service layer returns None/False for "not found"
def get_task(self, task_id: int) -> Task | None:
    return self._tasks.get(task_id)

# Handler layer converts to user message
task = service.get_task(task_id)
if task is None:
    print(f"Task not found: ID {task_id}")
```

### 6. Testing Strategy: pytest Fixtures vs Setup Methods

**Decision**: Use pytest fixtures for service instances

**Rationale**:
- Fixtures provide clean, isolated test setup
- Easy to share common test data across test modules
- Constitution mandates pytest

**Pattern**:
```python
@pytest.fixture
def task_service():
    """Provide fresh TaskService for each test."""
    return TaskService()

def test_add_task(task_service):
    task = task_service.add_task("Test task")
    assert task.id == 1
```

## Resolved Clarifications

No NEEDS CLARIFICATION items from Technical Context. All decisions made based on:
- Spec constraints (no external dependencies)
- Constitution principles (clean architecture, type hints, pytest)
- Python best practices for the given scope

## Dependencies Confirmed

### Runtime
- None (Python standard library only)

### Development
- pytest ^8.0 (testing)
- pytest-cov ^4.0 (coverage)
- ruff ^0.1 (linting)

## Conclusion

Phase I implementation will use:
- `@dataclass` for Task model
- `dict[int, Task]` for in-memory storage
- `input()` for CLI interaction
- Layered project structure (models/services/cli)
- Return values for expected errors, pytest fixtures for testing

All decisions align with spec constraints and constitution principles. No external dependencies required.
