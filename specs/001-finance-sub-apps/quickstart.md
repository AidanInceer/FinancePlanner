# Quickstart: Finance Sub-Apps Expansion

## Prerequisites
- Python 3.13+
- Dependencies installed from requirements.txt

## Run the app
1. Apply migrations:
   - `python manage.py migrate`
2. Start the server:
   - `python manage.py runserver`
3. Open the app:
   - http://localhost:8000/

## Use the calculators

### Rent vs Buy
1. Open the Rent vs Buy calculator tab/page.
2. Review default inputs and adjust as needed.
3. Click Calculate to see the summary and comparison graph.

### Emergency Fund
1. Enter monthly expenses and target months.
2. Add current savings (optional).
3. Click Calculate to see the target fund and savings gap.

### Financial Resilience Score
1. Enter savings, income stability, debt load, and insurance coverage.
2. Click Calculate to see the resilience index and weak points.

### Time-to-Freedom
1. Enter annual expenses, current investments, and annual contribution.
2. Set investment return and safe withdrawal rate.
3. Click Calculate to see the freedom number and timeline.

## API Endpoints (JSON)
- POST /api/rent-vs-buy/calculate
- POST /api/emergency-fund/calculate
- POST /api/resilience-score/calculate
- POST /api/time-to-freedom/calculate

See the contract file for request/response details:
- [specs/001-finance-sub-apps/contracts/finance-sub-apps-api.json](specs/001-finance-sub-apps/contracts/finance-sub-apps-api.json)
