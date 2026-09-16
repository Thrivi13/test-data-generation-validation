import re
from datetime import datetime
from typing import Any

from src.models import FieldRule


def _validate_type(value: Any, data_type: str) -> bool:
    """Check whether a value matches the expected data type."""

    if data_type == "string":
        return isinstance(value, str)

    if data_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)

    if data_type == "float":
        return isinstance(value, (int, float)) and not isinstance(value, bool)

    if data_type == "boolean":
        return isinstance(value, bool)

    return False


def _validate_format(value: Any, format_rule: str) -> bool:
    """Validate a value against a supported format rule."""

    if format_rule == "email":
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        return bool(re.match(pattern, str(value)))

    if format_rule == "phone":
        return bool(re.fullmatch(r"\d{10}", str(value)))

    if format_rule == "url":
        pattern = r"^https?://[^\s]+$"
        return bool(re.match(pattern, str(value)))

    if format_rule.startswith("date:"):
        date_format = format_rule.split(":", 1)[1]

        try:
            datetime.strptime(str(value), date_format)
            return True
        except ValueError:
            return False

    if format_rule.startswith("regex:"):
        pattern = format_rule.split(":", 1)[1]

        try:
            return bool(re.fullmatch(pattern, str(value)))
        except re.error:
            return False

    return True


def validate_field(value: Any, rule: FieldRule) -> tuple[bool, str]:
    """Validate one field value against its rule."""

    if value is None or value == "":
        if rule.required:
            return False, "Required field is missing."
        return True, "Optional field is empty."

    if not _validate_type(value, rule.data_type):
        return False, f"Expected type '{rule.data_type}'."

    if rule.minimum is not None:
        if rule.data_type == "string":
            if len(value) < rule.minimum:
                return False, "Value is below the minimum length."
        elif value < rule.minimum:
            return False, "Value is below the minimum."

    if rule.maximum is not None:
        if rule.data_type == "string":
            if len(value) > rule.maximum:
                return False, "Value exceeds the maximum length."
        elif value > rule.maximum:
            return False, "Value exceeds the maximum."

    if rule.allowed_values is not None:
        if value not in rule.allowed_values:
            return False, "Value is not in the allowed values."

    if rule.format_rule:
        if not _validate_format(value, rule.format_rule):
            return False, "Value does not match the required format."

    return True, "Value satisfies the field rules."


def validate_test_case(
    test_case: dict,
    rules: list[FieldRule],
) -> dict:
    """Validate all fields in one generated test case."""

    data = test_case.get("data", {})

    field_results = {}
    actual_valid = True

    for rule in rules:
        value = data.get(rule.field_name)

        is_valid, message = validate_field(value, rule)

        field_results[rule.field_name] = {
            "value": value,
            "valid": is_valid,
            "message": message,
        }

        if not is_valid:
            actual_valid = False

    expected_valid = test_case.get("expected_valid")

    matches_expectation = (
        None
        if expected_valid is None
        else expected_valid == actual_valid
    )

    return {
        "case_type": test_case.get("case_type"),
        "field_name": test_case.get("field_name"),
        "test_reason": test_case.get("test_reason"),
        "expected_valid": expected_valid,
        "actual_valid": actual_valid,
        "valid": actual_valid,
        "matches_expectation": matches_expectation,
        "data": data,
        "field_results": field_results,
    }


def validate_test_cases(
    test_cases: list[dict],
    rules: list[FieldRule],
) -> list[dict]:
    """Validate a collection of generated test cases."""

    return [
        validate_test_case(test_case, rules)
        for test_case in test_cases
    ]