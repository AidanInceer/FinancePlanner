---

description: "Task list for Student Loan Payoff Calculator implementation"
---

# Tasks: Student Loan Payoff Calculator

**Input**: Design documents from `/specs/001-loan-payoff-calc/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/calculator-api.json

**Tests**: Unit tests are REQUIRED and follow a CODE-FIRST approach:
  1. Implementation is created first
  2. Unit tests are written after to validate the implementation
  3. Tests mirror the source structure in tests/unit/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Project uses single Django project structure with calculator app at repository root.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create Django project structure per implementation plan in financeplanner/
- [X] T002 Initialize Django project with config/ directory and settings.py
- [X] T003 [P] Create calculator Django app in financeplanner/calculator/
- [X] T004 [P] Configure Ruff in pyproject.toml for linting and formatting
- [X] T005 [P] Create requirements.txt with Django 5.1, pytest-django dependencies
- [X] T006 [P] Setup .pre-commit-config.yaml with Ruff hooks
- [X] T007 [P] Create .env.example for environment variables template
- [X] T008 [P] Update .gitignore with Python, Django, and IDE patterns
- [X] T009 Create data/ directory for uk_tax_thresholds.json configuration
- [X] T010 [P] Create static/ directories for css/ and js/
- [X] T011 [P] Create tests/unit/calculator/ directory structure
- [X] T012 Configure URL routing in config/urls.py and calculator/urls.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T013 Create UK tax thresholds JSON data in data/uk_tax_thresholds.json
- [X] T014 [P] Initialize Django database with migrations (manage.py migrate)
- [X] T015 [P] Create base template structure in calculator/templates/calculator/base.html
- [X] T016 [P] Setup Bootstrap 5.3 CDN links in base template
- [X] T017 [P] Setup Chart.js 4.4.1 CDN links in base template
- [X] T018 Create health check endpoint in calculator/views.py
- [X] T019 [P] Configure Django CORS and security settings in config/settings.py
- [X] T020 [P] Setup pytest configuration in pyproject.toml with Django plugin
- [X] T021 Create base calculator page route in calculator/urls.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Input Financial Data (Priority: P1) 🎯 MVP

**Goal**: User visits calculator page and enters personal financial information (age, graduation, loan, income, investment data). System captures, validates, and stores data in session/calculation state.

**Independent Test**: Submit complete form with valid data and verify all fields are captured, validated, and ready for calculation.

### Implementation for User Story 1

- [X] T022 [P] [US1] Create CalculatorInput data class in calculator/models.py per data-model.md
- [X] T023 [P] [US1] Create input validation logic in calculator/validators.py (age, rates, ranges)
- [X] T024 [US1] Implement calculator form view in calculator/views.py (GET endpoint for /)
- [X] T025 [US1] Create Bootstrap form HTML in calculator/templates/calculator/index.html
- [X] T026 [US1] Add client-side form validation JavaScript in static/js/calculator.js
- [X] T027 [US1] Add form styling CSS in static/css/calculator.css
- [X] T028 [US1] Implement form field validation feedback (inline errors, checkmarks)
- [X] T029 [US1] Add computed field display (loan end date calculation) in frontend

### Unit Tests for User Story 1 (CODE-FIRST: Written AFTER implementation)

- [X] T030 [P] [US1] Unit tests for CalculatorInput data class in tests/unit/calculator/test_models.py
- [X] T031 [P] [US1] Unit tests for validators in tests/unit/calculator/test_validators.py (all validation rules)
- [X] T032 [P] [US1] Unit tests for calculator form view in tests/unit/calculator/test_views.py

**Checkpoint**: At this point, User Story 1 should be fully functional - users can enter all data and see validation feedback

---

## Phase 4: User Story 2 - Calculate Optimal Payoff Strategy (Priority: P2)

**Goal**: System calculates whether paying off loan early is beneficial compared to investing. Compares loan cost vs investment returns over 35 years, applies UK tax rules, and provides clear recommendation.

**Independent Test**: Provide complete dataset via API, verify calculation produces three scenarios with recommendation and supporting projections.

### Implementation for User Story 2

- [X] T033 [P] [US2] Create ScenarioProjection data class in calculator/models.py per data-model.md
- [X] T034 [P] [US2] Create YearlyProjection data class in calculator/models.py per data-model.md
- [X] T035 [P] [US2] Create PayoffRecommendation data class in calculator/models.py per data-model.md
- [X] T036 [US2] Implement loan calculation service in calculator/services.py (calculate_loan_balance)
- [X] T037 [US2] Implement investment calculation service in calculator/services.py (calculate_investment_value)
- [X] T038 [US2] Implement UK tax repayment calculation in calculator/services.py (apply_uk_tax_rules)
- [X] T039 [US2] Implement scenario projection service in calculator/services.py (project_scenario)
- [X] T040 [US2] Implement recommendation engine in calculator/services.py (generate_recommendation)
- [X] T041 [US2] Create POST /api/calculate endpoint in calculator/views.py per contracts/calculator-api.json
- [X] T042 [US2] Implement request validation and error handling in POST endpoint
- [X] T043 [US2] Add calculation result serialization (dataclass to JSON)
- [X] T044 [US2] Calculate crossover date logic (when investment > loan cost)
- [X] T045 [US2] Calculate net benefit and confidence levels
- [X] T046 [US2] Generate plain-language rationale text for recommendation

### Unit Tests for User Story 2 (CODE-FIRST: Written AFTER implementation)

- [X] T047 [P] [US2] Unit tests for ScenarioProjection data class in tests/unit/calculator/test_models.py
- [X] T048 [P] [US2] Unit tests for YearlyProjection data class in tests/unit/calculator/test_models.py
- [X] T049 [P] [US2] Unit tests for loan calculations in tests/unit/calculator/test_services.py
- [X] T050 [P] [US2] Unit tests for investment calculations in tests/unit/calculator/test_services.py
- [X] T051 [P] [US2] Unit tests for UK tax repayment in tests/unit/calculator/test_services.py
- [X] T052 [P] [US2] Unit tests for scenario projection in tests/unit/calculator/test_services.py
- [X] T053 [P] [US2] Unit tests for recommendation engine in tests/unit/calculator/test_services.py
- [X] T054 [P] [US2] Unit tests for /api/calculate endpoint in tests/unit/calculator/test_views.py

**Checkpoint**: At this point, User Story 2 should be fully functional - API returns three scenarios with recommendation

---

## Phase 5: User Story 3 - Visualize Payoff Scenarios with Uncertainty (Priority: P3)

**Goal**: System displays interactive line graph showing loan balance over time with three scenarios (optimistic, pessimistic, realistic) including shaded uncertainty bands. Graph annotates decision points and crossover dates.

**Independent Test**: Provide calculation results and verify graph renders with correct data points, three lines, shaded uncertainty regions, and decision markers.

### Implementation for User Story 3

- [X] T055 [P] [US3] Implement Chart.js graph rendering in static/js/calculator.js (renderPayoffGraph function)
- [X] T056 [P] [US3] Configure Chart.js dataset structure for three scenario lines
- [X] T057 [US3] Implement uncertainty band shading (fill between optimistic and pessimistic)
- [X] T058 [US3] Add investment value overlay line on graph
- [X] T059 [US3] Implement crossover date annotation markers
- [X] T060 [US3] Configure interactive tooltips with financial details
- [X] T061 [US3] Implement responsive chart scaling for mobile devices
- [X] T062 [US3] Add graph loading state and error handling
- [X] T063 [US3] Style graph container and legend in static/css/calculator.css
- [X] T064 [US3] Connect form submission to API call and graph update
- [X] T065 [US3] Display recommendation text below graph with savings amount
- [X] T066 [US3] Implement dynamic graph updates when user changes inputs

### Unit Tests for User Story 3 (CODE-FIRST: Written AFTER implementation)

Note: Frontend JavaScript testing is minimal per constitution (Option 4: Minimal frontend testing for simple UIs). Manual testing sufficient for MVP.

- [X] T067 [US3] Manual testing checklist: Verify graph renders on mobile (320px width)
- [X] T068 [US3] Manual testing checklist: Verify graph shows three scenario lines
- [X] T069 [US3] Manual testing checklist: Verify uncertainty bands are visible
- [X] T070 [US3] Manual testing checklist: Verify tooltips work on hover/touch
- [X] T071 [US3] Manual testing checklist: Verify decision markers are annotated
- [X] T072 [US3] Manual testing checklist: Verify graph updates when inputs change

**Checkpoint**: All user stories should now be independently functional - complete calculator with visualization

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and ensure production readiness

- [X] T073 [P] Update README.md with project overview, setup instructions, and usage
- [X] T074 [P] Add inline code documentation and docstrings per Python conventions
- [X] T075 [P] Verify Ruff configuration and run formatting on all Python files
- [X] T076 [P] Verify pre-commit hooks are installed and functional
- [X] T077 [P] Add edge case validation (age > loan end date, negative values, inverted rates)
- [X] T078 [P] Add error logging for calculation failures
- [X] T079 [P] Optimize calculation performance (target <2 seconds for 35-year projection)
- [X] T080 [P] Verify responsive design works on 320px minimum width
- [X] T081 [P] Add loading indicators during calculation
- [X] T082 [P] Verify accessibility (ARIA labels, keyboard navigation)
- [X] T083 Run quickstart.md validation (10-minute setup test)
- [X] T084 Review and validate all acceptance scenarios from spec.md
- [X] T085 Create commitizen configuration for conventional commits
- [X] T086 Security review: CSRF protection, input sanitization, rate limiting

**Phase 6 Complete**: All polish and production readiness tasks finished.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on CalculatorInput from US1 but is independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on calculation results from US2 but is independently testable

### Within Each User Story

- Implementation tasks come FIRST (models, services, views)
- Unit tests are written AFTER implementation is complete
- Models before services
- Services before views
- Core implementation before integration
- Story implementation complete before writing tests
- All tests for a story complete before moving to next priority

### Parallel Opportunities

**Phase 1 (Setup):**
- T004, T005, T006, T007, T008, T010, T011 can all run in parallel

**Phase 2 (Foundational):**
- T014, T015, T016, T017, T019, T020 can run in parallel after T013

**Phase 3 (User Story 1 - Implementation):**
- T022, T023 can run in parallel (models and validators)
- T025, T026, T027 can run in parallel (HTML, JS, CSS)

**Phase 3 (User Story 1 - Tests):**
- T030, T031, T032 can all run in parallel after implementation complete

**Phase 4 (User Story 2 - Implementation):**
- T033, T034, T035 can run in parallel (all data classes)
- T036, T037, T038 can run in parallel (separate calculation functions)

**Phase 4 (User Story 2 - Tests):**
- T047, T048, T049, T050, T051, T052, T053, T054 can all run in parallel after implementation complete

**Phase 5 (User Story 3 - Implementation):**
- T055, T056 can run in parallel (graph setup)
- T059, T060, T061 can run in parallel (annotations and interactions)

**Phase 6 (Polish):**
- T073, T074, T075, T076, T077, T078, T079, T080, T081, T082 can all run in parallel

---

## Parallel Example: User Story 1

```bash
# Implementation phase - Launch models and validators together:
Task T022: "Create CalculatorInput data class in calculator/models.py"
Task T023: "Create input validation logic in calculator/validators.py"

# After form view is ready - Launch frontend together:
Task T025: "Create Bootstrap form HTML in calculator/templates/calculator/index.html"
Task T026: "Add client-side validation JavaScript in static/js/calculator.js"
Task T027: "Add form styling CSS in static/css/calculator.css"

# After implementation complete - Launch all unit tests together:
Task T030: "Unit tests for CalculatorInput data class"
Task T031: "Unit tests for validators"
Task T032: "Unit tests for calculator form view"
```

---

## Parallel Example: User Story 2

```bash
# Data classes - Launch together:
Task T033: "Create ScenarioProjection data class"
Task T034: "Create YearlyProjection data class"
Task T035: "Create PayoffRecommendation data class"

# Calculation services - Launch together:
Task T036: "Implement loan calculation service"
Task T037: "Implement investment calculation service"
Task T038: "Implement UK tax repayment calculation"

# After implementation complete - Launch all unit tests together:
Task T047-T054: All test files can run in parallel
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. You now have a working form for data entry (MVP baseline)

### Incremental Delivery (Recommended)

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Working form (MVP!)
3. Add User Story 2 → Test independently → Working calculator with recommendation
4. Add User Story 3 → Test independently → Complete calculator with visualization
5. Add Polish → Production ready

Each story adds value without breaking previous stories. Can deploy after any story.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (12 tasks)
2. Once Foundational is done:
   - Developer A: User Story 1 (11 implementation tasks + 3 test tasks)
   - Developer B: User Story 2 (14 implementation tasks + 8 test tasks)
   - Developer C: User Story 3 (12 implementation tasks + 6 test tasks)
3. Stories complete and integrate independently
4. Team collaborates on Polish phase

**Note**: While stories CAN be done in parallel, they build on each other logically (US2 uses US1 input structure, US3 visualizes US2 calculations). Consider sequential delivery for simpler integration.

---

## Summary

- **Total Tasks**: 86 tasks
- **Setup Phase**: 12 tasks
- **Foundational Phase**: 9 tasks (BLOCKS all user stories)
- **User Story 1 (P1)**: 11 implementation + 3 test tasks = 14 tasks
- **User Story 2 (P2)**: 14 implementation + 8 test tasks = 22 tasks
- **User Story 3 (P3)**: 12 implementation + 6 test tasks = 18 tasks
- **Polish Phase**: 14 tasks
- **Parallel Opportunities**: 45+ tasks can run in parallel with proper task assignment

**MVP Scope**: Complete Setup + Foundational + User Story 1 = 35 tasks for working data entry form

**Full Feature**: All phases = 86 tasks for complete calculator with visualization and recommendation engine
