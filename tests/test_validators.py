import pytest
from decimal import Decimal
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError
from app.input_validators import InputValidator

config = CalculatorConfig(max_input_value=Decimal('100000000'))

# Positive test cases for valid inputs

def test_validate_number_positive_integer():
    assert InputValidator.validate_number(Decimal('10'), config) == Decimal('10')

def test_validate_number_negative_integer():
    assert InputValidator.validate_number(Decimal('-10'), config) == Decimal('-10')

def test_validate_number_zero():
    assert InputValidator.validate_number(Decimal('0'), config) == Decimal('0')

def test_validate_number_positive_decimal():
    assert InputValidator.validate_number(Decimal('10.5'), config) == Decimal('10.5')

def test_validate_number_negative_decimal():
    assert InputValidator.validate_number(Decimal('-10.5'), config) == Decimal('-10.5')

def test_validate_positive_string():
    assert InputValidator.validate_number(Decimal('10'), config) == Decimal('10')

def test_validate_negative_string():
    assert InputValidator.validate_number(Decimal('-10'), config) == Decimal('-10')

def test_validate_zero_string():
    assert InputValidator.validate_number(Decimal('0'), config) == Decimal('0')

# Negative test cases for invalid inputs/edge cases

def test_validate_invalid_string():
    with pytest.raises(ValidationError, match="Invalid number format: 'invalid'"):
        InputValidator.validate_number(Decimal('invalid'), config)

def test_validate_number_too_large():
    with pytest.raises(ValidationError, match="Invalid number format: '100000001'"):
        InputValidator.validate_number(Decimal('100000001'), config)

def test_validate_number_too_small():
    with pytest.raises(ValidationError, match="Invalid number format: '-100000001'"):
        InputValidator.validate_number(Decimal('-100000001'), config)

def test_validate_number_non_numeric_string():
    with pytest.raises(ValidationError, match="Invalid number format: 'abc'"):
        InputValidator.validate_number(Decimal('abc'), config)

def test_validate_number_empty_string():
    with pytest.raises(ValidationError, match="Invalid number format: ''"):
        InputValidator.validate_number(Decimal(''), config)

def test_validate_negative_number_too_large():
    with pytest.raises(ValidationError, match="Invalid number format: '-100000001'"):
        InputValidator.validate_number(Decimal('-100000001'), config)

def test_validate_negative_number_too_small():
    with pytest.raises(ValidationError, match="Invalid number format: '-100000001'"):
        InputValidator.validate_number(Decimal('-100000001'), config)

def test_validate_number_with_special_characters():
    with pytest.raises(ValidationError, match="Invalid number format: '10@'"):
        InputValidator.validate_number(Decimal('10@'), config)

def test_validate_number_with_spaces():
    with pytest.raises(ValidationError, match="Invalid number format: ' 10 '"):
        InputValidator.validate_number(Decimal(' 10 '), config)

def test_validate_number_with_commas():
    with pytest.raises(ValidationError, match="Invalid number format: '1,000'"):
        InputValidator.validate_number(Decimal('1,000'), config)

def test_validate_number_whitespace_only():
    with pytest.raises(ValidationError, match="Invalid number format: '   '"):
        InputValidator.validate_number(Decimal('   '), config)
