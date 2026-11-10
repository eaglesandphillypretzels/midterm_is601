import pytest
from unittest.mock import Mock, patch
from app.calculation import LoggingObserver, AutoSaveObserver
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig

# Sample setup for mock calculation
calculation_mock = Mock(spec = Calculation)