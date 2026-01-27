# Student Loan Payoff Calculator

A Django-based UK Plan 2 student loan calculator that helps graduates decide whether to actively pay off their student loan or invest the money instead. The calculator models three economic scenarios (optimistic, realistic, pessimistic) over a customizable time horizon and visualizes the outcomes with interactive charts.

## Overview

This calculator solves a common financial dilemma for UK graduates: "Should I pay off my student loan early or invest that money?"

The tool compares two strategies:
- **Strategy A**: Make minimum loan repayments and invest surplus income
- **Strategy B**: Make accelerated loan repayments to pay off debt faster

It accounts for:
- UK Plan 2 loan terms (9% repayment above £27,295 threshold)
- Income tax and National Insurance deductions
- Real-world investment returns with uncertainty modeling
- Loan balance growth from interest
- Three economic scenarios to capture uncertainty

**Key Features**:
- Single-page responsive calculator with 11 input fields
- Interactive Chart.js visualization with uncertainty bands
- Stateless design (no user accounts or data storage)
- UK-specific tax rules and thresholds
- Mobile-optimized interface (Bootstrap 5)

## Technology Stack

- **Backend**: Python 3.13 + Django 5.1
- **Frontend**: Bootstrap 5.3.2 + Chart.js 4.4.1
- **Testing**: pytest 8.3.4 + pytest-django 4.9.0
- **Linting**: Ruff 0.8.4
- **Database**: SQLite (development and production)
- **Hosting**: Designed for deployment to Heroku, Render, or similar PaaS

## Project Structure

```
FinancePlanner/
├── calculator/              # Main Django app
│   ├── models.py           # Data structures (dataclasses)
│   ├── services.py         # Business logic (calculations)
│   ├── views.py            # HTTP request handlers
│   ├── validators.py       # Input validation functions
│   ├── urls.py             # URL routing
│   └── templates/
│       └── calculator/
│           ├── base.html   # Bootstrap layout
│           └── index.html  # Calculator form
├── config/                  # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── data/
│   └── uk_tax_thresholds.json  # UK tax configuration
├── static/
│   ├── css/calculator.css  # Custom styles
│   └── js/calculator.js    # Form handling + Chart.js
├── tests/
│   └── unit/calculator/    # 71 unit tests
├── specs/
│   └── 001-loan-payoff-calc/  # Feature specification
├── manage.py
├── requirements.txt
├── pyproject.toml
└── .env.example
```

## Setup Instructions

### Prerequisites

- Python 3.13 or higher
- [UV](https://github.com/astral-sh/uv) (fast Python package manager)
- Git

### Installation

1. **Install UV** (if not already installed):
   ```bash
   # Windows (PowerShell)
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/FinancePlanner.git
   cd FinancePlanner
   ```

3. **Create a virtual environment**:
   ```bash
   uv venv

   # Activate on Windows:
   .venv\Scripts\activate

   # Activate on macOS/Linux:
   source .venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   uv pip install -r requirements.txt
   ```

   **Note**: UV is 10-100x faster than pip. If you prefer traditional pip:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
5. **Configure environment variables**:
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env and set:
   # - SECRET_KEY (generate with: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
   # - DEBUG=True for development, False for production
   # - ALLOWED_HOSTS=localhost,127.0.0.1 for development
   ```

6. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

7. **Verify the installation**:
   ```bash
   # Run tests (should show 72 passing)
   pytest

   # Start the development server
   python manage.py runserver
   ```

8. **Open in browser**:
   Navigate to [http://localhost:8000/](http://localhost:8000/)

## Usage

### Basic Workflow

1. **Enter Personal Information**:
   - Current age (18-70)
   - Graduation year (1998-2030)
   - Desired loan duration (1-30 years)

2. **Configure Investment Assumptions**:
   - Annual investment amount (£0-£100,000)
   - Optimistic return rate (0-20%)
   - Pessimistic return rate (0-20%)

3. **Provide Income/Loan Details**:
   - Annual gross income (£0-£500,000)
   - Current loan balance (£0-£200,000)
   - Annual loan repayment (£0-£50,000)
   - Loan interest rate (0-10%)

4. **Submit and View Results**:
   - Interactive graph shows loan balance over time (3 scenarios)
   - Investment value overlay line
   - Uncertainty bands between optimistic/pessimistic outcomes
   - Recommendation: "Pay off loan" or "Invest instead" with savings amount

### Example Scenarios

**Scenario 1: Recent Graduate**
- Age: 23, Graduated: 2024, Duration: 15 years
- Investment: £5,000/year, Returns: 8% (optimistic) / 4% (pessimistic)
- Income: £30,000, Loan: £45,000, Repayment: £2,000/year, Interest: 5.5%

**Scenario 2: Mid-Career Professional**
- Age: 30, Graduated: 2017, Duration: 10 years
- Investment: £10,000/year, Returns: 10% (optimistic) / 3% (pessimistic)
- Income: £50,000, Loan: £35,000, Repayment: £5,000/year, Interest: 4.5%

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/calculator/test_services.py

# Run with coverage
pytest --cov=calculator

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Lint and format with Ruff
ruff check .
ruff format .

# Install pre-commit hooks
pre-commit install
pre-commit run --all-files
```

### Making Changes

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and write tests
3. Run tests: `pytest`
4. Format code: `ruff format .`
5. Commit with conventional commits: `cz commit`
6. Push and create pull request

## API Documentation

### POST /calculate

Calculate loan payoff scenarios and return projection data.

**Request Body** (JSON):
```json
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
```

**Response** (200 OK):
```json
{
  "optimistic": {
    "scenario_label": "optimistic",
    "final_loan_balance": 12450.30,
    "final_investment_value": 89234.12,
    "years": [
      {"year": 1, "loan_balance": 43200.00, "investment_value": 5400.00},
      ...
    ]
  },
  "realistic": { ... },
  "pessimistic": { ... },
  "recommendation": {
    "decision": "invest",
    "savings_amount": 15234.50,
    "reasoning": "Investing provides £15,234.50 more wealth after 15 years."
  }
}
```

**Error Responses**:
- `400 Bad Request`: Invalid input data (see error messages in response)
- `500 Internal Server Error`: Calculation failure

### GET /health

Health check endpoint for monitoring.

**Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Deployment

### Environment Variables

Required for production:
- `SECRET_KEY`: Django secret key (generate securely)
- `DEBUG`: Set to `False`
- `ALLOWED_HOSTS`: Comma-separated list of domains
- `DATABASE_URL`: (Optional) PostgreSQL connection string

### Deployment Platforms

**Heroku**:
```bash
heroku create your-app-name
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
git push heroku main
heroku run python manage.py migrate
```

**Render**:
1. Create new Web Service
2. Connect GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn config.wsgi:application`
5. Add environment variables in dashboard

### Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Configure `ALLOWED_HOSTS` with production domain
- [ ] Use strong `SECRET_KEY` (not the example one)
- [ ] Enable HTTPS (handled by PaaS)
- [ ] Run `python manage.py check --deploy`
- [ ] Verify health check endpoint: `/health`

## Architecture Decisions

### Why Stateless Design?

No user accounts or database persistence:
- **Simplicity**: Fewer moving parts = easier maintenance
- **Privacy**: No personal data stored = no GDPR compliance burden
- **Scalability**: Stateless services scale horizontally effortlessly
- **MVP Focus**: Validates core value prop without premature features

### Why SQLite for Production?

- **Read-only data**: UK tax thresholds rarely change
- **Low traffic**: Single-user calculations, no concurrent writes
- **YAGNI principle**: Don't add PostgreSQL until proven necessary
- **Zero ops**: No database hosting costs or maintenance

### Why No Frontend Framework?

- **Vanilla JS + Bootstrap**: Adequate for single-page calculator
- **Lower complexity**: No build pipeline, transpilation, or npm hell
- **Faster initial load**: CDN-served libraries, no bundle bloat
- **YAGNI**: React/Vue overkill for this use case

## Contributing

This project follows the SpecKit methodology:
1. Features defined in `specs/` directory
2. Code-first development (implement before tests)
3. Unit tests only (no integration/E2E)
4. SOLID principles and YAGNI philosophy

See [specs/001-loan-payoff-calc/](specs/001-loan-payoff-calc/) for detailed feature specification.

## License

MIT License - see LICENSE file for details

## Support

For issues or questions:
- Open a GitHub issue
- Email: support@example.com
- Documentation: See `specs/` folder for detailed specifications

## Acknowledgements

- UK Student Loans Company for loan terms documentation
- Chart.js team for excellent visualization library
- Django community for robust web framework
