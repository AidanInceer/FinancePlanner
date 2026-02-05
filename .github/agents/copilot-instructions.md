# FinancePlanner Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-01-26

## Active Technologies
- Python 3.13 + Django 5.1, pytest, pytest-django, ruff, pre-commit (001-uk-income-tax-tab)
- SQLite (db.sqlite3) for app; calculator results are computed in-memory (001-uk-income-tax-tab)
- Python 3.13 + Django 5.1, Chart.js (existing frontend charts), Bootstrap 5 (001-finance-sub-apps)
- SQLite (db.sqlite3) for existing app; calculators remain stateless (001-finance-sub-apps)

- Python 3.13 + Django 5.1, Bootstrap 5.3, NEEDS CLARIFICATION: JavaScript charting library (Chart.js vs Plotly vs D3.js) (001-loan-payoff-calc)

## Project Structure

```text
backend/
frontend/
tests/
```

## Commands

cd src; pytest; ruff check .

## Code Style

Python 3.13: Follow standard conventions

## Recent Changes
- 001-finance-sub-apps: Added Python 3.13 + Django 5.1, Chart.js (existing frontend charts), Bootstrap 5
- 001-uk-income-tax-tab: Added Python 3.13 + Django 5.1, pytest, pytest-django, ruff, pre-commit

- 001-loan-payoff-calc: Added Python 3.13 + Django 5.1, Bootstrap 5.3, NEEDS CLARIFICATION: JavaScript charting library (Chart.js vs Plotly vs D3.js)

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
