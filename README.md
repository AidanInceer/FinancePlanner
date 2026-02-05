# FinancePlanner

FinancePlanner provides a suite of personal finance calculators for practical, scenario-based decisions.

## Quick Start

### Prerequisites

- Python 3.13+
- Git

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/FinancePlanner.git
   cd FinancePlanner
   ```

2. **Create and activate virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment**:
   ```bash
   # Windows
   copy .env.example .env

   # macOS/Linux
   cp .env.example .env
   ```

   Edit `.env` and generate a secret key:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. **Initialize database**:
   ```bash
   python manage.py migrate
   ```

6. **Start the server**:
   ```bash
   python manage.py runserver
   ```

7. **Open your browser**: Visit [http://localhost:8000/](http://localhost:8000/)

## How to Use

### Student Loan Payoff
1. Enter your personal details (age, graduation year, loan duration)
2. Add investment assumptions (annual amount, expected returns)
3. Provide income and loan details (salary, loan balance, repayment amount, interest rate)
4. Click "Calculate" to see an interactive chart comparing both strategies
5. Review the recommendation showing which strategy saves you more money

### UK Income Tax
1. Enter your income, pay frequency, and tax year
2. Add National Insurance and student loan selections
3. Click "Calculate" to see take-home pay and band breakdowns

### Rent vs Buy
1. Review the default purchase, rent, and investment assumptions
2. Adjust any inputs to match your scenario
3. Click "Compare" to see a summary and net worth projection graph

### Emergency Fund
1. Enter monthly expenses and target months
2. Add current savings (optional)
3. Click "Calculate" to see the target fund and savings gap

### Financial Resilience Score
1. Enter savings, income stability, debt load, and insurance coverage
2. Click "Calculate" to see your resilience index and weak points

### Time-to-Freedom
1. Enter annual expenses, investments, and contributions
2. Set investment return and safe withdrawal rate
3. Click "Calculate" to see your freedom number and timeline

## Need Help?

Run the test suite to verify everything is working:
```bash
pytest
```

## License

MIT License
