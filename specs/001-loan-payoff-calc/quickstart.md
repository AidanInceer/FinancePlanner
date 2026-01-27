# Quickstart Guide: Student Loan Payoff Calculator

**Purpose**: Get developers up and running with the project in under 10 minutes
**Prerequisites**: Python 3.13+, Git, text editor/IDE
**Date**: 2026-01-26

---

## 1. Clone and Setup (2 minutes)

```powershell
# Clone repository
git clone <repository_url>
cd FinancePlanner

# Checkout feature branch
git checkout 001-loan-payoff-calc

# Create virtual environment
python -m venv .venv

# Activate virtual environment (PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate virtual environment (Unix/Mac)
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 2. Project Structure Overview (1 minute)

```text
FinancePlanner/
├── financeplanner/          # Django project
│   ├── calculator/          # Calculator app (main feature)
│   │   ├── services.py      # Business logic (loan/investment calculations)
│   │   ├── validators.py    # Input validation
│   │   ├── views.py         # Django views and API endpoint
│   │   └── templates/       # HTML templates (Bootstrap)
│   └── config/              # Django settings
├── data/                    # UK tax configuration
│   └── uk_tax_thresholds.json
├── static/                  # CSS and JavaScript
│   ├── css/calculator.css
│   └── js/calculator.js     # Chart.js rendering
├── tests/                   # Unit tests
│   └── unit/calculator/
├── manage.py                # Django management
└── requirements.txt         # Python dependencies
```

---

## 3. Initialize Django Project (2 minutes)

```powershell
# Run migrations to set up database
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

---

## 4. Run Development Server (1 minute)

```powershell
# Start Django development server
python manage.py runserver

# Server will start at http://localhost:8000
# Open in browser: http://localhost:8000
```

**Expected Output:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
January 26, 2026 - 14:30:00
Django version 5.1, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## 5. Verify Installation (2 minutes)

### Test 1: Home Page

Visit http://localhost:8000 in your browser

**Expected**: Bootstrap-styled calculator form with input fields for:
- Age, graduation year, loan duration
- Investment amount and growth rates
- Income and loan details

### Test 2: Health Check

```powershell
# Test health endpoint
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-26T14:30:00Z"
}
```

### Test 3: API Calculation (via curl or Postman)

```powershell
# Test calculation API
curl -X POST http://localhost:8000/api/calculate `
  -H "Content-Type: application/json" `
  -d '{
    "age": 25,
    "graduation_year": 2023,
    "loan_duration_years": 35,
    "investment_amount": 50000,
    "investment_growth_high": 8.0,
    "investment_growth_low": 4.0,
    "pre_tax_income": 45000,
    "loan_repayment_annual": 2400,
    "loan_interest_current": 5.5,
    "loan_interest_high": 7.0,
    "loan_interest_low": 3.0
  }'
```

**Expected**: JSON response with `optimistic`, `pessimistic`, `realistic` scenarios and `recommendation`

---

## 6. Run Unit Tests (2 minutes)

```powershell
# Run all unit tests
pytest

# Run with coverage report
pytest --cov=financeplanner --cov-report=term-missing

# Run specific test module
pytest tests/unit/calculator/test_services.py

# Run in verbose mode
pytest -v
```

**Expected Output:**
```
======================== test session starts ========================
collected 15 items

tests/unit/calculator/test_services.py ........... [ 73%]
tests/unit/calculator/test_validators.py .... [100%]

======================== 15 passed in 2.35s =========================
```

---

## 7. Code Quality Checks (1 minute)

```powershell
# Run Ruff linting
ruff check .

# Run Ruff formatting check
ruff format --check .

# Auto-fix Ruff issues
ruff check --fix .
ruff format .
```

---

## 8. Development Workflow

### Making Changes

1. **Create feature branch** (if not already on one):
   ```powershell
   git checkout -b <feature-name>
   ```

2. **Make code changes** in appropriate files:
   - Business logic: `calculator/services.py`
   - Validation: `calculator/validators.py`
   - Views/API: `calculator/views.py`
   - Frontend: `static/js/calculator.js`

3. **Run tests** to verify changes:
   ```powershell
   pytest tests/unit/calculator/
   ```

4. **Check code quality**:
   ```powershell
   ruff check . && ruff format .
   ```

5. **Commit changes** (use Commitizen format):
   ```powershell
   git add .
   git commit -m "feat(calculator): add crossover year detection"
   ```

### Pre-commit Hooks (Recommended)

```powershell
# Install pre-commit hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

Hooks will automatically run Ruff checks before each commit.

---

## 9. Common Issues & Solutions

### Issue: Virtual environment not activating

**Solution:**
```powershell
# PowerShell: Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
.\.venv\Scripts\Activate.ps1
```

### Issue: Module not found errors

**Solution:**
```powershell
# Ensure you're in the virtual environment
pip install -r requirements.txt --upgrade
```

### Issue: Port 8000 already in use

**Solution:**
```powershell
# Use different port
python manage.py runserver 8080

# Or find and kill process using port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue: Static files not loading

**Solution:**
```powershell
# Collect static files again
python manage.py collectstatic --clear --noinput
```

---

## 10. Key Dependencies

From `requirements.txt`:

```txt
Django>=5.1,<5.2          # Web framework
pytest>=8.0               # Testing framework
pytest-django>=4.8        # Django pytest integration
ruff>=0.2                 # Linting and formatting
pre-commit>=3.6           # Git hooks
commitizen>=3.13          # Conventional commits
```

Frontend (CDN - no installation needed):
- Bootstrap 5.3.2
- Chart.js 4.4.1

---

## 11. Next Steps

### For New Developers

1. **Read the spec**: [specs/001-loan-payoff-calc/spec.md](../spec.md)
2. **Review data model**: [specs/001-loan-payoff-calc/data-model.md](data-model.md)
3. **Check API contracts**: [specs/001-loan-payoff-calc/contracts/calculator-api.json](contracts/calculator-api.json)
4. **Review implementation plan**: [specs/001-loan-payoff-calc/plan.md](plan.md)

### For Implementation

1. **Phase 1**: Implement core calculation logic in `calculator/services.py`
2. **Phase 2**: Add input validation in `calculator/validators.py`
3. **Phase 3**: Create Django views and API endpoint
4. **Phase 4**: Build Bootstrap form and Chart.js visualization
5. **Phase 5**: Write unit tests for all modules

See [specs/001-loan-payoff-calc/tasks.md](tasks.md) for detailed task breakdown (generated by `/speckit.tasks`).

---

## 12. Useful Commands Reference

```powershell
# Django management
python manage.py runserver           # Start dev server
python manage.py migrate            # Run database migrations
python manage.py makemigrations     # Create new migrations
python manage.py shell              # Django Python shell
python manage.py test               # Run Django tests

# Testing
pytest                              # Run all tests
pytest -v                           # Verbose output
pytest --cov=financeplanner         # With coverage
pytest -k "test_validation"         # Run specific tests
pytest --lf                         # Run last failed tests

# Code quality
ruff check .                        # Lint code
ruff format .                       # Format code
ruff check --fix .                  # Auto-fix issues

# Pre-commit
pre-commit install                  # Install hooks
pre-commit run --all-files          # Run all hooks
pre-commit autoupdate               # Update hook versions

# Git (Commitizen)
git commit -m "type(scope): message"  # Conventional commit format
# Types: feat, fix, docs, style, refactor, test, chore
```

---

## 13. Development Environment

**Recommended IDE**: VS Code with extensions:
- Python (Microsoft)
- Pylance (Microsoft)
- Django (Baptiste Darthenay)
- Ruff (Astral Software)

**Python Version**: 3.13+ (check with `python --version`)

**Browser DevTools**: Use for testing frontend Chart.js rendering

---

## Support

- **Technical Issues**: Check GitHub Issues
- **Constitution**: See [.specify/memory/constitution.md](../../.specify/memory/constitution.md)
- **Planning Docs**: See [specs/001-loan-payoff-calc/](.)

---

**Total Setup Time**: ~10 minutes
**Status**: Ready for development ✅
