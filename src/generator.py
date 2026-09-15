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


def _generate_boundary_values(rule: FieldRule) -> list[Any]:
    """Generate values around the defined boundaries."""

    values = []

    if rule.minimum is not None:
        values.append(rule.minimum)

    if rule.maximum is not None and rule.maximum != rule.minimum:
        values.append(rule.maximum)

    if rule.data_type == "string":
        if rule.minimum is not None and rule.minimum > 0:
            values.append("a" * (int(rule.minimum) - 1))

        if rule.maximum is not None:
            values.append("a" * (int(rule.maximum) + 1))

    elif rule.data_type == "integer":
        if rule.minimum is not None:
            values.append(rule.minimum - 1)

        if rule.maximum is not None:
            values.append(rule.maximum + 1)

    elif rule.data_type == "float":
        if rule.minimum is not None:
            values.append(rule.minimum - 0.1)

        if rule.maximum is not None:
            values.append(rule.maximum + 0.1)

    return values


def _generate_invalid_value(rule: FieldRule) -> Any:
    """Generate one value that should violate the field rule."""

    if rule.allowed_values:
        return "__invalid_value__"

    if rule.data_type == "integer":
        if rule.minimum is not None:
            return rule.minimum - 1
        return "not_an_integer"

    if rule.data_type == "float":
        if rule.minimum is not None:
            return rule.minimum - 0.1
        return "not_a_float"

    if rule.data_type == "boolean":
        return "not_a_boolean"

    if rule.format_rule == "email":
        return "invalid-email"

    if rule.format_rule == "phone":
        return "12345"

    if rule.format_rule == "url":
        return "not-a-url"

    if rule.format_rule and rule.format_rule.startswith("date:"):
        return "invalid-date"

    if rule.format_rule and rule.format_rule.startswith("regex:"):
        return "invalid"

    if rule.maximum is not None and rule.data_type == "string":
        return "x" * (int(rule.maximum) + 1)

    return ""


def generate_test_cases(rules: list[FieldRule]) -> list[dict]:
    """
    Generate valid, boundary, and invalid test cases
    from normalized field rules.
    """

    test_cases = []

    # One valid case containing valid values for all fields.
    valid_case = {
        rule.field_name: _generate_valid_value(rule)
        for rule in rules
    }

    test_cases.append(
        {
            "case_type": "valid",
            "data": valid_case,
        }
    )

    # Generate boundary cases field-by-field.
    for rule in rules:
        boundary_values = _generate_boundary_values(rule)

        for value in boundary_values:
            case_data = valid_case.copy()
            case_data[rule.field_name] = value

            test_cases.append(
                {
                    "case_type": "boundary",
                    "field_name": rule.field_name,
                    "data": case_data,
                }
            )

    # Generate invalid cases field-by-field.
    for rule in rules:
        case_data = valid_case.copy()
        case_data[rule.field_name] = _generate_invalid_value(rule)

        test_cases.append(
            {
                "case_type": "invalid",
                "field_name": rule.field_name,
                "data": case_data,
            }
        )

    return test_cases
