"""Unit tests for Calculator data models."""

from decimal import Decimal

from calculator.models import CalculatorInput, ScenarioType


class TestCalculatorInput:
    """Tests for CalculatorInput data class."""

    def test_calculator_input_creation(self):
        """Test creating a CalculatorInput instance."""
        calc_input = CalculatorInput(
            age=25,
            graduation_year=2023,
            current_year=2024,
            loan_duration_years=35,
            investment_amount=Decimal("50000.00"),
            investment_growth_high=Decimal("8.0"),
            investment_growth_low=Decimal("4.0"),
            investment_growth_average=Decimal("6.0"),
            investment_amount_growth=Decimal("0.0"),
            pre_tax_income=Decimal("45000.00"),
            salary_growth_optimistic=Decimal("5.0"),
            salary_growth_pessimistic=Decimal("2.0"),
            initial_loan_balance=Decimal("2400.00"),
            loan_interest_current=Decimal("5.5"),
            loan_interest_high=Decimal("7.0"),
            loan_interest_low=Decimal("3.0"),
        )

        assert calc_input.age == 25
        assert calc_input.graduation_year == 2023
        assert calc_input.loan_duration_years == 35

    def test_loan_end_year_property(self):
        """Test loan_end_year computed property."""
        calc_input = CalculatorInput(
            age=25,
            graduation_year=2023,
            current_year=2024,
            loan_duration_years=35,
            investment_amount=Decimal("50000.00"),
            investment_growth_high=Decimal("8.0"),
            investment_growth_low=Decimal("4.0"),
            investment_growth_average=Decimal("6.0"),
            investment_amount_growth=Decimal("0.0"),
            pre_tax_income=Decimal("45000.00"),
            salary_growth_optimistic=Decimal("5.0"),
            salary_growth_pessimistic=Decimal("2.0"),
            initial_loan_balance=Decimal("2400.00"),
            loan_interest_current=Decimal("5.5"),
            loan_interest_high=Decimal("7.0"),
            loan_interest_low=Decimal("3.0"),
        )

        assert calc_input.loan_end_year == 2058  # 2023 + 35

    def test_validate_valid_input(self):
        """Test validation with all valid inputs."""
        calc_input = CalculatorInput(
            age=25,
            graduation_year=2023,
            current_year=2024,
            loan_duration_years=35,
            investment_amount=Decimal("50000.00"),
            investment_growth_high=Decimal("8.0"),
            investment_growth_low=Decimal("4.0"),
            investment_growth_average=Decimal("6.0"),
            investment_amount_growth=Decimal("0.0"),
            pre_tax_income=Decimal("45000.00"),
            salary_growth_optimistic=Decimal("5.0"),
            salary_growth_pessimistic=Decimal("2.0"),
            initial_loan_balance=Decimal("2400.00"),
            loan_interest_current=Decimal("5.5"),
            loan_interest_high=Decimal("7.0"),
            loan_interest_low=Decimal("3.0"),
        )

        errors = calc_input.validate()
        assert len(errors) == 0

    def test_validate_age_too_low(self):
        """Test validation fails when age is too low."""
        calc_input = CalculatorInput(
            age=15,  # Too young
            graduation_year=2023,
            current_year=2024,
            loan_duration_years=35,
            investment_amount=Decimal("50000.00"),
            investment_growth_high=Decimal("8.0"),
            investment_growth_low=Decimal("4.0"),
            investment_growth_average=Decimal("6.0"),
            investment_amount_growth=Decimal("0.0"),
            pre_tax_income=Decimal("45000.00"),
            salary_growth_optimistic=Decimal("5.0"),
            salary_growth_pessimistic=Decimal("2.0"),
            initial_loan_balance=Decimal("2400.00"),
            loan_interest_current=Decimal("5.5"),
            loan_interest_high=Decimal("7.0"),
            loan_interest_low=Decimal("3.0"),
        )

        errors = calc_input.validate()
        assert any("Age must be between 18 and 100" in error for error in errors)

    def test_validate_investment_growth_inverted(self):
        """Test validation fails when investment growth low > high."""
        calc_input = CalculatorInput(
            age=25,
            graduation_year=2023,
            current_year=2024,
            loan_duration_years=35,
            investment_amount=Decimal("50000.00"),
            investment_growth_high=Decimal("4.0"),  # Lower than low
            investment_growth_low=Decimal("8.0"),  # Higher than high
            investment_growth_average=Decimal("6.0"),
            investment_amount_growth=Decimal("0.0"),
            pre_tax_income=Decimal("45000.00"),
            salary_growth_optimistic=Decimal("5.0"),
            salary_growth_pessimistic=Decimal("2.0"),
            initial_loan_balance=Decimal("2400.00"),
            loan_interest_current=Decimal("5.5"),
            loan_interest_high=Decimal("7.0"),
            loan_interest_low=Decimal("3.0"),
        )

        errors = calc_input.validate()
        assert any("cannot exceed high" in error for error in errors)

    def test_validate_loan_interest_out_of_range(self):
        """Test validation fails when current interest rate is outside low/high range."""
        calc_input = CalculatorInput(
            age=25,
            graduation_year=2023,
            current_year=2024,
            loan_duration_years=35,
            investment_amount=Decimal("50000.00"),
            investment_growth_high=Decimal("8.0"),
            investment_growth_low=Decimal("4.0"),
            investment_growth_average=Decimal("6.0"),
            investment_amount_growth=Decimal("0.0"),
            pre_tax_income=Decimal("45000.00"),
            salary_growth_optimistic=Decimal("5.0"),
            salary_growth_pessimistic=Decimal("2.0"),
            initial_loan_balance=Decimal("2400.00"),
            loan_interest_current=Decimal("10.0"),  # Outside range
            loan_interest_high=Decimal("7.0"),
            loan_interest_low=Decimal("3.0"),
        )

        errors = calc_input.validate()
        assert any("must be between low" in error for error in errors)

    def test_validate_negative_values(self):
        """Test validation fails with negative values."""
        calc_input = CalculatorInput(
            age=25,
            graduation_year=2023,
            current_year=2024,
            loan_duration_years=35,
            investment_amount=Decimal("-1000.00"),  # Negative
            investment_growth_high=Decimal("8.0"),
            investment_growth_low=Decimal("4.0"),
            investment_growth_average=Decimal("6.0"),
            investment_amount_growth=Decimal("0.0"),
            pre_tax_income=Decimal("45000.00"),
            salary_growth_optimistic=Decimal("5.0"),
            salary_growth_pessimistic=Decimal("2.0"),
            initial_loan_balance=Decimal("2400.00"),
            loan_interest_current=Decimal("5.5"),
            loan_interest_high=Decimal("7.0"),
            loan_interest_low=Decimal("3.0"),
        )

        errors = calc_input.validate()
        assert any("cannot be negative" in error for error in errors)


class TestScenarioType:
    """Tests for ScenarioType enum."""

    def test_scenario_type_values(self):
        """Test ScenarioType enum has correct values."""
        assert ScenarioType.OPTIMISTIC.value == "optimistic"
        assert ScenarioType.PESSIMISTIC.value == "pessimistic"
        assert ScenarioType.REALISTIC.value == "realistic"
