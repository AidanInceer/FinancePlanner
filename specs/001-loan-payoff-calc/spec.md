# Feature Specification: Student Loan Payoff Calculator

**Feature Branch**: `001-loan-payoff-calc`  
**Created**: 2026-01-26  
**Status**: Draft  
**Input**: User description: "Student loan payoff calculator - determine optimal payoff strategy with investment comparison and UK tax calculations"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Input Financial Data (Priority: P1)

A user visits the single-page calculator and enters their personal financial information to assess their student loan situation. The system captures age, graduation details, loan terms, income, investments, and loan parameters. This forms the foundation for any payoff analysis.

**Why this priority**: Without data input, no analysis can occur. This is the entry point for all users and delivers immediate value by organizing their financial picture in one place.

**Independent Test**: Can be fully tested by submitting a complete form with valid data and verifying all fields are captured, validated, and stored in the session/calculation state.

**Acceptance Scenarios**:

1. **Given** a user on the calculator page, **When** they enter age (25), graduation year (2023), and loan duration (35 years), **Then** the system calculates loan end date (2058) and displays it
2. **Given** a user entering investment data, **When** they input investment amount (£50,000), growth rate high (8%), growth rate low (4%), **Then** the system accepts and validates these ranges
3. **Given** a user entering income data, **When** they input pre-tax income (£45,000), **Then** the system validates against UK tax thresholds
4. **Given** a user entering loan details, **When** they input current repayment (£2,400/year), interest rate current (5.5%), high (7%), low (3%), **Then** the system validates rate ranges (low < current < high)
5. **Given** incomplete form data, **When** the user attempts to calculate, **Then** the system highlights missing required fields and prevents calculation

---

### User Story 2 - Calculate Optimal Payoff Strategy (Priority: P2)

Once data is entered, the system calculates whether paying off the loan early is financially beneficial compared to letting investments grow. It compares the total loan cost (with interest) against potential investment returns over the same period, accounting for UK tax implications on income-based repayments.

**Why this priority**: This is the core decision-making engine that answers the user's primary question: "Should I pay off my loan early?" It delivers the key insight users came for.

**Independent Test**: Can be tested by providing a complete dataset and verifying the calculation logic produces a recommendation with supporting financial projections (loan total cost vs investment growth).

**Acceptance Scenarios**:

1. **Given** user data with investments growing faster than loan interest, **When** calculation runs, **Then** system recommends "Do not pay off early" with breakeven date and savings amount
2. **Given** user data with loan interest exceeding investment returns, **When** calculation runs, **Then** system recommends "Pay off early" with optimal payoff date and savings amount
3. **Given** user data with marginal difference (<2% delta), **When** calculation runs, **Then** system indicates "Neutral - personal preference" with detailed comparison
4. **Given** multiple scenarios (best case, worst case, current rates), **When** calculation runs, **Then** system produces three projection timelines with uncertainty ranges
5. **Given** UK tax threshold data, **When** calculating yearly repayments, **Then** system applies correct Plan 2 repayment thresholds (9% over £27,295 as of 2023) and adjusts for inflation

---

### User Story 3 - Visualize Payoff Scenarios with Uncertainty (Priority: P3)

The system presents a line graph showing loan balance over time with multiple scenarios (best case, worst case, current rates) including shaded uncertainty bands. The graph clearly indicates crossover points where investment growth exceeds loan cost, and highlights the optimal decision date.

**Why this priority**: Visual representation makes complex financial projections accessible and helps users understand the uncertainty inherent in long-term financial planning. Enhances user confidence in the recommendation.

**Independent Test**: Can be tested by providing calculation results and verifying the graph renders with correct data points, three scenario lines, shaded uncertainty regions, and annotated decision points.

**Acceptance Scenarios**:

1. **Given** calculated projection data, **When** graph renders, **Then** it displays loan balance over time from graduation year to loan end date (35-year span)
2. **Given** high/low rate scenarios, **When** graph renders, **Then** it shows three lines (optimistic, pessimistic, realistic) with shaded area between high/low bounds
3. **Given** a recommended decision date, **When** graph renders, **Then** it annotates that date with a marker and tooltip explaining savings/cost
4. **Given** investment growth projections, **When** graph renders, **Then** it overlays investment value projection line for comparison
5. **Given** a mobile device, **When** viewing the graph, **Then** it responsively scales and remains readable with touch-enabled tooltips

---

### Edge Cases

- What happens when the user's age is greater than graduation year + loan duration (loan already ended)?
- How does the system handle negative investment amounts or zero income?
- What if interest rates are inverted (low > high, or current outside range)?
- How does the system handle extreme values (e.g., age 100, £10M investments)?
- What happens if UK tax thresholds change during the loan period (inflation adjustments)?
- How does the system respond if JavaScript charting library fails to load?
- What if the user changes input values after viewing results - does the graph update dynamically?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST capture user age, graduation year, and loan duration (years after graduation) to establish timeline
- **FR-002**: System MUST capture investment amount, annual growth rate (high %), annual growth rate (low %) to project investment returns
- **FR-003**: System MUST capture pre-tax annual income to calculate income-based loan repayments using UK tax rules
- **FR-004**: System MUST capture current loan repayment amount (annual), loan interest rate (current, high, low) to project loan costs
- **FR-005**: System MUST validate all numeric inputs for reasonable ranges (age 18-100, rates 0-20%, positive amounts)
- **FR-006**: System MUST validate that rate ranges are logical (low ≤ current ≤ high for both investment and loan rates)
- **FR-007**: System MUST apply UK Plan 2 student loan repayment rules: 9% of income above £27,295 threshold (2023 baseline)
- **FR-008**: System MUST store UK tax thresholds and repayment thresholds as configurable backend data (not user-editable)
- **FR-009**: System MUST calculate three scenarios: optimistic (low loan rate, high investment rate), pessimistic (high loan rate, low investment rate), realistic (current rates)
- **FR-010**: System MUST compute total loan cost including interest over the full repayment period
- **FR-011**: System MUST compute total investment value at loan end date for each scenario
- **FR-012**: System MUST determine optimal payoff decision: pay off early if loan cost > investment returns, otherwise do not pay off
- **FR-013**: System MUST identify the crossover date when investment value equals total loan cost (if exists)
- **FR-014**: System MUST calculate total savings or cost for each decision path (pay off vs invest)
- **FR-015**: System MUST display recommendation clearly: "Pay off early on [DATE]" or "Do not pay off - keep investing" with savings amount
- **FR-016**: System MUST render a line graph showing loan balance over time from graduation to loan end
- **FR-017**: System MUST render investment value projection on the same graph for visual comparison
- **FR-018**: System MUST display uncertainty bands (shaded regions) between high/low scenario lines
- **FR-019**: System MUST annotate the graph with decision point markers and explanatory tooltips
- **FR-020**: System MUST use Bootstrap 5 for responsive layout and form styling
- **FR-021**: System MUST provide form validation feedback inline (highlight errors, show valid checkmarks)
- **FR-022**: System MUST recalculate and update graph dynamically when user changes input values
- **FR-023**: System MUST be a single-page application (no navigation, all functionality on one page)

### Key Entities

- **User Session**: Represents a single calculation session containing all user inputs (age, graduation year, loan duration, investment data, income, loan parameters). Not persisted to database - exists only for duration of page session.

- **Calculation Result**: Represents the output of the payoff analysis including three scenario projections (optimistic, pessimistic, realistic), each containing yearly loan balance, yearly investment value, crossover date, optimal decision, and savings amount.

- **Tax Configuration**: Represents UK tax thresholds and student loan repayment thresholds by year. Stored as backend configuration data, including historical values and inflation adjustment factors for future projections.

- **Scenario Projection**: Represents a single financial projection timeline with yearly data points (year, loan balance, investment value, cumulative repayment, cumulative interest) from graduation year to loan end date.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete data entry and receive a recommendation in under 3 minutes
- **SC-002**: Calculation produces results within 2 seconds of form submission
- **SC-003**: Graph renders within 1 second with smooth animations and responsive interactions
- **SC-004**: Form validation catches 100% of invalid inputs before calculation (no server errors from bad data)
- **SC-005**: Page is fully responsive and usable on mobile devices (320px width minimum)
- **SC-006**: Users can understand the recommendation without financial expertise (plain language explanations)
- **SC-007**: Graph clearly shows uncertainty ranges and decision points without cluttering the visualization
- **SC-008**: 90% of users with complete data successfully view graph and recommendation on first attempt

## Assumptions

- UK Plan 2 student loan rules apply (standard UK student loan from 2012 onwards)
- Tax thresholds and repayment thresholds will be inflated at 2-3% annually for future projections
- Users understand basic financial concepts (interest rates, investment growth)
- Investment growth rates are compounded annually (not monthly)
- Loan interest compounds annually in line with UK student loan practice
- Users want a simple recommendation, not detailed tax optimization strategies
- Browser supports modern JavaScript (ES6+) and Canvas/SVG for charting
- No user authentication or data persistence required (calculator is stateless)
- Users access via desktop or mobile browser (no native app required)
