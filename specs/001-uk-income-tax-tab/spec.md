# Feature Specification: UK Income Tax Calculator Tab

**Feature Branch**: `001-uk-income-tax-tab`
**Created**: 2026-02-04
**Status**: Draft
**Input**: User description: "Please can you add to the current webpage with a new tab for an income tax calculator for the UK - you should account for all releveant parameters e.g. NI student loan types etc"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently (via UNIT TESTS)
  - Deployed independently
  - Demonstrated to users independently

  NOTE: This project uses UNIT TESTS ONLY. Integration and E2E tests are not required.
  Acceptance scenarios below define expected behavior; unit tests will validate this at the code level.
-->

### User Story 1 - Calculate UK take-home pay (Priority: P1)

As a user, I want to enter my income and key UK tax parameters so I can see my estimated take-home pay and total deductions.

**Why this priority**: This is the core value of the new tab and is the primary reason users will open it.

**Independent Test**: Can be fully tested by entering a set of inputs and verifying the displayed net pay and deduction totals.

**Acceptance Scenarios**:

1. **Given** a valid gross income and default UK tax parameters, **When** I calculate, **Then** I see net pay and a breakdown of income tax, NI, and student loan deductions.
2. **Given** a gross income below the personal allowance, **When** I calculate, **Then** income tax is £0 while other applicable deductions are still shown.

---

### User Story 2 - Adjust NI and student loan settings (Priority: P2)

As a user, I want to select my National Insurance category and student loan plan so the calculation reflects my situation.

**Why this priority**: These parameters materially change deductions and are explicitly requested.

**Independent Test**: Can be tested by switching NI category and loan plan and confirming deduction values change accordingly.

**Acceptance Scenarios**:

1. **Given** a fixed income, **When** I change my NI category or student loan plan, **Then** the corresponding deductions update while other values remain consistent.

---

### User Story 3 - Understand the deduction breakdown (Priority: P3)

As a user, I want a clear breakdown of how my deductions are calculated so I can trust the result.

**Why this priority**: Transparency reduces confusion and helps users validate inputs.

**Independent Test**: Can be tested by verifying that each deduction component is displayed with its amount and totals add up.

**Acceptance Scenarios**:

1. **Given** a completed calculation, **When** I view the results, **Then** I see itemized deductions and totals that sum to the net pay calculation.

### Edge Cases

- Income is exactly on a tax band boundary.
- Personal allowance is tapered for high incomes.
- NI category indicates exemption (e.g., no employee NI).
- Student loan threshold is not met (repayment should be £0).
- Inputs are missing, non-numeric, or negative.

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST provide a dedicated UK income tax calculator tab within the existing calculator interface.
- **FR-002**: System MUST allow users to enter gross income and select a pay frequency (annual, monthly, weekly) and convert results consistently to annual and monthly views.
- **FR-003**: System MUST allow users to select a UK tax jurisdiction (England/Wales/Northern Ireland or Scotland) for income tax banding.
- **FR-004**: System MUST allow users to select a National Insurance category and compute NI contributions accordingly.
- **FR-005**: System MUST allow users to select student loan repayment plan types (Plan 1, Plan 2, Plan 4, Plan 5, Postgraduate) and compute repayments accordingly.
- **FR-006**: System MUST allow users to enter optional adjustments that affect taxable pay (e.g., pension contributions as amount or percentage, and other pre-tax deductions).
- **FR-007**: System MUST display a results summary including gross income, taxable income, income tax, NI, student loan repayments, total deductions, and net pay.
- **FR-008**: System MUST display an itemized breakdown of deductions and show the effective deduction rate (total deductions divided by gross income).
- **FR-009**: System MUST validate inputs and provide clear error feedback for missing or invalid values.
- **FR-010**: System MUST clearly show which tax year rates are being used in the calculation.

### Acceptance Coverage

- **FR-001, FR-002, FR-007** are validated by User Story 1 acceptance scenarios.
- **FR-003, FR-004, FR-005, FR-006** are validated by User Story 2 acceptance scenarios and edge cases.
- **FR-008** is validated by User Story 3 acceptance scenarios.
- **FR-009, FR-010** are validated by input validation edge cases and results display requirements.

### Key Entities *(include if feature involves data)*

- **Tax Calculation Input**: User-provided income values, pay frequency, jurisdiction, NI category, student loan plan, and adjustment values.
- **Deduction Breakdown**: Calculated amounts for income tax, NI, student loan, total deductions, and effective deduction rate.
- **Net Pay Summary**: Gross income, taxable income, and net pay values for annual and monthly views.

### Assumptions

- Uses the latest published UK tax year thresholds and rates available to the product.
- Supports UK resident taxation only; savings/dividends/capital gains are out of scope.
- Provides an estimate for planning purposes and does not constitute financial advice.

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: 90% of users can complete a calculation and view results in under 2 minutes.
- **SC-002**: 95% of calculations display results within 2 seconds of submission.
- **SC-003**: 95% of tested scenarios match official reference examples within £1.
- **SC-004**: At least 80% of users report the breakdown as clear in feedback surveys.
