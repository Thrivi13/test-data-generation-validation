from typing import Any

from src.models import FieldRule


def _generate_valid_value(rule: FieldRule) -> Any:
    """Generate one value that should satisfy the field rule."""

    if rule.allowed_values:
        return rule.allowed_values[0]

    if rule.data_type == "integer":
        if rule.minimum is not None:
            return rule.minimum
        return 1

    if rule.data_type == "float":
        if rule.minimum is not None:
            return rule.minimum
        return 1.0

    if rule.data_type == "boolean":
        return True

    if rule.format_rule == "email":
        return "test@example.com"

    if rule.format_rule == "phone":
        return "9876543210"

    if rule.format_rule == "url":
        return "https://example.com"

    if rule.format_rule and rule.format_rule.startswith("date:"):
        return "2026-01-15"

    if rule.format_rule and rule.format_rule.startswith("regex:"):
        return "Valid1@"

    if rule.minimum is not None and rule.data_type == "string":
        return "a" * int(rule.minimum)

    return "test"


def _generate_boundary_values(
    rule: FieldRule,
) -> list[tuple[Any, bool, str]]:
    """Generate boundary values with expected validity and reason."""

    values = []

    if rule.data_type == "string":
        if rule.minimum is not None:
            minimum = int(rule.minimum)

            values.append(
                ("a" * minimum, True, "At minimum boundary")
            )

            if minimum > 0:
                values.append(
                    (
                        "a" * (minimum - 1),
                        False,
                        "Below minimum boundary",
                    )
                )

        if rule.maximum is not None:
            maximum = int(rule.maximum)

            values.append(
                ("a" * maximum, True, "At maximum boundary")
            )

            values.append(
                (
                    "a" * (maximum + 1),
                    False,
                    "Above maximum boundary",
                )
            )

    elif rule.data_type == "integer":
        if rule.minimum is not None:
            values.append(
                (rule.minimum, True, "At minimum boundary")
            )

            values.append(
                (
                    rule.minimum - 1,
                    False,
                    "Below minimum boundary",
                )
            )

        if rule.maximum is not None:
            values.append(
                (rule.maximum, True, "At maximum boundary")
            )

            values.append(
                (
                    rule.maximum + 1,
                    False,
                    "Above maximum boundary",
                )
            )

    elif rule.data_type == "float":
        if rule.minimum is not None:
            values.append(
                (rule.minimum, True, "At minimum boundary")
            )

            values.append(
                (
                    rule.minimum - 0.1,
                    False,
                    "Below minimum boundary",
                )
            )

        if rule.maximum is not None:
            values.append(
                (rule.maximum, True, "At maximum boundary")
            )

            values.append(
                (
                    rule.maximum + 0.1,
                    False,
                    "Above maximum boundary",
                )
            )

    return values


def _generate_invalid_value(rule: FieldRule) -> tuple[Any, str]:
    """Generate an invalid value with a specific reason."""

    if rule.allowed_values:
        return "__invalid_value__", "Invalid allowed value"

    if rule.format_rule == "email":
        return "invalid-email", "Invalid email format"

    if rule.format_rule == "phone":
        return "12345", "Invalid phone format"

    if rule.format_rule == "url":
        return "not-a-url", "Invalid URL format"

    if rule.format_rule and rule.format_rule.startswith("date:"):
        return "invalid-date", "Invalid date format"

    if rule.format_rule and rule.format_rule.startswith("regex:"):
        return "invalid", "Regex rule violation"

    if rule.data_type == "integer":
        if rule.minimum is not None:
            return rule.minimum - 1, "Below minimum"

        if rule.maximum is not None:
            return rule.maximum + 1, "Above maximum"

        return "not_an_integer", "Invalid integer value"

    if rule.data_type == "float":
        if rule.minimum is not None:
            return rule.minimum - 0.1, "Below minimum"

        if rule.maximum is not None:
            return rule.maximum + 0.1, "Above maximum"

        return "not_a_float", "Invalid float value"

    if rule.data_type == "boolean":
        return "not_a_boolean", "Invalid boolean value"

    if rule.data_type == "string":
        if rule.maximum is not None:
            return (
                "x" * (int(rule.maximum) + 1),
                "Above maximum length",
            )

        return "", "Invalid string value"

    return None, "Invalid value"


def _generate_wrong_type_value(rule: FieldRule) -> Any:
    """Generate a value with an incorrect data type."""

    if rule.data_type == "string":
        return 12345

    if rule.data_type == "integer":
        return "not_an_integer"

    if rule.data_type == "float":
        return "not_a_float"

    if rule.data_type == "boolean":
        return "not_a_boolean"

    return None


def generate_test_cases(rules: list[FieldRule]) -> list[dict]:
    """
    Generate valid, boundary, invalid, missing-required,
    and wrong-type test cases from normalized field rules.
    """

    test_cases = []

    valid_case = {
        rule.field_name: _generate_valid_value(rule)
        for rule in rules
    }

    test_cases.append(
        {
            "case_type": "valid",
            "test_reason": "Typical valid value",
            "expected_valid": True,
            "data": valid_case,
        }
    )

    for rule in rules:
        boundary_values = _generate_boundary_values(rule)

        for value, expected_valid, reason in boundary_values:
            case_data = valid_case.copy()
            case_data[rule.field_name] = value

            test_cases.append(
                {
                    "case_type": "boundary",
                    "field_name": rule.field_name,
                    "test_reason": reason,
                    "expected_valid": expected_valid,
                    "data": case_data,
                }
            )

    for rule in rules:
        value, reason = _generate_invalid_value(rule)

        case_data = valid_case.copy()
        case_data[rule.field_name] = value

        test_cases.append(
            {
                "case_type": "invalid",
                "field_name": rule.field_name,
                "test_reason": reason,
                "expected_valid": False,
                "data": case_data,
            }
        )

    for rule in rules:
        if rule.required:
            case_data = valid_case.copy()
            case_data[rule.field_name] = None

            test_cases.append(
                {
                    "case_type": "missing_required",
                    "field_name": rule.field_name,
                    "test_reason": "Missing required field",
                    "expected_valid": False,
                    "data": case_data,
                }
            )

    for rule in rules:
        case_data = valid_case.copy()
        case_data[rule.field_name] = _generate_wrong_type_value(rule)

        test_cases.append(
            {
                "case_type": "wrong_type",
                "field_name": rule.field_name,
                "test_reason": "Wrong data type",
                "expected_valid": False,
                "data": case_data,
            }
        )

    return test_cases