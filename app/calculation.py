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

    def _raise_div_zero(self):
        raise OperationError("Cannot divide by zero")

    def _raise_neg_power(self):
        raise OperationError("Negative exponent is not allowed for this operation")

    def _raise_invalid_root(self):
        raise OperationError("Invalid root operation")

    def _raise_invalid_modulus(self):
        raise OperationError("Invalid modulus operation")

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

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Calculation":
        try:
            operation = data["operation"]
            operand1 = Decimal(str(data["operand1"]))
            operand2 = Decimal(str(data["operand2"]))
            result = Decimal(str(data["result"]))
            timestamp_value = data.get("timestamp")
        except (KeyError, TypeError, ValueError, InvalidOperation) as exc:
            raise OperationError("Invalid calculation data") from exc

        calc = cls(operation=operation, operand1=operand1, operand2=operand2)

        if result != calc.result:
            logging.warning(
                "Loaded calculation result %s differs from computed result %s",
                result,
                calc.result,
            )

        if timestamp_value is not None:
            try:
                calc.timestamp = datetime.datetime.fromisoformat(str(timestamp_value))
            except ValueError:
                pass

        return calc

    def format_result(self, precision: int = 2) -> str:
        try:
            if self.result.is_infinite() or self.result.is_nan():
                return str(self.result)

            quant = Decimal("1").scaleb(-precision)
            quantized = self.result.quantize(quant, rounding=ROUND_HALF_UP)
            formatted = format(quantized, "f")
            if "." in formatted:
                formatted = formatted.rstrip("0").rstrip(".")
            return formatted if formatted else "0"
        except (InvalidOperation, ValueError, ArithmeticError):
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

