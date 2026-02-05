# Tasks: Finance Sub-Apps Expansion

**Input**: Design documents from `/specs/001-finance-sub-apps/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Unit tests are REQUIRED and follow a CODE-FIRST approach:
  1. Implementation is created first
  2. Unit tests are written after to validate the implementation
  3. Tests mirror the source structure in tests/unit/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Shared UI/JS scaffolding for multiple calculators

- [x] T001 Add shared calculator layout regions in templates/calculator/base.html
- [x] T002 [P] Add shared styles for calculator sections in static/css/calculator.css
- [x] T003 [P] Add shared JS utilities for API submit/validation in static/js/calculator.js

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core plumbing required before any calculator implementation

- [x] T004 Add routes for new calculator pages and APIs in calculator/urls.py and config/urls.py
- [x] T005 [P] Add shared numeric/rate validators in calculator/validators.py
- [x] T006 [P] Add shared serialization helpers for Decimal and series in calculator/services.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Rent vs Buy Comparison (Priority: P1) 🎯 MVP

**Goal**: Provide a configurable rent vs buy calculator with defaults, summary, and comparison graph.

**Independent Test**: Submit default inputs and verify summary + graph in the response and UI render.

### Implementation for User Story 1

- [x] T007 [P] [US1] Add RentVsBuy input/result dataclasses in calculator/models.py
- [x] T008 [US1] Implement rent vs buy calculation and series in calculator/services.py
- [x] T009 [US1] Implement rent vs buy validators in calculator/validators.py
- [x] T010 [US1] Add rent vs buy API view in calculator/views.py
- [x] T011 [US1] Add rent vs buy UI and defaults in templates/calculator/index.html
- [x] T012 [US1] Add rent vs buy JS handler and Chart.js rendering in static/js/calculator.js

### Unit Tests for User Story 1 (CODE-FIRST: Written AFTER implementation)

- [x] T013 [P] [US1] Unit tests for RentVsBuy models in tests/unit/calculator/test_models.py
- [x] T014 [P] [US1] Unit tests for rent vs buy services in tests/unit/calculator/test_services.py
- [x] T015 [P] [US1] Unit tests for rent vs buy validators in tests/unit/calculator/test_validators.py
- [x] T016 [P] [US1] Unit tests for rent vs buy view in tests/unit/calculator/test_views.py

**Checkpoint**: User Story 1 functional and independently testable

---

## Phase 4: User Story 2 - Emergency Fund Calculator (Priority: P2)

**Goal**: Provide a simple emergency fund target and savings gap calculator.

**Independent Test**: Submit monthly expenses and target months and verify target + gap.

### Implementation for User Story 2

- [x] T017 [P] [US2] Add EmergencyFund input/result dataclasses in calculator/models.py
- [x] T018 [US2] Implement emergency fund calculation in calculator/services.py
- [x] T019 [US2] Implement emergency fund validators in calculator/validators.py
- [x] T020 [US2] Add emergency fund API view in calculator/views.py
- [x] T021 [US2] Add emergency fund UI and defaults in templates/calculator/index.html
- [x] T022 [US2] Add emergency fund JS handler in static/js/calculator.js

### Unit Tests for User Story 2 (CODE-FIRST: Written AFTER implementation)

- [x] T023 [P] [US2] Unit tests for emergency fund models in tests/unit/calculator/test_models.py
- [x] T024 [P] [US2] Unit tests for emergency fund services in tests/unit/calculator/test_services.py
- [x] T025 [P] [US2] Unit tests for emergency fund validators in tests/unit/calculator/test_validators.py
- [x] T026 [P] [US2] Unit tests for emergency fund view in tests/unit/calculator/test_views.py

**Checkpoint**: User Story 2 functional and independently testable

---

## Phase 5: User Story 3 - Financial Resilience Score (Priority: P3)

**Goal**: Provide a resilience index and weak-point analysis.

**Independent Test**: Submit inputs and verify index plus weak points list.

### Implementation for User Story 3

- [x] T027 [P] [US3] Add ResilienceScore input/result dataclasses in calculator/models.py
- [x] T028 [US3] Implement resilience score calculation in calculator/services.py
- [x] T029 [US3] Implement resilience score validators in calculator/validators.py
- [x] T030 [US3] Add resilience score API view in calculator/views.py
- [x] T031 [US3] Add resilience score UI in templates/calculator/index.html
- [x] T032 [US3] Add resilience score JS handler in static/js/calculator.js

### Unit Tests for User Story 3 (CODE-FIRST: Written AFTER implementation)

- [x] T033 [P] [US3] Unit tests for resilience score models in tests/unit/calculator/test_models.py
- [x] T034 [P] [US3] Unit tests for resilience score services in tests/unit/calculator/test_services.py
- [x] T035 [P] [US3] Unit tests for resilience score validators in tests/unit/calculator/test_validators.py
- [x] T036 [P] [US3] Unit tests for resilience score view in tests/unit/calculator/test_views.py

**Checkpoint**: User Story 3 functional and independently testable

---

## Phase 6: User Story 4 - Time-to-Freedom Calculator (Priority: P3)

**Goal**: Provide freedom number and timeline without hype framing.

**Independent Test**: Submit inputs and verify freedom number and timeline output.

### Implementation for User Story 4

- [x] T037 [P] [US4] Add TimeToFreedom input/result dataclasses in calculator/models.py
- [x] T038 [US4] Implement time-to-freedom calculation and timeline in calculator/services.py
- [x] T039 [US4] Implement time-to-freedom validators in calculator/validators.py
- [x] T040 [US4] Add time-to-freedom API view in calculator/views.py
- [x] T041 [US4] Add time-to-freedom UI copy and inputs in templates/calculator/index.html
- [x] T042 [US4] Add time-to-freedom JS handler and timeline graph in static/js/calculator.js

### Unit Tests for User Story 4 (CODE-FIRST: Written AFTER implementation)

- [x] T043 [P] [US4] Unit tests for time-to-freedom models in tests/unit/calculator/test_models.py
- [x] T044 [P] [US4] Unit tests for time-to-freedom services in tests/unit/calculator/test_services.py
- [x] T045 [P] [US4] Unit tests for time-to-freedom validators in tests/unit/calculator/test_validators.py
- [x] T046 [P] [US4] Unit tests for time-to-freedom view in tests/unit/calculator/test_views.py

**Checkpoint**: User Story 4 functional and independently testable

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Documentation and UI consistency across calculators

- [x] T047 [P] Update README.md with new calculator descriptions
- [x] T048 [P] Ensure consistent labels/help text across calculators in templates/calculator/index.html
- [x] T049 [P] Refine responsive layout for new sections in static/css/calculator.css
- [x] T050 [P] Verify quickstart steps in specs/001-finance-sub-apps/quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: Depend on Foundational completion
- **Polish (Phase 7)**: Depends on completing desired user stories

### User Story Dependencies

- **US1 (P1)**: Depends on Phase 2 only
- **US2 (P2)**: Depends on Phase 2 only
- **US3 (P3)**: Depends on Phase 2 only
- **US4 (P3)**: Depends on Phase 2 only

### Within Each User Story

- Models before services
- Services before views
- Views before UI/JS wiring
- Unit tests written after implementation tasks complete

---

## Parallel Execution Examples

### User Story 1

- T007 and T009 can run in parallel (models vs validators)
- T011 and T012 can run in parallel (template vs JS)
- T013–T016 can run in parallel after implementation is complete

### User Story 2

- T017 and T019 can run in parallel (models vs validators)
- T021 and T022 can run in parallel (template vs JS)
- T023–T026 can run in parallel after implementation is complete

### User Story 3

- T027 and T029 can run in parallel (models vs validators)
- T031 and T032 can run in parallel (template vs JS)
- T033–T036 can run in parallel after implementation is complete

### User Story 4

- T037 and T039 can run in parallel (models vs validators)
- T041 and T042 can run in parallel (template vs JS)
- T043–T046 can run in parallel after implementation is complete

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Validate User Story 1 independently (summary + graph)

### Incremental Delivery

1. Deliver US1, then US2
2. Add US3 and US4 after US2
3. Apply polish tasks once all desired stories are complete

---

## Notes

- [P] tasks are parallelizable and target different files
- All tasks include explicit file paths
- Tests follow implementation and mirror source structure
- Avoid cross-story dependencies to preserve independent delivery
