from src.models import FieldRule
from src.validator import validate_field, validate_test_case


def test_valid_integer():
    rule = FieldRule(
        field_name="age",
        data_type="integer",
        required=True,
        minimum=18,
        maximum=65,
    )

    valid, message = validate_field(25, rule)

    assert valid is True
    assert "satisfies" in message.lower()


def test_integer_below_minimum_is_invalid():
    rule = FieldRule(
        field_name="age",
        data_type="integer",
        required=True,
        minimum=18,
        maximum=65,
    )

    valid, message = validate_field(17, rule)

    assert valid is False
    assert "minimum" in message.lower()


def test_string_length_validation():
    rule = FieldRule(
        field_name="username",
        data_type="string",
        required=True,
        minimum=3,
        maximum=10,
    )

    valid, _ = validate_field("ab", rule)

    assert valid is False


def test_allowed_values_validation():
    rule = FieldRule(
        field_name="status",
        data_type="string",
        required=True,
        allowed_values=["active", "inactive"],
    )

    valid, _ = validate_field("pending", rule)

    assert valid is False


def test_email_validation():
    rule = FieldRule(
        field_name="email",
        data_type="string",
        required=True,
        format_rule="email",
    )

    valid, _ = validate_field("test@example.com", rule)

    assert valid is True


def test_invalid_email():
    rule = FieldRule(
        field_name="email",
        data_type="string",
        required=True,
        format_rule="email",
    )

    valid, _ = validate_field("invalid-email", rule)

    assert valid is False


def test_required_field_missing():
    rule = FieldRule(
        field_name="username",
        data_type="string",
        required=True,
    )

    valid, message = validate_field("", rule)

    assert valid is False
    assert "required" in message.lower()


def test_optional_empty_field():
    rule = FieldRule(
        field_name="phone",
        data_type="string",
        required=False,
    )

    valid, _ = validate_field("", rule)

    assert valid is True


def test_validate_complete_test_case():
    rules = [
        FieldRule(
            field_name="age",
            data_type="integer",
            required=True,
            minimum=18,
            maximum=65,
        ),
        FieldRule(
            field_name="status",
            data_type="string",
            required=True,
            allowed_values=["active", "inactive"],
        ),
    ]

    test_case = {
        "case_type": "valid",
        "data": {
            "age": 25,
            "status": "active",
        },
    }

    result = validate_test_case(test_case, rules)

    assert result["valid"] is True
    assert result["field_results"]["age"]["valid"] is True
    assert result["field_results"]["status"]["valid"] is True
