import pytest
from decimal import Decimal
from typing import Any, Dict, Type

from app.exceptions import ValidationError
from app.operations import (
    Operation,
    Addition,
    Subtraction,
    Multiplication,
    Division,
    Power,
    Root,
    Modulus,
    Percent,
    AbsoluteDifference,
    OperationFactory,
)


class TestOperation:
    """Test base Operation class functionality."""

    def test_str_representation(self):
        """Test that string representation returns class name."""
        class TestOp(Operation):
            def execute(self, a: Decimal, b: Decimal) -> Decimal:
                return a

        assert str(TestOp()) == "TestOp"


class BaseOperationTest:
    """Base test class for all operations."""

    operation_class: Type[Operation]
    valid_test_cases: Dict[str, Dict[str, Any]]
    invalid_test_cases: Dict[str, Dict[str, Any]]

    def test_valid_operations(self):
        """Test operation with valid inputs."""
        operation = self.operation_class()
        for name, case in self.valid_test_cases.items():
            a = Decimal(str(case["a"]))
            b = Decimal(str(case["b"]))
            expected = Decimal(str(case["expected"]))
            result = operation.execute(a, b)
            assert result == expected, f"Failed case: {name}"

    def test_invalid_operations(self):
        """Test operation with invalid inputs raises appropriate errors."""
        operation = self.operation_class()
        for name, case in self.invalid_test_cases.items():
            a = Decimal(str(case["a"]))
            b = Decimal(str(case["b"]))
            error = case.get("error", ValidationError)
            error_message = case.get("message", "")

            with pytest.raises(error, match=error_message):
                operation.execute(a, b)


class TestAddition(BaseOperationTest):
    """Test Addition operation."""

    operation_class = Addition
    valid_test_cases = {
        "positive_numbers": {"a": "5", "b": "3", "expected": "8"},
        "negative_numbers": {"a": "-5", "b": "-3", "expected": "-8"},
        "mixed_signs": {"a": "-5", "b": "3", "expected": "-2"},
        "zero_sum": {"a": "5", "b": "-5", "expected": "0"},
        "decimals": {"a": "5.5", "b": "3.3", "expected": "8.8"},
        "large_numbers": {
            "a": "1e10",
            "b": "1e10",
            "expected": "20000000000"
        },
    }
    invalid_test_cases = {}  # Addition has no invalid cases


class TestSubtraction(BaseOperationTest):
    """Test Subtraction operation."""

    operation_class = Subtraction
    valid_test_cases = {
        "positive_numbers": {"a": "5", "b": "3", "expected": "2"},
        "negative_numbers": {"a": "-5", "b": "-3", "expected": "-2"},
        "mixed_signs": {"a": "-5", "b": "3", "expected": "-8"},
        "zero_result": {"a": "5", "b": "5", "expected": "0"},
        "decimals": {"a": "5.5", "b": "3.3", "expected": "2.2"},
        "large_numbers": {
            "a": "1e10",
            "b": "1e9",
            "expected": "9000000000"
        },
    }
    invalid_test_cases = {}  # Subtraction has no invalid cases


class TestMultiplication(BaseOperationTest):
    """Test Multiplication operation."""

    operation_class = Multiplication
    valid_test_cases = {
        "positive_numbers": {"a": "5", "b": "3", "expected": "15"},
        "negative_numbers": {"a": "-5", "b": "-3", "expected": "15"},
        "mixed_signs": {"a": "-5", "b": "3", "expected": "-15"},
        "multiply_by_zero": {"a": "5", "b": "0", "expected": "0"},
        "decimals": {"a": "5.5", "b": "3.3", "expected": "18.15"},
        "large_numbers": {
            "a": "1e5",
            "b": "1e5",
            "expected": "10000000000"
        },
    }
    invalid_test_cases = {}  # Multiplication has no invalid cases


class TestDivision(BaseOperationTest):
    """Test Division operation."""

    operation_class = Division
    valid_test_cases = {
        "positive_numbers": {"a": "6", "b": "2", "expected": "3"},
        "negative_numbers": {"a": "-6", "b": "-2", "expected": "3"},
        "mixed_signs": {"a": "-6", "b": "2", "expected": "-3"},
        "decimals": {"a": "5.5", "b": "2", "expected": "2.75"},
        "divide_zero": {"a": "0", "b": "5", "expected": "0"},
    }
    invalid_test_cases = {
        "divide_by_zero": {
            "a": "5",
            "b": "0",
            "error": ValidationError,
            "message": "Division by zero is not allowed"
        },
    }


class TestPower(BaseOperationTest):
    """Test Power operation."""

    operation_class = Power
    valid_test_cases = {
        "positive_integers": {"a": "2", "b": "3", "expected": "8"},
        "negative_base": {"a": "-2", "b": "3", "expected": "-8"},
        "fractional_exponent": {"a": "9", "b": "0.5", "expected": "3"},
        "zero_power": {"a": "5", "b": "0", "expected": "1"},
        "zero_base": {"a": "0", "b": "5", "expected": "0"},
    }
    invalid_test_cases = {
        "negative_exponent": {
            "a": "4",
            "b": "-1",
            "error": ValidationError,
            "message": "Negative exponents are not allowed for this operation"
        },
    }


class TestRoot(BaseOperationTest):
    """Test Root operation."""

    operation_class = Root
    valid_test_cases = {
        "square_root": {"a": "9", "b": "2", "expected": "3"},
        "cube_root": {"a": "8", "b": "3", "expected": "2"},
        "zero_root": {"a": "0", "b": "5", "expected": "0"},
        "positive_radicand": {"a": "8", "b": "3", "expected": "2"},
    }
    invalid_test_cases = {
        "negative_index": {
            "a": "8",
            "b": "-1",
            "error": ValidationError,
            "message": "Root index cannot be negative"
        },
        "zero_index": {
            "a": "8",
            "b": "0",
            "error": ValidationError,
            "message": "Root index cannot be zero"
        },
    }


class TestModulus(BaseOperationTest):
    """Test Modulus operation."""

    operation_class = Modulus
    valid_test_cases = {
        "positive_numbers": {"a": "7", "b": "3", "expected": "1"},
        "negative_numbers": {"a": "-7", "b": "3", "expected": "-1"},
        "zero_remainder": {"a": "8", "b": "4", "expected": "0"},
        "decimal_remainder": {"a": "7.5", "b": "2.5", "expected": "0"},
    }
    invalid_test_cases = {
        "divide_by_zero": {
            "a": "5",
            "b": "0",
            "error": ValidationError,
            "message": "Modulus by zero is not allowed"
        },
    }


class TestAbsoluteDifference(BaseOperationTest):
    """Test Absolute Difference operation."""

    operation_class = AbsoluteDifference
    valid_test_cases = {
        "positive_numbers": {"a": "5", "b": "3", "expected": "2"},
        "negative_numbers": {"a": "-5", "b": "-3", "expected": "2"},
        "mixed_signs": {"a": "-5", "b": "3", "expected": "8"},
        "zero_difference": {"a": "5", "b": "5", "expected": "0"},
        "decimals": {"a": "5.5", "b": "3.3", "expected": "2.2"},
    }
    invalid_test_cases = {}


class TestOperationFactory:
    """Test operation factory."""

    def test_create_addition(self):
        assert isinstance(OperationFactory.create("+"), Addition)

    def test_create_subtraction(self):
        assert isinstance(OperationFactory.create("-"), Subtraction)

    def test_create_multiplication(self):
        assert isinstance(OperationFactory.create("*"), Multiplication)

    def test_create_division(self):
        assert isinstance(OperationFactory.create("/"), Division)

    def test_create_power(self):
        assert isinstance(OperationFactory.create("^"), Power)

    def test_create_root(self):
        assert isinstance(OperationFactory.create("root"), Root)

    def test_create_modulus(self):
        assert isinstance(OperationFactory.create("%"), Modulus)

    def test_create_absolute_difference(self):
        assert isinstance(OperationFactory.create("absdiff"), AbsoluteDifference)

    def test_create_invalid_operation(self):
        with pytest.raises(ValidationError, match="Unsupported operation"):
            OperationFactory.create("invalid")

def test_modulus_negative_divisor():
    op = Modulus()
    with pytest.raises(ValidationError, match="Cannot perform modulus operation with a negative divisor."):
        op.execute(Decimal("5"), Decimal("-2"))

def test_percent_zero_division():
    op = Percent()
    with pytest.raises(ValidationError, match="Percent calculation cannot divide by zero."):
        op.execute(Decimal("5"), Decimal("0"))

def test_get_available_operations():
    ops = OperationFactory.get_available_operations()
    assert isinstance(ops, dict)
    assert "Addition" in ops

