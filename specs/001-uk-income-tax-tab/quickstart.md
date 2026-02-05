# UK Income Tax Calculator Tab - Quickstart

## Prerequisites
- Python 3.13+
- Dependencies installed (see repository README)

## Run the app
1. Start the Django server:
   - `python manage.py runserver`
2. Open http://localhost:8000/
3. Select the new UK Income Tax tab.

## Example API Request
POST `/api/income-tax/calculate`
```json
{
  "gross_income": 45000,
  "pay_frequency": "annual",
  "tax_jurisdiction": "england_wales_ni",
  "ni_category": "A",
  "student_loan_plan": "plan_2",
  "pension_contribution_type": "percentage",
  "pension_contribution_value": 5,
  "other_pretax_deductions": 0,
  "tax_year": "2025-26"
}
```

## Expected Output
Response includes:
- Gross and taxable income
- Income tax, NI, student loan deductions
- Total deductions and net pay (annual/monthly/weekly)
- Itemized band breakdowns
