---
description: "Task list template for CV Converter feature implementation"
---

# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md

**Tests**: Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

For CV Converter (single Python script project):
- **Main script**: `cv_converter.py` at repository root
- **Tests**: `tests/` directory (if tests added)
- **Fixtures**: `tests/fixtures/` for sample HTML files

<!--
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.

  The /speckit.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - CVConverter class structure

  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment

  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and environment setup

- [ ] T001 Verify Python 3.x is installed and accessible
- [ ] T002 Install dependencies from requirements.txt
- [ ] T003 [P] Verify WeasyPrint system dependencies are installed
- [ ] T004 [P] Create tests/ directory structure if tests requested

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before feature work

**For CV Converter features, this typically includes:**

- [ ] T005 Verify cv_converter.py loads and parses HTML correctly
- [ ] T006 [P] Create sample HTML fixtures for testing (FR and EN)
- [ ] T007 Ensure CVConverter class is properly structured for extension

**Checkpoint**: Foundation ready - feature implementation can now begin

---

## Phase 3: User Story 1 - [Title] (Priority: P1)

**Goal**: [Brief description of what this story delivers for CV Converter]

**Independent Test**: [e.g., "Run `python3 cv_converter.py tests/fixtures/sample_fr.html` and verify outputs"]

### Tests for User Story 1 (OPTIONAL)

> **NOTE: Write tests FIRST if requested, ensure they FAIL before implementation**

- [ ] T008 [P] [US1] Test for [feature] in tests/test_converter.py
- [ ] T009 [P] [US1] Integration test with sample HTML file

### Implementation for User Story 1

- [ ] T010 [US1] Add/modify method in CVConverter class in cv_converter.py
- [ ] T011 [US1] Update TRANSLATIONS dict if new section headers needed
- [ ] T012 [US1] Add error handling for edge cases
- [ ] T013 [US1] Update CLI help text in main() if new arguments added

**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - [Title] (Priority: P2)

**Goal**: [Brief description]

**Independent Test**: [How to verify this story works]

### Tests for User Story 2 (OPTIONAL)

- [ ] T014 [P] [US2] Test for [feature] in tests/test_converter.py

### Implementation for User Story 2

- [ ] T015 [US2] Implement [feature] in cv_converter.py
- [ ] T016 [US2] Integrate with existing CVConverter methods

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase N: Polish & Documentation

**Purpose**: Improvements affecting the overall tool

- [ ] TXXX Update README.md with new usage examples
- [ ] TXXX [P] Add inline comments for complex logic
- [ ] TXXX Verify French and English CVs both convert correctly
- [ ] TXXX Test ATS compatibility of generated DOCX files
- [ ] TXXX Run full conversion on real CV files as final validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - verify environment first
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all user stories being complete

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- CVConverter class modifications before CLI updates
- Core implementation before error handling polish
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup verification tasks marked [P] can run in parallel
- Tests for different features marked [P] can run in parallel
- Documentation updates marked [P] can run in parallel

---

## CV Converter Specific Notes

### Modifying CVConverter Class

When adding new functionality:
1. Add new section extraction method: `_add_[section](self, doc)`
2. Update TRANSLATIONS dict if new section headers needed
3. Call new method from `generate_docx()` in correct order
4. Consider PDF impact (WeasyPrint handles CSS automatically)

### Testing Checklist

- [ ] French CV conversion works
- [ ] English CV conversion works
- [ ] Language detection is accurate
- [ ] PDF preserves visual styling
- [ ] DOCX maintains proper structure
- [ ] Error messages are clear and helpful
- [ ] Custom output filenames work correctly

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate functionality
- Avoid: breaking existing FR/EN support, modifying expected HTML structure
