---
description: "Task list for UK Income Tax Calculator Tab"
---

# Tasks: UK Income Tax Calculator Tab

**Input**: Design documents from /specs/001-uk-income-tax-tab/
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Unit tests are REQUIRED and follow a CODE-FIRST approach:
1. Implementation is created first
2. Unit tests are written after to validate the implementation
3. Tests mirror the source structure in tests/unit/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Minimal shared setup for the new tab

- [x] T001 Review existing calculator UI structure and add tab container skeleton in calculator/templates/calculator/index.html
- [x] T002 [P] Add baseline styles for tabbed calculator layout in static/css/calculator.css

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T003 Update data/uk_tax_thresholds.json with 2025-26 income tax bands, personal allowance taper, NI thresholds/rates, and student loan plan thresholds
- [x] T004 [P] Add tax calculator dataclasses (input/output/band breakdown) in calculator/models.py
- [x] T005 [P] Add shared validation helpers for tax calculator inputs in calculator/validators.py
- [x] T006 Add tax configuration loader and annualization helpers in calculator/services.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Calculate UK take-home pay (Priority: P1) 🎯 MVP

**Goal**: Allow users to enter income and basic tax parameters to get net pay and total deductions.

**Independent Test**: Enter sample inputs and verify net pay and total deductions match expected values with income tax, NI, and student loan totals.

### Implementation for User Story 1

- [x] T007 [P] [US1] Implement income tax calculation (bands + personal allowance taper) in calculator/services.py
- [x] T008 [P] [US1] Implement National Insurance calculation using category A defaults in calculator/services.py
- [x] T009 [P] [US1] Implement student loan calculation using Plan 2 defaults in calculator/services.py
- [x] T010 [US1] Implement net pay aggregation and response mapping in calculator/services.py
- [x] T011 [US1] Add /api/income-tax/calculate endpoint in calculator/views.py
- [x] T012 [US1] Register income tax API route in calculator/urls.py
- [x] T013 [US1] Add UK income tax tab form (gross income, pay frequency, tax year, jurisdiction, pre-tax adjustments) in calculator/templates/calculator/index.html
- [x] T014 [US1] Wire tab submission + results summary rendering in static/js/calculator.js
- [x] T015 [US1] Update calculator/templates/calculator/base.html footer copy to include UK income tax calculator support

### Unit Tests for User Story 1 (CODE-FIRST: Written AFTER implementation)

- [x] T016 [P] [US1] Unit tests for tax calculation helpers in tests/unit/calculator/test_services.py
- [x] T017 [P] [US1] Unit tests for request validation in tests/unit/calculator/test_validators.py
- [x] T018 [P] [US1] Unit tests for API response shape in tests/unit/calculator/test_views.py

**Checkpoint**: User Story 1 fully functional and independently testable

---

## Phase 4: User Story 2 - Adjust NI and student loan settings (Priority: P2)

**Goal**: Allow users to select NI category and student loan plan and see deductions update.

**Independent Test**: Change NI category or loan plan and confirm deductions update while other values remain consistent.

### Implementation for User Story 2

- [x] T019 [P] [US2] Extend NI calculation to support categories A, B, C, H, J, M, Z in calculator/services.py
- [x] T020 [P] [US2] Extend student loan calculation to support plans 1, 2, 4, 5, and postgraduate in calculator/services.py
- [x] T021 [US2] Update validation rules for NI category and student loan plan in calculator/validators.py
- [x] T022 [US2] Add NI category and student loan plan selectors to calculator/templates/calculator/index.html
- [x] T023 [US2] Send NI category and loan plan in requests + update UI labels in static/js/calculator.js

### Unit Tests for User Story 2 (CODE-FIRST: Written AFTER implementation)

- [x] T024 [P] [US2] Unit tests for NI category calculations in tests/unit/calculator/test_services.py
- [x] T025 [P] [US2] Unit tests for student loan plan calculations in tests/unit/calculator/test_services.py
- [x] T026 [P] [US2] Unit tests for validation of NI/loan inputs in tests/unit/calculator/test_validators.py

**Checkpoint**: User Stories 1 and 2 both work independently

---

## Phase 5: User Story 3 - Understand the deduction breakdown (Priority: P3)

**Goal**: Provide itemized deduction breakdown so users can see how totals were derived.

**Independent Test**: For a completed calculation, verify band-level breakdowns sum to totals and match net pay math.

### Implementation for User Story 3

- [x] T027 [P] [US3] Add band-level breakdown outputs for income tax and NI in calculator/services.py
- [x] T028 [US3] Include band breakdowns in API response mapping in calculator/views.py
- [x] T029 [US3] Add breakdown tables/sections to calculator/templates/calculator/index.html
- [x] T030 [US3] Render breakdown tables and effective deduction rate in static/js/calculator.js
- [x] T031 [US3] Add supporting styles for breakdown tables in static/css/calculator.css

### Unit Tests for User Story 3 (CODE-FIRST: Written AFTER implementation)

- [x] T032 [P] [US3] Unit tests for band breakdown math in tests/unit/calculator/test_services.py
- [x] T033 [P] [US3] Unit tests for response breakdown fields in tests/unit/calculator/test_views.py

**Checkpoint**: All user stories fully functional and independently testable

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Quality, docs, and consistency updates

- [x] T034 [P] Update quickstart example if needed in specs/001-uk-income-tax-tab/quickstart.md
- [x] T035 [P] Ensure calculator copy and labels are consistent across tabs in calculator/templates/calculator/index.html
- [x] T036 [P] Run documentation pass for tax-year labeling in calculator/templates/calculator/index.html
- [x] T037 [P] Add unit test coverage for edge cases (band boundaries, allowance taper, zero loan threshold) in tests/unit/calculator/test_services.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - no dependency on other stories
- **User Story 2 (P2)**: Can start after Foundational - extends US1 calculations
- **User Story 3 (P3)**: Can start after Foundational - builds on US1 outputs

### Parallel Opportunities

- Foundational tasks T004 and T005 can run in parallel.
- US1 tasks T007–T009 can run in parallel before aggregation in T010.
- US2 tasks T019 and T020 can run in parallel.
- US3 tasks T027 and T031 can run in parallel.
- Unit test tasks within a story can run in parallel after implementation.

---

## Parallel Example: User Story 1

- Task: T007 Implement income tax calculation in calculator/services.py
- Task: T008 Implement National Insurance calculation in calculator/services.py
- Task: T009 Implement student loan calculation in calculator/services.py

After implementation:

- Task: T016 Unit tests for tax calculation helpers in tests/unit/calculator/test_services.py
- Task: T017 Unit tests for request validation in tests/unit/calculator/test_validators.py
- Task: T018 Unit tests for API response shape in tests/unit/calculator/test_views.py

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Stop and validate User Story 1 independently

### Incremental Delivery

1. Setup + Foundational → foundation ready
2. User Story 1 → test independently → demo MVP
3. User Story 2 → test independently → demo
4. User Story 3 → test independently → demo

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- CODE-FIRST: Implement functionality before writing tests
- Unit tests mirror source structure (tests/unit/calculator/test_*.py)
