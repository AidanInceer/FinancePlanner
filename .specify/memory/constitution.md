<!--
SYNC IMPACT REPORT
==================
Version change: N/A → 1.0.0 (Initial constitution)
Rationale: First formal constitution establishing Django web app best practices.

Principles defined:
- I. SOLID Design Principles (SRP, OCP, LSP, ISP, DIP)
- II. Code Organization & Modularity (DRY, Django app structure, clear boundaries)
- III. Code-First Development (Implementation before tests)
- IV. Unit Testing Only (No integration/e2e required)
- V. YAGNI & Simplicity (Build what's needed, avoid over-engineering)

Sections added:
- DevOps & CI/CD Requirements (tooling, automation, quality gates)
- Frontend Testing Strategy (options and recommendations)

Templates updated:
- ✅ plan-template.md: 
  - Constitution Check section with SOLID, modularity, code-first, unit-test-only gates
  - Technical Context updated with Django-specific dependencies and Ruff linting
  - Project Structure updated with Django app options (single/multi-app/monolithic)
  
- ✅ spec-template.md: 
  - User Scenarios section clarified with unit-test-only approach
  - Added note that acceptance scenarios are validated via unit tests
  
- ✅ tasks-template.md: 
  - Updated workflow to CODE-FIRST (implementation then tests)
  - All phases now show implementation tasks before unit test tasks
  - Removed contract/integration test references
  - Updated task IDs and parallel execution examples for code-first workflow
  - Updated notes section to emphasize code-first and test structure mirroring

Follow-up items:
- Frontend testing approach needs selection from provided options (Jest/Playwright/Visual/Minimal)
- Pre-commit hooks configuration to be implemented (.pre-commit-config.yaml)
- Ruff configuration in pyproject.toml to be created (line length: 100)
- GitHub Actions CI/CD workflow to be defined (.github/workflows/)
- .gitignore to be populated with comprehensive Python/Django patterns

Created: 2026-01-26
-->

# FinancePlanner Constitution

## Core Principles

### I. SOLID Design Principles (NON-NEGOTIABLE)

All Python code MUST adhere to SOLID principles:

- **Single Responsibility Principle (SRP)**: Each class/module has one reason to change. Django models handle data, views handle requests, services handle business logic.
- **Open/Closed Principle (OCP)**: Code is open for extension, closed for modification. Use inheritance, mixins, and Django's class-based views appropriately.
- **Liskov Substitution Principle (LSP)**: Subclasses must be substitutable for their base classes without breaking functionality.
- **Interface Segregation Principle (ISP)**: No client should depend on methods it doesn't use. Keep interfaces focused and minimal.
- **Dependency Inversion Principle (DIP)**: Depend on abstractions, not concretions. Use dependency injection and Django's settings configuration.

**Rationale**: SOLID principles ensure maintainable, testable, and scalable codebases. They prevent technical debt and enable safe refactoring.

### II. Code Organization & Modularity

Django apps MUST be modular, self-contained, and follow DRY principles:

- **Modular Django Apps**: Each Django app represents a cohesive domain boundary (e.g., `accounts`, `budgets`, `transactions`)
- **DRY (Don't Repeat Yourself)**: Extract common functionality into utilities, base classes, or Django middleware. No code duplication.
- **Clear Boundaries**: Apps should have minimal coupling. Use Django signals, events, or service layers for cross-app communication.
- **Standard Django Structure**: Follow Django conventions (`models.py`, `views.py`, `serializers.py`, `services.py`, `urls.py`)
- **Test Structure Mirrors Source**: Tests follow src structure: `tests/unit/accounts/`, `tests/unit/budgets/` etc.

**Rationale**: Modular design enables independent development, testing, and deployment of features. DRY reduces bugs and maintenance burden.

### III. Code-First Development

Code MUST be written before tests:

- **Implementation First**: Write production code to solve the problem
- **Tests Follow Source Structure**: After implementation, create corresponding unit tests in mirrored directory structure
- **Unit Tests Required**: All business logic, models, views, and services must have unit tests
- **Test Coverage Expected**: Aim for high coverage of critical paths, but quality over quantity

**Rationale**: Code-first approach allows rapid prototyping and iteration. Tests validate working implementations rather than constraining design prematurely.

### IV. Unit Testing Only

Testing strategy is focused exclusively on unit tests:

- **Unit Tests ONLY**: Integration tests and end-to-end tests are NOT required
- **Isolated Testing**: Use mocks, stubs, and fixtures to isolate units under test
- **Fast Execution**: Unit tests must run quickly (entire suite < 30 seconds preferred)
- **Pytest Framework**: Use pytest with Django plugin for all testing
- **Structure**: Tests mirror source at `tests/unit/<app_name>/test_<module>.py`

**Rationale**: Unit tests provide fast feedback, are easy to maintain, and sufficient for validating business logic in most web applications. Integration tests add complexity and slow down development.

### V. YAGNI & Simplicity

Start simple and build only what's needed:

- **YAGNI (You Aren't Gonna Need It)**: Don't build features or abstractions until they're required
- **Avoid Over-Engineering**: Resist premature optimization and unnecessary patterns
- **Start Concrete**: Begin with simple implementations, extract abstractions only when duplication appears 3+ times
- **Incremental Complexity**: Add complexity only when justified by actual requirements, not anticipated needs
- **Delete Unused Code**: Remove features, imports, and dependencies that aren't actively used

**Rationale**: Simple code is easier to understand, test, and modify. Premature abstraction creates unnecessary maintenance burden.

## DevOps & CI/CD Requirements

All Python Django projects MUST implement these DevOps practices:

### Code Quality & Formatting

- **Ruff**: Use for both linting and formatting (replaces Black, isort, flake8, pylint)
  - Configuration in `pyproject.toml`
  - Line length: 100 characters
  - Auto-fix enabled in CI
- **Pre-commit Hooks**: Run Ruff checks before every commit
  - Configuration: `.pre-commit-config.yaml`
  - Hooks: ruff-format, ruff-check, trailing-whitespace, end-of-file-fixer
- **Type Hints**: Use Python type hints for function signatures; run `mypy` in CI (optional but recommended)

### Version Control & Commit Standards

- **.gitignore**: Comprehensive Python/Django ignore patterns
  - Python: `__pycache__/`, `*.py[cod]`, `.pytest_cache/`, `.coverage`
  - Django: `*.sqlite3`, `media/`, `staticfiles/`, `local_settings.py`
  - Environment: `.env`, `.venv/`, `venv/`
  - IDE: `.vscode/`, `.idea/`, `.DS_Store`
- **Commitizen**: Enforce conventional commit messages
  - Format: `type(scope): subject`
  - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
  - Generate changelogs automatically

### Testing & CI Pipeline

- **Pytest**: All unit tests run in CI
  - Django pytest plugin required
  - Coverage reporting (aim for >80% on business logic)
  - Parallel execution for speed
- **CI Workflow** (GitHub Actions recommended):
  1. Checkout code
  2. Setup Python 3.13+
  3. Install dependencies (`pip install -r requirements.txt`)
  4. Run Ruff checks (`ruff check . && ruff format --check .`)
  5. Run pytest with coverage (`pytest --cov=src --cov-report=term-missing`)
  6. Fail build if coverage below threshold or tests fail

### Deployment Pipeline

- **Environment Separation**: dev, staging, production environments
- **Django Settings**: Use environment variables for sensitive config (never commit secrets)
- **Database Migrations**: Run `python manage.py migrate` in deployment pipeline
- **Static Files**: Collect static files (`python manage.py collectstatic --noinput`)
- **Health Checks**: Implement `/health/` endpoint for monitoring

## Frontend Testing Strategy

Frontend testing is OPTIONAL. If implemented, choose ONE approach:

### Option 1: Unit Testing with Jest (Recommended for React/Vue)

- **Framework**: Jest + Testing Library (@testing-library/react or @testing-library/vue)
- **Scope**: Component logic, state management, utility functions
- **Mocking**: API calls mocked, no real backend interaction
- **Coverage**: Focus on user interactions and component behavior

### Option 2: End-to-End with Playwright (If E2E Required)

- **Framework**: Playwright (modern, fast, reliable)
- **Scope**: Critical user journeys only (login, checkout, key workflows)
- **Frequency**: Run in staging environment, not on every commit
- **Maintenance**: Minimize number of E2E tests due to maintenance cost

### Option 3: Visual Regression Testing (Optional)

- **Framework**: Percy, Chromatic, or BackstopJS
- **Scope**: Component visual consistency across browsers
- **Use Case**: Design system components, high-visibility pages

### Option 4: Minimal/No Frontend Testing

- **Approach**: Rely on manual testing and Django backend unit tests
- **Justification**: For simple UIs or MVP projects, formal frontend tests may not be cost-effective
- **Fallback**: Implement frontend tests later if complexity grows

**Decision Required**: Select ONE option based on project complexity, team size, and UI criticality.

## Governance

This constitution supersedes all other practices and guidelines:

- **Compliance Mandatory**: All code reviews, PRs, and design decisions MUST align with these principles
- **Justification Required**: Any deviation requires explicit documentation explaining why the principle doesn't apply
- **Amendment Process**:
  1. Propose change with rationale and impact analysis
  2. Update affected templates and documentation
  3. Increment version per semantic versioning rules
  4. Document in Sync Impact Report
- **Versioning**: MAJOR.MINOR.PATCH format
  - MAJOR: Breaking changes to principles or governance
  - MINOR: New principles or sections added
  - PATCH: Clarifications, wording improvements, typo fixes

**Version**: 1.0.0 | **Ratified**: 2026-01-26 | **Last Amended**: 2026-01-26
