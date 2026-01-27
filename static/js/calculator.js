// Student Loan Payoff Calculator JavaScript

// Global chart instance
let payoffChart = null;

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
        form.addEventListener('submit', handleFormSubmit);

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
});

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
async function handleFormSubmit(event) {
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
        showError('Please correct the errors in the form');
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
    hideError();

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
        showError(error.message || 'An error occurred during calculation');
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
        overlay.classList.remove('hidden');
    }
}

/**
 * Hide loading overlay
 */
function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.classList.add('hidden');
    }
}

/**
 * Display error message
 */
function showError(message) {
    const errorDiv = document.getElementById('form-errors');
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.classList.remove('d-none');
    }
}

/**
 * Hide error message
 */
function hideError() {
    const errorDiv = document.getElementById('form-errors');
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
 * Add crossover year annotation to graph (future enhancement)
 */
function addCrossoverAnnotation(crossoverYear) {
    // This would require Chart.js annotation plugin
    // For MVP, we display crossover in the recommendation card
    console.log('Crossover year:', crossoverYear);
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
 * Show error message
 */
function showError(message) {
    const errorDiv = document.getElementById('error-message');
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.classList.remove('d-none');
        errorDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

/**
 * Hide error message
 */
function hideError() {
    const errorDiv = document.getElementById('error-message');
    if (errorDiv) {
        errorDiv.classList.add('d-none');
    }
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
