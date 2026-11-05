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