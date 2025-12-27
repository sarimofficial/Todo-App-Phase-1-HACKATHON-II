# Feature Specification: Phase I - Console Todo Application

**Feature Branch**: `001-phase1-console-todo`
**Created**: 2025-12-28
**Status**: Draft
**Input**: User description: "Phase I: In-memory Python console todo application with basic CRUD operations"

## Overview

Phase I delivers a minimal, in-memory Python console application for managing personal tasks. The application runs in a terminal, presents a menu-driven interface, and stores all data in memory (no persistence beyond runtime). This phase establishes the foundational task management concepts that will be extended in future phases.

## Scope

### In Scope

- Menu-based console interface
- In-memory task storage (list/dictionary)
- Single-user operation (no authentication)
- Basic CRUD operations: Add, View, Update, Delete
- Task completion status toggle

### Out of Scope

- Database persistence
- File-based storage
- Multi-user support
- Authentication/authorization
- Web or API interfaces
- Task priorities, due dates, categories, or tags
- Search or filtering capabilities
- Any features from Phase II-V

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View Task List (Priority: P1)

As a user, I want to see all my tasks so that I can understand what I need to do.

**Why this priority**: Viewing tasks is the most fundamental operation. Without this, users cannot verify any other operation worked correctly. This forms the foundation for testing all other features.

**Independent Test**: Can be fully tested by launching the application and selecting "View Tasks" from the menu. Delivers immediate value by showing the current state of all tasks.

**Acceptance Scenarios**:

1. **Given** the application is running and no tasks exist, **When** I select "View Tasks", **Then** I see a message indicating "No tasks found"
2. **Given** the application is running and tasks exist, **When** I select "View Tasks", **Then** I see a numbered list showing each task's ID, title, and completion status
3. **Given** tasks exist with mixed completion states, **When** I view the list, **Then** completed tasks are clearly marked (e.g., "[X]") and incomplete tasks are unmarked (e.g., "[ ]")

---

### User Story 2 - Add New Task (Priority: P1)

As a user, I want to add a new task so that I can track something I need to do.

**Why this priority**: Adding tasks is essential - without it, the application has no data to work with. This is a prerequisite for meaningful testing of view, update, and delete operations.

**Independent Test**: Can be fully tested by selecting "Add Task", entering a title, and then viewing the task list to confirm the task appears.

**Acceptance Scenarios**:

1. **Given** the application is running, **When** I select "Add Task" and enter a valid title, **Then** the task is created with a unique ID and marked as incomplete
2. **Given** the application is running, **When** I select "Add Task" and enter an empty title, **Then** I see an error message "Task title cannot be empty" and am prompted to try again
3. **Given** I successfully add a task, **When** I view the task list, **Then** the new task appears in the list with the title I entered

---

### User Story 3 - Mark Task Complete/Incomplete (Priority: P2)

As a user, I want to mark a task as complete or incomplete so that I can track my progress.

**Why this priority**: Toggling completion status is the primary way users interact with their task list on an ongoing basis. It's more frequently used than editing or deleting.

**Independent Test**: Can be fully tested by adding a task, marking it complete, viewing the list to confirm the status change, then marking it incomplete again.

**Acceptance Scenarios**:

1. **Given** an incomplete task exists, **When** I select "Toggle Complete" and enter its ID, **Then** the task is marked as complete
2. **Given** a complete task exists, **When** I select "Toggle Complete" and enter its ID, **Then** the task is marked as incomplete
3. **Given** I enter an ID that does not exist, **When** I try to toggle completion, **Then** I see an error message "Task not found" with the invalid ID

---

### User Story 4 - Update Task Title (Priority: P3)

As a user, I want to update a task's title so that I can correct mistakes or clarify what needs to be done.

**Why this priority**: Updating is less frequent than adding or completing tasks, but important for maintaining accurate task descriptions.

**Independent Test**: Can be fully tested by adding a task, updating its title, and viewing the list to confirm the change.

**Acceptance Scenarios**:

1. **Given** a task exists, **When** I select "Update Task", enter its ID, and provide a new title, **Then** the task's title is updated
2. **Given** I enter an ID that does not exist, **When** I try to update, **Then** I see an error message "Task not found" with the invalid ID
3. **Given** I provide an empty new title, **When** I try to update, **Then** I see an error message "Task title cannot be empty" and the original title is preserved

---

### User Story 5 - Delete Task (Priority: P3)

As a user, I want to delete a task so that I can remove items I no longer need to track.

**Why this priority**: Deletion is a less frequent operation and is destructive, so it's lower priority than the core add/view/complete workflow.

**Independent Test**: Can be fully tested by adding a task, deleting it by ID, and viewing the list to confirm it no longer appears.

**Acceptance Scenarios**:

1. **Given** a task exists, **When** I select "Delete Task" and enter its ID, **Then** the task is removed from the list
2. **Given** I enter an ID that does not exist, **When** I try to delete, **Then** I see an error message "Task not found" with the invalid ID
3. **Given** I delete a task, **When** I view the task list, **Then** the deleted task no longer appears

---

### User Story 6 - Exit Application (Priority: P3)

As a user, I want to exit the application gracefully so that I can end my session.

**Why this priority**: Basic application lifecycle management. Low priority but necessary for a complete user experience.

**Independent Test**: Can be fully tested by selecting "Exit" from the menu and confirming the application terminates.

**Acceptance Scenarios**:

1. **Given** the application is running, **When** I select "Exit", **Then** the application displays a goodbye message and terminates
2. **Given** tasks exist in memory, **When** I exit and restart the application, **Then** all previous tasks are gone (no persistence)

---

### Edge Cases

- **Empty task list operations**: Attempting to update, delete, or toggle tasks when no tasks exist displays "No tasks found"
- **Invalid ID format**: Entering non-numeric input when an ID is expected displays "Invalid ID format - please enter a number"
- **Very long task titles**: Titles exceeding 200 characters are truncated to 200 characters with a warning message
- **Special characters in titles**: All printable characters are accepted in task titles
- **Whitespace-only titles**: Titles containing only whitespace are treated as empty and rejected

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display a numbered menu with options: Add Task, View Tasks, Update Task, Delete Task, Toggle Complete, Exit
- **FR-002**: System MUST assign a unique sequential integer ID to each new task starting from 1
- **FR-003**: System MUST store tasks in memory only; no data persists after application exit
- **FR-004**: System MUST validate that task titles are non-empty and contain at least one non-whitespace character
- **FR-005**: System MUST display clear error messages for invalid operations (invalid ID, empty title, task not found)
- **FR-006**: System MUST return to the main menu after completing any operation (except Exit)
- **FR-007**: System MUST handle invalid menu selections by displaying "Invalid option" and re-displaying the menu
- **FR-008**: System MUST display task completion status visually using "[ ]" for incomplete and "[X]" for complete
- **FR-009**: System MUST truncate task titles longer than 200 characters and display a warning
- **FR-010**: System MUST accept numeric input for task IDs and reject non-numeric input with a clear error message

### Key Entities

- **Task**: Represents a single todo item
  - **ID**: Unique integer identifier (auto-assigned, sequential starting from 1)
  - **Title**: String describing the task (1-200 characters, non-empty)
  - **Completed**: Boolean flag indicating completion status (default: False)

## CLI Interaction Flow

```
=== Todo Application ===

1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Complete
6. Exit

Select option: _
```

### Menu Option Flows

**Add Task**:
```
Enter task title: _
[Success: "Task added with ID: X"]
[Error: "Task title cannot be empty"]
```

**View Tasks**:
```
=== Your Tasks ===
1. [ ] Buy groceries
2. [X] Call mom
3. [ ] Finish report

[Or: "No tasks found"]
```

**Update Task**:
```
Enter task ID to update: _
[Error if not found: "Task not found: ID X"]
Enter new title: _
[Success: "Task X updated"]
[Error: "Task title cannot be empty"]
```

**Delete Task**:
```
Enter task ID to delete: _
[Success: "Task X deleted"]
[Error: "Task not found: ID X"]
```

**Toggle Complete**:
```
Enter task ID to toggle: _
[Success: "Task X marked as complete" or "Task X marked as incomplete"]
[Error: "Task not found: ID X"]
```

**Exit**:
```
Goodbye!
[Application terminates]
```

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a new task in under 10 seconds (2 interactions: select menu option, enter title)
- **SC-002**: Users can view all tasks in a single screen without scrolling for lists of up to 20 tasks
- **SC-003**: Users can complete any CRUD operation in 3 or fewer interactions from the main menu
- **SC-004**: 100% of error conditions display user-friendly messages (no stack traces or technical errors shown to user)
- **SC-005**: Application responds to all user inputs within 1 second
- **SC-006**: Users can successfully complete a full workflow (add task, mark complete, delete task) on first attempt without documentation

## Assumptions

- Single user operates the application at a time
- Terminal supports standard input/output
- User understands basic menu navigation (entering numbers)
- Task IDs are displayed consistently wherever tasks are shown
- Application runs until explicitly exited by user

## Constraints

- No external dependencies beyond Python standard library
- No file I/O operations
- No network operations
- No database connections
- No graphical user interface
- No concurrent access handling required
