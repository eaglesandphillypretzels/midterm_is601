from dataclasses import dataclass, field
import datetime
from decimal import Decimal, InvalidOperation
import logging
from typing import Any, Dict

from app.exceptions import OperationError


@dataclass
class Calculation:
    """
    This class encapsulates the basic elements of calculation results: operations as performed, operands used, the result of the calculation, and a recorded timestamp. It provides the methods for performing the calculation, serializing the data for storage, and deserializing the data to recreate a Calculation instance.
    """
    # Required fields
    operation: str
    operand1: Decimal
    operand2: Decimal

    # Fields with default values
    result: Decimal = field(init=False)
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

    def __post_init__(self):
        self.result = self.calculate()

    def _raise_div_zero(self):
        raise OperationError("Cannot divide by zero")

    def _raise_neg_power(self):
        raise OperationError("Negative exponent is not allowed for this operation")

    def _raise_invalid_root(self):
        raise OperationError("Invalid root operation")

    def _raise_invalid_modulus(self):
        raise OperationError("Invalid modulus operation")

    def calculate(self) -> Decimal:
        operations = {
            "Addition": lambda x, y: x + y,
            "Subtraction": lambda x, y: x - y,
            "Multiplication": lambda x, y: x * y,
            "Division": lambda x, y: x / y if y != 0 else self._raise_div_zero(),
            "Power": lambda x, y: Decimal(pow(float(x), float(y))) if y >= 0 else self._raise_neg_power(),
            "Root": lambda x, y: (
                Decimal(pow(float(x), 1 / float(y)))
                if x >= 0 and y != 0
                else self._raise_invalid_root()
            ),
            "Modulus": lambda x, y: x % y if y >= 0 else self._raise_invalid_modulus(),
            "Percent": lambda x, y: (x / y) * 100,
            "Absolute Difference": lambda x, y: abs(x - y),
        }

        op = operations.get(self.operation)
        if not op:
            raise OperationError(f"Unknown operation: {self.operation}")

        try:
            return op(self.operand1, self.operand2)
        except (InvalidOperation, ValueError, ArithmeticError) as e:
            raise OperationError(f"Calculation failed: {str(e)}")

