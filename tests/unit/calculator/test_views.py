"""Unit tests for calculator views."""

import json
from datetime import datetime

import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class TestCalculatorViews:
    """Tests for calculator views."""

    def setup_method(self):
        """Set up test client."""
        self.client = Client()

    def test_index_view_returns_200(self):
        """Test index view returns HTTP 200."""
        response = self.client.get(reverse("calculator:index"))
        assert response.status_code == 200

    def test_index_view_uses_correct_template(self):
        """Test index view uses the correct template."""
        response = self.client.get(reverse("calculator:index"))
        assert "calculator/index.html" in [t.name for t in response.templates]

    def test_health_check_returns_200(self):
        """Test health check endpoint returns HTTP 200."""
        response = self.client.get(reverse("calculator:health_check"))
        assert response.status_code == 200

    def test_health_check_returns_json(self):
        """Test health check returns JSON response."""
        response = self.client.get(reverse("calculator:health_check"))
        assert response["Content-Type"] == "application/json"

    def test_health_check_contains_status(self):
        """Test health check response contains status field."""
        response = self.client.get(reverse("calculator:health_check"))
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    def test_health_check_contains_timestamp(self):
        """Test health check response contains timestamp field."""
        response = self.client.get(reverse("calculator:health_check"))
        data = response.json()
        assert "timestamp" in data
        # Verify timestamp is a valid ISO format
        datetime.fromisoformat(data["timestamp"])

    def test_calculate_endpoint_returns_501_placeholder(self):
        """Test calculate endpoint returns calculation results."""
        response = self.client.post(
            reverse("calculator:calculate"),
            data=json.dumps(
                {
                    "age": 25,
                    "graduation_year": 2023,
                    "current_year": 2024,
                    "loan_duration_years": 35,
                    "investment_amount": 50000,
                    "investment_growth_high": 8.0,
                    "investment_growth_low": 4.0,
                    "investment_growth_average": 6.0,
                    "investment_amount_growth": 0.0,
                    "pre_tax_income": 45000,
                    "salary_growth_optimistic": 5.0,
                    "salary_growth_pessimistic": 2.0,
                    "initial_loan_balance": 2400,
                    "loan_interest_current": 5.5,
                    "loan_interest_high": 7.0,
                    "loan_interest_low": 3.0,
                }
            ),
            content_type="application/json",
        )
        # Should return 200 with calculation results
        assert response.status_code == 200
        data = response.json()
        assert "optimistic" in data
        assert "pessimistic" in data
        assert "realistic" in data
        assert "recommendation" in data

    def test_index_view_contains_form_fields(self):
        """Test index view contains all required form fields."""
        response = self.client.get(reverse("calculator:index"))
        content = response.content.decode("utf-8")

        # Check for key form fields
        assert 'id="age"' in content
        assert 'id="graduation_year"' in content
        assert 'id="loan_duration_years"' in content
        assert 'id="investment_amount"' in content
        assert 'id="investment_growth_high"' in content
        assert 'id="investment_growth_low"' in content
        assert 'id="pre_tax_income"' in content
        assert 'id="initial_loan_balance"' in content
        assert 'id="loan_interest_current"' in content
        assert 'id="loan_interest_high"' in content
        assert 'id="loan_interest_low"' in content

        assert 'id="tax_gross_income"' in content
        assert 'id="bonus_annual"' in content
        assert 'id="tax_pay_frequency"' in content
        assert 'id="tax_year"' in content
        assert 'id="tax_jurisdiction"' in content
        assert 'id="ni_category"' in content
        assert 'id="student_loan_plan"' in content

        assert 'id="rvb_property_price"' in content
        assert 'id="rvb_deposit_amount"' in content
        assert 'id="rvb_monthly_rent"' in content
        assert 'id="ef_monthly_expenses"' in content
        assert 'id="rs_savings"' in content
        assert 'id="ff_annual_expenses"' in content

    def test_index_view_contains_bootstrap(self):
        """Test index view includes Bootstrap CSS."""
        response = self.client.get(reverse("calculator:index"))
        content = response.content.decode("utf-8")
        assert "bootstrap" in content.lower()

    def test_index_view_contains_chart_js(self):
        """Test index view includes Chart.js."""
        response = self.client.get(reverse("calculator:index"))
        content = response.content.decode("utf-8")
        assert "chart.js" in content.lower()

    def test_calculate_endpoint_with_invalid_data(self):
        """Test calculate endpoint with invalid input data."""
        response = self.client.post(
            reverse("calculator:calculate"),
            data=json.dumps(
                {
                    "age": 15,  # Invalid - too young
                    "graduation_year": 2023,
                    "current_year": 2024,
                    "loan_duration_years": 35,
                    "investment_amount": 50000,
                    "investment_growth_high": 8.0,
                    "investment_growth_low": 4.0,
                    "investment_growth_average": 6.0,
                    "investment_amount_growth": 0.0,
                    "pre_tax_income": 45000,
                    "salary_growth_optimistic": 5.0,
                    "salary_growth_pessimistic": 2.0,
                    "initial_loan_balance": 2400,
                    "loan_interest_current": 5.5,
                    "loan_interest_high": 7.0,
                    "loan_interest_low": 3.0,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 400
        data = response.json()
        assert "errors" in data

    def test_calculate_endpoint_with_missing_fields(self):
        """Test calculate endpoint with missing required fields."""
        response = self.client.post(
            reverse("calculator:calculate"),
            data=json.dumps({"age": 25}),  # Missing required fields
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_income_tax_endpoint_returns_200(self):
        """Test income tax calculation endpoint returns results."""
        response = self.client.post(
            reverse("calculator:income_tax_calculate"),
            data=json.dumps(
                {
                    "gross_income": 45000,
                    "bonus_annual": 0,
                    "pay_frequency": "annual",
                    "tax_jurisdiction": "england_wales_ni",
                    "ni_category": "A",
                    "student_loan_plan": "none",
                    "pension_contribution_type": "none",
                    "pension_contribution_value": 0,
                    "other_pretax_deductions": 0,
                    "tax_year": "2025-26",
                }
            ),
            content_type="application/json",
        )

        assert response.status_code == 200
        data = response.json()
        assert "gross_annual" in data
        assert "income_tax_annual" in data
        assert "ni_annual" in data
        assert "student_loan_annual" in data
        assert "income_tax_bands" in data
        assert "ni_bands" in data

    def test_income_tax_endpoint_with_invalid_data(self):
        """Test income tax endpoint handles invalid input."""
        response = self.client.post(
            reverse("calculator:income_tax_calculate"),
            data=json.dumps(
                {
                    "gross_income": -10,
                    "bonus_annual": 0,
                    "pay_frequency": "annual",
                    "tax_jurisdiction": "england_wales_ni",
                    "ni_category": "A",
                    "student_loan_plan": "none",
                    "tax_year": "2025-26",
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 400
        assert "errors" in response.json()

    def test_rent_vs_buy_endpoint_returns_200(self):
        response = self.client.post(
            reverse("calculator:rent_vs_buy_calculate"),
            data=json.dumps(
                {
                    "property_price": 300000,
                    "deposit_amount": 60000,
                    "mortgage_rate": 0.05,
                    "mortgage_term_years": 25,
                    "monthly_rent": 1400,
                    "rent_growth_rate": 0.03,
                    "home_appreciation_rate": 0.03,
                    "maintenance_rate": 0.01,
                    "property_tax_rate": 0.005,
                    "insurance_annual": 350,
                    "buying_costs": 5000,
                    "selling_costs": 6000,
                    "investment_return_rate": 0.05,
                    "analysis_years": 10,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "graph_series" in data

    def test_emergency_fund_endpoint_returns_200(self):
        response = self.client.post(
            reverse("calculator:emergency_fund_calculate"),
            data=json.dumps(
                {
                    "monthly_expenses": 2000,
                    "target_months": 6,
                    "current_savings": 3000,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.json()
        assert "target_fund" in data
        assert "savings_gap" in data

    def test_resilience_score_endpoint_returns_200(self):
        response = self.client.post(
            reverse("calculator:resilience_score_calculate"),
            data=json.dumps(
                {
                    "savings": 8000,
                    "income_stability": 70,
                    "debt_load": 4000,
                    "insurance_coverage": 65,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.json()
        assert "resilience_index" in data
        assert "weak_points" in data

    def test_time_to_freedom_endpoint_returns_200(self):
        response = self.client.post(
            reverse("calculator:time_to_freedom_calculate"),
            data=json.dumps(
                {
                    "annual_expenses": 28000,
                    "current_investments": 25000,
                    "annual_contribution": 8000,
                    "investment_return_rate": 0.05,
                    "safe_withdrawal_rate": 0.04,
                }
            ),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.json()
        assert "freedom_number" in data
        assert "timeline_series" in data
