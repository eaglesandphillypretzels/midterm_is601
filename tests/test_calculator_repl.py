import pytest
from unittest.mock import patch
from app.calculator_repl import calculator_repl
from app.calculator import Calculator

# --- Simple Commands ---
@pytest.mark.parametrize("command,expected_output", [
    ("help", "Available commands:"),
    ("clear", "History cleared"),
    ("history", "No calculations in history"),
])
def test_simple_commands(command, expected_output, capsys):
    with patch('builtins.input', side_effect=[command, 'exit']):
        calculator_repl()
    assert expected_output in capsys.readouterr().out

# --- Exit & Save Variations ---
@pytest.mark.parametrize("save_side_effect,expected_output", [
    (None, "History saved successfully"),
    (Exception("Save failed"), "Warning: Could not save history"),
])
def test_exit_command(save_side_effect, expected_output, capsys):
    with patch('app.calculator.Calculator.save_history', side_effect=save_side_effect):
        with patch('builtins.input', return_value='exit'):
            calculator_repl()
    assert expected_output in capsys.readouterr().out

# --- Full Loop & Math ---
@patch('builtins.input', side_effect=['add', '5', '3', 'history', 'undo', 'redo', 'clear', 'save', 'load', 'exit'])
def test_repl_full_loop(mock_input, capsys):
    calculator_repl()
    out = capsys.readouterr().out
    assert "Result: 8" in out
    assert "1. Addition" in out  # Covers populated history
    assert "Operation undone" in out
    assert "Operation redone" in out
    assert "History cleared" in out
    assert "History saved successfully" in out
    assert "History loaded successfully" in out

# --- Cancellation Paths ---
@patch('builtins.input', side_effect=['add', 'cancel', 'exit'])
def test_repl_cancel_first_number(mock_input, capsys):
    calculator_repl()
    assert "Operation cancelled" in capsys.readouterr().out

@patch('builtins.input', side_effect=['add', '5', 'cancel', 'exit'])
def test_repl_cancel_second_number(mock_input, capsys):
    calculator_repl()
    assert "Operation cancelled" in capsys.readouterr().out

# --- Error Handling in REPL ---
@patch('builtins.input', side_effect=['unknown_cmd_xyz', 'exit'])
def test_repl_unknown_command(mock_input, capsys):
    calculator_repl()
    assert "Unknown command" in capsys.readouterr().out

@patch('builtins.input', side_effect=['add', '1', '1', 'exit'])
@patch('app.calculator.Calculator.perform_operation', side_effect=Exception("Unexpected REPL error"))
def test_repl_unexpected_exception_in_loop(mock_perform, mock_input, capsys):
    calculator_repl()
    assert "Unexpected error" in capsys.readouterr().out or "Error" in capsys.readouterr().out

# --- System Interrupts (Safe versions that don't infinite loop) ---
@patch('builtins.input', side_effect=[KeyboardInterrupt, 'exit'])
def test_repl_keyboard_interrupt(mock_input, capsys):
    calculator_repl()
    assert "Operation cancelled" in capsys.readouterr().out

@patch('builtins.input', side_effect=[EOFError])
def test_repl_eof_error(mock_input, capsys):
    calculator_repl()
    assert "Input terminated" in capsys.readouterr().out

@patch('builtins.input', side_effect=[Exception("Random system error"), 'exit'])
def test_repl_generic_exception(mock_input, capsys):
    calculator_repl()
    assert "Error" in capsys.readouterr().out

# --- Fatal Initialization ---
@patch('app.calculator_repl.Calculator')
def test_repl_fatal_initialization_error(mock_calculator_class, capsys):
    mock_calculator_class.side_effect = Exception("Fatal init error")
    with pytest.raises(Exception, match="Fatal init error"):
        calculator_repl()
    assert "Fatal error" in capsys.readouterr().out

@patch('builtins.input', side_effect=['add', '5', '3', 'history', 'exit'])
def test_repl_history_with_data(mock_input, capsys):
    """Hits line 71: history display when NOT empty"""
    calculator_repl()
    assert "1. Addition" in capsys.readouterr().out

@patch('builtins.input', side_effect=['clear', 'exit'])
def test_repl_clear_cmd(mock_input, capsys):
    """Hits line 79: clear command"""
    calculator_repl()
    assert "History cleared" in capsys.readouterr().out

@patch('builtins.input', side_effect=['save', 'exit'])
def test_repl_save_cmd(mock_input, capsys):
    """Hits lines 87-88: save command"""
    calculator_repl()
    assert "History saved successfully" in capsys.readouterr().out

@patch('builtins.input', side_effect=['load', 'exit'])
def test_repl_load_cmd(mock_input, capsys):
    """Hits lines 96-97: load command"""
    calculator_repl()
    out = capsys.readouterr().out
    assert "History loaded successfully" in out or "Error loading history" in out

@patch('builtins.input', side_effect=['add', '1', 'cancel', 'exit'])
def test_repl_cancel_second_number(mock_input, capsys):
    """Hits line 127: canceling the second number"""
    calculator_repl()
    assert "Operation cancelled" in capsys.readouterr().out

@patch('builtins.input', side_effect=[KeyboardInterrupt, 'exit'])
def test_repl_ctrl_c(mock_input, capsys):
    """Hits lines 157-159: KeyboardInterrupt block"""
    calculator_repl()
    assert "Operation cancelled" in capsys.readouterr().out

@patch('builtins.input', side_effect=['undo', 'exit'])
def test_repl_nothing_to_undo(mock_input, capsys):
    """Covers the 'Nothing to undo' branch when the undo stack is empty."""
    calculator_repl()
    out = capsys.readouterr().out
    assert "Nothing to undo" in out

@patch('builtins.input', side_effect=['redo', 'exit'])
def test_repl_nothing_to_redo(mock_input, capsys):
    """Covers the 'Nothing to redo' branch when the redo stack is empty."""
    calculator_repl()
    out = capsys.readouterr().out
    assert "Nothing to redo" in out