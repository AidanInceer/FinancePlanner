# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.13, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]
**Primary Dependencies**: [e.g., Django 5.x, FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]
**Storage**: [if applicable, e.g., PostgreSQL, SQLite, CoreData, files or N/A]
**Testing**: [e.g., pytest with Django plugin or NEEDS CLARIFICATION]
**Linting/Formatting**: [e.g., Ruff or NEEDS CLARIFICATION]
**Target Platform**: [e.g., Linux server, Docker, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: [web/mobile/desktop - determines source structure]
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [ ] **SOLID Compliance**: Does the design follow Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion principles?
- [ ] **Modularity & DRY**: Are Django apps properly bounded? Is there code duplication that should be extracted?
- [ ] **Code-First Approach**: Is the plan structured for implementation-first with tests following?
- [ ] **Unit Tests Only**: Does the testing strategy focus exclusively on unit tests (no integration/e2e)?
- [ ] **YAGNI Check**: Are we building only what's needed, or introducing unnecessary abstractions/features?
- [ ] **DevOps Tooling**: Are Ruff, pre-commit, pytest, and commitizen properly configured?
- [ ] **Frontend Testing Decision**: Has a frontend testing approach been selected (or explicitly deferred)?

**Violations/Justifications**: [Document any principle violations and why they're necessary]

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
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
# [REMOVE IF UNUSED] Option 1: Single Django App (Simple MVP)
src/
├── accounts/          # Django app for user management
├── core/              # Shared utilities, base classes
└── config/            # Django settings and configuration

tests/
└── unit/
    ├── accounts/
    └── core/

# [REMOVE IF UNUSED] Option 2: Django Multi-App (Recommended for modular domains)
backend/
├── apps/
│   ├── accounts/      # User authentication, profiles
│   ├── budgets/       # Budget management domain
│   ├── transactions/  # Transaction tracking domain
│   └── reports/       # Reporting and analytics domain
├── core/              # Shared utilities, middleware
├── config/            # Django settings, urls, wsgi
└── tests/
    └── unit/
        ├── accounts/
        ├── budgets/
        ├── transactions/
        └── reports/

frontend/
├── src/
│   ├── components/    # Reusable UI components
│   ├── pages/         # Page-level components
│   ├── services/      # API client, state management
│   └── utils/         # Helper functions
└── tests/             # Frontend tests (if selected)

# [REMOVE IF UNUSED] Option 3: Monolithic Django (Traditional structure)
project_name/
├── app_name/          # Main Django app
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── services.py
│   └── urls.py
├── static/
├── templates/
├── tests/
│   └── unit/
│       └── app_name/
└── manage.py
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
