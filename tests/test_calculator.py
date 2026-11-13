import datetime
from pathlib import Path
import pandas as pd
import pytest
from unittest.mock import Mock, patch, PropertyMock
from decimal import Decimal
from tempfile import TemporaryDirectory
from app.calculator import Calculator
from app.calculation import Calculation
from app.calculator_repl import calculator_repl
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError
from app.history import LoggingObserver, AutoSaveObserver
from app.operations import OperationFactory
from app.operations import Addition

@pytest.fixture
def calculator():
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        config = CalculatorConfig(base_dir=temp_path)

        with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
            patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file, \
            patch.object(CalculatorConfig, 'history_dir', new_callable=PropertyMock) as mock_history_dir, \
            patch.object(CalculatorConfig, 'history_file', new_callable=PropertyMock) as mock_history_file:

            mock_log_dir.return_value = temp_path / "logs"
            mock_log_file.return_value = temp_path / "logs/calculator.log"
            mock_history_dir.return_value = temp_path / "history"
            mock_history_file.return_value = temp_path / "history/calculator_history.csv"

            yield Calculator(config=config)
            
# Test Calculator Initialization

def test_calculator_initialization(calculator):
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []
    assert calculator.operation_strategy is None

# Test No Operation Used

def test_perform_operation_no_strategy(calculator):
    with pytest.raises(OperationError, match="No operation set"):
        calculator.perform_operation(1, 2)

def test_undo_and_redo(calculator):
    calculator.set_operation(Addition())
    calculator.perform_operation(Decimal("5"), Decimal("3"))
    assert len(calculator.history) == 1
    
    # Test Undo
    assert calculator.undo() is True
    assert len(calculator.history) == 0
    
    # Test Redo
    assert calculator.redo() is True
    assert len(calculator.history) == 1
    
    # Clear and test empty undo/redo branches
    calculator.clear_history()
    assert calculator.undo() is False
    assert calculator.redo() is False

def test_save_and_show_history(calculator):
    calculator.set_operation(Addition())
    calculator.perform_operation(Decimal("5"), Decimal("3"))
    
    # Show history
    history_str = calculator.show_history()
    assert len(history_str) == 1
    
    # Save history (covers the 'if history_data' branch)
    calculator.save_history()
    assert calculator.config.history_file.exists()
    
    # Save empty history (covers the 'else' branch for empty CSV)
    calculator.clear_history()
    calculator.save_history()

def test_get_history_dataframe(calculator):
    calculator.set_operation(Addition())
    calculator.perform_operation(Decimal("5"), Decimal("3"))
    df = calculator.get_history_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.iloc[0]['operation'] == 'Addition'

def test_load_history(calculator):
    # Save some history first
    calculator.set_operation(Addition())
    calculator.perform_operation(Decimal("10"), Decimal("5"))
    calculator.save_history()
    
    # Clear and reload
    calculator.clear_history()
    assert len(calculator.history) == 0
    
    calculator.load_history()
    assert len(calculator.history) == 1

def test_perform_operation_validation_error(calculator):
    """Cover the ValidationError branch in perform_operation."""
    calculator.set_operation(Addition())
    with pytest.raises(ValidationError):
        calculator.perform_operation("invalid", "input")

def test_perform_operation_generic_exception(calculator):
    """Cover the generic Exception branch in perform_operation."""
    calculator.set_operation(Addition())
    # Mock the operation to raise a generic exception
    with patch.object(Addition, 'execute', side_effect=Exception("Generic error")):
        with pytest.raises(OperationError, match="Operation failed"):
            calculator.perform_operation(1, 2)

def test_save_history_permission_error(calculator):
    """Cover the except block in save_history when writing fails."""
    calculator.set_operation(Addition())
    calculator.perform_operation(Decimal("1"), Decimal("1"))
    
    # Mock the pandas CSV writer to raise an OS error (simulating a permissions issue)
    with patch('pandas.DataFrame.to_csv', side_effect=OSError("Permission denied")):
        with pytest.raises(OperationError, match="Failed to save history"):
            calculator.save_history()

def test_load_history_file_not_found(calculator):
    """Cover the branch in load_history when the file doesn't exist."""
    # Ensure the file doesn't exist
    if calculator.config.history_file.exists():
        calculator.config.history_file.unlink()
    
    # This should not raise an error, just log and return
    calculator.load_history()
    assert len(calculator.history) == 0

@patch('app.calculator.logging.basicConfig', side_effect=Exception("Logging setup failed"))
def test_setup_logging_failure(mock_logging, capsys):
    """Cover the except block in _setup_logging when logging fails."""
    # The code catches the exception and prints a message
    calc = Calculator()
    captured = capsys.readouterr()
    assert "Could not load existing history" in captured.out or "Logging setup failed" in captured.out

def test_add_and_remove_observer(calculator):
    """Cover the add_observer and remove_observer methods."""
    observer = LoggingObserver()
    
    # Add observer
    calculator.add_observer(observer)
    assert observer in calculator.observers
    
    # Remove observer
    calculator.remove_observer(observer)
    assert observer not in calculator.observers

def test_remove_observer(calculator):
    """Cover line 68: remove_observer logging."""
    obs = LoggingObserver()
    calculator.add_observer(obs)
    calculator.remove_observer(obs)
    assert obs not in calculator.observers

def test_save_empty_history(calculator):
    """Cover line 121: logging.info('Empty history saved')."""
    calculator.clear_history()
    calculator.save_history()
    assert calculator.config.history_file.exists()

def test_calculation_invalid_operation_name():
    """Cover the first except block when OperationFactory fails."""
    with pytest.raises(OperationError):
        Calculation(operation="FakeOperation", operand1=Decimal("1"), operand2=Decimal("2"))

def test_calculation_division_by_zero():
    """Cover the second except block when operation.execute fails."""
    with pytest.raises(OperationError):
        Calculation(operation="Division", operand1=Decimal("1"), operand2=Decimal("0"))

def test_calculation_root_zero_degree():
    """Cover the Root zero-degree branch."""
    with pytest.raises(OperationError):
        Calculation(operation="Root", operand1=Decimal("16"), operand2=Decimal("0"))

def test_remove_observer(calculator):
    """Cover line 68: remove_observer logging."""
    obs = LoggingObserver()
    calculator.add_observer(obs)
    calculator.remove_observer(obs)
    assert obs not in calculator.observers

def test_save_empty_history(calculator):
    """Cover line 121: logging.info('Empty history saved')."""
    calculator.clear_history()
    calculator.save_history()
    assert calculator.config.history_file.exists()