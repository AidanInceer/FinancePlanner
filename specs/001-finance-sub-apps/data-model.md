# Data Model: Finance Sub-Apps Expansion

## Overview
Stateless calculation models representing inputs and outputs for each calculator. No persistence beyond request lifecycle.

## Entities

### RentVsBuyInput
- **Fields**:
  - `property_price` (decimal, required)
  - `deposit_amount` (decimal, required)
  - `mortgage_rate` (decimal, required, 0–1)
  - `mortgage_term_years` (int, required)
  - `monthly_rent` (decimal, required)
  - `rent_growth_rate` (decimal, required, 0–1)
  - `home_appreciation_rate` (decimal, required, 0–1)
  - `maintenance_rate` (decimal, required, 0–1)
  - `property_tax_rate` (decimal, optional, 0–1)
  - `insurance_annual` (decimal, optional)
  - `buying_costs` (decimal, optional)
  - `selling_costs` (decimal, optional)
  - `investment_return_rate` (decimal, required, 0–1)
  - `analysis_years` (int, required, >=1)
- **Validation rules**: Non-negative values, rates between 0 and 1, `deposit_amount <= property_price`.

### RentVsBuyResult
- **Fields**:
  - `total_cost_rent` (decimal)
  - `total_cost_buy` (decimal)
  - `net_worth_rent` (decimal)
  - `net_worth_buy` (decimal)
  - `break_even_year` (int or null)
  - `summary` (string)
  - `graph_series` (list of year/value pairs)

### EmergencyFundInput
- **Fields**:
  - `monthly_expenses` (decimal, required)
  - `target_months` (int, required)
  - `current_savings` (decimal, optional)
- **Validation rules**: Non-negative values, `target_months >= 1`.

### EmergencyFundResult
- **Fields**:
  - `target_fund` (decimal)
  - `savings_gap` (decimal)
  - `coverage_months` (decimal, optional)

### ResilienceScoreInput
- **Fields**:
  - `savings` (decimal, required)
  - `income_stability` (int, required, 0–100)
  - `debt_load` (decimal, required)
  - `insurance_coverage` (int, required, 0–100)
- **Validation rules**: Non-negative values, scores between 0 and 100.

### ResilienceScoreResult
- **Fields**:
  - `resilience_index` (int, 0–100)
  - `weak_points` (list of strings)
  - `summary` (string)

### TimeToFreedomInput
- **Fields**:
  - `annual_expenses` (decimal, required)
  - `current_investments` (decimal, required)
  - `annual_contribution` (decimal, required)
  - `investment_return_rate` (decimal, required, 0–1)
  - `safe_withdrawal_rate` (decimal, required, 0–1)
- **Validation rules**: Non-negative values, rates between 0 and 1.

### TimeToFreedomResult
- **Fields**:
  - `freedom_number` (decimal)
  - `years_to_freedom` (int or null)
  - `timeline_series` (list of year/value pairs)
  - `summary` (string)

## Relationships
- Inputs map 1:1 to their corresponding results for each calculation request.
- Graph series fields provide time-based data for Chart.js rendering.
