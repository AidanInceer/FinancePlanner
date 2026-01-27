# Data Model: Student Loan Payoff Calculator

**Phase**: 1 - Design & Contracts
**Purpose**: Define entities, validation rules, and data structures
**Date**: 2026-01-26

## Overview

The calculator is stateless - no user data is persisted. All data structures represent in-memory calculations for a single user session. UK tax configuration is read-only reference data.

---

## Core Entities

### 1. CalculatorInput

**Purpose**: Represents all user-provided data for a single calculation session

**Attributes:**

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `age` | Integer | 18 ≤ age ≤ 100 | User's current age |
| `graduation_year` | Integer | 1980 ≤ year ≤ current_year + 10 | Year user graduated |
| `loan_duration_years` | Integer | 1 ≤ duration ≤ 50 | Loan lifetime (typically 35 years) |
| `investment_amount` | Decimal | ≥ 0 | Current investment value (£) |
| `investment_growth_high` | Decimal | 0 ≤ rate ≤ 20 | Optimistic annual return (%) |
| `investment_growth_low` | Decimal | 0 ≤ rate ≤ 20 | Pessimistic annual return (%) |
| `pre_tax_income` | Decimal | ≥ 0 | Annual income before tax (£) |
| `loan_repayment_annual` | Decimal | ≥ 0 | Current annual loan repayment (£) |
| `loan_interest_current` | Decimal | 0 ≤ rate ≤ 20 | Current interest rate (%) |
| `loan_interest_high` | Decimal | 0 ≤ rate ≤ 20 | Pessimistic interest rate (%) |
| `loan_interest_low` | Decimal | 0 ≤ rate ≤ 20 | Optimistic interest rate (%) |

**Validation Rules:**

1. `investment_growth_low ≤ investment_growth_high`
2. `loan_interest_low ≤ loan_interest_current ≤ loan_interest_high`
3. `graduation_year + age ≥ current_year` (cannot graduate in future if already past that age)
4. All numeric fields must be non-negative except where specified
5. Percentage rates stored as decimals (e.g., 5% = 5.0, not 0.05)

**Computed Fields:**

- `loan_end_year`: `graduation_year + loan_duration_years`
- `current_year`: `datetime.now().year`
- `years_remaining`: `loan_end_year - current_year`

**Python Type:**

```python
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class CalculatorInput:
    age: int
    graduation_year: int
    loan_duration_years: int
    investment_amount: Decimal
    investment_growth_high: Decimal
    investment_growth_low: Decimal
    pre_tax_income: Decimal
    loan_repayment_annual: Decimal
    loan_interest_current: Decimal
    loan_interest_high: Decimal
    loan_interest_low: Decimal

    @property
    def loan_end_year(self) -> int:
        return self.graduation_year + self.loan_duration_years

    def validate(self) -> list[str]:
        """Returns list of validation errors, empty if valid"""
        errors = []

        if not (18 <= self.age <= 100):
            errors.append("Age must be between 18 and 100")

        if self.investment_growth_low > self.investment_growth_high:
            errors.append("Investment growth low cannot exceed high")

        if not (self.loan_interest_low <= self.loan_interest_current <= self.loan_interest_high):
            errors.append("Loan interest current must be between low and high")

        # Add remaining validations...
        return errors
```

---

### 2. ScenarioProjection

**Purpose**: Represents financial projection for one scenario (optimistic, pessimistic, or realistic)

**Attributes:**

| Field | Type | Description |
|-------|------|-------------|
| `scenario_type` | Enum | "optimistic", "pessimistic", "realistic" |
| `investment_growth_rate` | Decimal | Annual investment return used (%) |
| `loan_interest_rate` | Decimal | Annual loan interest used (%) |
| `yearly_data` | List[YearlyProjection] | Year-by-year breakdown |
| `total_loan_cost` | Decimal | Sum of all repayments + interest (£) |
| `final_investment_value` | Decimal | Investment value at loan end date (£) |
| `crossover_year` | Integer or None | Year when investment > loan cost (if exists) |
| `net_benefit` | Decimal | Investment value - loan cost (positive = invest wins) |

**Python Type:**

```python
from enum import Enum

class ScenarioType(Enum):
    OPTIMISTIC = "optimistic"
    PESSIMISTIC = "pessimistic"
    REALISTIC = "realistic"

@dataclass
class ScenarioProjection:
    scenario_type: ScenarioType
    investment_growth_rate: Decimal
    loan_interest_rate: Decimal
    yearly_data: list['YearlyProjection']
    total_loan_cost: Decimal
    final_investment_value: Decimal
    crossover_year: int | None
    net_benefit: Decimal
```

---

### 3. YearlyProjection

**Purpose**: Represents financial state for a single year within a scenario

**Attributes:**

| Field | Type | Description |
|-------|------|-------------|
| `year` | Integer | Calendar year (e.g., 2024) |
| `loan_balance` | Decimal | Outstanding loan balance (£) |
| `investment_value` | Decimal | Investment portfolio value (£) |
| `annual_repayment` | Decimal | Loan repayment this year (£) |
| `interest_accrued` | Decimal | Loan interest accrued this year (£) |
| `investment_growth` | Decimal | Investment growth this year (£) |

**Python Type:**

```python
@dataclass
class YearlyProjection:
    year: int
    loan_balance: Decimal
    investment_value: Decimal
    annual_repayment: Decimal
    interest_accrued: Decimal
    investment_growth: Decimal
```

---

### 4. CalculationResult

**Purpose**: Complete output from calculator including all scenarios and recommendation

**Attributes:**

| Field | Type | Description |
|-------|------|-------------|
| `optimistic` | ScenarioProjection | Best-case scenario |
| `pessimistic` | ScenarioProjection | Worst-case scenario |
| `realistic` | ScenarioProjection | Current-rate scenario |
| `recommendation` | PayoffRecommendation | Optimal decision |
| `calculated_at` | DateTime | Timestamp of calculation |

**Python Type:**

```python
from datetime import datetime

@dataclass
class CalculationResult:
    optimistic: ScenarioProjection
    pessimistic: ScenarioProjection
    realistic: ScenarioProjection
    recommendation: 'PayoffRecommendation'
    calculated_at: datetime
```

---

### 5. PayoffRecommendation

**Purpose**: Optimal payoff decision with supporting rationale

**Attributes:**

| Field | Type | Description |
|-------|------|-------------|
| `decision` | Enum | "pay_off_early", "keep_investing", "neutral" |
| `optimal_date` | Date or None | Recommended early payoff date (if applicable) |
| `savings_amount` | Decimal | Financial benefit of recommended path (£) |
| `confidence` | Enum | "high", "medium", "low" based on scenario variance |
| `rationale` | String | Plain-language explanation |

**Decision Logic:**

```python
class PayoffDecision(Enum):
    PAY_OFF_EARLY = "pay_off_early"
    KEEP_INVESTING = "keep_investing"
    NEUTRAL = "neutral"

class Confidence(Enum):
    HIGH = "high"      # Scenarios agree (>5% difference)
    MEDIUM = "medium"  # Moderate variance (2-5% difference)
    LOW = "low"        # High uncertainty (<2% difference)

@dataclass
class PayoffRecommendation:
    decision: PayoffDecision
    optimal_date: date | None
    savings_amount: Decimal
    confidence: Confidence
    rationale: str

    @staticmethod
    def generate(result: CalculationResult) -> 'PayoffRecommendation':
        """
        Generate recommendation from calculation result

        Logic:
        - If realistic.net_benefit > 0 and variance low: KEEP_INVESTING (high confidence)
        - If realistic.net_benefit < 0 and variance low: PAY_OFF_EARLY (high confidence)
        - If |net_benefit| < 2% of loan cost: NEUTRAL (low confidence)
        - If scenarios disagree: Lower confidence
        """
        # Implementation in services.py
        pass
```

---

### 6. TaxConfiguration

**Purpose**: UK Plan 2 student loan and tax thresholds (read-only reference data)

**Attributes:**

| Field | Type | Description |
|-------|------|-------------|
| `year` | Integer | Tax year |
| `repayment_threshold` | Decimal | Income threshold for repayments (£) |
| `repayment_rate` | Decimal | Percentage above threshold (9% = 0.09) |
| `inflation_adjustment` | Decimal | Annual threshold increase rate (2.5% = 0.025) |

**Source**: `data/uk_tax_thresholds.json`

**Example JSON:**

```json
{
  "plan_2": {
    "base_year": 2023,
    "repayment_threshold": 27295,
    "repayment_rate": 0.09,
    "inflation_adjustment": 0.025,
    "threshold_history": [
      {"year": 2021, "threshold": 27295},
      {"year": 2022, "threshold": 27295},
      {"year": 2023, "threshold": 27295}
    ]
  }
}
```

**Python Type:**

```python
@dataclass
class TaxConfiguration:
    year: int
    repayment_threshold: Decimal
    repayment_rate: Decimal
    inflation_adjustment: Decimal

    @staticmethod
    def load_from_json() -> dict[int, 'TaxConfiguration']:
        """Load tax config from data/uk_tax_thresholds.json"""
        # Implementation in services.py
        pass

    def get_threshold_for_year(self, target_year: int) -> Decimal:
        """Calculate threshold for future year with inflation adjustment"""
        years_ahead = target_year - self.year
        if years_ahead <= 0:
            return self.repayment_threshold

        # Compound inflation adjustment
        adjusted = self.repayment_threshold * (1 + self.inflation_adjustment) ** years_ahead
        return Decimal(adjusted).quantize(Decimal('0.01'))
```

---

## Validation Summary

### Input Validation

All validation happens in `calculator/validators.py`:

```python
class CalculatorInputValidator:
    def validate_age(self, age: int) -> list[str]:
        """Validate age is within reasonable bounds"""

    def validate_rates(self, low: Decimal, current: Decimal, high: Decimal) -> list[str]:
        """Validate rate range logic"""

    def validate_timeline(self, age: int, grad_year: int, current_year: int) -> list[str]:
        """Validate timeline consistency"""

    def validate_all(self, input_data: CalculatorInput) -> list[str]:
        """Run all validations and return combined errors"""
```

### Business Logic Validation

Validation during calculation in `calculator/services.py`:

- Check for division by zero in investment calculations
- Ensure year ranges don't exceed reasonable bounds (max 50 years)
- Validate that loan balance doesn't go negative
- Ensure investment value doesn't become negative

---

## Data Flow

```text
1. User submits form (HTML) → POST /api/calculate
2. Django view creates CalculatorInput from request.data
3. CalculatorInputValidator.validate_all() → return errors if invalid
4. CalculatorService.calculate(input) → CalculationResult
   a. Load TaxConfiguration from JSON
   b. Generate ScenarioProjection for optimistic scenario
   c. Generate ScenarioProjection for pessimistic scenario
   d. Generate ScenarioProjection for realistic scenario
   e. PayoffRecommendation.generate(result) → recommendation
5. Return CalculationResult as JSON to frontend
6. JavaScript renders Chart.js graph from yearly_data arrays
```

---

## Database Schema

**Note**: This calculator is stateless. No database models needed for user data.

**Optional**: If we want to track tax thresholds in database instead of JSON:

```python
# calculator/models.py (OPTIONAL - not implementing initially per YAGNI)

class UKTaxThreshold(models.Model):
    """
    OPTIONAL: Could store UK tax thresholds in database
    Currently using JSON file approach per research.md decision
    """
    year = models.IntegerField(unique=True)
    repayment_threshold = models.DecimalField(max_digits=10, decimal_places=2)
    repayment_rate = models.DecimalField(max_digits=4, decimal_places=3)  # 0.09 = 9%
    inflation_adjustment = models.DecimalField(max_digits=4, decimal_places=3)

    class Meta:
        ordering = ['-year']
```

**Decision**: Not implementing database model initially. JSON file sufficient per YAGNI principle. Can migrate to database model later if needed.

---

## Frontend Data Structures

JavaScript objects for Chart.js integration:

```javascript
// Response from /api/calculate
interface CalculationResponse {
  optimistic: {
    yearly_data: Array<{
      year: number,
      loan_balance: number,
      investment_value: number
    }>,
    total_loan_cost: number,
    final_investment_value: number
  },
  pessimistic: { /* same structure */ },
  realistic: { /* same structure */ },
  recommendation: {
    decision: "pay_off_early" | "keep_investing" | "neutral",
    savings_amount: number,
    confidence: "high" | "medium" | "low",
    rationale: string
  }
}
```

---

## Next Steps

Data model complete. Ready to generate API contracts in Phase 1.
