from dataclasses import dataclass
from decimal import Decimal
from numbers import Number
from pathlib import Path
import os
from typing import Optional

from dotenv import load_dotenv

from app.exceptions import ConfigurationError

load_dotenv()

def get_project_root() -> Path:
    return current_file.parent.parent

@dataclass
class CalculatorConfig:
    
    def __init__(
        self,
        base_dir: Optional[Path] = None,
        max_history_size: Optional[int] = None,
        auto_save: Optional[bool] = None,
        precision: Optional[int] = None,
        max_input_value: Optional[Number] = None,
        default_encoding: Optional[str] = None
    )
        project_root = get_project_root()
        self.base_dir = base_dir or Path(
            os.getenv('CALCULATOR_BASE_DIR', str(project_root))
        ).resolve()

        # Max history size
        self.max_history_size = max_history_size or int(
            os.getenv ('CALCULATOR_MAX_HISTORY_SIZE', '500')
        )

    # Auto-save preference
        auto_save_env = os.getenv('CALCULATOR_AUTO_SAVE', 'true').lower()
        self.auto_save = auto_save if auto_save is not None else (
            auto_save_env == 'true' or auto_save_env == '1'
        )

        # Calculation precision
        self.precision = precision or int(
            os.getenv('CALCULATOR_PRECISION', '10')
        )

        # Maximum input value allowed
        self.max_input_value = max_input_value or Decimal(
            os.getenv('CALCULATOR_MAX_INPUT_VALUE', '1e999')
        )

        # Default encoding for file operations
        self.default_encoding = default_encoding or os.getenv(
            'CALCULATOR_DEFAULT_ENCODING', 'utf-8'
        )

    @property
    def log_dir(self) -> Path:
        return Path(os.getenv(
            'CALCULATOR_LOG_DIR',
            str(self.base_dir / "logs")
        )).resolve()

    @property
    def history_dir(self) -> Path:
        return Path(os.getenv(
            'CALCULATOR_HISTORY_DIR',
            str(self.base_dir / "history")
        )).resolve()