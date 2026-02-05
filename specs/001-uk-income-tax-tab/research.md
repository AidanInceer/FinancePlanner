# Phase 0 Research: UK Income Tax Calculator Tab

## Decision 1: Tax year rates and bands
- **Decision**: Use the latest published UK tax year (6 Apr 2025–5 Apr 2026) for income tax bands and personal allowance taper.
- **Rationale**: This is the latest official guidance on GOV.UK and provides up-to-date thresholds for calculation accuracy.
- **Alternatives considered**:
  - 2024–25 rates (rejected: less current).
  - User-selectable multiple tax years (rejected for MVP scope).

## Decision 2: Jurisdiction-specific income tax bands
- **Decision**: Support England/Wales/Northern Ireland bands and Scotland bands separately.
- **Rationale**: Scottish income tax has distinct bands/rates; user must be able to select jurisdiction.
- **Alternatives considered**:
  - UK-wide single banding (rejected: inaccurate for Scotland).

## Decision 3: Personal allowance taper
- **Decision**: Implement personal allowance tapering at £100,000 adjusted net income and removal at £125,140.
- **Rationale**: Required for accurate higher-income calculations and explicitly documented by GOV.UK.
- **Alternatives considered**:
  - Ignore taper (rejected: inaccurate for high incomes).

## Decision 4: National Insurance (Class 1) thresholds and categories
- **Decision**: Use 2025–26 Class 1 thresholds (LEL/PT/UEL) and support common employee categories: A, B, C, H, J, M, Z.
- **Rationale**: These are the most common employee categories and cover standard, reduced, deferment, and exemption cases.
- **Alternatives considered**:
  - Only Category A (rejected: does not meet requirements for NI category selection).

## Decision 5: Student loan repayment plans
- **Decision**: Support Plan 1, Plan 2, Plan 4, Plan 5 (9% over threshold) and Postgraduate (6% over threshold) using GOV.UK annual thresholds.
- **Rationale**: These plan types were explicitly requested and cover typical UK borrower scenarios.
- **Alternatives considered**:
  - Plan 2 only (rejected: insufficient coverage).

## Decision 6: Data source for thresholds
- **Decision**: Store tax thresholds/rates in a JSON configuration file (extend existing UK tax config data).
- **Rationale**: Keeps rates auditable and editable without code changes; aligns with existing pattern in the project.
- **Alternatives considered**:
  - Hard-coded constants (rejected: harder to maintain).
  - External API (rejected: adds dependencies and runtime variability).

## Sources
- Income tax rates and bands: https://www.gov.uk/income-tax-rates
- Scottish income tax: https://www.gov.uk/scottish-income-tax
- Personal allowance taper: https://www.gov.uk/income-tax-rates/income-over-100000
- NI thresholds and rates: https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2025-to-2026
- NI category letters: https://www.gov.uk/national-insurance-rates-letters
- Student loan thresholds and rates: https://www.gov.uk/repaying-your-student-loan/what-you-pay
