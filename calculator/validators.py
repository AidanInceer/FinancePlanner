"""
Input validation logic for calculator form submissions.

This module provides validation functions for all user inputs to the
Student Loan Payoff Calculator. Each validator follows a consistent pattern:
- Takes raw input value (any type)
- Returns tuple of (is_valid: bool, error_message: str)
- Returns ("", True) if valid, (error_message, False) if invalid

Validation Functions:
    validate_age(): Age must be 18-100
    validate_year(): Year must be 1980-2040 (configurable range)
    validate_percentage(): Percentage must be 0-20% (for interest/return rates)
    validate_non_negative_decimal(): Value must be >= 0 (for amounts)
    validate_positive_integer(): Value must be > 0 (for durations)
    validate_rate_range(): Custom rate range validation (for percentage inputs)

All validators handle type coercion, None values, and invalid formats gracefully.
Used by both client-side JavaScript validation and server-side API validation.
"""

from decimal import Decimal, InvalidOperation


def validate_age(value: int) -> tuple[bool, str]:
    """
    Validate age is between 18 and 100.

    Args:
        value: Age to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        age = int(value)
        if 18 <= age <= 100:
            return True, ""
        return False, "Age must be between 18 and 100"
    except (ValueError, TypeError):
        return False, "Age must be a valid number"


def validate_year(value: int, min_year: int = 1980, max_year: int = 2040) -> tuple[bool, str]:
    """
    Validate year is within acceptable range.

    Args:
        value: Year to validate
        min_year: Minimum acceptable year
        max_year: Maximum acceptable year

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        year = int(value)
        if min_year <= year <= max_year:
            return True, ""
        return False, f"Year must be between {min_year} and {max_year}"
    except (ValueError, TypeError):
        return False, "Year must be a valid number"


def validate_percentage(
    value: float | Decimal, min_rate: float = 0.0, max_rate: float = 20.0
) -> tuple[bool, str]:
    """
    Validate percentage is within acceptable range.

    Args:
        value: Percentage to validate (as decimal, e.g., 5.0 for 5%)
        min_rate: Minimum acceptable rate
        max_rate: Maximum acceptable rate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        rate = float(value)
        if min_rate <= rate <= max_rate:
            return True, ""
        return False, f"Percentage must be between {min_rate}% and {max_rate}%"
    except (ValueError, TypeError, InvalidOperation):
        return False, "Percentage must be a valid number"


def validate_non_negative_decimal(value: Decimal | float) -> tuple[bool, str]:
    """
    Validate value is non-negative.

    Args:
        value: Value to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        decimal_value = Decimal(str(value))
        if decimal_value >= 0:
            return True, ""
        return False, "Value cannot be negative"
    except (ValueError, TypeError, InvalidOperation):
        return False, "Value must be a valid number"


def validate_positive_integer(
    value: int, min_value: int = 1, max_value: int = 50
) -> tuple[bool, str]:
    """
    Validate integer is positive and within range.

    Args:
        value: Integer to validate
        min_value: Minimum acceptable value
        max_value: Maximum acceptable value

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        int_value = int(value)
        if min_value <= int_value <= max_value:
            return True, ""
        return False, f"Value must be between {min_value} and {max_value}"
    except (ValueError, TypeError):
        return False, "Value must be a valid number"


def validate_rate_range(low: float, current: float, high: float) -> tuple[bool, str]:
    """
    Validate that low <= current <= high for interest rates.

    Args:
        low: Low rate estimate
        current: Current rate
        high: High rate estimate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        if low <= current <= high:
            return True, ""
        return (
            False,
            f"Current rate ({current}%) must be between low ({low}%) and high ({high}%)",
        )
    except (ValueError, TypeError):
        return False, "Rates must be valid numbers"


def validate_pay_frequency(value: str) -> tuple[bool, str]:
    """
    Validate pay frequency.

    Args:
        value: Pay frequency string

    Returns:
        Tuple of (is_valid, error_message)
    """
    valid = {"annual", "monthly", "weekly"}
    if value in valid:
        return True, ""
    return False, "Pay frequency must be annual, monthly, or weekly"


def validate_tax_jurisdiction(value: str) -> tuple[bool, str]:
    """
    Validate UK tax jurisdiction selection.
    """
    valid = {"england_wales_ni", "scotland"}
    if value in valid:
        return True, ""
    return False, "Tax jurisdiction must be england_wales_ni or scotland"


def validate_ni_category(value: str) -> tuple[bool, str]:
    """
    Validate National Insurance category.
    """
    valid = {"A", "B", "C", "H", "J", "M", "Z"}
    if value in valid:
        return True, ""
    return False, "NI category must be one of A, B, C, H, J, M, Z"


def validate_student_loan_plan(value: str) -> tuple[bool, str]:
    """
    Validate student loan plan selection.
    """
    valid = {"none", "plan_1", "plan_2", "plan_4", "plan_5", "postgraduate"}
    if value in valid:
        return True, ""
    return False, "Student loan plan must be none, plan_1, plan_2, plan_4, plan_5, or postgraduate"


def validate_pension_contribution(
    contribution_type: str,
    contribution_value: Decimal | float,
) -> tuple[bool, str]:
    """
    Validate pension contribution inputs.
    """
    valid_types = {"none", "percentage", "amount"}
    if contribution_type not in valid_types:
        return False, "Pension contribution type must be none, percentage, or amount"

    if contribution_type == "none":
        return True, ""

    try:
        value = Decimal(str(contribution_value))
    except (ValueError, TypeError, InvalidOperation):
        return False, "Pension contribution must be a valid number"

    if value < 0:
        return False, "Pension contribution cannot be negative"

    if contribution_type == "percentage" and value > 100:
        return False, "Pension contribution percentage cannot exceed 100"

    return True, ""


def validate_rate_decimal(
    value: Decimal | float,
    min_rate: float = 0.0,
    max_rate: float = 1.0,
) -> tuple[bool, str]:
    """
    Validate a decimal rate between 0 and 1 (inclusive).
    """
    try:
        rate = float(value)
        if min_rate <= rate <= max_rate:
            return True, ""
        return False, f"Rate must be between {min_rate} and {max_rate}"
    except (ValueError, TypeError, InvalidOperation):
        return False, "Rate must be a valid number"


def validate_score_percent(value: int | float) -> tuple[bool, str]:
    """
    Validate a score between 0 and 100.
    """
    try:
        score = float(value)
        if 0 <= score <= 100:
            return True, ""
        return False, "Score must be between 0 and 100"
    except (ValueError, TypeError):
        return False, "Score must be a valid number"
