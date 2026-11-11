import pytest
import os
from decimal import Decimal
from pathlib import Path
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError

# Temporary environment variables
os.environ['CALCULATOR_MAX_HISTORY_SIZE'] = '500'
os.environ['CALCULATOR_AUTO_SAVE'] = 'false'
os.environ['CALCULATOR_PRECISION'] = '8'
os.environ['CALCULATOR_MAX_INPUT_VALUE'] = '1000'
os.environ['CALCULATOR_DEFAULT_ENCODING'] = 'utf-16'
os.environ['CALCULATOR_LOG_DIR'] = './test_logs'
os.environ['CALCULATOR_HISTORY_DIR'] = './test_history'
os.environ['CALCULATOR_HISTORY_FILE'] = './test_history/test_history.csv'
os.environ['CALCULATOR_LOG_FILE'] = './test_logs/test_log.log'

# Helper function to clear specific environment variables
def clear_env_vars(*args):
    for var in args:
        os.environ.pop(var, None)

def test_default_configuration():
    config = CalculatorConfig()
    assert getattr(config, 'max_history_size') == 500
    assert getattr(config, 'auto_save') is False
    assert getattr(config, 'precision') == 8
    assert getattr(config, 'max_input_value') == Decimal("1000")
    assert getattr(config, 'default_encoding') == 'utf-16'
    assert getattr(config, 'log_dir') == Path('./test_logs').resolve()
    assert getattr(config, 'history_dir') == Path('./test_history').resolve()
    assert getattr(config, 'history_file') == Path('./test_history/test_history.csv').resolve()
    assert getattr(config, 'log_file') == Path('./test_logs/test_log.log').resolve()

def test_custom_configuration():
    config = CalculatorConfig(
        max_history_size=300,
        auto_save=True,
        precision=5,
        max_input_value=Decimal("500"),
        default_encoding="ascii"
    )
    assert getattr(config, 'max_history_size') == 300
    assert getattr(config, 'auto_save') is True
    assert getattr(config, 'precision') == 5
    assert getattr(config, 'max_input_value') == Decimal("500")
    assert getattr(config, 'default_encoding') == "ascii"

def test_directory_properties():
    clear_env_vars(
        'CALCULATOR_LOG_DIR',
        'CALCULATOR_HISTORY_DIR',
        'CALCULATOR_LOG_FILE',
        'CALCULATOR_HISTORY_FILE',
    )
    config = CalculatorConfig(base_dir=Path('/custom_base_dir'))
    assert config.log_dir == Path('/custom_base_dir/logs').resolve()
    assert config.history_dir == Path('/custom_base_dir/history').resolve()