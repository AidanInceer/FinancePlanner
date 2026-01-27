"""
HTTP request handlers (views) for the calculator application.

This module defines the three HTTP endpoints for the Student Loan Payoff Calculator:
1. index() - GET / - Renders the calculator form (HTML page)
2. calculate() - POST /calculate - Processes calculation requests (JSON API)
3. health_check() - GET /health - System health monitoring endpoint

All endpoints follow RESTful conventions. The calculate endpoint accepts JSON,
performs validation, and returns structured JSON responses with appropriate
HTTP status codes.

Error Handling:
    - 400 Bad Request: Invalid input data (validation errors)
    - 500 Internal Server Error: Calculation failures or system errors
    - 200 OK: Successful calculation with complete projection data

CSRF exempt on /calculate endpoint since it's a stateless calculator API.
"""

import json
from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import CalculatorInput
from .services import calculate_payoff_scenarios, serialize_calculation_result


@require_GET
def index(request):
    """
    Render the calculator landing page.

    Displays a Bootstrap 5 form with 11 input fields for personal info,
    investment assumptions, and loan details. The form submits to the
    /calculate API endpoint via JavaScript.

    Args:
        request (HttpRequest): Django request object

    Returns:
        HttpResponse: Rendered HTML page with calculator form
    """
    return render(request, "calculator/index.html")


@csrf_exempt
@require_POST
def calculate(request):
    """
    Calculate loan payoff scenarios and return JSON projection data.

    Accepts POST request with JSON body containing 11 input fields.
    Validates inputs, performs multi-year projections for three scenarios
    (optimistic/realistic/pessimistic), and returns complete calculation
    results including recommendation.

    Args:
        request (HttpRequest): Django request with JSON body

    Returns:
        JsonResponse:
            - 200 OK: Calculation result with scenarios and recommendation
            - 400 Bad Request: Validation errors
            - 500 Internal Server Error: Calculation failures

    Request Body Example:
        {
            "age": 25,
            "graduation_year": 2022,
            "loan_duration_years": 15,
            "investment_amount": 5000,
            "optimistic_return": 0.08,
            "pessimistic_return": 0.04,
            "gross_income": 35000,
            "loan_balance": 45000,
            "annual_repayment": 3000,
            "loan_interest_rate": 0.055
        }
    """
    try:
        # Parse JSON request body
        data = json.loads(request.body)

        # Convert to Decimal for financial precision
        calc_input = CalculatorInput(
            age=int(data["age"]),
            current_year=int(data["current_year"]),
            graduation_year=int(data["graduation_year"]),
            loan_duration_years=int(data["loan_duration_years"]),
            investment_amount=Decimal(str(data["investment_amount"])),
            investment_growth_high=Decimal(str(data["investment_growth_high"])),
            investment_growth_low=Decimal(str(data["investment_growth_low"])),
            investment_growth_average=Decimal(str(data["investment_growth_average"])),
            investment_amount_growth=Decimal(str(data["investment_amount_growth"])),
            pre_tax_income=Decimal(str(data["pre_tax_income"])),
            salary_growth_optimistic=Decimal(str(data["salary_growth_optimistic"])),
            salary_growth_pessimistic=Decimal(str(data["salary_growth_pessimistic"])),
            initial_loan_balance=Decimal(str(data["initial_loan_balance"])),
            loan_interest_current=Decimal(str(data["loan_interest_current"])),
            loan_interest_high=Decimal(str(data["loan_interest_high"])),
            loan_interest_low=Decimal(str(data["loan_interest_low"])),
        )

        # Validate input
        errors = calc_input.validate()
        if errors:
            return JsonResponse({"errors": errors}, status=400)

        # Perform calculation
        result = calculate_payoff_scenarios(calc_input)

        # Serialize result
        response_data = serialize_calculation_result(result)

        return JsonResponse(response_data, status=200)

    except (KeyError, ValueError, InvalidOperation) as e:
        return JsonResponse({"errors": [f"Invalid input: {str(e)}"]}, status=400)
    except Exception as e:
        return JsonResponse({"errors": [f"Calculation error: {str(e)}"]}, status=500)


@require_GET
def health_check(request):
    """
    Health check endpoint for system monitoring.

    Returns 200 OK with current timestamp to indicate service is running.
    Used by load balancers, monitoring tools, and deployment pipelines
    to verify application availability.

    Args:
        request (HttpRequest): Django request object

    Returns:
        JsonResponse: {"status": "healthy", "timestamp": "2024-01-15T10:30:00"}
    """
    return JsonResponse({"status": "healthy", "timestamp": datetime.now().isoformat()})
