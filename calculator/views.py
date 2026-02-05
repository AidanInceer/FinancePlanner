"""
HTTP request handlers (views) for the calculator application.

This module defines the three HTTP endpoints for the Student Loan Payoff
Calculator:
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

from .models import (
    CalculatorInput,
    EmergencyFundInput,
    RentVsBuyInput,
    ResilienceScoreInput,
    TaxCalculationInput,
    TimeToFreedomInput,
)
from .services import (
    calculate_emergency_fund as calculate_emergency_fund_service,
)
from .services import (
    calculate_income_tax_result,
    calculate_payoff_scenarios,
    serialize_calculation_result,
    serialize_emergency_fund_result,
    serialize_income_tax_result,
    serialize_rent_vs_buy_result,
    serialize_resilience_score_result,
    serialize_time_to_freedom_result,
)
from .services import (
    calculate_rent_vs_buy as calculate_rent_vs_buy_service,
)
from .services import (
    calculate_resilience_score as calculate_resilience_score_service,
)
from .services import (
    calculate_time_to_freedom as calculate_time_to_freedom_service,
)


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
        return JsonResponse(
            {"errors": [f"Invalid input: {str(e)}"]},
            status=400,
        )
    except Exception as e:
        return JsonResponse(
            {"errors": [f"Calculation error: {str(e)}"]},
            status=500,
        )


@csrf_exempt
@require_POST
def calculate_income_tax(request):
    """
    Calculate UK income tax, NI, and student loan deductions.

    Accepts POST request with JSON body containing income and tax parameters.
    Returns a summary of deductions and net pay with band breakdowns.
    """
    try:
        data = json.loads(request.body)

        calc_input = TaxCalculationInput(
            gross_income=Decimal(str(data["gross_income"])),
            bonus_annual=Decimal(str(data.get("bonus_annual", 0))),
            pay_frequency=str(data["pay_frequency"]),
            tax_jurisdiction=str(data["tax_jurisdiction"]),
            ni_category=str(data["ni_category"]),
            student_loan_plan=str(data["student_loan_plan"]),
            pension_contribution_type=str(data.get("pension_contribution_type", "none")),
            pension_contribution_value=Decimal(str(data.get("pension_contribution_value", 0))),
            other_pretax_deductions=Decimal(str(data.get("other_pretax_deductions", 0))),
            tax_year=str(data["tax_year"]),
        )

        errors = calc_input.validate()
        if errors:
            return JsonResponse({"errors": errors}, status=400)

        result = calculate_income_tax_result(calc_input)
        response_data = serialize_income_tax_result(result)

        return JsonResponse(response_data, status=200)

    except (KeyError, ValueError, InvalidOperation) as e:
        return JsonResponse(
            {"errors": [f"Invalid input: {str(e)}"]},
            status=400,
        )
    except Exception as e:
        return JsonResponse(
            {"errors": [f"Calculation error: {str(e)}"]},
            status=500,
        )


@csrf_exempt
@require_POST
def calculate_rent_vs_buy(request):
    """
    Calculate rent vs buy comparison and return JSON summary + graph series.
    """
    try:
        data = json.loads(request.body)

        calc_input = RentVsBuyInput(
            property_price=Decimal(str(data["property_price"])),
            deposit_amount=Decimal(str(data["deposit_amount"])),
            mortgage_rate=Decimal(str(data["mortgage_rate"])),
            mortgage_term_years=int(data["mortgage_term_years"]),
            monthly_rent=Decimal(str(data["monthly_rent"])),
            rent_growth_rate=Decimal(str(data["rent_growth_rate"])),
            home_appreciation_rate=Decimal(str(data["home_appreciation_rate"])),
            maintenance_rate=Decimal(str(data["maintenance_rate"])),
            property_tax_rate=Decimal(str(data.get("property_tax_rate", 0))),
            insurance_annual=Decimal(str(data.get("insurance_annual", 0))),
            buying_costs=Decimal(str(data.get("buying_costs", 0))),
            selling_costs=Decimal(str(data.get("selling_costs", 0))),
            investment_return_rate=Decimal(str(data["investment_return_rate"])),
            analysis_years=int(data["analysis_years"]),
        )

        errors = calc_input.validate()
        if errors:
            return JsonResponse({"errors": errors}, status=400)

        result = calculate_rent_vs_buy_service(calc_input)
        return JsonResponse(serialize_rent_vs_buy_result(result), status=200)

    except (KeyError, ValueError, InvalidOperation) as e:
        return JsonResponse(
            {"errors": [f"Invalid input: {str(e)}"]},
            status=400,
        )
    except Exception as e:
        return JsonResponse(
            {"errors": [f"Calculation error: {str(e)}"]},
            status=500,
        )


@csrf_exempt
@require_POST
def calculate_emergency_fund(request):
    """
    Calculate emergency fund target and gap.
    """
    try:
        data = json.loads(request.body)

        calc_input = EmergencyFundInput(
            monthly_expenses=Decimal(str(data["monthly_expenses"])),
            target_months=int(data["target_months"]),
            current_savings=Decimal(str(data.get("current_savings", 0))),
        )

        errors = calc_input.validate()
        if errors:
            return JsonResponse({"errors": errors}, status=400)

        result = calculate_emergency_fund_service(calc_input)
        return JsonResponse(serialize_emergency_fund_result(result), status=200)

    except (KeyError, ValueError, InvalidOperation) as e:
        return JsonResponse(
            {"errors": [f"Invalid input: {str(e)}"]},
            status=400,
        )
    except Exception as e:
        return JsonResponse(
            {"errors": [f"Calculation error: {str(e)}"]},
            status=500,
        )


@csrf_exempt
@require_POST
def calculate_resilience_score(request):
    """
    Calculate financial resilience score and weak points.
    """
    try:
        data = json.loads(request.body)

        calc_input = ResilienceScoreInput(
            savings=Decimal(str(data["savings"])),
            income_stability=int(data["income_stability"]),
            debt_load=Decimal(str(data["debt_load"])),
            insurance_coverage=int(data["insurance_coverage"]),
        )

        errors = calc_input.validate()
        if errors:
            return JsonResponse({"errors": errors}, status=400)

        result = calculate_resilience_score_service(calc_input)
        return JsonResponse(
            serialize_resilience_score_result(result),
            status=200,
        )

    except (KeyError, ValueError, InvalidOperation) as e:
        return JsonResponse(
            {"errors": [f"Invalid input: {str(e)}"]},
            status=400,
        )
    except Exception as e:
        return JsonResponse(
            {"errors": [f"Calculation error: {str(e)}"]},
            status=500,
        )


@csrf_exempt
@require_POST
def calculate_time_to_freedom(request):
    """
    Calculate freedom number and time-to-freedom timeline.
    """
    try:
        data = json.loads(request.body)

        calc_input = TimeToFreedomInput(
            annual_expenses=Decimal(str(data["annual_expenses"])),
            current_investments=Decimal(str(data["current_investments"])),
            annual_contribution=Decimal(str(data["annual_contribution"])),
            investment_return_rate=Decimal(str(data["investment_return_rate"])),
            safe_withdrawal_rate=Decimal(str(data["safe_withdrawal_rate"])),
        )

        errors = calc_input.validate()
        if errors:
            return JsonResponse({"errors": errors}, status=400)

        result = calculate_time_to_freedom_service(calc_input)
        return JsonResponse(
            serialize_time_to_freedom_result(result),
            status=200,
        )

    except (KeyError, ValueError, InvalidOperation) as e:
        return JsonResponse(
            {"errors": [f"Invalid input: {str(e)}"]},
            status=400,
        )
    except Exception as e:
        return JsonResponse(
            {"errors": [f"Calculation error: {str(e)}"]},
            status=500,
        )


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
    return JsonResponse(
        {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
        }
    )
