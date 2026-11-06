import pytest
from decimal import Decimal
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError
from app.input_validators import InputValidator

config = CalculatorConfig(max_input_value=Decimal('100000000'))

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

# Negative test cases for invalid inputs
def test_validate_invalid_string():
    with pytest.raises(ValidationError):
        InputValidator.validate_number(Decimal('invalid'), config)

def test_validate_number_too_large():
    with pytest.raises(ValidationError):
        InputValidator.validate_number(Decimal('100000001'), config)

def test_validate_number_too_small():
    with pytest.raises(ValidationError):
        InputValidator.validate_number(Decimal('-100000001'), config)

def 