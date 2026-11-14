from dataclasses import dataclass, field
import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import logging
from typing import Any, Dict

from app.exceptions import OperationError, ValidationError
from app.operations import OperationFactory


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

    def calculate(self) -> Decimal:
        try:
            operation = OperationFactory.create(self.operation)
        except ValidationError as exc:
            raise OperationError(str(exc)) from exc

        try:
            if self.operation == "Root" and self.operand2 == 0:
                raise ValidationError("Division by zero is not allowed")
            return operation.execute(self.operand1, self.operand2)
        except ValidationError as exc:
            message = str(exc)
            if self.operation == "Root" and self.operand2 == 0:
                message = "Division by zero is not allowed"
            raise OperationError(message) from exc
        except (InvalidOperation, ValueError, ArithmeticError, TypeError) as exc:
            raise OperationError(f"Calculation failed: {str(exc)}") from exc

    def to_dict(self) -> Dict[str, str]:
        return {
            "operation": self.operation,
            "operand1": str(self.operand1),
            "operand2": str(self.operand2),
            "result": str(self.result),
            "timestamp": self.timestamp.isoformat(),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Calculation":
        try:
            calc = Calculation(
                operation=data["operation"],
                operand1 = Decimal(data['operand1']),
                operand2 = Decimal(data["operand2"])
            )

            calc.timestamp = datetime.datetime.fromisoformat(data["timestamp"])

            saved_result = Decimal(data['result'])
            if calc.result != saved_result:
                logging.warning(
                    f"Loaded calculation result {saved_result} "
                    f"differs from computed result {calc.result}"
                )  # pragma: no cover

            return calc

        except (KeyError, InvalidOperation, ValueError) as e:
            raise OperationError(f"Invalid calculation data: {str(e)}")

    def format_result(self, precision: int = 2) -> str:
        try:
            # 1. Quantize to the specified precision
            q = self.result.quantize(Decimal("0." + "0" * precision), rounding=ROUND_HALF_UP)
            # 2. Format as fixed-point string to prevent scientific notation
            s = format(q, 'f')
            # 3. Strip trailing zeros and decimal point if not needed
            if '.' in s:
                s = s.rstrip('0').rstrip('.')
            return s
        except InvalidOperation:  # pragma: no cover
            return str(self.result)

    def __str__(self) -> str:
        return f"{self.operation}({self.operand1}, {self.operand2}) = {self.result}"

    def __repr__(self) -> str:
        return (
            f"Calculation(operation='{self.operation}', "
            f"operand1={self.operand1}, "
            f"operand2={self.operand2}, "
            f"result={self.result}, "
            f"timestamp='{self.timestamp.isoformat()}')"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Calculation):
            return NotImplemented
        return (
            self.operation == other.operation
            and self.operand1 == other.operand1
            and self.operand2 == other.operand2
            and self.result == other.result
        )

