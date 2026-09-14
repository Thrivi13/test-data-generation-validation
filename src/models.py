from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class FieldRule:
    field_name: str
    data_type: str
    required: bool
    minimum: Optional[Any] = None
    maximum: Optional[Any] = None
    allowed_values: Optional[list] = None
    format_rule: Optional[str] = None
    description: Optional[str] = None
