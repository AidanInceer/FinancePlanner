"""
Data models for the Student Loan Payoff Calculator.

This module defines dataclasses representing the core domain entities:
- CalculatorInput: User-provided parameters for loan/investment scenarios
- ScenarioProjection: Multi-year projection for a single economic scenario
- YearlyProjection: Single year's loan and investment values
- PayoffRecommendation: Decision output with savings analysis
- CalculationResult: Complete calculation output (3 scenarios + recommendation)

All models are immutable dataclasses for thread-safety and testability.
No database persistence - stateless calculator design.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum


@dataclass
class CalculatorInput:
    """
    User input for loan payoff calculation.

    Represents all parameters needed to compare two financial strategies:
    - Strategy A: Minimum loan repayment + invest surplus
    - Strategy B: Accelerated loan repayment

    Attributes:
        age (int): Current age of the user (18-100)
        graduation_year (int): Year of graduation (1998-2030)
        current_year (int): Current year for calculations (1980-2100)
        loan_duration_years (int): Desired time horizon for analysis (1-50 years)
        investment_amount (Decimal): Annual investment amount in GBP (0-100,000)
        investment_growth_high (Decimal): Optimistic return rate as decimal (0.0-0.20)
        investment_growth_low (Decimal): Pessimistic return rate as decimal (0.0-0.20)
        investment_growth_average (Decimal): Average return rate as decimal (0.0-0.20)
        investment_amount_growth (Decimal): Annual investment amount growth rate as
            decimal (0.0-0.20)
        pre_tax_income (Decimal): Annual gross income in GBP (0-500,000)
        salary_growth_optimistic (Decimal): Optimistic salary growth rate as decimal (0.0-0.20)
        salary_growth_pessimistic (Decimal): Pessimistic salary growth rate as decimal (0.0-0.20)
        initial_loan_balance (Decimal): Current outstanding loan balance in GBP (0-200,000)
        loan_interest_current (Decimal): Current loan interest rate as decimal (0.0-0.20)
        loan_interest_high (Decimal): Pessimistic loan interest rate as decimal (0.0-0.20)
        loan_interest_low (Decimal): Optimistic loan interest rate as decimal (0.0-0.20)

    Methods:
        validate() -> list[str]: Returns list of validation error messages

    Properties:
        loan_end_year: Calculated year when loan would be forgiven
        current_year: Current calendar year
        years_remaining: Years until loan forgiveness
    """

    age: int
    graduation_year: int
    current_year: int
    loan_duration_years: int
    investment_amount: Decimal
    investment_growth_high: Decimal
    investment_growth_low: Decimal
    investment_growth_average: Decimal
    investment_amount_growth: Decimal
    pre_tax_income: Decimal
    salary_growth_optimistic: Decimal
    salary_growth_pessimistic: Decimal
    initial_loan_balance: Decimal
    loan_interest_current: Decimal
    loan_interest_high: Decimal
    loan_interest_low: Decimal

    @property
    def loan_end_year(self) -> int:
        """Calculate the year when the loan will end."""
        return self.graduation_year + self.loan_duration_years

    @property
    def years_remaining(self) -> int:
        """Calculate years remaining until loan end."""
        return self.loan_end_year - self.current_year

    def validate(self) -> list[str]:
        """
        Validate all input fields.

        Returns:
            List of validation error messages, empty if valid
        """
        errors = []

        # Age validation
        if not (18 <= self.age <= 100):
            errors.append("Age must be between 18 and 100")

        # Current year validation
        if not (1980 <= self.current_year <= 2100):
            errors.append("Current year must be between 1980 and 2100")

        # Graduation year validation
        if not (1980 <= self.graduation_year <= self.current_year + 10):
            errors.append(f"Graduation year must be between 1980 and {self.current_year + 10}")

        # Loan duration validation
        if not (1 <= self.loan_duration_years <= 50):
            errors.append("Loan duration must be between 1 and 50 years")

        # Investment growth validation
        if self.investment_growth_low > self.investment_growth_high:
            errors.append(
                f"Investment growth low ({self.investment_growth_low}%) "
                f"cannot exceed high ({self.investment_growth_high}%)"
            )

        if not (0 <= self.investment_growth_low <= 20):
            errors.append("Investment growth low must be between 0% and 20%")

        if not (0 <= self.investment_growth_high <= 20):
            errors.append("Investment growth high must be between 0% and 20%")

        if not (0 <= self.investment_growth_average <= 20):
            errors.append("Investment growth average must be between 0% and 20%")

        if not (
            self.investment_growth_low
            <= self.investment_growth_average
            <= self.investment_growth_high
        ):
            errors.append(
                f"Investment growth average ({self.investment_growth_average}%) "
                f"must be between low ({self.investment_growth_low}%) "
                f"and high ({self.investment_growth_high}%)"
            )

        # Loan interest validation
        if not (self.loan_interest_low <= self.loan_interest_current <= self.loan_interest_high):
            errors.append(
                f"Loan interest current ({self.loan_interest_current}%) "
                f"must be between low ({self.loan_interest_low}%) "
                f"and high ({self.loan_interest_high}%)"
            )

        if not (0 <= self.loan_interest_low <= 20):
            errors.append("Loan interest low must be between 0% and 20%")

        if not (0 <= self.loan_interest_current <= 20):
            errors.append("Loan interest current must be between 0% and 20%")

        if not (0 <= self.loan_interest_high <= 20):
            errors.append("Loan interest high must be between 0% and 20%")

        # Non-negative value validation
        if self.investment_amount < 0:
            errors.append("Investment amount cannot be negative")

        if self.pre_tax_income < 0:
            errors.append("Pre-tax income cannot be negative")

        if self.initial_loan_balance < 0:
            errors.append("Initial loan balance cannot be negative")

        # Growth rate validation
        if not (0 <= self.investment_amount_growth <= 20):
            errors.append("Investment amount growth must be between 0% and 20%")

        if not (0 <= self.salary_growth_optimistic <= 20):
            errors.append("Salary growth optimistic must be between 0% and 20%")

        if not (0 <= self.salary_growth_pessimistic <= 20):
            errors.append("Salary growth pessimistic must be between 0% and 20%")

        if self.salary_growth_pessimistic > self.salary_growth_optimistic:
            errors.append(
                f"Salary growth pessimistic ({self.salary_growth_pessimistic}%) "
                f"cannot exceed optimistic ({self.salary_growth_optimistic}%)"
            )

        # Logical validation
        if self.graduation_year + self.age < self.current_year:
            errors.append(
                "Invalid combination: graduation year and age don't align with current year"
            )

        # Edge case: Age beyond loan forgiveness date
        loan_forgiveness_age = self.age + (self.loan_end_year - self.current_year)
        if loan_forgiveness_age > 100:
            errors.append(
                f"Loan would not be forgiven until age {loan_forgiveness_age}, "
                f"which exceeds maximum age of 100"
            )

        # Edge case: Graduation year in the distant future
        if self.graduation_year > self.current_year:
            errors.append(
                f"Graduation year ({self.graduation_year}) is in the future. "
                f"This calculator is for graduates only."
            )

        # Edge case: Ensure realistic loan interest rate ordering
        if self.loan_interest_low > self.loan_interest_high:
            errors.append(
                f"Loan interest low ({self.loan_interest_low}%) "
                f"cannot exceed high ({self.loan_interest_high}%)"
            )

        return errors


class ScenarioType(Enum):
    """
    Economic scenario types for uncertainty modeling.

    OPTIMISTIC: High investment returns, low loan interest
    PESSIMISTIC: Low investment returns, high loan interest
    REALISTIC: Average of optimistic and pessimistic rates
    """

    OPTIMISTIC = "optimistic"
    PESSIMISTIC = "pessimistic"
    REALISTIC = "realistic"


@dataclass
class YearlyProjection:
    """
    Financial state snapshot for a single year.

    Represents one year's data point in a multi-year projection,
    tracking both loan and investment balances over time.

    Attributes:
        year (int): Year number (1-indexed, relative to start of projection)
        loan_balance (Decimal): Outstanding loan balance in GBP at year end
        investment_value (Decimal): Investment portfolio value in GBP at year end
        annual_repayment (Decimal): Total loan repayment made this year in GBP
        interest_accrued (Decimal): Loan interest charged this year in GBP
        investment_growth (Decimal): Investment returns earned this year in GBP
    """

    year: int
    loan_balance: Decimal
    investment_value: Decimal
    annual_repayment: Decimal
    interest_accrued: Decimal
    investment_growth: Decimal


@dataclass
class ScenarioProjection:
    """
    Multi-year financial projection for a single economic scenario.

    Contains year-by-year loan and investment values under one set of
    assumptions (optimistic/realistic/pessimistic). Used to compare
    final outcomes across different economic conditions.

    Attributes:
        scenario_type (ScenarioType): Which scenario this represents
        investment_growth_rate (Decimal): Annual return rate as decimal
        loan_interest_rate (Decimal): Annual loan interest rate as decimal
        yearly_data (list[YearlyProjection]): Year-by-year financial snapshots
        total_loan_cost (Decimal): Sum of all interest paid over projection period
        final_investment_value (Decimal): Investment value at end of projection
    """

    scenario_type: ScenarioType
    investment_growth_rate: Decimal
    loan_interest_rate: Decimal
    yearly_data: list[YearlyProjection]
    total_loan_cost: Decimal
    final_investment_value: Decimal
    crossover_year: int | None
    net_benefit: Decimal


@dataclass
class PayoffRecommendation:
    """
    Decision output with actionable financial advice.

    Analyzes the three scenario projections to recommend whether
    the user should pay off their loan early or invest the money.
    Includes confidence level and plain-language reasoning.

    Attributes:
        decision (str): "pay_off_early", "invest", or "neutral"
        confidence (str): "high", "medium", or "low" based on scenario variance
        rationale (str): Plain-language explanation of the recommendation
        net_benefit_amount (Decimal): Expected benefit in GBP (positive = invest wins)
        crossover_year (int | None): Year when investment surpasses loan cost (if applicable)
    """

    decision: str  # "pay_off_early", "invest", "neutral"
    confidence: str  # "high", "medium", "low"
    rationale: str  # Plain-language explanation
    net_benefit_amount: Decimal  # Positive = invest wins, negative = pay off wins
    crossover_year: int | None  # Year when investment surpasses loan cost


@dataclass
class CalculationResult:
    """
    Complete calculation output containing all scenarios and final recommendation.

    Aggregates the three economic scenarios (optimistic/realistic/pessimistic)
    and provides a single recommendation based on the most likely outcome.
    This is the top-level response object returned to the client.

    Attributes:
        optimistic (ScenarioProjection): Best-case scenario projection
        pessimistic (ScenarioProjection): Worst-case scenario projection
        realistic (ScenarioProjection): Most likely scenario projection
        recommendation (PayoffRecommendation): Final decision with rationale
    """

    optimistic: ScenarioProjection
    pessimistic: ScenarioProjection
    realistic: ScenarioProjection
    recommendation: PayoffRecommendation
    calculated_at: datetime
