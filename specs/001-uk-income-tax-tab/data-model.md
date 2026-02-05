# Phase 1 Data Model: UK Income Tax Calculator Tab

## Entity: TaxCalculationInput
**Represents**: All user inputs required to compute UK take-home pay.

**Fields**
- `gross_income`: decimal (required, >= 0)
- `pay_frequency`: enum (`annual`, `monthly`, `weekly`)
- `tax_jurisdiction`: enum (`england_wales_ni`, `scotland`)
- `ni_category`: enum (`A`, `B`, `C`, `H`, `J`, `M`, `Z`)
- `student_loan_plan`: enum (`none`, `plan_1`, `plan_2`, `plan_4`, `plan_5`, `postgraduate`)
- `pension_contribution_type`: enum (`none`, `percentage`, `amount`)
- `pension_contribution_value`: decimal (>= 0)
- `other_pretax_deductions`: decimal (>= 0)
- `tax_year`: string (e.g., `2025-26`)

**Validation Rules**
- `gross_income` must be non-negative.
- `pension_contribution_value` required when `pension_contribution_type` is `percentage` or `amount`.
- `pension_contribution_value` for percentage must be within 0–100.
- Pre-tax deductions must not exceed gross income.

## Entity: TaxConfiguration
**Represents**: Static thresholds and rates for a specific tax year.

**Fields**
- `tax_year`: string
- `personal_allowance`: decimal
- `personal_allowance_taper_start`: decimal
- `personal_allowance_taper_end`: decimal
- `income_tax_bands`: list of bands by jurisdiction (rate + threshold range)
- `ni_thresholds`: LEL/PT/UEL annual values
- `ni_rates_by_category`: rate table by category for main/upper bands
- `student_loan_plans`: per-plan threshold + rate

**Relationships**
- `TaxCalculationInput.tax_year` references `TaxConfiguration.tax_year`.

## Entity: DeductionBreakdown
**Represents**: Output deduction detail for a single calculation.

**Fields**
- `taxable_income`: decimal
- `income_tax_total`: decimal
- `income_tax_bands`: list of band-level amounts (rate, band range, tax due)
- `ni_total`: decimal
- `ni_bands`: list of band-level amounts (rate, band range, contribution due)
- `student_loan_total`: decimal
- `total_deductions`: decimal
- `effective_deduction_rate`: decimal (0–1)

## Entity: NetPaySummary
**Represents**: Output net pay summary for display.

**Fields**
- `gross_annual`: decimal
- `net_annual`: decimal
- `net_monthly`: decimal
- `net_weekly`: decimal

## State Transitions
- `TaxCalculationInput` → validated → calculation → `DeductionBreakdown` + `NetPaySummary`

## Notes
- Entities are immutable for calculation safety.
- No persistence required for MVP; results are computed per-request.
