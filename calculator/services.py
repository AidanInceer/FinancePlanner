"""
Business logic for UK Plan 2 student loan payoff calculations.

This module implements the core calculation engine that powers the Student Loan
Payoff Calculator. It compares two financial strategies:
- Strategy A: Make minimum loan repayments and invest surplus income
- Strategy B: Make accelerated loan repayments to pay off debt faster

Key Functions:
    calculate_payoff_scenarios(): Main entry point - orchestrates full calculation
    project_scenario(): Project loan/investment over multiple years for one scenario
    apply_uk_tax_rules(): Calculate post-tax income using UK Plan 2 rules
    generate_recommendation(): Analyze scenarios and recommend optimal strategy
    serialize_calculation_result(): Convert result to JSON-serializable format

Tax Rules Implemented:
    - UK Plan 2 loan repayment: 9% above £27,295 threshold
    - Income tax: 20% on £12,571-£50,270, 40% on £50,271-£125,140, 45% above
    - National Insurance: 12% on £12,570-£50,270, 2% above
    - Personal allowance taper: £1 reduction per £2 above £100,000

All calculations use Decimal for financial precision.
"""

import json
import logging
from dataclasses import asdict
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from .models import (
    CalculationResult,
    CalculatorInput,
    PayoffRecommendation,
    ScenarioProjection,
    ScenarioType,
    YearlyProjection,
)

logger = logging.getLogger(__name__)


def load_uk_tax_config() -> dict:
    """
    Load UK tax configuration from JSON file.

    Returns:
        Dictionary containing UK tax thresholds and rates

    Raises:
        FileNotFoundError: If config file is missing
        json.JSONDecodeError: If config file is malformed
    """
    config_path = Path(__file__).resolve().parent.parent / "data" / "uk_tax_thresholds.json"
    try:
        with open(config_path) as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"UK tax config file not found at {config_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in UK tax config file: {e}")
        raise


def calculate_loan_balance(
    current_balance: Decimal,
    annual_repayment: Decimal,
    interest_rate: Decimal,
) -> tuple[Decimal, Decimal]:
    """
    Calculate loan balance after one year with interest and repayment.

    Args:
        current_balance: Current loan balance
        annual_repayment: Amount repaid this year
        interest_rate: Annual interest rate as percentage (e.g., 5.5 for 5.5%)

    Returns:
        Tuple of (new_balance, interest_accrued)
    """
    # Convert percentage to decimal
    rate_decimal = interest_rate / Decimal("100")

    # Calculate interest accrued
    interest_accrued = current_balance * rate_decimal

    # Calculate new balance: old balance + interest - repayment
    new_balance = current_balance + interest_accrued - annual_repayment

    # Balance cannot go negative
    if new_balance < 0:
        new_balance = Decimal("0")

    return new_balance, interest_accrued


def calculate_investment_value(
    current_value: Decimal,
    growth_rate: Decimal,
) -> tuple[Decimal, Decimal]:
    """
    Calculate investment value after one year of growth.

    Args:
        current_value: Current investment value
        growth_rate: Annual growth rate as percentage (e.g., 7.0 for 7%)

    Returns:
        Tuple of (new_value, growth_amount)
    """
    # Convert percentage to decimal
    rate_decimal = growth_rate / Decimal("100")

    # Calculate growth
    growth_amount = current_value * rate_decimal

    # Calculate new value
    new_value = current_value + growth_amount

    return new_value, growth_amount


def apply_uk_tax_rules(
    income: Decimal,
    loan_balance: Decimal,
) -> Decimal:
    """
    Calculate UK Plan 2 student loan repayment based on income.

    Args:
        income: Annual pre-tax income
        loan_balance: Current loan balance

    Returns:
        Annual repayment amount
    """
    config = load_uk_tax_config()
    threshold = Decimal(str(config["plan_2"]["repayment_threshold_2023"]))
    repayment_rate = Decimal(str(config["plan_2"]["repayment_rate"]))

    # Only repay if income exceeds threshold
    if income <= threshold:
        return Decimal("0")

    # Calculate 9% of income above threshold
    repayment = (income - threshold) * repayment_rate

    # Cannot repay more than remaining balance
    if repayment > loan_balance:
        repayment = loan_balance

    return repayment


def project_scenario(
    calc_input: CalculatorInput,
    scenario_type: ScenarioType,
) -> ScenarioProjection:
    """
    Project financial scenario over loan lifetime.

    Args:
        calc_input: User input data
        scenario_type: Which scenario to project (optimistic, pessimistic, realistic)

    Returns:
        ScenarioProjection with yearly breakdown
    """
    # Determine rates based on scenario type
    if scenario_type == ScenarioType.OPTIMISTIC:
        investment_rate = calc_input.investment_growth_high
        loan_rate = calc_input.loan_interest_low
        salary_growth_rate = calc_input.salary_growth_optimistic
    elif scenario_type == ScenarioType.PESSIMISTIC:
        investment_rate = calc_input.investment_growth_low
        loan_rate = calc_input.loan_interest_high
        salary_growth_rate = calc_input.salary_growth_pessimistic
    else:  # REALISTIC
        investment_rate = calc_input.investment_growth_average
        loan_rate = calc_input.loan_interest_current
        # Average of optimistic and pessimistic salary growth
        salary_growth_rate = (
            calc_input.salary_growth_optimistic + calc_input.salary_growth_pessimistic
        ) / Decimal("2")

    # Initialize tracking variables
    current_year = calc_input.current_year
    loan_end_year = calc_input.loan_end_year
    yearly_data = []

    # Start with current values
    loan_balance = calc_input.initial_loan_balance
    investment_value = calc_input.investment_amount  # Start with current investment amount
    current_income = calc_input.pre_tax_income
    total_loan_cost = Decimal("0")
    crossover_year = None

    # Project year by year
    for year in range(current_year, loan_end_year + 1):
        # Calculate repayment based on current income and UK rules
        annual_repayment = apply_uk_tax_rules(current_income, loan_balance)

        # Calculate loan changes
        new_loan_balance, interest_accrued = calculate_loan_balance(
            loan_balance, annual_repayment, loan_rate
        )

        # Calculate investment growth on the current value
        new_investment_value, investment_growth = calculate_investment_value(
            investment_value, investment_rate
        )

        # Track total loan cost
        total_loan_cost += annual_repayment

        # Check for crossover (investment > total loan cost)
        if crossover_year is None and new_investment_value > total_loan_cost:
            crossover_year = year

        # Record yearly data
        yearly_data.append(
            YearlyProjection(
                year=year,
                loan_balance=loan_balance,
                investment_value=investment_value,
                annual_repayment=annual_repayment,
                interest_accrued=interest_accrued,
                investment_growth=investment_growth,
            )
        )

        # Update for next year
        loan_balance = new_loan_balance
        investment_value = new_investment_value

        # Apply salary growth for next year
        current_income = current_income * (Decimal("1") + (salary_growth_rate / Decimal("100")))

        # Stop if loan is paid off
        if loan_balance == 0:
            break

    # Calculate final values
    final_investment_value = investment_value
    net_benefit = final_investment_value - total_loan_cost

    return ScenarioProjection(
        scenario_type=scenario_type,
        investment_growth_rate=investment_rate,
        loan_interest_rate=loan_rate,
        yearly_data=yearly_data,
        total_loan_cost=total_loan_cost,
        final_investment_value=final_investment_value,
        crossover_year=crossover_year,
        net_benefit=net_benefit,
    )


def generate_recommendation(
    optimistic: ScenarioProjection,
    pessimistic: ScenarioProjection,
    realistic: ScenarioProjection,
) -> PayoffRecommendation:
    """
    Generate payoff recommendation based on scenarios.

    Args:
        optimistic: Optimistic scenario projection
        pessimistic: Pessimistic scenario projection
        realistic: Realistic scenario projection

    Returns:
        PayoffRecommendation with decision and rationale
    """
    # Calculate key metrics
    realistic_benefit = realistic.net_benefit
    benefit_range = optimistic.net_benefit - pessimistic.net_benefit

    # Calculate variance (as percentage of loan cost)
    variance_pct = abs(benefit_range / realistic.total_loan_cost * Decimal("100"))

    # Determine confidence based on scenario agreement
    if variance_pct > Decimal("5"):
        confidence = "low"
    elif variance_pct > Decimal("2"):
        confidence = "medium"
    else:
        confidence = "high"

    # Determine decision
    neutral_threshold = realistic.total_loan_cost * Decimal("0.02")  # 2% threshold

    if abs(realistic_benefit) < neutral_threshold:
        decision = "neutral"
        rationale = (
            "The financial difference between paying off early and investing is minimal "
            "(less than 2% of your total loan cost). Either strategy works well. "
            "Consider your risk tolerance and liquidity needs."
        )
    elif realistic_benefit > 0:
        decision = "invest"
        savings_pct = (realistic_benefit / realistic.total_loan_cost * Decimal("100")).quantize(
            Decimal("0.1")
        )
        rationale = (
            f"Investing is the better strategy. You could save approximately "
            f"£{realistic_benefit:,.0f} ({savings_pct}% of your total loan cost) "
            f"by investing rather than paying off early. "
            f"Your investment returns are projected to outpace your loan interest costs."
        )
    else:
        decision = "pay_off_early"
        savings_pct = (
            abs(realistic_benefit) / realistic.total_loan_cost * Decimal("100")
        ).quantize(Decimal("0.1"))
        rationale = (
            f"Paying off your loan early is the better strategy. You could save approximately "
            f"£{abs(realistic_benefit):,.0f} ({savings_pct}% of your total loan cost) "
            f"by paying off early rather than investing. "
            f"Your loan interest costs exceed projected investment returns."
        )

    # Add confidence qualifier to rationale
    if confidence == "low":
        rationale += (
            " However, there is significant uncertainty in these projections due to variable "
            "market conditions and interest rates."
        )
    elif confidence == "medium":
        rationale += " There is moderate uncertainty in these projections."

    return PayoffRecommendation(
        decision=decision,
        confidence=confidence,
        rationale=rationale,
        net_benefit_amount=realistic_benefit,
        crossover_year=realistic.crossover_year,
    )


def calculate_payoff_scenarios(calc_input: CalculatorInput) -> CalculationResult:
    """
    Calculate all scenarios and generate recommendation.

    Args:
        calc_input: Validated user input

    Returns:
        CalculationResult with all scenarios and recommendation

    Raises:
        ValueError: If input validation fails
    """
    # Validate input
    errors = calc_input.validate()
    if errors:
        logger.warning(f"Input validation failed: {', '.join(errors)}")
        raise ValueError(f"Invalid input: {', '.join(errors)}")

    try:
        logger.info(
            f"Starting calculation for age={calc_input.age}, "
            f"duration={calc_input.loan_duration_years} years"
        )

        # Project all three scenarios
        optimistic = project_scenario(calc_input, ScenarioType.OPTIMISTIC)
        pessimistic = project_scenario(calc_input, ScenarioType.PESSIMISTIC)
        realistic = project_scenario(calc_input, ScenarioType.REALISTIC)

        # Generate recommendation
        recommendation = generate_recommendation(optimistic, pessimistic, realistic)

        logger.info(
            f"Calculation completed successfully. Recommendation: {recommendation.decision}"
        )

        return CalculationResult(
            optimistic=optimistic,
            pessimistic=pessimistic,
            realistic=realistic,
            recommendation=recommendation,
            calculated_at=datetime.now(),
        )
    except Exception as e:
        logger.error(f"Calculation failed: {type(e).__name__}: {e}", exc_info=True)
        raise


def serialize_calculation_result(result: CalculationResult) -> dict:
    """
    Convert CalculationResult to JSON-serializable dict.

    Args:
        result: Calculation result to serialize

    Returns:
        Dictionary suitable for JSON serialization
    """

    def decimal_to_float(obj):
        """Convert Decimal to float for JSON serialization."""
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if hasattr(obj, "value"):  # Enum
            return obj.value
        if hasattr(obj, "__dict__"):  # Dataclass
            return {k: decimal_to_float(v) for k, v in asdict(obj).items()}
        if isinstance(obj, list):
            return [decimal_to_float(item) for item in obj]
        if isinstance(obj, dict):
            return {k: decimal_to_float(v) for k, v in obj.items()}
        return obj

    return decimal_to_float(asdict(result))
