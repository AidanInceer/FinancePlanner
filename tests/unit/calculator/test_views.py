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
