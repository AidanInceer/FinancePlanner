# Feature Specification: Finance Sub-Apps Expansion

**Feature Branch**: `001-finance-sub-apps`
**Created**: February 4, 2026
**Status**: Draft
**Input**: User description: "Build more sub apps for the finance app: configurable Rent vs Buy calculator with defaults plus summary and graph; Emergency Fund Calculator; Financial Resilience Score (inputs: savings, income stability, debt load, insurance; output: resilience index + weak points); Time-to-Freedom Calculator (FIRE-style, no cult framing; output: freedom number + timeline)."

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

### User Story 1 - Rent vs Buy Comparison (Priority: P1)

As a user, I want a highly configurable rent vs buy calculator with reasonable defaults so I can compare outcomes without needing deep expertise.

**Why this priority**: It is the most complex, highest-value decision tool and serves as a flagship calculator.

**Independent Test**: Can be fully tested by providing a set of inputs and verifying the summary and chart outputs.

**Acceptance Scenarios**:

1. **Given** the calculator loads, **When** the user accepts default values, **Then** a comparison summary and a visual comparison graph are displayed.
2. **Given** the user updates any input, **When** they calculate, **Then** the summary and graph update to reflect the new inputs.
3. **Given** a required input is missing or invalid, **When** the user calculates, **Then** a clear validation message is shown and results are not updated.

---

### User Story 2 - Emergency Fund Calculator (Priority: P2)

As a user, I want a simple emergency fund calculator so I can understand my target savings and current gap.

**Why this priority**: It is a high-demand, low-complexity tool that delivers quick value.

**Independent Test**: Can be fully tested by entering expenses and target months and validating the target and gap outputs.

**Acceptance Scenarios**:

1. **Given** monthly expenses and target months are provided, **When** the user calculates, **Then** the target emergency fund and savings gap are shown.
2. **Given** the user adjusts target months, **When** they recalculate, **Then** the target updates accordingly.

---

### User Story 3 - Financial Resilience Score (Priority: P3)

As a user, I want a resilience score based on my savings, income stability, debt load, and insurance so I can identify weak points to improve.

**Why this priority**: It provides an actionable health check that complements the calculators.

**Independent Test**: Can be fully tested by entering the four inputs and validating the index and weak-point outputs.

**Acceptance Scenarios**:

1. **Given** all four inputs are provided, **When** the user calculates, **Then** a resilience index and a list of weak points are displayed.
2. **Given** one input indicates elevated risk, **When** the score is calculated, **Then** that area is flagged as a weak point.

---

### User Story 4 - Time-to-Freedom Calculator (Priority: P3)

As a user, I want a time-to-freedom calculator so I can see my freedom number and an estimated timeline without hype or cult framing.

**Why this priority**: It supports long-term planning and complements the other tools.

**Independent Test**: Can be fully tested by entering inputs and validating the freedom number and timeline outputs.

**Acceptance Scenarios**:

1. **Given** required inputs are provided, **When** the user calculates, **Then** a freedom number and an estimated timeline are shown.
2. **Given** the user increases contributions, **When** they recalculate, **Then** the timeline shortens or stays the same.

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

- Zero or negative values for savings, expenses, or contributions.
- Extremely large values that could skew results.
- Missing required inputs for any calculator.
- Inconsistent inputs (e.g., expenses exceeding income by a large margin).
- Non-numeric characters or unexpected formats in numeric fields.

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: The system MUST provide a Rent vs Buy calculator with pre-filled, reasonable default values.
- **FR-002**: The Rent vs Buy calculator MUST allow users to adjust all key assumptions and inputs.
- **FR-003**: The Rent vs Buy calculator MUST display both a written summary and a visual comparison graph.
- **FR-004**: The system MUST provide an Emergency Fund calculator that outputs a target fund amount and a savings gap.
- **FR-005**: The Emergency Fund calculator MUST allow users to set target coverage in months.
- **FR-006**: The system MUST provide a Financial Resilience Score calculator using savings, income stability, debt load, and insurance inputs.
- **FR-007**: The Financial Resilience Score output MUST include a single index value and a list of weak points.
- **FR-008**: The system MUST provide a Time-to-Freedom calculator that outputs a freedom number and an estimated timeline.
- **FR-009**: Each calculator MUST validate required inputs and show clear error messages when inputs are invalid.
- **FR-010**: Each calculator MUST recompute results when inputs change.
- **FR-011**: All outputs MUST use the app’s default currency and time units consistently.

### Key Entities *(include if feature involves data)*

- **Calculation Scenario**: A set of inputs for one calculator session.
- **Result Summary**: The primary outputs displayed to the user (targets, index, freedom number, timeline).
- **Comparison Graph Data**: The values used to render the rent vs buy visual comparison.
- **Resilience Assessment**: The computed index and the associated weak points.

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: 90% of users can complete any calculator flow and obtain results in under 5 minutes.
- **SC-002**: 95% of calculation attempts produce results without validation errors on the first try.
- **SC-003**: Users report at least 4 out of 5 average satisfaction for clarity of results and explanations.
- **SC-004**: The Rent vs Buy calculator summary and graph are viewed by at least 60% of calculator users.

## Assumptions

- Reasonable default values are derived from common, publicly known averages and can be edited by the user.
- The app’s existing default currency and time units are used without user-specific localization changes.
- Calculators do not require user accounts or data persistence beyond the current session.

## Scope Boundaries

- Out of scope: user authentication, long-term storage of personal financial data, and personalized financial advice.

## Dependencies

- Existing calculator navigation and layout within the finance app.
