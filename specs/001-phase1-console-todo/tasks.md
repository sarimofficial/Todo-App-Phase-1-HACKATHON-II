# Tasks: Phase I - Console Todo Application

**Input**: Design documents from `/specs/001-phase1-console-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: Tests are OPTIONAL per feature specification - only included where explicitly requested.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths assume single project structure per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create `src/` directory with `__init__.py` at repository root
- [ ] T002 Create `src/models/` directory with `__init__.py`
- [ ] T003 Create `src/services/` directory with `__init__.py`
- [ ] T004 Create `src/cli/` directory with `__init__.py`
- [ ] T005 Create `tests/` directory with `__init__.py`
- [ ] T006 Create `tests/unit/` directory with `__init__.py`
- [ ] T007 Create `tests/integration/` directory with `__init__.py`

**Reference**: plan.md "Source Code" section, project structure

**Checkpoint**: Directory structure created per plan.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [ ] T010 [US1][US2][US3][US4][US5] Create Task dataclass in `src/models/task.py`
  - Fields: `id: int`, `title: str`, `completed: bool = False`
  - Include docstrings per constitution quality principles
  - Reference: data-model.md "Python Implementation" section

- [ ] T011 [US1][US2][US3][US4][US5] Create TaskService class in `src/services/task_service.py`
  - Private `_tasks: dict[int, Task]` for storage
  - Private `_next_id: int = 1` for ID generation
  - Method `add_task(title: str) -> Task`
  - Method `get_all_tasks() -> list[Task]`
  - Method `get_task(task_id: int) -> Task | None`
  - Method `update_task(task_id: int, title: str) -> bool`
  - Method `delete_task(task_id: int) -> bool`
  - Method `toggle_complete(task_id: int) -> bool`
  - Reference: plan.md "In-Memory Storage Strategy" section
  - Reference: data-model.md "Operations" table

- [ ] T012 [US1][US2][US3][US4][US5] Create validation functions in `src/cli/handlers.py`
  - `validate_title(title: str) -> tuple[str, str | None]`
    - Check non-empty, whitespace-only, max 200 chars
    - Return (normalized_title, error_message or None)
  - `validate_id(id_input: str) -> tuple[int | None, str | None]`
    - Parse integer, return error on non-numeric
  - Reference: plan.md "Input Validation" section

**Checkpoint**: Foundation ready - Task model, TaskService, and validation functions complete

---

## Phase 3: User Story 1 - View Task List (Priority: P1) MVP

**Goal**: Users can view all tasks with completion status from the menu

**Independent Test**: Run application, select "View Tasks" option, verify tasks display with correct format

### Tests for User Story 1 (OPTIONAL)

- [ ] T020 [P] [US1] Unit test for Task model in `tests/unit/test_task.py`
- [ ] T021 [P] [US1] Unit test for TaskService.get_all_tasks() in `tests/unit/test_task_service.py`
- [ ] T022 [P] [US1] Unit test for task display format in `tests/unit/test_task.py`

### Implementation for User Story 1

- [ ] T023 [US1] Create `src/cli/menu.py` with menu display functions
  - `display_menu() -> None`: Print the numbered menu options (1-6)
  - `get_user_choice() -> int`: Get and return user input as integer
  - Reference: plan.md "CLI Control Flow" section
  - Reference: spec.md "CLI Interaction Flow" section

- [ ] T024 [US1] Create task display function in `src/cli/handlers.py`
  - `format_task(task: Task) -> str`: Format as "ID. [ ] Title" or "ID. [X] Title"
  - `display_tasks(tasks: list[Task]) -> None`: Display all tasks or "No tasks found" message
  - Reference: data-model.md "Display Format" section
  - Reference: spec.md "View Tasks" menu flow

- [ ] T025 [US1] Create view handler in `src/cli/handlers.py`
  - `handle_view_tasks(task_service: TaskService) -> None`
  - Get tasks from service, display using format_task/display_tasks
  - Reference: spec.md "User Story 1 - View Task List" acceptance scenarios

**Checkpoint**: User Story 1 complete - users can view tasks from the menu

---

## Phase 4: User Story 2 - Add New Task (Priority: P1) MVP

**Goal**: Users can add new tasks with validation

**Independent Test**: Add a task, then view tasks to confirm it appears with correct ID

### Tests for User Story 2 (OPTIONAL)

- [ ] T030 [P] [US2] Unit test for validate_title in `tests/unit/test_task.py`
- [ ] T031 [P] [US2] Unit test for TaskService.add_task() in `tests/unit/test_task_service.py`

### Implementation for User Story 2

- [ ] T032 [US2] Implement add_task method in `src/services/task_service.py`
  - Create Task with sequential ID starting from 1
  - Store in `_tasks` dict
  - Increment `_next_id`
  - Return created Task
  - Reference: plan.md "ID Generation Strategy" section
  - Reference: spec.md "Add Task" acceptance scenarios

- [ ] T033 [US2] Create add handler in `src/cli/handlers.py`
  - `handle_add_task(task_service: TaskService) -> None`
  - Prompt for task title
  - Validate using validate_title()
  - Handle truncation warning for titles >200 chars
  - Call task_service.add_task()
  - Display success message with new task ID
  - Reference: spec.md "Add Task" menu flow

**Checkpoint**: User Story 2 complete - users can add tasks that appear in view

---

## Phase 5: User Story 3 - Mark Task Complete/Incomplete (Priority: P2)

**Goal**: Users can toggle task completion status

**Independent Test**: Add task, mark complete, verify "[X]" appears, mark incomplete, verify "[ ]" appears

### Tests for User Story 3 (OPTIONAL)

- [ ] T040 [P] [US3] Unit test for TaskService.toggle_complete() in `tests/unit/test_task_service.py`

### Implementation for User Story 3

- [ ] T041 [US3] Implement toggle_complete method in `src/services/task_service.py`
  - Find task by ID
  - Flip completed boolean
  - Return True on success, False if not found
  - Reference: data-model.md "State Transitions" section

- [ ] T042 [US3] Create toggle handler in `src/cli/handlers.py`
  - `handle_toggle_complete(task_service: TaskService) -> None`
  - Prompt for task ID
  - Validate using validate_id()
  - Handle "Task not found" error
  - Call task_service.toggle_complete()
  - Display "marked as complete" or "marked as incomplete"
  - Reference: spec.md "Toggle Complete" menu flow
  - Reference: spec.md "User Story 3 - Mark Task Complete/Incomplete"

**Checkpoint**: User Story 3 complete - users can toggle task completion status

---

## Phase 6: User Story 4 - Update Task Title (Priority: P3)

**Goal**: Users can modify task titles

**Independent Test**: Add task, update its title, verify the change appears in view

### Tests for User Story 4 (OPTIONAL)

- [ ] T050 [P] [US4] Unit test for TaskService.update_task() in `tests/unit/test_task_service.py`

### Implementation for User Story 4

- [ ] T051 [US4] Implement update_task method in `src/services/task_service.py`
  - Find task by ID
  - Update title field
  - Return True on success, False if not found
  - Reference: spec.md "User Story 4 - Update Task Title"

- [ ] T052 [US4] Create update handler in `src/cli/handlers.py`
  - `handle_update_task(task_service: TaskService) -> None`
  - Prompt for task ID
  - Validate using validate_id()
  - Prompt for new title
  - Validate using validate_title()
  - Handle errors: invalid ID, empty title
  - Call task_service.update_task()
  - Display success message
  - Reference: spec.md "Update Task" menu flow

**Checkpoint**: User Story 4 complete - users can update task titles

---

## Phase 7: User Story 5 - Delete Task (Priority: P3)

**Goal**: Users can remove tasks

**Independent Test**: Add task, delete it, verify it no longer appears in view

### Tests for User Story 5 (OPTIONAL)

- [ ] T060 [P] [US5] Unit test for TaskService.delete_task() in `tests/unit/test_task_service.py`

### Implementation for User Story 5

- [ ] T061 [US5] Implement delete_task method in `src/services/task_service.py`
  - Remove task from `_tasks` dict
  - Return True on success, False if not found
  - Reference: spec.md "User Story 5 - Delete Task"

- [ ] T062 [US5] Create delete handler in `src/cli/handlers.py`
  - `handle_delete_task(task_service: TaskService) -> None`
  - Prompt for task ID
  - Validate using validate_id()
  - Handle "Task not found" error
  - Call task_service.delete_task()
  - Display success message
  - Reference: spec.md "Delete Task" menu flow

**Checkpoint**: User Story 5 complete - users can delete tasks

---

## Phase 8: User Story 6 - Exit Application (Priority: P3)

**Goal**: Users can exit gracefully with goodbye message

**Independent Test**: Select Exit, verify "Goodbye!" displays and application terminates

### Implementation for User Story 6

- [ ] T070 [US6] Create main application entry point in `src/main.py`
  - Initialize TaskService
  - Run menu loop (while True)
  - Dispatch to appropriate handler based on user choice
  - Handle Exit (option 6): display "Goodbye!" and break loop
  - Handle invalid menu option: display "Invalid option" and continue
  - Reference: plan.md "CLI Control Flow" diagram
  - Reference: spec.md "Exit Application" menu flow

- [ ] T071 [US6] Wire all handlers in `src/cli/handlers.py`
  - Create handler functions that use task_service
  - Reference: plan.md "Component Overview" architecture diagram

**Checkpoint**: User Story 6 complete - application can start, run menu loop, and exit gracefully

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T080 [P] Create pytest configuration in `pyproject.toml` or `pytest.ini`
  - Configure test discovery
  - Enable coverage reporting
  - Reference: plan.md "Testing Strategy" section

- [ ] T081 [P] Configure ruff linting in `pyproject.toml`
  - Enable ruff for Python linting
  - Configure line length, rules
  - Reference: plan.md "Dependencies" section

- [ ] T082 Run full test suite and verify 80%+ coverage
  - Execute: `pytest --cov=src --cov-report=term-missing`
  - Address any coverage gaps
  - Reference: plan.md "Test Coverage Targets"

- [ ] T083 Run ruff linting and fix any issues
  - Execute: `ruff check src/ tests/`
  - Execute: `ruff format src/ tests/`
  - Reference: constitution quality principles

- [ ] T084 Verify quickstart.md instructions work
  - Run application per quickstart.md
  - Test complete workflow: add, view, toggle, delete
  - Reference: quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - User stories can proceed in parallel once foundation is done
  - Or sequentially in priority order (US1 → US2 → US3 → US4 → US5 → US6)
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

| Story | Priority | Can Start After | Dependencies |
|-------|----------|-----------------|--------------|
| US1 (View Tasks) | P1 | Phase 2 | None (foundation only) |
| US2 (Add Task) | P1 | Phase 2 | None (foundation only) |
| US3 (Toggle Complete) | P2 | Phase 2 | Foundation; benefits from US2 adding tasks |
| US4 (Update Task) | P3 | Phase 2 | Foundation; benefits from US2 adding tasks |
| US5 (Delete Task) | P3 | Phase 2 | Foundation; benefits from US2 adding tasks |
| US6 (Exit) | P3 | Phase 2 | Depends on all other handlers being wired |

### Within Each User Story

- Foundational (model, service) before UI
- Unit tests before implementation (if TDD requested)
- Handler wiring last
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1**: All directory creation tasks (T001-T007) can run in parallel
- **Phase 2**: Task dataclass (T010) can start after directories; TaskService (T011) can start after Task; validation (T012) can start in parallel with TaskService
- **Phase 3-8**: Once foundation complete, user stories can run in parallel (different handler files, no shared dependencies)
- **Phase 9**: All polish tasks can run in parallel

---

## Parallel Example: Foundational Phase

```bash
# These can run in parallel after Setup:
Task T010: Create Task dataclass in src/models/task.py
Task T011: Create TaskService class in src/services/task_service.py
Task T012: Create validation functions in src/cli/handlers.py
```

---

## Implementation Strategy

### MVP First (User Story 1 + User Story 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (View Tasks)
4. Complete Phase 4: User Story 2 (Add Task)
5. **STOP and VALIDATE**: Test add + view workflow
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → View works!
3. Add User Story 2 → Test independently → Add works! (MVP!)
4. Add User Story 3 → Test independently → Toggle works!
5. Add User Story 4 → Test independently → Update works!
6. Add User Story 5 → Test independently → Delete works!
7. Add User Story 6 → Test independently → Exit works!
8. Polish phase → Finalize

### Single Developer Strategy

Execute phases sequentially within each phase to avoid file conflicts:

1. Complete Phase 1 (all tasks)
2. Complete Phase 2 (all tasks)
3. Complete Phase 3 (US1 - View Tasks)
4. Complete Phase 4 (US2 - Add Task)
5. Complete Phase 5 (US3 - Toggle Complete)
6. Complete Phase 6 (US4 - Update Task)
7. Complete Phase 7 (US5 - Delete Task)
8. Complete Phase 8 (US6 - Exit Application)
9. Complete Phase 9 (Polish)

---

## Notes

- **[P]** tasks = different files, no dependencies, can run in parallel
- **[Story]** label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (if TDD requested)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| Phase 1 | T001-T007 | Setup - Directory structure |
| Phase 2 | T010-T012 | Foundational - Model, Service, Validation |
| Phase 3 | T020-T025 | US1 - View Task List |
| Phase 4 | T030-T033 | US2 - Add New Task |
| Phase 5 | T040-T042 | US3 - Toggle Complete |
| Phase 6 | T050-T052 | US4 - Update Task |
| Phase 7 | T060-T062 | US5 - Delete Task |
| Phase 8 | T070-T071 | US6 - Exit Application |
| Phase 9 | T080-T084 | Polish - Tests, Linting, Coverage |

**Total Tasks**: 84
