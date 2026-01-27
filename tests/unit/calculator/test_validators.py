"""Unit tests for input validators."""

from decimal import Decimal

from calculator.validators import (
    validate_age,
    validate_non_negative_decimal,
    validate_percentage,
    validate_positive_integer,
    validate_rate_range,
    validate_year,
)


class TestValidateAge:
    """Tests for validate_age function."""

    def test_valid_age(self):
        """Test validation passes for valid ages."""
        is_valid, error = validate_age(25)
        assert is_valid is True
        assert error == ""

    def test_minimum_age(self):
        """Test validation passes for minimum age (18)."""
        is_valid, error = validate_age(18)
        assert is_valid is True
        assert error == ""

    def test_maximum_age(self):
        """Test validation passes for maximum age (100)."""
        is_valid, error = validate_age(100)
        assert is_valid is True
        assert error == ""

    def test_age_too_low(self):
        """Test validation fails for age below 18."""
        is_valid, error = validate_age(17)
        assert is_valid is False
        assert "between 18 and 100" in error

    def test_age_too_high(self):
        """Test validation fails for age above 100."""
        is_valid, error = validate_age(101)
        assert is_valid is False
        assert "between 18 and 100" in error

    def test_invalid_age_type(self):
        """Test validation fails for invalid type."""
        is_valid, error = validate_age("abc")
        assert is_valid is False
        assert "valid number" in error


class TestValidateYear:
    """Tests for validate_year function."""

    def test_valid_year(self):
        """Test validation passes for valid year."""
        is_valid, error = validate_year(2023)
        assert is_valid is True
        assert error == ""

    def test_custom_range(self):
        """Test validation with custom min/max."""
        is_valid, error = validate_year(2000, min_year=1990, max_year=2010)
        assert is_valid is True
        assert error == ""

    def test_year_out_of_range(self):
        """Test validation fails for year outside range."""
        is_valid, error = validate_year(1950, min_year=1980, max_year=2040)
        assert is_valid is False
        assert "between 1980 and 2040" in error


class TestValidatePercentage:
    """Tests for validate_percentage function."""

    def test_valid_percentage(self):
        """Test validation passes for valid percentage."""
        is_valid, error = validate_percentage(5.5)
        assert is_valid is True
        assert error == ""

    def test_zero_percentage(self):
        """Test validation passes for 0%."""
        is_valid, error = validate_percentage(0.0)
        assert is_valid is True
        assert error == ""

    def test_maximum_percentage(self):
        """Test validation passes for maximum percentage."""
        is_valid, error = validate_percentage(20.0)
        assert is_valid is True
        assert error == ""

    def test_percentage_too_high(self):
        """Test validation fails for percentage above max."""
        is_valid, error = validate_percentage(25.0)
        assert is_valid is False
        assert "between 0" in error and "20" in error

    def test_negative_percentage(self):
        """Test validation fails for negative percentage."""
        is_valid, error = validate_percentage(-1.0)
        assert is_valid is False
        assert "between 0" in error and "20" in error

    def test_percentage_as_decimal(self):
        """Test validation works with Decimal type."""
        is_valid, error = validate_percentage(Decimal("7.5"))
        assert is_valid is True
        assert error == ""


class TestValidateNonNegativeDecimal:
    """Tests for validate_non_negative_decimal function."""

    def test_positive_value(self):
        """Test validation passes for positive value."""
        is_valid, error = validate_non_negative_decimal(Decimal("1000.50"))
        assert is_valid is True
        assert error == ""

    def test_zero_value(self):
        """Test validation passes for zero."""
        is_valid, error = validate_non_negative_decimal(Decimal("0.00"))
        assert is_valid is True
        assert error == ""

    def test_negative_value(self):
        """Test validation fails for negative value."""
        is_valid, error = validate_non_negative_decimal(Decimal("-500.00"))
        assert is_valid is False
        assert "cannot be negative" in error

    def test_float_input(self):
        """Test validation works with float input."""
        is_valid, error = validate_non_negative_decimal(1234.56)
        assert is_valid is True
        assert error == ""


class TestValidatePositiveInteger:
    """Tests for validate_positive_integer function."""

    def test_valid_integer(self):
        """Test validation passes for valid integer."""
        is_valid, error = validate_positive_integer(25)
        assert is_valid is True
        assert error == ""

    def test_minimum_value(self):
        """Test validation passes for minimum value."""
        is_valid, error = validate_positive_integer(1)
        assert is_valid is True
        assert error == ""

    def test_maximum_value(self):
        """Test validation passes for maximum value."""
        is_valid, error = validate_positive_integer(50)
        assert is_valid is True
        assert error == ""

    def test_value_too_low(self):
        """Test validation fails for value below minimum."""
        is_valid, error = validate_positive_integer(0)
        assert is_valid is False
        assert "between 1 and 50" in error

    def test_value_too_high(self):
        """Test validation fails for value above maximum."""
        is_valid, error = validate_positive_integer(51)
        assert is_valid is False
        assert "between 1 and 50" in error


class TestValidateRateRange:
    """Tests for validate_rate_range function."""

    def test_valid_range(self):
        """Test validation passes when current is between low and high."""
        is_valid, error = validate_rate_range(3.0, 5.5, 7.0)
        assert is_valid is True
        assert error == ""

    def test_current_equals_low(self):
        """Test validation passes when current equals low."""
        is_valid, error = validate_rate_range(5.0, 5.0, 7.0)
        assert is_valid is True
        assert error == ""

    def test_current_equals_high(self):
        """Test validation passes when current equals high."""
        is_valid, error = validate_rate_range(3.0, 7.0, 7.0)
        assert is_valid is True
        assert error == ""

    def test_current_below_low(self):
        """Test validation fails when current is below low."""
        is_valid, error = validate_rate_range(5.0, 3.0, 7.0)
        assert is_valid is False
        assert "must be between low" in error

    def test_current_above_high(self):
        """Test validation fails when current is above high."""
        is_valid, error = validate_rate_range(3.0, 9.0, 7.0)
        assert is_valid is False
        assert "must be between low" in error
