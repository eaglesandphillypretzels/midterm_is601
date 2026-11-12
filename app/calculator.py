from decimal import Decimal
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento
from app.exceptions import OperationError, ValidationError
from app.history import HistoryObserver
from app.input_validators import InputValidator
from app.operations import Operation

Number = Union[int, float, Decimal]
CalculationResult = Union[Number, str]

class Calculator:

    def __init__(self, config: Optional [CalculatorConfig] = None):
        
        if config is None:
            current_file = Path(__file__)
            project_root = current_file.parent.parent
            config = CalculatorConfig (base_dir=project_root)

        self.config = config
        self.config.validate()

        os.makedirs(self.config.log_dir, exist_ok=True)

        self._setup_logging()

        self.history: List[Calculation] = []
        self.operation_strategy: Optional
        [Operation] = None

        self.observers: List[HistoryObserver] = []

        self.undo_stack: List[CalculatorMemento] = []
        self.redo_stack: List[CalculatorMemento] = []

        self._setup_directories()

        try:
            self.load_history()
        except Exception as e:
            logging.warning(f"Could not load existing history: {e}")

        logging.info("Calculator initialized with configuration")

    def _setup_logging(self) -> None:
        """
        Confirms the existence of all necessary directories for history management.
        """
        self.config.history_dir.mkdir(parents=True, exist_ok=True)
    
    def add_observer(self, observer: HistoryObserver) -> None:
        self.observers.append(observer)
        logging.info (f"Added observer: {observer.__class__.__name__}")
    
    def remove_observer(self, observer: HistoryObserver) -> None:
        self.observers.remove(observer)
        logging.info(f"Removed observer: {observer.__class__.__name__}")

    def notify_observers(self, calculation: Calculation) -> None:
        for observer in self.observers:
            observer.update(calculation)

    def set_operation(self, operation: Operation) -> None:
        self.operation_strategy = operation
        logging.info(f"Set operation: {operation}")

    def perform_operation(
        self,
        a: Union[str, Number],
        b: Union[str, Number]
    ) -> CalculationResult:
        
        if not self.operation_strategy:
            raise OperationError("No operation set")

        try:
            # Validate and convert inputs to Decimal
            validated_a = InputValidator.validate_number(a, self.config)
            validated_b = InputValidator.validate_number(b, self.config)

             # Execute the operation strategy
            result = self.operation_strategy.execute(validated_a, validated_b)

            # Create a new Calculation instance with the operation details
            calculation = Calculation(
                operation=str(self.operation_strategy),
                operand1=validated_a,
                operand2=validated_b
            )

            # Save the current state to the undo stack before making changes
            self.undo_stack.append(CalculatorMemento(self.history.copy()))

            # Clear the redo stack since new operation invalidates the redo history
            self.redo_stack.clear()

            # Append the new calculation to the history
            self.history.append(calculation)

            # Ensure the history does not exceed the maximum size