from django.urls import path

from . import views

app_name = "calculator"

urlpatterns = [
    path("", views.index, name="index"),
    path("api/calculate", views.calculate, name="calculate"),
    path("api/income-tax/calculate", views.calculate_income_tax, name="income_tax_calculate"),
    path("api/rent-vs-buy/calculate", views.calculate_rent_vs_buy, name="rent_vs_buy_calculate"),
    path(
        "api/emergency-fund/calculate",
        views.calculate_emergency_fund,
        name="emergency_fund_calculate",
    ),
    path(
        "api/resilience-score/calculate",
        views.calculate_resilience_score,
        name="resilience_score_calculate",
    ),
    path(
        "api/time-to-freedom/calculate",
        views.calculate_time_to_freedom,
        name="time_to_freedom_calculate",
    ),
    path("health", views.health_check, name="health_check"),
]
