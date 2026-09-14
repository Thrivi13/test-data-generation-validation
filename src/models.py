from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class RawFieldRule:
    """Represents a field rule exactly as read from the input table."""

    field_name: str
    data_type: str
    required: Any
    minimum: Any = None
    maximum: Any = None
    allowed_values: Any = None
    format_rule: Any = None
    description: Any = None


@dataclass
class FieldRule:
    """Represents a validated and normalized field rule."""

    field_name: str
    data_type: str
    required: bool
    minimum: Optional[Any] = None
    maximum: Optional[Any] = None
    allowed_values: Optional[list] = None
    format_rule: Optional[str] = None
    description: Optional[str] = None
