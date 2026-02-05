# Implementation Plan: Finance Sub-Apps Expansion

**Branch**: `001-finance-sub-apps` | **Date**: February 4, 2026 | **Spec**: [specs/001-finance-sub-apps/spec.md](specs/001-finance-sub-apps/spec.md)
**Input**: Feature specification from `/specs/001-finance-sub-apps/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Add four new calculators (Rent vs Buy with defaults, Emergency Fund, Financial Resilience Score, and Time-to-Freedom) to the existing Django calculator app. Each calculator will expose a JSON calculation endpoint, render a form UI with defaults, validate inputs, and display results. Rent vs Buy will include a summary plus a Chart.js comparison graph.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.13
**Primary Dependencies**: Django 5.1, Chart.js (existing frontend charts), Bootstrap 5
**Storage**: SQLite (db.sqlite3) for existing app; calculators remain stateless
**Testing**: pytest with pytest-django
**Linting/Formatting**: Ruff
**Target Platform**: Web (Django server, local or hosted)
**Project Type**: Web
**Performance Goals**: Interactive calculations return results in under 1 second for typical inputs
**Constraints**: No persistence of personal inputs beyond the current session
**Scale/Scope**: Single-app calculator experience with multiple calculator views

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **SOLID Compliance**: Does the design follow Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion principles?
- [x] **Modularity & DRY**: Are Django apps properly bounded? Is there code duplication that should be extracted?
- [x] **Code-First Approach**: Is the plan structured for implementation-first with tests following?
- [x] **Unit Tests Only**: Does the testing strategy focus exclusively on unit tests (no integration/e2e)?
- [x] **YAGNI Check**: Are we building only what's needed, or introducing unnecessary abstractions/features?
- [x] **DevOps Tooling**: Are Ruff, pre-commit, pytest, and commitizen properly configured?
- [x] **Frontend Testing Decision**: Has a frontend testing approach been selected (or explicitly deferred)?

**Violations/Justifications**: None.

## Constitution Check (Post-Design)

- [x] **SOLID Compliance**
- [x] **Modularity & DRY**
- [x] **Code-First Approach**
- [x] **Unit Tests Only**
- [x] **YAGNI Check**
- [x] **DevOps Tooling**
- [x] **Frontend Testing Decision**

**Violations/Justifications**: None.

## Project Structure

### Documentation (this feature)

```text
specs/001-finance-sub-apps/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
calculator/
├── models.py
├── services.py
├── validators.py
├── views.py
├── urls.py
├── templates/
│   └── calculator/
│       ├── base.html
│       └── index.html
└── static/
  ├── css/
  │   └── calculator.css
  └── js/
    └── calculator.js

config/
├── settings.py
├── urls.py
└── wsgi.py

tests/
└── unit/
  └── calculator/
    ├── test_models.py
    ├── test_services.py
    ├── test_validators.py
    └── test_views.py

manage.py
```

**Structure Decision**: Continue with the existing monolithic Django structure using the `calculator` app for all calculator features.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
