// Student Loan Payoff Calculator JavaScript

// Global chart instances
let payoffChart = null;
let rentVsBuyChart = null;
let freedomChart = null;

const currencyFormatter = new Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency: 'GBP',
    maximumFractionDigits: 0,
});

function formatCurrency(value) {
    return currencyFormatter.format(Number(value) || 0);
}

function formatPercent(value, decimals = 1) {
    return `${Number(value).toFixed(decimals)}%`;
}

function showFormError(elementId, message) {
    const target = document.getElementById(elementId);
    if (!target) return;
    target.textContent = message;
    target.classList.remove('d-none');
}

function clearFormError(elementId) {
    const target = document.getElementById(elementId);
    if (!target) return;
    target.textContent = '';
    target.classList.add('d-none');
}

async function postJson(url, payload) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
    });

    const data = await response.json();
    if (!response.ok) {
        const errors = data.errors ? data.errors.join(', ') : 'Unable to calculate.';
        throw new Error(errors);
    }
    return data;
}

/**
 * Initialize the calculator when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('Calculator initialized');

    // Auto-fill current year
    const currentYearInput = document.getElementById('current_year');
    if (currentYearInput && !currentYearInput.value) {
        currentYearInput.value = new Date().getFullYear();
    }

    const form = document.getElementById('calculator-form');
    if (form) {
        form.addEventListener('submit', handleLoanFormSubmit);

        // Add real-time validation
        const inputs = form.querySelectorAll('input[type="number"]');
        inputs.forEach(input => {
            input.addEventListener('blur', validateField);
            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid')) {
                    validateField.call(this);
                }
            });
        });

        // Auto-calculate annual repayment when income changes
        const incomeInput = document.getElementById('pre_tax_income');
        if (incomeInput) {
            incomeInput.addEventListener('input', calculateAnnualRepayment);
            incomeInput.addEventListener('blur', calculateAnnualRepayment);
        }
    }

    const taxForm = document.getElementById('income-tax-form');
    if (taxForm) {
        taxForm.addEventListener('submit', handleIncomeTaxSubmit);

        const pensionTypeSelect = document.getElementById('pension_contribution_type');
        if (pensionTypeSelect) {
            pensionTypeSelect.addEventListener('change', updatePensionSuffix);
            updatePensionSuffix();
        }
    }

    const rentVsBuyForm = document.getElementById('rent-vs-buy-form');
    if (rentVsBuyForm) {
        rentVsBuyForm.addEventListener('submit', handleRentVsBuySubmit);
    }

    const emergencyFundForm = document.getElementById('emergency-fund-form');
    if (emergencyFundForm) {
        emergencyFundForm.addEventListener('submit', handleEmergencyFundSubmit);
    }

    const resilienceForm = document.getElementById('resilience-form');
    if (resilienceForm) {
        resilienceForm.addEventListener('submit', handleResilienceSubmit);
    }

    const freedomForm = document.getElementById('freedom-form');
    if (freedomForm) {
        freedomForm.addEventListener('submit', handleFreedomSubmit);
    }
});

function updatePensionSuffix() {
    const pensionType = document.getElementById('pension_contribution_type');
    const pensionSuffix = document.getElementById('pension-value-suffix');
    const pensionValue = document.getElementById('pension_contribution_value');

    if (!pensionType || !pensionSuffix || !pensionValue) return;

    if (pensionType.value === 'percentage') {
        pensionSuffix.textContent = '%';
        pensionValue.step = '0.1';
        pensionValue.max = '100';
    } else {
        pensionSuffix.textContent = '£';
        pensionValue.step = '0.01';
        pensionValue.removeAttribute('max');
    }
}

/**
 * Calculate annual loan repayment based on UK Plan 2 rules
 * 9% of income above £27,295 threshold
 */
function calculateAnnualRepayment() {
    const incomeInput = document.getElementById('pre_tax_income');
    const repaymentInput = document.getElementById('loan_repayment_annual');

    if (!incomeInput || !repaymentInput) return;

    const income = parseFloat(incomeInput.value) || 0;
    const threshold = 27295; // UK Plan 2 threshold
    const rate = 0.09; // 9% repayment rate

    let annualRepayment = 0;
    if (income > threshold) {
        annualRepayment = (income - threshold) * rate;
    }

    // Display with 2 decimal places
    repaymentInput.value = annualRepayment > 0 ? annualRepayment.toFixed(2) : '0.00';
}

/**
 * Validate a single form field
 */
function validateField() {
    const value = parseFloat(this.value);
    const min = parseFloat(this.min);
    const max = parseFloat(this.max);

    let isValid = true;

    if (this.required && (!this.value || this.value.trim() === '')) {
        isValid = false;
    } else if (!isNaN(min) && value < min) {
        isValid = false;
    } else if (!isNaN(max) && value > max) {
        isValid = false;
    }

    if (isValid) {
        this.classList.remove('is-invalid');
        this.classList.add('is-valid');
    } else {
        this.classList.remove('is-valid');
        this.classList.add('is-invalid');
    }

    return isValid;
}

/**
 * Validate investment growth range
 */
function validateInvestmentGrowthRange() {
    const lowInput = document.getElementById('investment_growth_low');
    const highInput = document.getElementById('investment_growth_high');

    const low = parseFloat(lowInput.value);
    const high = parseFloat(highInput.value);

    if (low > high) {
        highInput.setCustomValidity('Optimistic return must be higher than pessimistic return');
        highInput.classList.add('is-invalid');
        return false;
    } else {
        highInput.setCustomValidity('');
        highInput.classList.remove('is-invalid');
        return true;
    }
}

/**
 * Validate loan interest rate range
 */
function validateLoanInterestRange() {
    const lowInput = document.getElementById('loan_interest_low');
    const currentInput = document.getElementById('loan_interest_current');
    const highInput = document.getElementById('loan_interest_high');

    const low = parseFloat(lowInput.value);
    const current = parseFloat(currentInput.value);
    const high = parseFloat(highInput.value);

    let isValid = true;

    if (current < low || current > high) {
        currentInput.setCustomValidity('Current rate must be between optimistic and pessimistic rates');
        currentInput.classList.add('is-invalid');
        isValid = false;
    } else {
        currentInput.setCustomValidity('');
        currentInput.classList.remove('is-invalid');
    }

    return isValid;
}

/**
 * Handle form submission
 */
async function handleLoanFormSubmit(event) {
    event.preventDefault();

    // Validate all fields
    const form = event.target;
    const inputs = form.querySelectorAll('input[type="number"]');
    let allValid = true;

    inputs.forEach(input => {
        if (!validateField.call(input)) {
            allValid = false;
        }
    });

    // Validate ranges
    if (!validateInvestmentGrowthRange()) {
        allValid = false;
    }

    if (!validateLoanInterestRange()) {
        allValid = false;
    }

    if (!allValid) {
        showLoanError('Please correct the errors in the form');
        return;
    }

    // Collect form data
    const formData = {
        age: parseInt(document.getElementById('age').value),
        current_year: parseInt(document.getElementById('current_year').value),
        graduation_year: parseInt(document.getElementById('graduation_year').value),
        loan_duration_years: parseInt(document.getElementById('loan_duration_years').value),
        investment_amount: parseFloat(document.getElementById('investment_amount').value),
        investment_growth_high: parseFloat(document.getElementById('investment_growth_high').value),
        investment_growth_low: parseFloat(document.getElementById('investment_growth_low').value),
        investment_growth_average: parseFloat(document.getElementById('investment_growth_average').value),
        investment_amount_growth: 0.0,  // Fixed at 0 - field removed from form
        pre_tax_income: parseFloat(document.getElementById('pre_tax_income').value),
        salary_growth_optimistic: parseFloat(document.getElementById('salary_growth_optimistic').value),
        salary_growth_pessimistic: parseFloat(document.getElementById('salary_growth_pessimistic').value),
        initial_loan_balance: parseFloat(document.getElementById('initial_loan_balance').value),
        loan_interest_current: parseFloat(document.getElementById('loan_interest_current').value),
        loan_interest_high: parseFloat(document.getElementById('loan_interest_high').value),
        loan_interest_low: parseFloat(document.getElementById('loan_interest_low').value)
    };

    // Show loading
    showLoading();
    hideLoanError();

    try {
        // Call API
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.errors ? errorData.errors.join(', ') : 'Calculation failed');
        }

        const result = await response.json();

        // Display results
        displayResults(result);

    } catch (error) {
        showLoanError(error.message || 'An error occurred during calculation');
    } finally {
        hideLoading();
    }
}

/**
 * Handle income tax form submission
 */
async function handleIncomeTaxSubmit(event) {
    event.preventDefault();

    const form = event.target;
    let allValid = true;

    const numberInputs = form.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        if (input.value !== '') {
            if (!validateField.call(input)) {
                allValid = false;
            }
        } else if (input.required) {
            input.classList.add('is-invalid');
            allValid = false;
        }
    });

    const requiredSelects = form.querySelectorAll('select[required]');
    requiredSelects.forEach(select => {
        if (!select.value) {
            select.classList.add('is-invalid');
            allValid = false;
        } else {
            select.classList.remove('is-invalid');
        }
    });

    const pensionType = document.getElementById('pension_contribution_type').value;
    const pensionValueInput = document.getElementById('pension_contribution_value');
    if (pensionType !== 'none') {
        const pensionValue = parseFloat(pensionValueInput.value) || 0;
        if (pensionValue < 0 || (pensionType === 'percentage' && pensionValue > 100)) {
            pensionValueInput.classList.add('is-invalid');
            allValid = false;
        } else {
            pensionValueInput.classList.remove('is-invalid');
        }
    } else {
        pensionValueInput.classList.remove('is-invalid');
    }

    if (!allValid) {
        showTaxError('Please correct the errors in the form');
        return;
    }

    const formData = {
        gross_income: parseFloat(document.getElementById('tax_gross_income').value),
        bonus_annual: parseFloat(document.getElementById('bonus_annual').value) || 0,
        pay_frequency: document.getElementById('tax_pay_frequency').value,
        tax_jurisdiction: document.getElementById('tax_jurisdiction').value,
        ni_category: document.getElementById('ni_category').value,
        student_loan_plan: document.getElementById('student_loan_plan').value,
        pension_contribution_type: pensionType,
        pension_contribution_value: parseFloat(
            document.getElementById('pension_contribution_value').value
        ) || 0,
        other_pretax_deductions: parseFloat(
            document.getElementById('other_pretax_deductions').value
        ) || 0,
        tax_year: document.getElementById('tax_year').value
    };

    showLoading();
    hideTaxError();

    try {
        const response = await fetch('/api/income-tax/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.errors ? errorData.errors.join(', ') : 'Calculation failed');
        }

        const result = await response.json();
        displayIncomeTaxResults(result);

    } catch (error) {
        showTaxError(error.message || 'An error occurred during calculation');
    } finally {
        hideLoading();
    }
}

/**
 * Display calculation results
 */
function displayResults(data) {
    // Show results section
    const resultsSection = document.getElementById('results-section');
    resultsSection.classList.remove('d-none');

    // Display recommendation
    displayRecommendation(data.recommendation);

    // Render graph
    renderPayoffGraph(data);

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Display recommendation
 */
function displayRecommendation(recommendation) {
    const content = document.getElementById('recommendation-content');
    const card = document.getElementById('recommendation-card');

    // Update card styling based on decision
    card.classList.remove('warning', 'danger');
    if (recommendation.decision === 'pay_off_early') {
        card.classList.add('warning');
    }

    // Format net benefit
    const benefit = Math.abs(recommendation.net_benefit_amount);
    const benefitFormatted = new Intl.NumberFormat('en-GB', {
        style: 'currency',
        currency: 'GBP',
        maximumFractionDigits: 0
    }).format(benefit);

    // Build HTML
    content.innerHTML = `
        <div class="mb-3">
            <h3 class="h4">${getDecisionTitle(recommendation.decision)}</h3>
            <p class="lead">${recommendation.rationale}</p>
        </div>
        <div class="row">
            <div class="col-md-4">
                <strong>Net Benefit:</strong> ${benefitFormatted}
            </div>
            <div class="col-md-4">
                <strong>Confidence:</strong> ${recommendation.confidence.toUpperCase()}
            </div>
            ${recommendation.crossover_year ? `
            <div class="col-md-4">
                <strong>Crossover Year:</strong> ${recommendation.crossover_year}
            </div>
            ` : ''}
        </div>
    `;
}

/**
 * Get decision title
 */
function getDecisionTitle(decision) {
    const titles = {
        'invest': '📈 Invest Your Money',
        'pay_off_early': '💰 Pay Off Loan Early',
        'neutral': '⚖️ Either Option Works'
    };
    return titles[decision] || 'Recommendation';
}

/**
 * Show loading overlay
 */
function showLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.classList.remove('d-none');
    }
}

/**
 * Hide loading overlay
 */
function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.classList.add('d-none');
    }
}

/**
 * Display error message
 */
function showLoanError(message) {
    const errorDiv = document.getElementById('loan-form-errors');
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.classList.remove('d-none');
    }
}

function hideLoanError() {
    const errorDiv = document.getElementById('loan-form-errors');
    if (errorDiv) {
        errorDiv.classList.add('d-none');
    }
}

function showTaxError(message) {
    const errorDiv = document.getElementById('tax-form-errors');
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.classList.remove('d-none');
    }
}

function hideTaxError() {
    const errorDiv = document.getElementById('tax-form-errors');
    if (errorDiv) {
        errorDiv.classList.add('d-none');
    }
}

/**
 * Get CSRF token from cookie
 */
function getCsrfToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Render payoff graph with Chart.js
 */
function renderPayoffGraph(data) {
    const ctx = document.getElementById('payoff-chart');
    if (!ctx || !data.optimistic || !data.pessimistic || !data.realistic) {
        console.error('Cannot render graph: missing data or canvas element');
        return;
    }

    // Destroy existing chart if it exists
    if (payoffChart) {
        payoffChart.destroy();
    }

    // Extract years and data from realistic scenario
    const years = data.realistic.yearly_data.map(y => y.year);

    // Prepare datasets
    const datasets = [
        {
            label: 'Optimistic Loan Balance',
            data: data.optimistic.yearly_data.map(y => y.loan_balance),
            borderColor: 'rgba(40, 167, 69, 1)',
            backgroundColor: 'rgba(40, 167, 69, 0.1)',
            borderWidth: 2,
            tension: 0.4,
            fill: false,
            yAxisID: 'y'
        },
        {
            label: 'Realistic Loan Balance',
            data: data.realistic.yearly_data.map(y => y.loan_balance),
            borderColor: 'rgba(13, 110, 253, 1)',
            backgroundColor: 'rgba(13, 110, 253, 0.2)',
            borderWidth: 3,
            tension: 0.4,
            fill: '-1',  // Fill to previous dataset (creates uncertainty band)
            yAxisID: 'y'
        },
        {
            label: 'Pessimistic Loan Balance',
            data: data.pessimistic.yearly_data.map(y => y.loan_balance),
            borderColor: 'rgba(220, 53, 69, 1)',
            backgroundColor: 'rgba(220, 53, 69, 0.1)',
            borderWidth: 2,
            tension: 0.4,
            fill: '-1',  // Fill to previous dataset (creates uncertainty band)
            yAxisID: 'y'
        },
        {
            label: 'Investment Value - Optimistic',
            data: data.optimistic.yearly_data.map(y => y.investment_value),
            borderColor: 'rgba(255, 193, 7, 0.7)',
            backgroundColor: 'rgba(255, 193, 7, 0.1)',
            borderWidth: 1,
            borderDash: [3, 3],
            tension: 0.4,
            fill: false,
            yAxisID: 'y'
        },
        {
            label: 'Investment Value - Realistic',
            data: data.realistic.yearly_data.map(y => y.investment_value),
            borderColor: 'rgba(255, 193, 7, 1)',
            backgroundColor: 'rgba(255, 193, 7, 0.2)',
            borderWidth: 3,
            borderDash: [5, 5],
            tension: 0.4,
            fill: '-1',  // Fill to previous dataset (creates uncertainty band)
            yAxisID: 'y'
        },
        {
            label: 'Investment Value - Pessimistic',
            data: data.pessimistic.yearly_data.map(y => y.investment_value),
            borderColor: 'rgba(255, 193, 7, 0.7)',
            backgroundColor: 'rgba(255, 193, 7, 0.1)',
            borderWidth: 1,
            borderDash: [3, 3],
            tension: 0.4,
            fill: '-1',  // Fill to previous dataset (creates uncertainty band)
            yAxisID: 'y'
        }
    ];

    // Create chart
    payoffChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: years,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Loan Balance vs Investment Value Over Time',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                tooltip: {
                    enabled: true,
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            label += new Intl.NumberFormat('en-GB', {
                                style: 'currency',
                                currency: 'GBP',
                                maximumFractionDigits: 0
                            }).format(context.parsed.y);
                            return label;
                        }
                    }
                },
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        usePointStyle: true,
                        padding: 15
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Year',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    ticks: {
                        callback: function(value, index) {
                            // Show fewer labels on mobile
                            if (window.innerWidth < 768) {
                                return index % 5 === 0 ? this.getLabelForValue(value) : '';
                            }
                            return this.getLabelForValue(value);
                        }
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Amount (£)',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    ticks: {
                        callback: function(value) {
                            return '£' + value.toLocaleString('en-GB', {
                                maximumFractionDigits: 0
                            });
                        }
                    },
                    beginAtZero: true
                }
            }
        }
    });

    // Add crossover annotation if exists
    if (data.recommendation.crossover_year) {
        addCrossoverAnnotation(data.recommendation.crossover_year);
    }
}

/**
 * Display income tax calculation results
 */
function displayIncomeTaxResults(data) {
    const resultsSection = document.getElementById('tax-results-section');
    resultsSection.classList.remove('d-none');

    const currencyFormatter = new Intl.NumberFormat('en-GB', {
        style: 'currency',
        currency: 'GBP',
        maximumFractionDigits: 2
    });

    document.getElementById('tax-summary-year').textContent = data.tax_year;
    document.getElementById('summary-gross').textContent = currencyFormatter.format(data.gross_annual);
    document.getElementById('summary-taxable').textContent = currencyFormatter.format(data.taxable_annual);
    document.getElementById('summary-total-deductions').textContent = currencyFormatter.format(
        data.total_deductions_annual
    );
    document.getElementById('summary-income-tax').textContent = currencyFormatter.format(data.income_tax_annual);
    document.getElementById('summary-ni').textContent = currencyFormatter.format(data.ni_annual);
    document.getElementById('summary-student-loan').textContent = currencyFormatter.format(
        data.student_loan_annual
    );
    document.getElementById('summary-net-annual').textContent = currencyFormatter.format(data.net_annual);
    document.getElementById('summary-net-monthly').textContent = currencyFormatter.format(data.net_monthly);
    document.getElementById('summary-net-weekly').textContent = currencyFormatter.format(data.net_weekly);
    document.getElementById('summary-effective-rate').textContent = `${
        (data.effective_deduction_rate * 100).toFixed(2)
    }%`;

    const incomeTaxBody = document.getElementById('income-tax-breakdown');
    incomeTaxBody.innerHTML = '';
    data.income_tax_bands.forEach(band => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${band.band_name}</td>
            <td>${(band.rate * 100).toFixed(2)}%</td>
            <td>${currencyFormatter.format(band.taxable_amount)}</td>
            <td>${currencyFormatter.format(band.amount)}</td>
        `;
        incomeTaxBody.appendChild(row);
    });

    const niBody = document.getElementById('ni-breakdown');
    niBody.innerHTML = '';
    data.ni_bands.forEach(band => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${band.band_name}</td>
            <td>${(band.rate * 100).toFixed(2)}%</td>
            <td>${currencyFormatter.format(band.taxable_amount)}</td>
            <td>${currencyFormatter.format(band.amount)}</td>
        `;
        niBody.appendChild(row);
    });

    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Add crossover year annotation to graph (future enhancement)
 */
function addCrossoverAnnotation(crossoverYear) {
    // This would require Chart.js annotation plugin
    // For MVP, we display crossover in the recommendation card
    console.log('Crossover year:', crossoverYear);
}

/**
 * Get CSRF token from cookie or meta tag
 */
function getCsrfToken() {
    // Try to get from cookie first
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='));

    if (cookieValue) {
        return cookieValue.split('=')[1];
    }

    // Fall back to meta tag
    const metaTag = document.querySelector('meta[name="csrf-token"]');
    return metaTag ? metaTag.getAttribute('content') : '';
}

async function handleRentVsBuySubmit(event) {
    event.preventDefault();
    clearFormError('rent-vs-buy-errors');

    const form = event.target;
    const inputs = form.querySelectorAll('input[type="number"]');
    let allValid = true;
    inputs.forEach(input => {
        if (!validateField.call(input)) {
            allValid = false;
        }
    });

    if (!allValid) {
        showFormError('rent-vs-buy-errors', 'Please correct the errors in the form');
        return;
    }

    const payload = {
        property_price: parseFloat(document.getElementById('rvb_property_price').value),
        deposit_amount: parseFloat(document.getElementById('rvb_deposit_amount').value),
        mortgage_rate: parseFloat(document.getElementById('rvb_mortgage_rate').value) / 100,
        mortgage_term_years: parseInt(document.getElementById('rvb_mortgage_term').value),
        monthly_rent: parseFloat(document.getElementById('rvb_monthly_rent').value),
        rent_growth_rate: parseFloat(document.getElementById('rvb_rent_growth').value) / 100,
        home_appreciation_rate: parseFloat(document.getElementById('rvb_home_growth').value) / 100,
        maintenance_rate: parseFloat(document.getElementById('rvb_maintenance_rate').value) / 100,
        property_tax_rate: parseFloat(document.getElementById('rvb_property_tax_rate').value) / 100,
        insurance_annual: parseFloat(document.getElementById('rvb_insurance_annual').value),
        buying_costs: parseFloat(document.getElementById('rvb_buying_costs').value),
        selling_costs: parseFloat(document.getElementById('rvb_selling_costs').value),
        investment_return_rate: parseFloat(document.getElementById('rvb_investment_return').value) / 100,
        analysis_years: parseInt(document.getElementById('rvb_analysis_years').value),
    };

    showLoading();
    try {
        const data = await postJson('/api/rent-vs-buy/calculate', payload);
        displayRentVsBuyResults(data);
    } catch (error) {
        showFormError('rent-vs-buy-errors', error.message || 'Unable to calculate rent vs buy.');
    } finally {
        hideLoading();
    }
}

function displayRentVsBuyResults(data) {
    const section = document.getElementById('rent-vs-buy-results');
    section.classList.remove('d-none');

    document.getElementById('rvb-summary-text').textContent = data.summary;
    document.getElementById('rvb-total-rent').textContent = formatCurrency(data.total_cost_rent);
    document.getElementById('rvb-total-buy').textContent = formatCurrency(data.total_cost_buy);
    document.getElementById('rvb-net-rent').textContent = formatCurrency(data.net_worth_rent);
    document.getElementById('rvb-net-buy').textContent = formatCurrency(data.net_worth_buy);
    document.getElementById('rvb-break-even').textContent =
        data.break_even_year ? `${data.break_even_year} years` : 'Not within range';

    renderRentVsBuyChart(data.graph_series);
    section.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function renderRentVsBuyChart(series) {
    const ctx = document.getElementById('rent-vs-buy-chart');
    if (!ctx) return;

    if (rentVsBuyChart) {
        rentVsBuyChart.destroy();
    }

    const labels = series.map(point => `Year ${point.year}`);
    const rentValues = series.map(point => point.rent_value);
    const buyValues = series.map(point => point.buy_value);

    rentVsBuyChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets: [
                {
                    label: 'Rent Net Worth',
                    data: rentValues,
                    borderColor: 'rgba(13, 110, 253, 1)',
                    backgroundColor: 'rgba(13, 110, 253, 0.2)',
                    borderWidth: 2,
                    tension: 0.3
                },
                {
                    label: 'Buy Net Worth',
                    data: buyValues,
                    borderColor: 'rgba(25, 135, 84, 1)',
                    backgroundColor: 'rgba(25, 135, 84, 0.2)',
                    borderWidth: 2,
                    tension: 0.3
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    ticks: {
                        callback: function(value) {
                            return '£' + value.toLocaleString('en-GB', { maximumFractionDigits: 0 });
                        }
                    }
                }
            }
        }
    });
}

async function handleEmergencyFundSubmit(event) {
    event.preventDefault();
    clearFormError('emergency-fund-errors');

    const form = event.target;
    const inputs = form.querySelectorAll('input[type="number"]');
    let allValid = true;
    inputs.forEach(input => {
        if (!validateField.call(input)) {
            allValid = false;
        }
    });

    if (!allValid) {
        showFormError('emergency-fund-errors', 'Please correct the errors in the form');
        return;
    }

    const payload = {
        monthly_expenses: parseFloat(document.getElementById('ef_monthly_expenses').value),
        target_months: parseInt(document.getElementById('ef_target_months').value),
        current_savings: parseFloat(document.getElementById('ef_current_savings').value || 0)
    };

    showLoading();
    try {
        const data = await postJson('/api/emergency-fund/calculate', payload);
        displayEmergencyFundResults(data);
    } catch (error) {
        showFormError('emergency-fund-errors', error.message || 'Unable to calculate emergency fund.');
    } finally {
        hideLoading();
    }
}

function displayEmergencyFundResults(data) {
    const section = document.getElementById('emergency-fund-results');
    section.classList.remove('d-none');

    document.getElementById('ef-target-fund').textContent = formatCurrency(data.target_fund);
    document.getElementById('ef-savings-gap').textContent = formatCurrency(data.savings_gap);
    document.getElementById('ef-coverage').textContent =
        data.coverage_months ? `${Number(data.coverage_months).toFixed(1)} months` : 'N/A';

    section.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

async function handleResilienceSubmit(event) {
    event.preventDefault();
    clearFormError('resilience-errors');

    const form = event.target;
    const inputs = form.querySelectorAll('input[type="number"]');
    let allValid = true;
    inputs.forEach(input => {
        if (!validateField.call(input)) {
            allValid = false;
        }
    });

    if (!allValid) {
        showFormError('resilience-errors', 'Please correct the errors in the form');
        return;
    }

    const payload = {
        savings: parseFloat(document.getElementById('rs_savings').value),
        income_stability: parseInt(document.getElementById('rs_income_stability').value),
        debt_load: parseFloat(document.getElementById('rs_debt_load').value),
        insurance_coverage: parseInt(document.getElementById('rs_insurance').value)
    };

    showLoading();
    try {
        const data = await postJson('/api/resilience-score/calculate', payload);
        displayResilienceResults(data);
    } catch (error) {
        showFormError('resilience-errors', error.message || 'Unable to calculate resilience score.');
    } finally {
        hideLoading();
    }
}

function displayResilienceResults(data) {
    const section = document.getElementById('resilience-results');
    section.classList.remove('d-none');

    document.getElementById('rs-index').textContent = `${data.resilience_index}/100`;
    document.getElementById('rs-summary').textContent = data.summary;

    const weakPoints = document.getElementById('rs-weak-points');
    weakPoints.innerHTML = '';
    if (data.weak_points.length === 0) {
        weakPoints.innerHTML = '<li class="text-success">No weak points detected</li>';
    } else {
        data.weak_points.forEach(point => {
            const li = document.createElement('li');
            li.textContent = point;
            weakPoints.appendChild(li);
        });
    }

    section.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

async function handleFreedomSubmit(event) {
    event.preventDefault();
    clearFormError('freedom-errors');

    const form = event.target;
    const inputs = form.querySelectorAll('input[type="number"]');
    let allValid = true;
    inputs.forEach(input => {
        if (!validateField.call(input)) {
            allValid = false;
        }
    });

    if (!allValid) {
        showFormError('freedom-errors', 'Please correct the errors in the form');
        return;
    }

    const payload = {
        annual_expenses: parseFloat(document.getElementById('ff_annual_expenses').value),
        current_investments: parseFloat(document.getElementById('ff_current_investments').value),
        annual_contribution: parseFloat(document.getElementById('ff_annual_contribution').value),
        investment_return_rate: parseFloat(document.getElementById('ff_return_rate').value) / 100,
        safe_withdrawal_rate: parseFloat(document.getElementById('ff_withdrawal_rate').value) / 100
    };

    showLoading();
    try {
        const data = await postJson('/api/time-to-freedom/calculate', payload);
        displayFreedomResults(data);
    } catch (error) {
        showFormError('freedom-errors', error.message || 'Unable to calculate time-to-freedom.');
    } finally {
        hideLoading();
    }
}

function displayFreedomResults(data) {
    const section = document.getElementById('freedom-results');
    section.classList.remove('d-none');

    document.getElementById('ff-number').textContent = formatCurrency(data.freedom_number);
    document.getElementById('ff-timeline').textContent =
        data.years_to_freedom !== null ? `${data.years_to_freedom} years` : 'More than 60 years';
    document.getElementById('ff-summary').textContent = data.summary;

    renderFreedomChart(data.timeline_series);
    section.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function renderFreedomChart(series) {
    const ctx = document.getElementById('freedom-chart');
    if (!ctx) return;

    if (freedomChart) {
        freedomChart.destroy();
    }

    const labels = series.map(point => `Year ${point.year}`);
    const values = series.map(point => point.portfolio_value);

    freedomChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets: [
                {
                    label: 'Projected Portfolio',
                    data: values,
                    borderColor: 'rgba(255, 193, 7, 1)',
                    backgroundColor: 'rgba(255, 193, 7, 0.2)',
                    borderWidth: 2,
                    tension: 0.3
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    ticks: {
                        callback: function(value) {
                            return '£' + value.toLocaleString('en-GB', { maximumFractionDigits: 0 });
                        }
                    }
                }
            }
        }
    });
}
