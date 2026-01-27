# Changelog

## [Version 1.3] - Growth Rates & Error Bars

### Added
- **Salary Growth YoY** - Optimistic and pessimistic annual salary increase rates
  - Salary grows each year in projections based on scenario type
  - Optimistic scenario uses optimistic growth rate
  - Pessimistic scenario uses pessimistic growth rate
  - Realistic scenario uses average of both rates

- **Investment Amount Growth** - Annual increase in investment contributions
  - Investment amount grows year-over-year (e.g., 3% increase = £5,000 → £5,150 → £5,304.50)
  - Same growth rate applied across all scenarios

- **Average Investment Return Rate** - Dedicated field for realistic scenario
  - Previously calculated as average of high/low, now user-configurable
  - Must be between low and high rates

- **Error Bars on Chart** - Visual uncertainty bands for investment projections
  - Shows optimistic, realistic, and pessimistic investment value lines
  - Shaded areas between lines represent uncertainty/variance
  - Makes it easier to see the range of possible outcomes

### Changed
- **Investment logic**: Investment value now starts at £0 and accumulates annual contributions
  - Previous: Investment started at full amount
  - New: Adds annual investment each year (more realistic)

- **Calculation engine**: Income-based repayments now account for salary growth
  - Each year's repayment calculated from current year's grown income
  - More accurate long-term projections

### Technical Details
- Updated `CalculatorInput` with 4 new fields: `salary_growth_optimistic`, `salary_growth_pessimistic`, `investment_amount_growth`, `investment_growth_average`
- Modified `project_scenario()` to apply YoY growth for income and investment amounts
- Enhanced Chart.js to show 6 lines (3 loan balance + 3 investment value) with uncertainty bands
- All 72 unit tests updated and passing

### Example Use Cases
1. **Career Growth**: Model aggressive (5%) vs conservative (2%) salary growth
2. **Investment Strategy**: Plan for increasing investment amounts as income rises (e.g., 3% annual increase)
3. **Risk Analysis**: See full range of investment outcomes with visual error bars

---

## [Version 1.2] - User-Configurable Current Year

### Added
- **Current Year** input field - allows users to specify the year to start calculations from
- Auto-fills with current year by default, but can be modified for scenario modeling
- Validation ensures year is between 1980 and 2100

### Changed
- Converted `current_year` from auto-calculated property to user input field
- Updated form layout to include current year field between age and graduation year
- Modified all calculation logic to use user-provided current year instead of `datetime.now().year`
- Updated 72 unit tests to include `current_year` parameter

### Why This Change?
Users can now model historical scenarios or project from different starting years. For example:
- "What if I started repaying in 2023?" (historical analysis)
- "What will happen if I start repaying in 2026?" (future projections)
- Compare multiple scenarios with different starting years

---

## [Version 1.1] - Auto-Calculate Loan Repayments

## Summary of Changes

Successfully updated the Student Loan Payoff Calculator to:
1. ✅ Add an **Initial Loan Balance** field for users to enter their current loan amount
2. ✅ **Auto-calculate annual loan repayments** based on UK Plan 2 rules (9% of income above £27,295 threshold)
3. ✅ Make the repayment field **read-only** and automatically populated

## Key Changes

### 1. Form Updates (index.html)
- Added new field: **"Current Loan Balance (£)"** - user input for initial loan amount
- Changed **"Annual Repayment (£)"** to **read-only** with helper text: "Auto-calculated: 9% above £27,295"
- Reorganized layout: Income, Loan Balance, and Auto-calculated Repayment in one row

### 2. Model Updates (models.py)
- Replaced `loan_repayment_annual` field with `initial_loan_balance` in `CalculatorInput` dataclass
- Updated validation to check for non-negative initial loan balance
- Updated docstrings to reflect the new field

### 3. Calculation Logic (services.py)
- Updated `project_scenario()` to use `initial_loan_balance` from user input instead of estimated value
- Removed the rough estimation logic that was calculating loan balance from repayment

### 4. JavaScript Auto-Calculation (calculator.js)
- Added `calculateAnnualRepayment()` function that runs when income field changes
- **Formula**: If income > £27,295, then repayment = (income - £27,295) × 9%
- Displays result with 2 decimal places (e.g., "1,593.45")
- Updates in real-time as user types income

### 5. API Updates (views.py)
- Updated API endpoint to accept `initial_loan_balance` instead of `loan_repayment_annual`
- Automatically works with new model structure

### 6. Test Updates
- Updated all 72 tests to use `initial_loan_balance` instead of `loan_repayment_annual`
- All tests passing ✅

## How It Works Now

### User Experience
1. User enters their **annual pre-tax income** (e.g., £45,000)
2. User enters their **current loan balance** (e.g., £35,000)
3. The **annual repayment** field automatically calculates and displays:
   - If income = £45,000: Repayment = (£45,000 - £27,295) × 9% = **£1,593.45/year**
   - If income < £27,295: Repayment = **£0.00** (below repayment threshold)

### UK Plan 2 Rules Applied
- **Repayment Threshold**: £27,295
- **Repayment Rate**: 9% of income above threshold
- **Auto-calculation**: Updates instantly when income changes
- **Accurate**: Matches official UK student loan repayment calculations

## Example Scenarios

### Scenario 1: Graduate earning £35,000
- Income: £35,000
- Threshold: £27,295
- Above threshold: £35,000 - £27,295 = £7,705
- **Annual repayment: £7,705 × 9% = £693.45**

### Scenario 2: Graduate earning £50,000
- Income: £50,000
- Threshold: £27,295
- Above threshold: £50,000 - £27,295 = £22,705
- **Annual repayment: £22,705 × 9% = £2,043.45**

### Scenario 3: Graduate earning £25,000 (below threshold)
- Income: £25,000
- Below threshold
- **Annual repayment: £0.00**

## Testing

All tests updated and passing:
```bash
pytest
# 72 passed in 0.46s
```

Test coverage includes:
- ✅ Model validation with new field
- ✅ View endpoints accepting new parameter
- ✅ Service calculations using initial loan balance
- ✅ Performance tests (35-year projection in 0.018s)

## Benefits

1. **More Accurate**: Uses actual loan balance instead of estimated value
2. **Easier to Use**: Auto-calculates repayments - users don't need to figure out their repayment amount
3. **Follows UK Rules**: Implements official Plan 2 repayment calculation (9% above £27,295)
4. **Real-time Updates**: Repayment recalculates as user types income
5. **Educational**: Shows users exactly how much they'll repay based on their income

## Development Server

Server running at: http://127.0.0.1:8000/

To test:
1. Open http://127.0.0.1:8000/
2. Enter income (e.g., £45,000)
3. Watch the "Annual Repayment" field auto-populate
4. Enter loan balance (e.g., £35,000)
5. Submit form to see projections

## Technical Details

### JavaScript Function
```javascript
function calculateAnnualRepayment() {
    const income = parseFloat(incomeInput.value) || 0;
    const threshold = 27295; // UK Plan 2 threshold
    const rate = 0.09; // 9% repayment rate

    let annualRepayment = 0;
    if (income > threshold) {
        annualRepayment = (income - threshold) * rate;
    }

    repaymentInput.value = annualRepayment > 0 ? annualRepayment.toFixed(2) : '0.00';
}
```

### Model Field
```python
initial_loan_balance: Decimal  # New field for current outstanding loan amount
```

### API Request Example
```json
{
  "age": 25,
  "pre_tax_income": 45000,
  "initial_loan_balance": 35000,
  ...
}
```

Annual repayment is calculated automatically in the backend using the same UK Plan 2 formula.
