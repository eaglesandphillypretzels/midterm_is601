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
        pass

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
        """
        Validate operands, checking for division by zero.

        Overrides the base class method to ensure that the divisor is not zero.

        Args:
            a (Decimal): Dividend.
            b (Decimal): Divisor.

        Raises:
            ValidationError: If the divisor is zero.
        """
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

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Raise a number to the power of another number."""
        self.validate_operands(a, b)
        return Decimal(str(pow(float(a), float(b))))

class Root(Operation):
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if a < 0:
            raise ValidationError("Cannot calculate root of negative number")
        if b == 0:
            raise ValidationError("Zero root is undefined")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Find the nth root of a number."""
        self.validate_operands(a, b)
        return Decimal(pow(float(a), 1 / float(b)))

class Modulus(Operation):
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Cannot perform modulus operation with a divisor of zero.")
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


class UnknownOperation(Operation):
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        raise ValidationError("Unknown operation")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Raise a validation error for unsupported operations."""
        self.validate_operands(a, b)
        raise ValidationError("Unknown operation")
