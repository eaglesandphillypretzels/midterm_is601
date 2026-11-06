import pytest
from decimal import Decimal
from datetime import datetime
from app.calculation import Calculator
from app.exceptions import OperationError
import logging

def test_addition():
    calc = Calculator()
    result = calc.add(operation="Addition", operands=[Decimal('2.5'), Decimal('3.5')])
    assert result == Decimal('6.0')

def test_subtraction():
    calc = Calculator()
    result = calc.subtract(operation="Subtraction", operands=[Decimal('5.0'), Decimal('2.0')])
    assert result == Decimal('3.0')

def test_multiplication():
    calc = Calculator()
    result = calc.multiply(operation="Multiplication", operands=[Decimal('2.0'), Decimal('3.0')])
    assert result == Decimal('6.0')

def test_division():
    calc = Calculator()
    result = calc.divide(operation="Division", operands=[Decimal('6.0'), Decimal('2.0')])
    assert result == Decimal('3.0')

def test_division_by_zero():
    calc = Calculator()
    with pytest.raises(OperationError):
        calc.divide(operation="Division", operands=[Decimal('6.0'), Decimal('0.0')])

def test_power():
    calc = Calculator()
    result = calc.power(operation="Power", operands=[Decimal('2.0'), Decimal('3.0')])
    assert result == Decimal('8.0')

def test_negative_power():
    calc = Calculator()
    result = calc.power(operation="Power", operands=[Decimal('2.0'), Decimal('-3.0')])
    assert result == Decimal('0.125')

def test_square_root():
    calc = Calculator()
    result = calc.square_root(operation="Square Root", operands=[Decimal('16.0')])
    assert result == Decimal('4.0')

def test_invalid_square_root():
    calc = Calculator()
    with pytest.raises(OperationError, match="Cannot calculate the square root of a negative number."):
        calc.square_root(operation="Square Root", operands=[Decimal('-16.0')])

def test_modulus():
    calc = Calculator()
    result = calc.modulus(operation="Modulus", operands=[Decimal('10.0'), Decimal('3.0')])
    assert result == Decimal('1.0')

def test_invalid_modulus():
    calc = Calculator()
    with pytest.raises(OperationError, match="Cannot perform modulus operation with a divisor of zero."):
        calc.modulus(operation="Modulus", operands=[Decimal('10.0'), Decimal('0.0')])

def test_integer_division():
    calc = Calculator()
    result = calc.integer_division(operation="Integer Division", operands=[Decimal('7.0'), Decimal('2.0')])
    assert result == Decimal('3.0')

def test_invalid_integer_division():
    calc = Calculator()
    with pytest.raises(OperationError, match="Cannot perform integer division with a divisor of zero."):
        calc.integer_division(operation="Integer Division", operands=[Decimal('7.0'), Decimal('0.0')])

def test_percent():
    calc = Calculator()
    result = calc.percent(operation="Percent", operands=[Decimal('50.0'), Decimal('200.0')])
    assert result == Decimal('100.0')

def test_absolute_difference():
    calc = Calculator()
    result = calc.absolute_difference(operation="Absolute Difference", operands=[Decimal('5.0'), Decimal('3.0')])
    assert result == Decimal('2.0')

def test_unknown_operation():
    calc = Calculator()
    with pytest.raises(OperationError, match="Unknown operation: Unknown"):
        calc.add(operation="Unknown", operands=[Decimal('1.0'), Decimal('2.0')])

def test_to_dict():
    calc = Calculator()
    result = calc.to_dict(operation="Addition", operands=[Decimal('2.5'), Decimal('3.5')], result=Decimal('6.0'))
    assert result == {
        "operation": "Addition",
        "operands": [Decimal('2.5'), Decimal('3.5')],
        "result": Decimal('6.0'),
        "timestamp": result["timestamp"]  # We can't assert the exact timestamp, but we can check its presence
    }

def test_from_dict():
    calc = Calculator()
    data = {
        "operation": "Addition",
        "operands": [Decimal('2.5'), Decimal('3.5')],
        "result": Decimal('6.0'),
        "timestamp": datetime.now().isoformat()
    }
    calc = Calculation.from_dict(data)
    assert calc.operation == "Addition"
    assert calc.operands == [Decimal('2.5'), Decimal('3.5')]
    assert calc.result == Decimal('6.0')

def test_invalid_from_dict():
    data = {
        "operation": "Addition",
        "operands": [Decimal('2.5'), Decimal('3.5')],
        # Missing 'result' and 'timestamp'
    }
    with pytest.raises(OperationError, match="Invalid data for Calculation.from_dict: missing required fields."):
        Calculation.from_dict(data)

def test_format_result():
    calc = Calculator()
    result = calc.format_result(Decimal('6.0'))
    assert result == '6.0'

def test_equality():
    calc1 = Calculator()
    calc2 = Calculator()
    calc3 = Calculator()
    result1 = calc1.add(operation="Addition", operands=[Decimal('2.5'), Decimal('3.5')])
    result2 = calc2.add(operation="Addition", operands=[Decimal('2.5'), Decimal('3.5')])
    result3 = calc1.add(operation="Subtraction", operands=[Decimal('2.5'), Decimal('4.5')])
    assert result1 == result2
    assert result1 != result3

def test_logging(caplog):
    calc = Calculator()
    with caplog.at_level(logging.INFO):
        calc.add(operation="Addition", operands=[Decimal('2.5'), Decimal('3.5')])
    assert "Performed Addition on operands [Decimal('2.5'), Decimal('3.5')] with result Decimal('6.0')" in caplog.text

# Logging test for error handling
def test_logging_error(caplog):
    calc = Calculator()
    with caplog.at_level(logging.ERROR):
        with pytest.raises(OperationError):
            calc.divide(operation="Division", operands=[Decimal('6.0'), Decimal('0.0')])
    assert "Error during Division: Cannot divide by zero." in caplog.text

# Logging warning record test
def test_logging_warning(caplog):
    """
    Test that a warning is logged when a saved calculation 
    from the dictionary does not match the expected result.
    """
    # Arrange
    data = {
        "operation": "Addition",
        "operands": [Decimal('2.5'), Decimal('3.5')],
        "result": Decimal('5.0'),  # Intentionally incorrect result
        "timestamp": datetime.now().isoformat()
    }

    # Act
    with caplog.at_level(logging.WARNING):
        calc = Calculation.from_dict(data)

    # Assert
    assert "Warning: The result from the saved calculation does not match the expected result." in caplog.text

def test_calculation_overflow():
    calc = Calculator()
    with pytest.raises(OperationError, match="Calculation result overflowed the maximum allowed value."):
        calc.add(operation="Addition", operands=[Decimal('1e+1000'), Decimal('1e+1000')])

def test_format_result_invalid():
    """Test that formatting infinity or NaN raises an OperationError."""
    calc = Calculator()
    with pytest.raises(OperationError):
        calc.format_result(float('inf'))

def test_format_result_nan():
    """Test that formatting NaN raises an OperationError."""
    calc = Calculator()
    with pytest.raises(OperationError):
        calc.format_result(float('nan'))

# Quantizing Infinity raises an InvalidOperation error, so we need to handle that in the format_result method.
assert calc.format_result(Decimal('Infinity')) == 'Infinity'

def test_equality_not_implemented():
    """Test that equality comparison with a non-Calculation object returns NotImplemented."""
    calc = Calculator()
    result = calc.add(operation="Addition", operands=[Decimal('2.5'), Decimal('3.5')])
    assert (result == "not a calculation") is False

assert calc1 != "not a calculation"
assert calc1 != 5

def test_str_representation():
    calc = Calculator()
    result = calc.add(operation="Addition", operands=[Decimal('2.5'), Decimal('3.5')])
    assert str(result) == "Calculation(operation='Addition', operands=[Decimal('2.5'), Decimal('3.5')], result=Decimal('6.0'), timestamp=" + str(result.timestamp) + ")"

def test_repr_representation():
    calc = Calculator()
    result = calc.add(operation="Addition", operands=[Decimal('2.5'), Decimal('3.5')])
    assert repr(result) == "Calculation(operation='Addition', operands=[Decimal('2.5'), Decimal('3.5')], result=Decimal('6.0'), timestamp=" + str(result.timestamp) + ")"