# Research Findings: Finance Sub-Apps Expansion

## Decision 1: Keep calculators within the existing `calculator` Django app
- **Decision**: Implement new calculators as additional views/services within the existing `calculator` app.
- **Rationale**: Current project structure is monolithic and already hosts calculator logic, templates, and static assets. This minimizes cross-app coupling and avoids unnecessary scaffolding.
- **Alternatives considered**: Creating a new Django app per calculator; rejected to avoid over-engineering for related calculator features.

## Decision 2: Use JSON calculation endpoints with existing client-side pattern
- **Decision**: Expose POST JSON endpoints per calculator and render results in the existing template/JS pattern.
- **Rationale**: Current calculators use POST JSON APIs with client-side rendering and validation, which aligns with the project’s established approach and enables consistent UX.
- **Alternatives considered**: Server-rendered POST forms; rejected to maintain parity with existing calculation flow and dynamic updates.

## Decision 3: Rent vs Buy graph implemented with Chart.js
- **Decision**: Use existing Chart.js dependency for the Rent vs Buy comparison graph.
- **Rationale**: Chart.js is already present in the project for visualization, reducing new dependencies and ensuring visual consistency.
- **Alternatives considered**: Custom SVG/Canvas rendering or another charting library; rejected to avoid extra dependencies.

## Decision 4: Frontend testing approach
- **Decision**: Defer formal frontend testing (Option 4: Minimal/No Frontend Testing).
- **Rationale**: UI complexity is modest and the project’s testing focus is backend unit tests. Manual verification is sufficient for initial delivery.
- **Alternatives considered**: Jest component tests; rejected to keep scope aligned with current testing strategy.

## Decision 5: Stateless calculations (no persistence of personal inputs)
- **Decision**: Do not store calculator inputs/results in the database.
- **Rationale**: Feature scope excludes long-term storage and aligns with current calculator behavior.
- **Alternatives considered**: Persisting calculation scenarios; rejected as out of scope.
