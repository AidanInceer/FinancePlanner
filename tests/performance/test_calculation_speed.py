"""Performance test for calculator service."""

import time
from decimal import Decimal

from calculator.models import CalculatorInput
from calculator.services import calculate_payoff_scenarios


def test_35_year_projection_performance():
    """Test that a 35-year projection completes in under 2 seconds."""
    # Create a calculator input for 35 years
    calc_input = CalculatorInput(
        age=23,
        graduation_year=2020,
        current_year=2024,
        loan_duration_years=35,
        investment_amount=Decimal("5000"),
        investment_growth_high=Decimal("8.0"),
        investment_growth_low=Decimal("3.0"),
        investment_growth_average=Decimal("6.0"),
        investment_amount_growth=Decimal("0.0"),
        pre_tax_income=Decimal("35000"),
        salary_growth_optimistic=Decimal("5.0"),
        salary_growth_pessimistic=Decimal("2.0"),
        initial_loan_balance=Decimal("2500"),
        loan_interest_current=Decimal("5.5"),
        loan_interest_high=Decimal("7.0"),
        loan_interest_low=Decimal("4.0"),
    )

    # Measure execution time
    start_time = time.perf_counter()
    result = calculate_payoff_scenarios(calc_input)
    end_time = time.perf_counter()

    execution_time = end_time - start_time
    print(f"\n35-year projection completed in {execution_time:.4f} seconds")

    # Verify result
    assert result is not None
    assert len(result.optimistic.yearly_data) > 0
    assert len(result.pessimistic.yearly_data) > 0
    assert len(result.realistic.yearly_data) > 0

    # Performance assertion: should complete in under 2 seconds
    assert execution_time < 2.0, f"Calculation took {execution_time:.4f}s (target: <2.0s)"

    print(f"✓ Performance target met ({execution_time:.4f}s < 2.0s)")


if __name__ == "__main__":
    import os
    import sys

    import django

    # Setup Django environment
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()

    # Run performance test
    test_35_year_projection_performance()
