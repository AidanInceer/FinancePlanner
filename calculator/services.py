"""
Business logic for UK Plan 2 student loan payoff calculations.

This module implements the core calculation engine that powers the Student Loan
Payoff Calculator. It compares two financial strategies:
- Strategy A: Make minimum loan repayments and invest surplus income
- Strategy B: Make accelerated loan repayments to pay off debt faster

Key Functions:
    calculate_payoff_scenarios(): Main entry point that orchestrates
        calculation
    project_scenario(): Project loan/investment over multiple years
        per scenario
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
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

from .models import (
    BandBreakdown,
    CalculationResult,
    CalculatorInput,
    DeductionBreakdown,
    EmergencyFundInput,
    EmergencyFundResult,
    IncomeTaxCalculationResult,
    NetPaySummary,
    PayoffRecommendation,
    RentVsBuyInput,
    RentVsBuyResult,
    ResilienceScoreInput,
    ResilienceScoreResult,
    ScenarioProjection,
    ScenarioType,
    TaxCalculationInput,
    TimeToFreedomInput,
    TimeToFreedomResult,
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


def get_tax_year_config(config: dict, tax_year: str) -> dict:
    """
    Get tax year configuration for income tax calculations.

    Args:
        config: Full tax config dictionary
        tax_year: Tax year key (e.g., "2025-26")

    Returns:
        Tax year configuration dict
    """
    tax_years = config.get("tax_years", {})
    if tax_year not in tax_years:
        raise ValueError(f"Unsupported tax year: {tax_year}")
    return tax_years[tax_year]


def quantize_money(value: Decimal) -> Decimal:
    """Quantize money values to 2 decimal places."""
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def serialize_decimal(value: Decimal, places: str = "0.01") -> float:
    """Serialize Decimal to float with given precision."""
    return float(value.quantize(Decimal(places), rounding=ROUND_HALF_UP))


def serialize_series(series: list[dict]) -> list[dict]:
    """Serialize list of dicts containing Decimal values to floats."""
    serialized = []
    for item in series:
        converted = {}
        for key, value in item.items():
            if isinstance(value, Decimal):
                converted[key] = serialize_decimal(value)
            else:
                converted[key] = value
        serialized.append(converted)
    return serialized


def annualize_income(gross_income: Decimal, pay_frequency: str) -> Decimal:
    """
    Convert income to annual amount based on pay frequency.
    """
    if pay_frequency == "annual":
        return gross_income
    if pay_frequency == "monthly":
        return gross_income * Decimal("12")
    if pay_frequency == "weekly":
        return gross_income * Decimal("52")
    raise ValueError("Invalid pay frequency")


def calculate_pension_deduction(
    gross_annual: Decimal,
    contribution_type: str,
    contribution_value: Decimal,
) -> Decimal:
    """
    Calculate pension contribution deduction from gross income.
    """
    if contribution_type == "none":
        return Decimal("0")
    if contribution_type == "percentage":
        return gross_annual * (contribution_value / Decimal("100"))
    if contribution_type == "amount":
        return contribution_value
    raise ValueError("Invalid pension contribution type")


def calculate_personal_allowance(
    adjusted_income: Decimal,
    tax_config: dict,
) -> Decimal:
    """
    Calculate personal allowance using taper rules.
    """
    allowance = Decimal(str(tax_config["personal_allowance"]))
    taper_start = Decimal(str(tax_config["personal_allowance_taper_start"]))
    taper_end = Decimal(str(tax_config["personal_allowance_taper_end"]))

    if adjusted_income <= taper_start:
        return allowance

    if adjusted_income >= taper_end:
        return Decimal("0")

    reduction = (adjusted_income - taper_start) / Decimal("2")
    reduced_allowance = allowance - reduction
    return max(Decimal("0"), reduced_allowance)


def calculate_income_tax(
    taxable_income: Decimal,
    bands: list[dict],
) -> tuple[Decimal, list[BandBreakdown]]:
    """
    Calculate income tax using band definitions.
    """
    total_tax = Decimal("0")
    breakdowns: list[BandBreakdown] = []

    for band in bands:
        band_from = Decimal(str(band["from"]))
        band_to = band["to"]
        band_rate = Decimal(str(band["rate"]))

        if band_to is None:
            taxable_amount = max(Decimal("0"), taxable_income - band_from)
        else:
            band_to_decimal = Decimal(str(band_to))
            taxable_amount = max(Decimal("0"), min(taxable_income, band_to_decimal) - band_from)

        tax_amount = taxable_amount * band_rate
        total_tax += tax_amount

        breakdowns.append(
            BandBreakdown(
                band_name=band["name"],
                rate=band_rate,
                from_amount=band_from,
                to_amount=(Decimal(str(band_to)) if band_to is not None else None),
                taxable_amount=taxable_amount,
                amount=tax_amount,
            )
        )

    return total_tax, breakdowns


def calculate_ni_contributions(
    adjusted_income: Decimal,
    ni_config: dict,
    ni_category: str,
) -> tuple[Decimal, list[BandBreakdown]]:
    """
    Calculate National Insurance contributions for employee.
    """
    thresholds = ni_config["thresholds"]
    pt = Decimal(str(thresholds["pt"]))
    uel = Decimal(str(thresholds["uel"]))

    category_rates = ni_config["categories"].get(ni_category)
    if not category_rates:
        raise ValueError("Unsupported NI category")

    main_rate = Decimal(str(category_rates["main_rate"]))
    upper_rate = Decimal(str(category_rates["upper_rate"]))

    main_band = max(Decimal("0"), min(adjusted_income, uel) - pt)
    upper_band = max(Decimal("0"), adjusted_income - uel)

    main_amount = main_band * main_rate
    upper_amount = upper_band * upper_rate
    total = main_amount + upper_amount

    breakdowns = [
        BandBreakdown(
            band_name="Main rate",
            rate=main_rate,
            from_amount=pt,
            to_amount=uel,
            taxable_amount=main_band,
            amount=main_amount,
        ),
        BandBreakdown(
            band_name="Upper rate",
            rate=upper_rate,
            from_amount=uel,
            to_amount=None,
            taxable_amount=upper_band,
            amount=upper_amount,
        ),
    ]

    return total, breakdowns


def calculate_student_loan(
    adjusted_income: Decimal,
    plans_config: dict,
    plan_key: str,
) -> Decimal:
    """
    Calculate student loan repayment.
    """
    plan = plans_config.get(plan_key)
    if not plan:
        raise ValueError("Unsupported student loan plan")

    threshold = Decimal(str(plan["threshold"]))
    rate = Decimal(str(plan["rate"]))

    if rate == 0:
        return Decimal("0")

    if adjusted_income <= threshold:
        return Decimal("0")

    return (adjusted_income - threshold) * rate


def calculate_income_tax_result(
    calc_input: TaxCalculationInput,
) -> IncomeTaxCalculationResult:
    """
    Calculate UK income tax, NI, and student loan deductions.
    """
    config = load_uk_tax_config()
    tax_config = get_tax_year_config(config, calc_input.tax_year)

    base_gross_annual = annualize_income(
        calc_input.gross_income,
        calc_input.pay_frequency,
    )
    gross_annual = base_gross_annual + calc_input.bonus_annual

    pension_deduction = calculate_pension_deduction(
        gross_annual,
        calc_input.pension_contribution_type,
        calc_input.pension_contribution_value,
    )
    pretax_total = pension_deduction + calc_input.other_pretax_deductions
    if pretax_total > gross_annual:
        raise ValueError("Pre-tax deductions cannot exceed gross income")
    adjusted_income = max(Decimal("0"), gross_annual - pretax_total)

    personal_allowance = calculate_personal_allowance(
        adjusted_income,
        tax_config,
    )
    taxable_income = max(Decimal("0"), adjusted_income - personal_allowance)

    bands = tax_config["income_tax_bands"][calc_input.tax_jurisdiction]
    income_tax_total, income_tax_bands = calculate_income_tax(
        taxable_income,
        bands,
    )

    ni_income_base = gross_annual
    ni_total, ni_bands = calculate_ni_contributions(
        ni_income_base,
        tax_config["ni"],
        calc_input.ni_category,
    )

    student_loan_total = calculate_student_loan(
        adjusted_income,
        tax_config["student_loan_plans"],
        calc_input.student_loan_plan,
    )

    total_deductions = pretax_total + income_tax_total + ni_total + student_loan_total
    net_annual = gross_annual - total_deductions

    net_monthly = net_annual / Decimal("12")
    net_weekly = net_annual / Decimal("52")

    effective_rate = total_deductions / gross_annual if gross_annual > 0 else Decimal("0")

    deductions = DeductionBreakdown(
        taxable_income=taxable_income,
        income_tax_total=income_tax_total,
        income_tax_bands=income_tax_bands,
        ni_total=ni_total,
        ni_bands=ni_bands,
        student_loan_total=student_loan_total,
        total_deductions=total_deductions,
        effective_deduction_rate=effective_rate,
    )

    net_pay = NetPaySummary(
        gross_annual=gross_annual,
        net_annual=net_annual,
        net_monthly=net_monthly,
        net_weekly=net_weekly,
    )

    return IncomeTaxCalculationResult(
        tax_year=calc_input.tax_year,
        deductions=deductions,
        net_pay=net_pay,
    )


def serialize_income_tax_result(result: IncomeTaxCalculationResult) -> dict:
    """Serialize income tax result to JSON-friendly dict."""
    return {
        "tax_year": result.tax_year,
        "gross_annual": float(quantize_money(result.net_pay.gross_annual)),
        "taxable_annual": float(quantize_money(result.deductions.taxable_income)),
        "income_tax_annual": float(quantize_money(result.deductions.income_tax_total)),
        "ni_annual": float(quantize_money(result.deductions.ni_total)),
        "student_loan_annual": float(quantize_money(result.deductions.student_loan_total)),
        "total_deductions_annual": float(quantize_money(result.deductions.total_deductions)),
        "net_annual": float(quantize_money(result.net_pay.net_annual)),
        "net_monthly": float(quantize_money(result.net_pay.net_monthly)),
        "net_weekly": float(quantize_money(result.net_pay.net_weekly)),
        "effective_deduction_rate": float(result.deductions.effective_deduction_rate),
        "income_tax_bands": [
            {
                "band_name": band.band_name,
                "rate": float(band.rate),
                "from": float(band.from_amount),
                "to": (float(band.to_amount) if band.to_amount is not None else None),
                "taxable_amount": float(quantize_money(band.taxable_amount)),
                "amount": float(quantize_money(band.amount)),
            }
            for band in result.deductions.income_tax_bands
        ],
        "ni_bands": [
            {
                "band_name": band.band_name,
                "rate": float(band.rate),
                "from": float(band.from_amount),
                "to": (float(band.to_amount) if band.to_amount is not None else None),
                "taxable_amount": float(quantize_money(band.taxable_amount)),
                "amount": float(quantize_money(band.amount)),
            }
            for band in result.deductions.ni_bands
        ],
    }


def calculate_rent_vs_buy(calc_input: RentVsBuyInput) -> RentVsBuyResult:
    """Calculate rent vs buy outcomes and return summary data."""
    mortgage_principal = calc_input.property_price - calc_input.deposit_amount
    monthly_rate = calc_input.mortgage_rate / Decimal("12")
    total_months = calc_input.mortgage_term_years * 12

    if monthly_rate == 0:
        monthly_payment = (
            mortgage_principal / Decimal(total_months) if total_months > 0 else Decimal("0")
        )
    else:
        monthly_payment = mortgage_principal * (
            monthly_rate / (Decimal("1") - (Decimal("1") + monthly_rate) ** (-total_months))
        )

    rent_total = Decimal("0")
    buy_total = calc_input.buying_costs

    home_value = calc_input.property_price
    mortgage_balance = mortgage_principal
    rent_annual = calc_input.monthly_rent * Decimal("12")

    investment_balance = calc_input.deposit_amount + calc_input.buying_costs

    series: list[dict] = []
    break_even_year = None

    for year in range(1, calc_input.analysis_years + 1):
        annual_interest = Decimal("0")
        annual_principal = Decimal("0")

        for _ in range(12):
            if mortgage_balance <= 0:
                break
            interest = mortgage_balance * monthly_rate
            principal_payment = monthly_payment - interest
            if principal_payment < 0:
                principal_payment = Decimal("0")
            mortgage_balance = max(Decimal("0"), mortgage_balance - principal_payment)
            annual_interest += interest
            annual_principal += principal_payment

        maintenance_cost = home_value * calc_input.maintenance_rate
        property_tax_cost = home_value * calc_input.property_tax_rate
        insurance_cost = calc_input.insurance_annual

        annual_buy_cost = (
            (monthly_payment * Decimal("12"))
            + maintenance_cost
            + property_tax_cost
            + insurance_cost
        )
        buy_total += annual_buy_cost
        rent_total += rent_annual

        if annual_buy_cost > rent_annual:
            investment_balance += annual_buy_cost - rent_annual

        investment_balance = investment_balance * (Decimal("1") + calc_input.investment_return_rate)

        home_value = home_value * (Decimal("1") + calc_input.home_appreciation_rate)

        net_worth_buy = home_value - mortgage_balance - calc_input.selling_costs
        net_worth_rent = investment_balance

        if break_even_year is None and net_worth_buy >= net_worth_rent:
            break_even_year = year

        series.append(
            {
                "year": year,
                "rent_value": net_worth_rent,
                "buy_value": net_worth_buy,
            }
        )

        rent_annual = rent_annual * (Decimal("1") + calc_input.rent_growth_rate)

    buy_total += calc_input.selling_costs

    final_rent = series[-1]["rent_value"] if series else investment_balance
    final_buy = series[-1]["buy_value"] if series else home_value - mortgage_balance

    if final_buy > final_rent:
        summary = "Buying is projected to build more net worth over the analysis period."
    elif final_buy < final_rent:
        summary = "Renting is projected to build more net worth over the analysis period."
    else:
        summary = "Renting and buying are projected to be broadly similar over the analysis period."

    return RentVsBuyResult(
        total_cost_rent=rent_total,
        total_cost_buy=buy_total,
        net_worth_rent=final_rent,
        net_worth_buy=final_buy,
        break_even_year=break_even_year,
        summary=summary,
        graph_series=series,
    )


def serialize_rent_vs_buy_result(result: RentVsBuyResult) -> dict:
    return {
        "total_cost_rent": serialize_decimal(quantize_money(result.total_cost_rent)),
        "total_cost_buy": serialize_decimal(quantize_money(result.total_cost_buy)),
        "net_worth_rent": serialize_decimal(quantize_money(result.net_worth_rent)),
        "net_worth_buy": serialize_decimal(quantize_money(result.net_worth_buy)),
        "break_even_year": result.break_even_year,
        "summary": result.summary,
        "graph_series": serialize_series(result.graph_series),
    }


def calculate_emergency_fund(calc_input: EmergencyFundInput) -> EmergencyFundResult:
    target_fund = calc_input.monthly_expenses * Decimal(calc_input.target_months)
    savings_gap = max(Decimal("0"), target_fund - calc_input.current_savings)
    if calc_input.monthly_expenses > 0:
        coverage = calc_input.current_savings / calc_input.monthly_expenses
    else:
        coverage = None

    return EmergencyFundResult(
        target_fund=target_fund,
        savings_gap=savings_gap,
        coverage_months=coverage,
    )


def serialize_emergency_fund_result(result: EmergencyFundResult) -> dict:
    return {
        "target_fund": serialize_decimal(quantize_money(result.target_fund)),
        "savings_gap": serialize_decimal(quantize_money(result.savings_gap)),
        "coverage_months": float(result.coverage_months)
        if result.coverage_months is not None
        else None,
    }


def calculate_resilience_score(calc_input: ResilienceScoreInput) -> ResilienceScoreResult:
    savings_score = Decimal("100")
    if calc_input.debt_load > 0:
        ratio = calc_input.savings / calc_input.debt_load
        savings_score = min(Decimal("100"), max(Decimal("0"), ratio * Decimal("100")))

    debt_score = Decimal("100")
    if calc_input.debt_load > 0:
        debt_score = max(
            Decimal("0"),
            Decimal("100")
            - (calc_input.debt_load / (calc_input.savings + Decimal("1")) * Decimal("100")),
        )

    index = (
        savings_score * Decimal("0.3")
        + Decimal(calc_input.income_stability) * Decimal("0.3")
        + debt_score * Decimal("0.2")
        + Decimal(calc_input.insurance_coverage) * Decimal("0.2")
    )
    resilience_index = int(index.quantize(Decimal("1"), rounding=ROUND_HALF_UP))

    weak_points = []
    if savings_score < 50:
        weak_points.append("Low savings buffer")
    if calc_input.income_stability < 50:
        weak_points.append("Income stability risk")
    if debt_score < 50:
        weak_points.append("High debt load")
    if calc_input.insurance_coverage < 50:
        weak_points.append("Low insurance coverage")

    if weak_points:
        summary = "Focus on the highlighted weak points to improve resilience."
    else:
        summary = "Your resilience profile looks balanced across the key factors."

    return ResilienceScoreResult(
        resilience_index=resilience_index,
        weak_points=weak_points,
        summary=summary,
    )


def serialize_resilience_score_result(result: ResilienceScoreResult) -> dict:
    return {
        "resilience_index": result.resilience_index,
        "weak_points": result.weak_points,
        "summary": result.summary,
    }


def calculate_time_to_freedom(calc_input: TimeToFreedomInput) -> TimeToFreedomResult:
    if calc_input.safe_withdrawal_rate == 0:
        freedom_number = Decimal("0")
    else:
        freedom_number = calc_input.annual_expenses / calc_input.safe_withdrawal_rate

    portfolio = calc_input.current_investments
    timeline = []
    years_to_freedom = None
    max_years = 60

    for year in range(1, max_years + 1):
        portfolio = (portfolio + calc_input.annual_contribution) * (
            Decimal("1") + calc_input.investment_return_rate
        )
        timeline.append({"year": year, "portfolio_value": portfolio})
        if years_to_freedom is None and portfolio >= freedom_number:
            years_to_freedom = year

    if years_to_freedom is not None:
        summary = (
            f"At this pace you could reach financial freedom in about {years_to_freedom} years."
        )
    else:
        summary = "At this pace you may need to increase contributions or returns to reach freedom."

    return TimeToFreedomResult(
        freedom_number=freedom_number,
        years_to_freedom=years_to_freedom,
        timeline_series=timeline,
        summary=summary,
    )


def serialize_time_to_freedom_result(result: TimeToFreedomResult) -> dict:
    return {
        "freedom_number": serialize_decimal(quantize_money(result.freedom_number)),
        "years_to_freedom": result.years_to_freedom,
        "timeline_series": serialize_series(result.timeline_series),
        "summary": result.summary,
    }


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
        scenario_type: Which scenario to project
            (optimistic, pessimistic, realistic)

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
            "The financial difference between paying off early "
            "and investing is minimal (less than 2% of your total loan cost). "
            "Either strategy works well. Consider your risk tolerance "
            "and liquidity needs."
        )
    elif realistic_benefit > 0:
        decision = "invest"
        savings_pct = (realistic_benefit / realistic.total_loan_cost * Decimal("100")).quantize(
            Decimal("0.1")
        )
        rationale = (
            "Investing is the better strategy. You could save approximately "
            f"£{realistic_benefit:,.0f} "
            f"({savings_pct}% of your total loan cost) "
            "by investing rather than paying off early. "
            "Your investment returns are projected to outpace "
            "your loan interest costs."
        )
    else:
        decision = "pay_off_early"
        savings_pct = (
            abs(realistic_benefit) / realistic.total_loan_cost * Decimal("100")
        ).quantize(Decimal("0.1"))
        rationale = (
            "Paying off your loan early is the better strategy. "
            "You could save approximately "
            f"£{abs(realistic_benefit):,.0f} "
            f"({savings_pct}% of your total loan cost) "
            "by paying off early rather than investing. "
            "Your loan interest costs exceed projected investment returns."
        )

    # Add confidence qualifier to rationale
    if confidence == "low":
        rationale += (
            " However, there is significant uncertainty in these projections "
            "due to variable market conditions and interest rates."
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


def calculate_payoff_scenarios(
    calc_input: CalculatorInput,
) -> CalculationResult:
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
        error_list = ", ".join(errors)
        logger.warning(f"Input validation failed: {error_list}")
        raise ValueError(f"Invalid input: {error_list}")

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
        recommendation = generate_recommendation(
            optimistic,
            pessimistic,
            realistic,
        )

        logger.info(
            "Calculation completed successfully. Recommendation: " f"{recommendation.decision}"
        )

        return CalculationResult(
            optimistic=optimistic,
            pessimistic=pessimistic,
            realistic=realistic,
            recommendation=recommendation,
            calculated_at=datetime.now(),
        )
    except Exception as e:
        logger.error(
            f"Calculation failed: {type(e).__name__}: {e}",
            exc_info=True,
        )
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
