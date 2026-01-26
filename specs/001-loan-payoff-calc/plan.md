# Implementation Plan: Student Loan Payoff Calculator

**Branch**: `001-loan-payoff-calc` | **Date**: 2026-01-26 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-loan-payoff-calc/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Single-page student loan payoff calculator that helps users determine optimal repayment strategy. Compares early loan payoff against investment growth over the loan lifetime, accounting for UK Plan 2 student loan rules and tax thresholds. Delivers clear recommendation with interactive graph showing three scenarios (optimistic, pessimistic, realistic) and uncertainty bands. Built with Django backend for calculations and Bootstrap 5 frontend for responsive UI.

## Technical Context

**Language/Version**: Python 3.13  
**Primary Dependencies**: Django 5.1, Bootstrap 5.3, Chart.js 4.4.1  
**Storage**: SQLite (development and production)  
**Testing**: pytest with Django plugin (pytest-django)  
**Linting/Formatting**: Ruff  
**Target Platform**: Web browser (desktop and mobile), Django development server (local), Railway (production deployment)  
**Project Type**: web (single-page Django application with Bootstrap frontend)  
**Performance Goals**: Calculate 3 scenarios with 35-year projections in <2 seconds, render graph in <1 second  
**Constraints**: Stateless (no user auth/persistence), responsive design (320px minimum width), <3 minute user journey from entry to recommendation  
**Scale/Scope**: Single calculator page, ~4-5 input groups (time, personal finance, loan, hidden UK tax config), 3 calculation scenarios, 1 interactive graph  
**Frontend Framework**: Bootstrap 5.3 for responsive layout and forms  
**Charting**: Chart.js 4.4.1 (lightweight, native uncertainty bands, Bootstrap compatible)  
**UK Tax Data**: JSON configuration file at `data/uk_tax_thresholds.json` (version controlled, simple updates)

**Research Decisions** (see [research.md](research.md) for details):
- Chart.js selected over Plotly/D3.js for simplicity and performance (60KB vs 1-3MB)
- SQLite for production (read-only config data, stateless app, no scaling concerns)
- Railway for MVP deployment with migration path to DigitalOcean
- JSON file for UK tax thresholds (YAGNI compliant, version controlled)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **SOLID Compliance**: Does the design follow Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion principles?
  - **PASS**: Calculator service handles business logic (SRP), UK tax configuration is injected (DIP), validation logic is separate from calculation logic (SRP), service layer abstracts calculations from views (separation of concerns)

- [x] **Modularity & DRY**: Are Django apps properly bounded? Is there code duplication that should be extracted?
  - **PASS**: Single Django app `calculator` for this feature (appropriate for single-page calculator), common financial utilities will be extracted to `core` app if needed, no anticipated duplication since it's one cohesive feature

- [x] **Code-First Approach**: Is the plan structured for implementation-first with tests following?
  - **PASS**: Implementation tasks come before test tasks in all phases, tests validate working code rather than constraining design

- [x] **Unit Tests Only**: Does the testing strategy focus exclusively on unit tests (no integration/e2e)?
  - **PASS**: All testing via pytest unit tests with mocking, no integration or E2E tests planned, frontend JavaScript tested manually (constitution allows minimal frontend testing for simple UIs)

- [x] **YAGNI Check**: Are we building only what's needed, or introducing unnecessary abstractions/features?
  - **PASS**: Single-page calculator with no auth, no persistence, no user accounts - minimal viable feature. UK tax data as JSON config (not over-engineered database schema). Simple service pattern, no repository abstraction layer.

- [x] **DevOps Tooling**: Are Ruff, pre-commit, pytest, and commitizen properly configured?
  - **PASS**: Ruff for linting/formatting (configured in pyproject.toml), pre-commit hooks planned, pytest with Django plugin, commitizen for conventional commits (all per constitution requirements)

- [x] **Frontend Testing Decision**: Has a frontend testing approach been selected (or explicitly deferred)?
  - **PASS**: Option 4 selected - Minimal frontend testing. Rationale: Single-page calculator with straightforward Bootstrap forms and JavaScript graph rendering. Manual testing sufficient for MVP. Django backend unit tests cover business logic. Can add Jest tests later if frontend complexity grows.

**Violations/Justifications**: None - all gates pass

## Project Structure

### Documentation (this feature)

```text
specs/001-loan-payoff-calc/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   └── calculator-api.json
└── checklists/
    └── requirements.md  # Already created
```

### Source Code (repository root)

```text
# Single Django project with calculator app (chosen structure)

financeplanner/                 # Django project root
├── calculator/                 # Calculator Django app
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py              # Tax configuration model (if needed)
│   ├── views.py               # Single-page view + API endpoint
│   ├── services.py            # Calculation logic (loan, investment, scenarios)
│   ├── validators.py          # Input validation logic
│   ├── urls.py                # URL routing
│   └── templates/
│       └── calculator/
│           └── index.html     # Single-page calculator with Bootstrap
├── core/                       # Shared utilities (if needed later)
│   ├── __init__.py
│   └── utils.py
├── config/                     # Django settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── static/                     # Static files
│   ├── css/
│   │   └── calculator.css     # Custom styles
│   └── js/
│       └── calculator.js      # Form handling, graph rendering
├── data/                       # Configuration data
│   └── uk_tax_thresholds.json # UK Plan 2 thresholds by year
├── tests/                      # Test suite
│   └── unit/
│       ├── calculator/
│       │   ├── test_services.py
│       │   ├── test_validators.py
│       │   └── test_views.py
│       └── core/
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Ruff config, project metadata
├── .pre-commit-config.yaml    # Pre-commit hooks config
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore patterns
└── README.md                  # Project documentation
```

**Structure Decision**: Single Django project structure chosen (Option 1 adapted). Rationale: This is a simple single-page calculator - no need for multi-app complexity or frontend/backend separation. The `calculator` app is self-contained, `core` app reserved for future shared utilities if needed. Follows Django conventions while keeping it minimal per YAGNI principle.

## Complexity Tracking

No violations - all constitution gates pass. No complexity justification needed.


---

## Planning Summary

**Status**:  Planning Complete (Phase 0 & Phase 1)

### Artifacts Generated

1. **[plan.md](plan.md)** - This implementation plan with technical context, constitution check, and project structure
2. **[research.md](research.md)** - Technology decisions (Chart.js, SQLite, Railway, JSON config)
3. **[data-model.md](data-model.md)** - Data structures, validation rules, and Python types
4. **[contracts/calculator-api.json](contracts/calculator-api.json)** - OpenAPI specification for calculator API
5. **[quickstart.md](quickstart.md)** - Developer setup guide (10-minute onboarding)

### Key Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| **Architecture** | Single Django app + Bootstrap SPA | YAGNI - simple calculator needs no multi-app complexity |
| **Charting** | Chart.js 4.4.1 | 60KB, native uncertainty bands, Bootstrap compatible |
| **Database** | SQLite (dev + prod) | Stateless app with read-only config, no scaling needed |
| **Deployment** | Railway  DigitalOcean | Free MVP tier with clear scaling path |
| **UK Tax Data** | JSON config file | Version controlled, simple annual updates, YAGNI |
| **Frontend Testing** | Minimal (manual) | Simple UI, backend unit tests cover logic, can add later |

### Constitution Compliance

All 7 gates **PASS**:
-  SOLID principles followed (SRP, DIP, separation of concerns)
-  Modular design (single focused app, DRY approach)
-  Code-first workflow (implementation before tests)
-  Unit tests only (no integration/e2e)
-  YAGNI compliant (no over-engineering)
-  DevOps tooling ready (Ruff, pytest, pre-commit, commitizen)
-  Frontend testing decided (minimal for MVP)

### Next Steps

**Phase 2**: Run \/speckit.tasks\ to generate detailed implementation tasks

The generated tasks.md will break down implementation into:
- **Setup Phase**: Django project initialization, dependencies
- **Foundational Phase**: Core infrastructure (settings, static files, UK tax config)
- **User Story 1 (P1)**: Input form with validation
- **User Story 2 (P2)**: Calculation engine and API endpoint
- **User Story 3 (P3)**: Chart.js visualization with uncertainty bands
- **Polish Phase**: Testing, documentation, deployment prep

### Technology Stack (Final)

**Backend:**
- Python 3.13
- Django 5.1
- pytest + pytest-django
- Ruff

**Frontend:**
- Bootstrap 5.3.2 (CDN)
- Chart.js 4.4.1 (CDN)
- Vanilla JavaScript

**Infrastructure:**
- SQLite database
- Railway hosting (MVP)
- Git + GitHub
- Pre-commit hooks

**Dependencies:** See quickstart.md for full requirements.txt

---

**Planning Phase Complete**: Ready for task generation and implementation 
