# Implementation Plan: UK Income Tax Calculator Tab

**Branch**: `001-uk-income-tax-tab` | **Date**: 2026-02-04 | **Spec**: [specs/001-uk-income-tax-tab/spec.md](specs/001-uk-income-tax-tab/spec.md)
**Input**: Feature specification from `/specs/001-uk-income-tax-tab/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Add a new UK income tax calculator tab to the existing Django calculator UI. The tab will accept gross income and key UK tax parameters (jurisdiction, NI category, student loan plan, pre-tax deductions) and return a clear breakdown of income tax, National Insurance, and student loan deductions plus net pay. Calculations will use tax-year configuration stored in a JSON data file and be exposed via a dedicated JSON API endpoint.

## Technical Context

**Language/Version**: Python 3.13
**Primary Dependencies**: Django 5.1, pytest, pytest-django, ruff, pre-commit
**Storage**: SQLite (db.sqlite3) for app; calculator results are computed in-memory
**Testing**: pytest with pytest-django
**Linting/Formatting**: Ruff (format + lint)
**Target Platform**: Web app (Django) deployed on standard Linux server/runtime
**Project Type**: Web
**Performance Goals**: 95% of calculations return within 2 seconds
**Constraints**: No external APIs; calculations are deterministic and use local JSON config
**Scale/Scope**: Single-page calculator with per-request computation; low concurrency expected

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **SOLID Compliance**: Calculation logic stays in services; inputs/outputs in dataclasses.
- [x] **Modularity & DRY**: Extend existing `calculator` app; reuse shared validation utilities.
- [x] **Code-First Approach**: Plan sequences implementation before unit tests.
- [x] **Unit Tests Only**: Only unit tests are planned.
- [x] **YAGNI Check**: No extra abstractions beyond needed calculation and UI.
- [x] **DevOps Tooling**: Ruff, pre-commit, pytest, and commitizen already configured.
- [x] **Frontend Testing Decision**: Option 4 (minimal/no frontend testing) selected for this simple UI.

**Violations/Justifications**: None.

**Post-Phase 1 Re-check**: All gates remain satisfied after design artifacts were produced.

## Project Structure

### Documentation (this feature)

```text
specs/001-uk-income-tax-tab/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
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
static/
├── css/
│   └── calculator.css
└── js/
  └── calculator.js
data/
└── uk_tax_thresholds.json
config/
├── settings.py
└── urls.py
tests/
└── unit/
  └── calculator/
    ├── test_models.py
    ├── test_services.py
    └── test_validators.py
manage.py
```

**Structure Decision**: Monolithic Django app with a single `calculator` domain, matching current repository layout.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
