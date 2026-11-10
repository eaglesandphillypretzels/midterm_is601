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