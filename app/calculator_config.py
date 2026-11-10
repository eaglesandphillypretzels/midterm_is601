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
            os.getenv ('CALCULATOR_MAX_HISTORY_SIZE', '2000')
        )

        