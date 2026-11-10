import pytest
from unittest.mock import Mock, patch
from app.calculation import LoggingObserver, AutoSaveObserver
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig

# Sample setup for mock calculation

calculation_mock = Mock(spec = Calculation)
calculation_mock.operation = "addition"
calculation_mock.operand1 = 5
calculation_mock.operand2 = 3
calculation_mock.result = 8

# Test cases for LoggingObserver

@patch('logging.info')
def test_logging_observer_logs_calculation (Logging_info_mock):
    observer = LoggingObserver()
    observer.update(calculation_mock)
    Logging_info_mock.assert_called_once_with(
        "Calculation performed: addition (5, 3) = 8"
    )

def test_logging_observer_no_calculation():
    observer = LoggingObserver()
    with pytest.raises(AttributeError):
        observer.update(None) # Passing None raises an exception as there is no logged calculation

# Test cases for AutoSaveObserver

def test_autosave_observer_triggers_save():
    calculator_mock = Mock(spec=Calculator)
    calculator_mock.config = Mock (spec=CalculatorConfig)
    calculator_mock.config.auto_save = True
    observer = AutoSaveObserver(calculator_mock)

    observer.update(calculation_mock)
    calculator_mock.save_history.assert_called_once()

@patch('logging.info')
def test_autosave_observer_logs_autosave(Logging_info_mock):
    calculator_mock = Mock(spec=Calculator)
    calculator_mock.config.auto_save = True
    observer = AutoSaveObserver(calculator_mock)

    observer.update(calculation_mock)
    logging_info_mock.assert_called_once_with("History auto-saved") 