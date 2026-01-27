# Student Loan Payoff Calculator

Should you pay off your UK student loan early or invest the money instead? This calculator helps you decide by comparing both strategies across optimistic, realistic, and pessimistic scenarios.

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

1. Enter your personal details (age, graduation year, loan duration)
2. Add investment assumptions (annual amount, expected returns)
3. Provide income and loan details (salary, loan balance, repayment amount, interest rate)
4. Click "Calculate" to see an interactive chart comparing both strategies
5. Review the recommendation showing which strategy saves you more money

The calculator models UK Plan 2 student loans with realistic tax deductions (Income Tax, National Insurance) and shows you three scenarios to help you make an informed decision.

## Need Help?

Run the test suite to verify everything is working:
```bash
pytest
```

## License

MIT License
