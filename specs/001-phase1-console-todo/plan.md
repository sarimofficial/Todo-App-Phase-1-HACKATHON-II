# Implementation Plan: Phase I - Console Todo Application

**Branch**: `001-phase1-console-todo` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-phase1-console-todo/spec.md`

## Summary

Phase I implements a minimal in-memory Python console application for task management. The application provides a menu-driven CLI interface with basic CRUD operations (Add, View, Update, Delete) and task completion toggling. All data is stored in memory using Python's built-in data structures - no persistence, no external dependencies.

This phase establishes the foundational task management domain model and user interaction patterns that will be extended with persistence, APIs, and advanced features in subsequent phases.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: None (Python standard library only)
**Storage**: In-memory (Python dictionary)
**Testing**: pytest
**Target Platform**: Any platform with Python 3.11+ (Windows, macOS, Linux)
**Project Type**: Single project (console application)
**Performance Goals**: <1 second response for all operations (per SC-005)
**Constraints**: No external dependencies, no persistence, no network
**Scale/Scope**: Single user, up to 20 tasks displayed without scrolling (per SC-002)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development ✅

| Gate | Status | Evidence |
|------|--------|----------|
| Approved specification exists | ✅ PASS | `specs/001-phase1-console-todo/spec.md` |
| Plan derived from spec only | ✅ PASS | All features trace to FR-001 through FR-010 |
| No new features introduced | ✅ PASS | Plan implements only spec requirements |

### Principle II: Agent Behavior Rules ✅

| Gate | Status | Evidence |
|------|--------|----------|
| No code written yet | ✅ PASS | Planning phase only |
| No feature invention | ✅ PASS | All items from spec |
| Clarifications at plan level | ✅ PASS | No implementation-time decisions deferred |

### Principle III: Phase Governance ✅

| Gate | Status | Evidence |
|------|--------|----------|
| Phase scope respected | ✅ PASS | In-memory only, no Phase II-V features |
| No future-phase leakage | ✅ PASS | No database, API, or AI references |
| Architecture scoped to phase | ✅ PASS | Simple Python structures only |

### Principle IV: Technology Constraints ⚠️ JUSTIFIED DEVIATION

| Gate | Status | Evidence |
|------|--------|----------|
| Python 3.11+ | ✅ PASS | Using Python as mandated |
| FastAPI/SQLModel/NeonDB | ⚠️ N/A | Not applicable for Phase I per spec constraints |
| pytest for testing | ✅ PASS | Will use pytest |
| No unauthorized dependencies | ✅ PASS | Standard library only |

**Deviation Justification**: The constitution's Phase Architecture table shows Phase I scope as "Core Todo API" with FastAPI/SQLModel/NeonDB. However, the approved Phase I specification explicitly constrains this phase to be an in-memory console application with no databases, files, or web frameworks. Per the Constitution's Supremacy Clause, the specification's explicit constraints for this phase take precedence for implementation details, while the constitution's technology stack applies when those technologies are used. This is a valid phased approach where Phase I establishes domain logic before Phase II adds persistence and APIs.

### Principle V: Quality Principles ✅

| Gate | Status | Evidence |
|------|--------|----------|
| Clean architecture | ✅ PASS | Separation: models, services, CLI |
| Type hints | ✅ PASS | All code will include type hints |
| Linting (ruff) | ✅ PASS | Will configure ruff |
| Docstrings | ✅ PASS | All public functions documented |
| Test coverage 80% | ✅ PASS | Target 80%+ coverage |

## Project Structure

### Documentation (this feature)

```text
specs/001-phase1-console-todo/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── checklists/          # Validation checklists
│   └── requirements.md
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── main.py              # Application entry point
├── models/
│   ├── __init__.py
│   └── task.py          # Task dataclass
├── services/
│   ├── __init__.py
│   └── task_service.py  # Task CRUD operations
└── cli/
    ├── __init__.py
    ├── menu.py          # Menu display and input handling
    └── handlers.py      # Menu option handlers

tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   ├── test_task.py           # Task model tests
│   └── test_task_service.py   # Service layer tests
└── integration/
    ├── __init__.py
    └── test_cli_flow.py       # End-to-end CLI tests
```

**Structure Decision**: Single project structure selected. Clean separation between:
- **models/**: Pure data structures (Task dataclass)
- **services/**: Business logic (TaskService with CRUD operations)
- **cli/**: User interface (menu display, input handling, output formatting)

This structure supports the constitution's clean architecture principle while keeping the implementation minimal for Phase I.

## Architecture Design

### Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        main.py                               │
│                    (Entry Point)                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      cli/menu.py                             │
│                   (Menu Loop & Input)                        │
│  - display_menu()                                            │
│  - get_user_choice()                                         │
│  - run_menu_loop()                                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    cli/handlers.py                           │
│                  (Menu Option Handlers)                      │
│  - handle_add_task()                                         │
│  - handle_view_tasks()                                       │
│  - handle_update_task()                                      │
│  - handle_delete_task()                                      │
│  - handle_toggle_complete()                                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 services/task_service.py                     │
│                    (Business Logic)                          │
│  - add_task(title) -> Task                                   │
│  - get_all_tasks() -> list[Task]                             │
│  - get_task(id) -> Task | None                               │
│  - update_task(id, title) -> bool                            │
│  - delete_task(id) -> bool                                   │
│  - toggle_complete(id) -> bool                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    models/task.py                            │
│                     (Data Model)                             │
│  @dataclass                                                  │
│  class Task:                                                 │
│      id: int                                                 │
│      title: str                                              │
│      completed: bool = False                                 │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Input** → `cli/menu.py` receives menu selection
2. **Dispatch** → `cli/handlers.py` routes to appropriate handler
3. **Business Logic** → `services/task_service.py` performs operation
4. **Data** → `models/task.py` Task instances stored in dictionary
5. **Output** → Handler formats and prints result to stdout

### In-Memory Storage Strategy

```python
# In TaskService (services/task_service.py)
class TaskService:
    def __init__(self):
        self._tasks: dict[int, Task] = {}  # ID -> Task mapping
        self._next_id: int = 1             # Auto-increment counter
```

**Design Decisions**:
- **Dictionary over List**: O(1) lookup by ID for update/delete/toggle operations
- **Sequential IDs**: Simple counter, never reused (deleted IDs leave gaps)
- **Single Instance**: One TaskService instance created at startup, passed to handlers

### ID Generation Strategy

Per FR-002: "System MUST assign a unique sequential integer ID to each new task starting from 1"

```python
def add_task(self, title: str) -> Task:
    task = Task(id=self._next_id, title=title, completed=False)
    self._tasks[self._next_id] = task
    self._next_id += 1
    return task
```

- IDs start at 1 (user-friendly, per spec CLI examples)
- IDs are never reused even after deletion
- Counter persists for application lifetime (resets on restart)

### Error Handling Strategy

| Error Type | Detection Point | User Message | Implementation |
|------------|-----------------|--------------|----------------|
| Empty title | `handlers.py` | "Task title cannot be empty" | Check `title.strip()` |
| Whitespace-only | `handlers.py` | "Task title cannot be empty" | Check `title.strip()` |
| Title too long | `handlers.py` | Warning + truncate | Check `len(title) > 200` |
| Invalid ID format | `handlers.py` | "Invalid ID format - please enter a number" | `try/except ValueError` |
| Task not found | `task_service.py` | "Task not found: ID X" | Return `None` or `False` |
| Invalid menu option | `menu.py` | "Invalid option" | Check against valid range |
| Empty task list | `handlers.py` | "No tasks found" | Check `len(tasks) == 0` |

**Principle**: All errors handled gracefully with user-friendly messages. No stack traces shown to user (per SC-004).

### Input Validation

```python
# Title validation (in handlers.py)
def validate_title(title: str) -> tuple[str, str | None]:
    """Validate and normalize task title.

    Returns:
        tuple: (normalized_title, error_message or None)
    """
    stripped = title.strip()
    if not stripped:
        return "", "Task title cannot be empty"
    if len(stripped) > 200:
        return stripped[:200], "Warning: Title truncated to 200 characters"
    return stripped, None

# ID validation (in handlers.py)
def validate_id(id_input: str) -> tuple[int | None, str | None]:
    """Validate task ID input.

    Returns:
        tuple: (parsed_id or None, error_message or None)
    """
    try:
        return int(id_input), None
    except ValueError:
        return None, "Invalid ID format - please enter a number"
```

### CLI Control Flow

```
┌──────────────────────────────────────────┐
│              Application Start            │
└──────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────┐
│         Initialize TaskService            │
└──────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────┐
│            Display Menu                   │◄────────────┐
└──────────────────────────────────────────┘             │
                    │                                     │
                    ▼                                     │
┌──────────────────────────────────────────┐             │
│          Get User Choice                  │             │
└──────────────────────────────────────────┘             │
                    │                                     │
        ┌───────────┼───────────┐                        │
        ▼           ▼           ▼                        │
    [1-5]       [6/Exit]    [Invalid]                    │
        │           │           │                        │
        ▼           │           ▼                        │
┌───────────┐       │    ┌─────────────┐                │
│  Execute  │       │    │   Display   │                │
│  Handler  │       │    │   "Invalid  │                │
└───────────┘       │    │    option"  │                │
        │           │    └─────────────┘                │
        │           │           │                        │
        ▼           │           │                        │
┌───────────┐       │           │                        │
│  Display  │       │           │                        │
│  Result   │       │           │                        │
└───────────┘       │           │                        │
        │           │           │                        │
        └───────────┴───────────┴────────────────────────┘
                    │
                    ▼ (Exit selected)
┌──────────────────────────────────────────┐
│           Display "Goodbye!"              │
└──────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────┐
│           Application Exit                │
└──────────────────────────────────────────┘
```

## Complexity Tracking

> No constitution violations requiring justification. The Phase I scope deviation from the full technology stack is already approved in the specification.

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| No FastAPI/SQLModel | Use pure Python | Spec explicitly prohibits web frameworks and databases |
| Dictionary storage | `dict[int, Task]` | Simplest structure meeting O(1) lookup requirement |
| No persistence | In-memory only | Spec constraint; data lost on exit is expected behavior |

## Dependencies

### Runtime Dependencies

None. Python 3.11+ standard library only.

### Development Dependencies

| Package | Purpose | Version |
|---------|---------|---------|
| pytest | Unit and integration testing | ^8.0 |
| pytest-cov | Test coverage reporting | ^4.0 |
| ruff | Linting and formatting | ^0.1 |

## Testing Strategy

### Test Pyramid

```
        ┌─────────────────┐
        │  Integration    │  tests/integration/test_cli_flow.py
        │     Tests       │  - Full menu loop scenarios
        │    (10%)        │  - User workflow validation
        └─────────────────┘
               │
        ┌──────┴──────┐
        │             │
┌───────────────┐ ┌───────────────┐
│   Service     │ │    Model      │  tests/unit/
│   Tests       │ │    Tests      │  - test_task_service.py
│   (50%)       │ │   (40%)       │  - test_task.py
└───────────────┘ └───────────────┘
```

### Test Coverage Targets

| Component | Target | Rationale |
|-----------|--------|-----------|
| `models/task.py` | 100% | Simple dataclass, full coverage trivial |
| `services/task_service.py` | 100% | Core business logic, must be fully tested |
| `cli/handlers.py` | 90% | Input validation and formatting |
| `cli/menu.py` | 80% | I/O heavy, some paths harder to test |
| **Overall** | **80%+** | Per constitution requirement |

### Key Test Scenarios

From spec acceptance scenarios:

1. **Add Task**: Valid title, empty title, whitespace-only, >200 chars
2. **View Tasks**: Empty list, populated list, mixed completion states
3. **Update Task**: Valid update, invalid ID, empty new title
4. **Delete Task**: Valid delete, invalid ID, already deleted
5. **Toggle Complete**: Complete→Incomplete, Incomplete→Complete, invalid ID
6. **Menu**: Valid options 1-6, invalid option, non-numeric input

## Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Scope creep (adding features) | Medium | High | Strict adherence to spec, no "improvements" |
| Over-engineering | Medium | Medium | Keep structures minimal, avoid abstractions |
| ID overflow | Very Low | Low | Python int unlimited; not a concern for Phase I scale |
