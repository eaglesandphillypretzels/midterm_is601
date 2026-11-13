import pytest
from unittest.mock import Mock, patch
from decimal import Decimal

from app.calculation import Calculation
from app.history import AutoSaveObserver, HistoryObserver, LoggingObserver


class ConcreteHistoryObserver(HistoryObserver):
    def update(self, calculation: Calculation) -> None:
        pass


@pytest.fixture
def calculation_mock():
    calc = Mock(spec=Calculation)
    calc.operation = "Addition"
    calc.operand1 = Decimal("5")
    calc.operand2 = Decimal("3")
    calc.result = Decimal("8")
    return calc


def test_history_observer_is_abstract():
    with pytest.raises(TypeError):
        HistoryObserver()  # type: ignore[reportAbstractUsage]


def test_concrete_history_observer_can_be_instantiated():
    observer = ConcreteHistoryObserver()
    assert isinstance(observer, HistoryObserver)


@patch("logging.info")
def test_logging_observer_logs_calculation(logging_info_mock, calculation_mock):
    observer = LoggingObserver()
    observer.update(calculation_mock)

    logging_info_mock.assert_called_once_with(
        "Calculation performed: Addition (5, 3) = 8"
    )


def test_logging_observer_no_calculation():
    observer = LoggingObserver()
    with pytest.raises(AttributeError):
        observer.update(None)  # type: ignore[arg-type]


@patch("logging.info")
def test_autosave_observer_logs_autosave(logging_info_mock, calculation_mock):
    calculator_mock = Mock()
    calculator_mock.config = Mock()
    calculator_mock.config.auto_save = True
    calculator_mock.save_history = Mock()

    observer = AutoSaveObserver(calculator_mock)
    observer.update(calculation_mock)

    calculator_mock.save_history.assert_called_once_with()
    logging_info_mock.assert_called_once_with("History auto-saved")


def test_autosave_observer_triggers_save_when_enabled(calculation_mock):
    calculator_mock_obj = Mock()
    calculator_mock_obj.config = Mock()
    calculator_mock_obj.config.auto_save = True
    calculator_mock_obj.save_history = Mock()

    observer = AutoSaveObserver(calculator_mock_obj)
    observer.update(calculation_mock)

    calculator_mock_obj.save_history.assert_called_once_with()


def test_autosave_observer_does_not_trigger_save_when_disabled(calculation_mock):
    calculator_mock_obj = Mock()
    calculator_mock_obj.config = Mock()
    calculator_mock_obj.config.auto_save = False
    calculator_mock_obj.save_history = Mock()

    observer = AutoSaveObserver(calculator_mock_obj)
    observer.update(calculation_mock)

    calculator_mock_obj.save_history.assert_not_called()


def test_autosave_observer_no_calculation():
    calculator_mock_obj = Mock()
    calculator_mock_obj.config = Mock()
    calculator_mock_obj.config.auto_save = True
    calculator_mock_obj.save_history = Mock()

    observer = AutoSaveObserver(calculator_mock_obj)
    with pytest.raises(AttributeError):
        observer.update(None)  # type: ignore[arg-type]


def test_autosave_observer_invalid_calculator_missing_attributes():
    with pytest.raises(TypeError):
        AutoSaveObserver(object())


def test_autosave_observer_invalid_calculator_missing_save_history():
    calculator_mock_obj = Mock()
    calculator_mock_obj.config = Mock()
    del calculator_mock_obj.save_history
    with pytest.raises(TypeError):
        AutoSaveObserver(calculator_mock_obj)
