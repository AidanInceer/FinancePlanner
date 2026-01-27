"""Unit tests for calculation services."""

from decimal import Decimal

import pytest

from calculator.models import CalculatorInput, ScenarioType
from calculator.services import (
    apply_uk_tax_rules,
    calculate_investment_value,
    calculate_loan_balance,
    calculate_payoff_scenarios,
    generate_recommendation,
    load_uk_tax_config,
    project_scenario,
    serialize_calculation_result,
)


class TestLoadUKTaxConfig:
    """Tests for load_uk_tax_config function."""

    def test_load_config_success(self):
        """Test loading UK tax configuration."""
        config = load_uk_tax_config()
        assert "plan_2" in config
        assert "repayment_threshold_2023" in config["plan_2"]
        assert "repayment_rate" in config["plan_2"]

    def test_config_has_expected_values(self):
        """Test config contains expected Plan 2 values."""
        config = load_uk_tax_config()
        assert config["plan_2"]["repayment_threshold_2023"] == 27295
        assert config["plan_2"]["repayment_rate"] == 0.09


class TestCalculateLoanBalance:
    """Tests for calculate_loan_balance function."""

    def test_loan_with_positive_balance(self):
        """Test loan calculation with remaining balance."""
        new_balance, interest = calculate_loan_balance(
            current_balance=Decimal("10000"),
            annual_repayment=Decimal("500"),
            interest_rate=Decimal("5.0"),
        )

        assert interest == Decimal("500.0")  # 5% of 10000
        assert new_balance == Decimal("10000.0")  # 10000 + 500 - 500

    def test_loan_fully_paid_off(self):
        """Test loan when repayment exceeds balance + interest."""
        new_balance, interest = calculate_loan_balance(
            current_balance=Decimal("1000"),
            annual_repayment=Decimal("2000"),
            interest_rate=Decimal("5.0"),
        )

        assert new_balance == Decimal("0")  # Cannot go negative

    def test_loan_zero_interest(self):
        """Test loan with zero interest rate."""
        new_balance, interest = calculate_loan_balance(
            current_balance=Decimal("5000"),
            annual_repayment=Decimal("500"),
            interest_rate=Decimal("0.0"),
        )

        assert interest == Decimal("0.0")
        assert new_balance == Decimal("4500.0")


class TestCalculateInvestmentValue:
    """Tests for calculate_investment_value function."""

    def test_investment_positive_growth(self):
        """Test investment with positive growth."""
        new_value, growth = calculate_investment_value(
            current_value=Decimal("10000"),
            growth_rate=Decimal("7.0"),
        )

        assert growth == Decimal("700.0")  # 7% of 10000
        assert new_value == Decimal("10700.0")

    def test_investment_zero_growth(self):
        """Test investment with zero growth."""
        new_value, growth = calculate_investment_value(
            current_value=Decimal("5000"),
            growth_rate=Decimal("0.0"),
        )

        assert growth == Decimal("0.0")
        assert new_value == Decimal("5000.0")

    def test_investment_high_growth(self):
        """Test investment with high growth rate."""
        new_value, growth = calculate_investment_value(
            current_value=Decimal("50000"),
            growth_rate=Decimal("15.0"),
        )

        assert growth == Decimal("7500.0")  # 15% of 50000
        assert new_value == Decimal("57500.0")


class TestApplyUKTaxRules:
    """Tests for apply_uk_tax_rules function."""

    def test_income_below_threshold(self):
        """Test repayment when income is below threshold."""
        repayment = apply_uk_tax_rules(
            income=Decimal("25000"),  # Below 27295
            loan_balance=Decimal("30000"),
        )

        assert repayment == Decimal("0")

    def test_income_above_threshold(self):
        """Test repayment when income exceeds threshold."""
        repayment = apply_uk_tax_rules(
            income=Decimal("40000"),  # 12705 above threshold
            loan_balance=Decimal("30000"),
        )

        # 9% of (40000 - 27295) = 9% of 12705 = 1143.45
        expected = Decimal("40000") - Decimal("27295")
        expected *= Decimal("0.09")
        assert abs(repayment - expected) < Decimal("0.01")

    def test_repayment_exceeds_balance(self):
        """Test repayment cannot exceed loan balance."""
        repayment = apply_uk_tax_rules(
            income=Decimal("100000"),  # Very high income
            loan_balance=Decimal("1000"),  # Small balance
        )

        assert repayment <= Decimal("1000")


class TestProjectScenario:
    """Tests for project_scenario function."""

    def setup_method(self):
        """Set up test data."""
        self.calc_input = CalculatorInput(
            age=25,
            graduation_year=2023,
            current_year=2024,
            loan_duration_years=35,
            investment_amount=Decimal("50000"),
            investment_growth_high=Decimal("8.0"),
            investment_growth_low=Decimal("4.0"),
            investment_growth_average=Decimal("6.0"),
            investment_amount_growth=Decimal("0.0"),
            pre_tax_income=Decimal("45000"),
            salary_growth_optimistic=Decimal("5.0"),
            salary_growth_pessimistic=Decimal("2.0"),
            initial_loan_balance=Decimal("2400"),
            loan_interest_current=Decimal("5.5"),
            loan_interest_high=Decimal("7.0"),
            loan_interest_low=Decimal("3.0"),
        )

    def test_optimistic_scenario(self):
        """Test optimistic scenario projection."""
        projection = project_scenario(self.calc_input, ScenarioType.OPTIMISTIC)

        assert projection.scenario_type == ScenarioType.OPTIMISTIC
        assert projection.investment_growth_rate == Decimal("8.0")
        assert projection.loan_interest_rate == Decimal("3.0")
        assert len(projection.yearly_data) > 0

    def test_pessimistic_scenario(self):
        """Test pessimistic scenario projection."""
        projection = project_scenario(self.calc_input, ScenarioType.PESSIMISTIC)

        assert projection.scenario_type == ScenarioType.PESSIMISTIC
        assert projection.investment_growth_rate == Decimal("4.0")
        assert projection.loan_interest_rate == Decimal("7.0")

    def test_realistic_scenario(self):
        """Test realistic scenario projection."""
        projection = project_scenario(self.calc_input, ScenarioType.REALISTIC)

        assert projection.scenario_type == ScenarioType.REALISTIC
        # Realistic uses average of high/low for investment
        expected_investment_rate = (Decimal("8.0") + Decimal("4.0")) / Decimal("2")
        assert projection.investment_growth_rate == expected_investment_rate
        assert projection.loan_interest_rate == Decimal("5.5")

    def test_scenario_has_yearly_data(self):
        """Test scenario projection includes yearly breakdown."""
        projection = project_scenario(self.calc_input, ScenarioType.REALISTIC)

        assert len(projection.yearly_data) > 0
        first_year = projection.yearly_data[0]
        assert hasattr(first_year, "year")
        assert hasattr(first_year, "loan_balance")
        assert hasattr(first_year, "investment_value")


class TestGenerateRecommendation:
    """Tests for generate_recommendation function."""

    def setup_method(self):
        """Set up test data."""
        self.calc_input = CalculatorInput(
            age=25,
            graduation_year=2023,
            current_year=2024,
            loan_duration_years=35,
            investment_amount=Decimal("50000"),
            investment_growth_high=Decimal("8.0"),
            investment_growth_low=Decimal("4.0"),
            investment_growth_average=Decimal("6.0"),
            investment_amount_growth=Decimal("0.0"),
            pre_tax_income=Decimal("45000"),
            salary_growth_optimistic=Decimal("5.0"),
            salary_growth_pessimistic=Decimal("2.0"),
            initial_loan_balance=Decimal("2400"),
            loan_interest_current=Decimal("5.5"),
            loan_interest_high=Decimal("7.0"),
            loan_interest_low=Decimal("3.0"),
        )

    def test_recommendation_structure(self):
        """Test recommendation has required fields."""
        optimistic = project_scenario(self.calc_input, ScenarioType.OPTIMISTIC)
        pessimistic = project_scenario(self.calc_input, ScenarioType.PESSIMISTIC)
        realistic = project_scenario(self.calc_input, ScenarioType.REALISTIC)

        recommendation = generate_recommendation(optimistic, pessimistic, realistic)

        assert hasattr(recommendation, "decision")
        assert hasattr(recommendation, "confidence")
        assert hasattr(recommendation, "rationale")
        assert hasattr(recommendation, "net_benefit_amount")

    def test_recommendation_decision_valid(self):
        """Test recommendation decision is one of valid options."""
        optimistic = project_scenario(self.calc_input, ScenarioType.OPTIMISTIC)
        pessimistic = project_scenario(self.calc_input, ScenarioType.PESSIMISTIC)
        realistic = project_scenario(self.calc_input, ScenarioType.REALISTIC)

        recommendation = generate_recommendation(optimistic, pessimistic, realistic)

        assert recommendation.decision in ["invest", "pay_off_early", "neutral"]

    def test_recommendation_confidence_valid(self):
        """Test recommendation confidence is one of valid options."""
        optimistic = project_scenario(self.calc_input, ScenarioType.OPTIMISTIC)
        pessimistic = project_scenario(self.calc_input, ScenarioType.PESSIMISTIC)
        realistic = project_scenario(self.calc_input, ScenarioType.REALISTIC)

        recommendation = generate_recommendation(optimistic, pessimistic, realistic)

        assert recommendation.confidence in ["high", "medium", "low"]


class TestCalculatePayoffScenarios:
    """Tests for calculate_payoff_scenarios function."""

    def test_valid_input_produces_result(self):
        """Test calculation with valid input."""
        calc_input = CalculatorInput(
            age=25,
            graduation_year=2023,
            current_year=2024,
            loan_duration_years=35,
            investment_amount=Decimal("50000"),
            investment_growth_high=Decimal("8.0"),
            investment_growth_low=Decimal("4.0"),
            investment_growth_average=Decimal("6.0"),
            investment_amount_growth=Decimal("0.0"),
            pre_tax_income=Decimal("45000"),
            salary_growth_optimistic=Decimal("5.0"),
            salary_growth_pessimistic=Decimal("2.0"),
            initial_loan_balance=Decimal("2400"),
            loan_interest_current=Decimal("5.5"),
            loan_interest_high=Decimal("7.0"),
            loan_interest_low=Decimal("3.0"),
        )

        result = calculate_payoff_scenarios(calc_input)

        assert result.optimistic is not None
        assert result.pessimistic is not None
        assert result.realistic is not None
        assert result.recommendation is not None

    def test_invalid_input_raises_error(self):
        """Test calculation with invalid input raises ValueError."""
        calc_input = CalculatorInput(
            age=15,  # Too young
            graduation_year=2023,
            current_year=2024,
            loan_duration_years=35,
            investment_amount=Decimal("50000"),
            investment_growth_high=Decimal("8.0"),
            investment_growth_low=Decimal("4.0"),
            investment_growth_average=Decimal("6.0"),
            investment_amount_growth=Decimal("0.0"),
            pre_tax_income=Decimal("45000"),
            salary_growth_optimistic=Decimal("5.0"),
            salary_growth_pessimistic=Decimal("2.0"),
            initial_loan_balance=Decimal("2400"),
            loan_interest_current=Decimal("5.5"),
            loan_interest_high=Decimal("7.0"),
            loan_interest_low=Decimal("3.0"),
        )

        with pytest.raises(ValueError):
            calculate_payoff_scenarios(calc_input)


class TestSerializeCalculationResult:
    """Tests for serialize_calculation_result function."""

    def test_serialization_produces_dict(self):
        """Test serialization produces a dictionary."""
        calc_input = CalculatorInput(
            age=25,
            graduation_year=2023,
            current_year=2024,
            loan_duration_years=35,
            investment_amount=Decimal("50000"),
            investment_growth_high=Decimal("8.0"),
            investment_growth_low=Decimal("4.0"),
            investment_growth_average=Decimal("6.0"),
            investment_amount_growth=Decimal("0.0"),
            pre_tax_income=Decimal("45000"),
            salary_growth_optimistic=Decimal("5.0"),
            salary_growth_pessimistic=Decimal("2.0"),
            initial_loan_balance=Decimal("2400"),
            loan_interest_current=Decimal("5.5"),
            loan_interest_high=Decimal("7.0"),
            loan_interest_low=Decimal("3.0"),
        )

        result = calculate_payoff_scenarios(calc_input)
        serialized = serialize_calculation_result(result)

        assert isinstance(serialized, dict)
        assert "optimistic" in serialized
        assert "pessimistic" in serialized
        assert "realistic" in serialized
        assert "recommendation" in serialized

    def test_serialized_values_are_json_compatible(self):
        """Test serialized values can be converted to JSON."""
        import json

        calc_input = CalculatorInput(
            age=25,
            graduation_year=2023,
            current_year=2024,
            loan_duration_years=35,
            investment_amount=Decimal("50000"),
            investment_growth_high=Decimal("8.0"),
            investment_growth_low=Decimal("4.0"),
            investment_growth_average=Decimal("6.0"),
            investment_amount_growth=Decimal("0.0"),
            pre_tax_income=Decimal("45000"),
            salary_growth_optimistic=Decimal("5.0"),
            salary_growth_pessimistic=Decimal("2.0"),
            initial_loan_balance=Decimal("2400"),
            loan_interest_current=Decimal("5.5"),
            loan_interest_high=Decimal("7.0"),
            loan_interest_low=Decimal("3.0"),
        )

        result = calculate_payoff_scenarios(calc_input)
        serialized = serialize_calculation_result(result)

        # Should not raise exception
        json_str = json.dumps(serialized)
        assert isinstance(json_str, str)
        assert len(json_str) > 0
