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