import math

from src.models import RawFieldRule, FieldRule


def _is_empty(value):
    """Return True when a value is missing or empty."""
    if value is None:
        return True

    if isinstance(value, float) and math.isnan(value):
        return True

    if isinstance(value, str) and value.strip() == "":
        return True

    return False


def _normalize_required(value):
    """Convert a required value into a boolean."""
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        value = value.strip().lower()

        if value == "true":
            return True

        if value == "false":
            return False

    raise ValueError("Required must be True or False.")


def _normalize_number(value, data_type):
    """Convert numeric boundaries to the appropriate type."""
    if _is_empty(value):
        return None

    try:
        if data_type == "integer":
            return int(float(value))

        if data_type == "float":
            return float(value)

        if data_type == "string":
            return int(float(value))

    except (TypeError, ValueError):
        raise ValueError(
            f"Invalid numeric boundary '{value}' for type '{data_type}'."
        )

    return None


def _normalize_allowed_values(value):
    """Convert pipe-separated allowed values into a list."""
    if _is_empty(value):
        return None

    if isinstance(value, str):
        values = [item.strip() for item in value.split("|")]
        values = [item for item in values if item]

        return values if values else None

    raise ValueError("Allowed values must be pipe-separated text.")


def normalize_rule(raw_rule: RawFieldRule) -> FieldRule:
    """Convert a RawFieldRule into a validated FieldRule."""

    data_type = str(raw_rule.data_type).strip().lower()

    if data_type not in {"string", "integer", "float", "boolean"}:
        raise ValueError(f"Unsupported data type: {data_type}")

    format_rule = None
    if not _is_empty(raw_rule.format_rule):
        format_rule = str(raw_rule.format_rule).strip()

    description = None
    if not _is_empty(raw_rule.description):
        description = str(raw_rule.description).strip()

    return FieldRule(
        field_name=raw_rule.field_name.strip(),
        data_type=data_type,
        required=_normalize_required(raw_rule.required),
        minimum=_normalize_number(raw_rule.minimum, data_type),
        maximum=_normalize_number(raw_rule.maximum, data_type),
        allowed_values=_normalize_allowed_values(raw_rule.allowed_values),
        format_rule=format_rule,
        description=description,
    )