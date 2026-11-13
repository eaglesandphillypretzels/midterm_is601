import pytest
from unittest.mock import patch, MagicMock
from decimal import Decimal
from app.calculator_repl import calculator_repl
from app.exceptions import OperationError, ValidationError

# Testing Simple Commands

@pytest.mark.parametrize("command,expected_output", [
    ("help", "Available commands:"),
    ("clear", "History cleared"),
    ("history", "No calculations in history"),
])
def test_simple_commands(command, expected_output, capsys):
    """Test simple commands that don't require additional input"""
    with patch('builtins.input', side_effect=[command, 'exit']):
        calculator_repl()
    
    captured = capsys.readouterr()
    assert expected_output in captured.out

# Testing Exit Command Variations

@pytest.mark.parametrize("save_side_effect,expected_output", [
    (None, "History saved successfully"),
    (Exception("Save failed"), "Warning: Could not save history"),
])
def test_exit_command(save_side_effect, expected_output, capsys):
    """Test exit command with different save outcomes"""
    with patch('app.calculator.Calculator.save_history', side_effect=save_side_effect):
        with patch('builtins.input', return_value='exit'):
            calculator_repl()
    
    captured = capsys.readouterr()
    assert expected_output in captured.out

@patch('builtins.input', side_effect=['help', 'history', 'add', '5', '3', 'history', 'undo', 'redo', 'clear', 'save', 'exit'])
def test_repl_full_loop(mock_input, capsys):
    calculator_repl()
    captured = capsys.readouterr()
    assert "Available commands" in captured.out
    assert "No calculations in history" in captured.out
    assert "Result: 8" in captured.out
    assert "Operation undone" in captured.out
    assert "Operation redone" in captured.out
    assert "History cleared" in captured.out
    assert "Goodbye" in captured.out

@patch('builtins.input', side_effect=['add', 'cancel', 'exit'])
def test_repl_cancel_operation(mock_input, capsys):
    calculator_repl()
    captured = capsys.readouterr()
    assert "Operation cancelled" in captured.out

@patch('builtins.input', side_effect=['unknown_cmd', 'exit'])
def test_repl_unknown_command(mock_input, capsys):
    calculator_repl()
    captured = capsys.readouterr()
    assert "Unknown command" in captured.out

@patch('builtins.input', side_effect=[KeyboardInterrupt, 'exit'])
def test_repl_keyboard_interrupt(mock_input, capsys):
    calculator_repl()
    captured = capsys.readouterr()
    assert "Operation cancelled" in captured.out

@patch('builtins.input', side_effect=EOFError)
def test_repl_eof_error(mock_input, capsys):
    calculator_repl()
    captured = capsys.readouterr()
    assert "Input terminated" in captured.out

@patch('builtins.input', side_effect=['load', 'exit'])
def test_repl_load_command(mock_input, capsys):
    calculator_repl()
    captured = capsys.readouterr()
    assert "History loaded successfully" in captured.out or "Error loading history" in captured.out

@patch('builtins.input', side_effect=[KeyboardInterrupt, 'exit'])
def test_repl_ctrl_c_interrupt(mock_input, capsys):
    calculator_repl()
    captured = capsys.readouterr()
    assert "Operation cancelled" in captured.out

@patch('builtins.input', side_effect=EOFError)
def test_repl_ctrl_d_eof(mock_input, capsys):
    calculator_repl()
    captured = capsys.readouterr()
    assert "Input terminated" in captured.out

@patch('app.calculator_repl.Calculator')
def test_repl_fatal_initialization_error(mock_calculator_class, capsys):
    """Cover the fatal error block at the end of calculator_repl."""
    # Make the Calculator initialization fail
    mock_calculator_class.side_effect = Exception("Fatal init error")
    
    with pytest.raises(Exception, match="Fatal init error"):
        calculator_repl()
    
    captured = capsys.readouterr()
    assert "Fatal error" in captured.out

@patch('builtins.input', side_effect=['add', '1', '1', 'exit'])
@patch('app.calculator_repl.Calculator.perform_operation', side_effect=Exception("Unexpected REPL error"))
def test_repl_unexpected_exception_in_loop(mock_perform, mock_input, capsys):
    """Cover the generic except Exception block inside the REPL while loop."""
    calculator_repl()
    captured = capsys.readouterr()
    assert "Unexpected error" in captured.out or "Error" in captured.out

@patch('builtins.input', side_effect=['unknown_command_xyz', 'exit'])
def test_repl_unknown_command(mock_input, capsys):
    """Cover the 'Unknown command' print branch."""
    calculator_repl()
    captured = capsys.readouterr()
    assert "Unknown command" in captured.out

@patch('builtins.input', side_effect=KeyboardInterrupt)
def test_repl_keyboard_interrupt(mock_input, capsys):
    """Cover the KeyboardInterrupt except block."""
    calculator_repl()
    captured = capsys.readouterr()
    assert "Operation cancelled" in captured.out

@patch('builtins.input', side_effect=EOFError)
def test_repl_eof_error(mock_input, capsys):
    """Cover the EOFError except block."""
    calculator_repl()
    captured = capsys.readouterr()
    assert "Input terminated" in captured.out

@patch('builtins.input', side_effect=Exception("Random system error"))
def test_repl_generic_exception(mock_input, capsys):
    """Cover the generic Exception except block."""
    calculator_repl()
    captured = capsys.readouterr()
    assert "Error" in captured.out