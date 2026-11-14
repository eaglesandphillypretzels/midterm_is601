from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict
from app.exceptions import ValidationError

class Operation(ABC):
    """
    Abstract base class for all calculator methods, determining operations interface.
    """

    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        pass  # pragma: no cover

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        pass # pragma: no cover

    def __str__(self) -> str:
        return self.__class__.__name__

class Addition(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Add two numbers."""
        self.validate_operands(a, b)
        return a + b
class Subtraction(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Subtract one number from another."""
        self.validate_operands(a, b)
        return a - b
class Multiplication(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Multiply two numbers."""
        self.validate_operands(a, b)
        return a * b
class Division(Operation):
    def validate_operands(self, a: Decimal, b: Decimal) -> None:

        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Division by zero is not allowed")
        
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Divide one number by another."""
        self.validate_operands(a, b)
        return a / b
class Power(Operation):
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if b < 0:
            raise ValidationError("Negative exponents are not allowed for this operation")
        
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Raise a number to the power of another number."""
        self.validate_operands(a, b)
        return Decimal(str(pow(float(a), float(b))))
class Root(Operation):
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Root index cannot be zero")
        if b < 0:
            raise ValidationError("Root index cannot be negative")
        # Prevent even roots of negative numbers (e.g., square root of -4)
        if a < 0 and int(b) % 2 == 0:
            raise ValidationError("Invalid root operation")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Find the nth root of a number."""
        self.validate_operands(a, b)
        return Decimal(pow(float(a), 1 / float(b)))
class Modulus(Operation):
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Modulus by zero is not allowed.")
        if b < 0:
            raise ValidationError("Cannot perform modulus operation with a negative divisor.")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Return the remainder after dividing one number by another."""
        self.validate_operands(a, b)
        return a % b
class Percent(Operation):
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Percent calculation cannot divide by zero.")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Return the percentage of one number relative to another."""
        self.validate_operands(a, b)
        return (a / b) * Decimal("100")
class AbsoluteDifference(Operation):
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Return the absolute value of the difference between two numbers."""
        self.validate_operands(a, b)
        return abs(a - b)
class OperationFactory:
    """Create operation instances from a registry of names and aliases."""

    _operations: Dict[str, type[Operation]] = {}

    @classmethod
    def register(cls, operation_class: type[Operation], *aliases: str) -> None:
        for alias in (operation_class.__name__, *aliases):
            cls._operations[alias.strip().lower()] = operation_class

    @classmethod
    def create(cls, name: str) -> Operation:
        key = str(name).strip().lower()
        operation_class = cls._operations.get(key)
        if operation_class is None:
            raise ValidationError(f"Unsupported operation: {name}")
        return operation_class()

    @classmethod
    def get_available_operations(cls) -> Dict[str, type[Operation]]:
        return dict(cls._operations)


OperationFactory.register(Addition, "add", "+")
OperationFactory.register(Subtraction, "subtract", "-")
OperationFactory.register(Multiplication, "multiply", "*", "x")
OperationFactory.register(Division, "divide", "/")
OperationFactory.register(Power, "^", "**")
OperationFactory.register(Root)
OperationFactory.register(Modulus, "modulo", "%")
OperationFactory.register(Percent)
OperationFactory.register(AbsoluteDifference, "absolute difference", "absdiff")