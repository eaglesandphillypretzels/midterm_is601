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
        pass # pragma: no cover

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        pass

    def __str__(self) -> str:
        return self.__class__.__name__

    class Addition(Operation):
        def execute(self, a: Decimal, b: Decimal) -> Decimal:
            """
        Add two numbers.

        Args:
            a (Decimal): First operand.
            b (Decimal): Second operand.

        Returns:
            Decimal: Sum of the two operands.
        """
        self.validate_operands(a, b)
        return a + b

    