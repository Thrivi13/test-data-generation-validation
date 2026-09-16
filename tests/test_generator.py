from src.generator import generate_test_cases
from src.models import FieldRule


def test_generate_test_cases():
    rules = [
        FieldRule(
            field_name="age",
            data_type="integer",
            required=True,
            minimum=18,
            maximum=65,
        ),
        FieldRule(
            field_name="email",
            data_type="string",
            required=True,
            format_rule="email",
        ),
    ]

    test_cases = generate_test_cases(rules)

    assert len(test_cases) > 0

    valid_cases = [
        case
        for case in test_cases
        if case["case_type"] == "valid"
    ]

    boundary_cases = [
        case
        for case in test_cases
        if case["case_type"] == "boundary"
    ]

    invalid_cases = [
        case
        for case in test_cases
        if case["case_type"] == "invalid"
    ]

    missing_cases = [
        case
        for case in test_cases
        if case["case_type"] == "missing_required"
    ]

    wrong_type_cases = [
        case
        for case in test_cases
        if case["case_type"] == "wrong_type"
    ]

    assert len(valid_cases) == 1
    assert len(boundary_cases) == 4
    assert len(invalid_cases) == 2
    assert len(missing_cases) == 2
    assert len(wrong_type_cases) == 2


def test_boundary_test_reasons():
    rule = FieldRule(
        field_name="age",
        data_type="integer",
        required=True,
        minimum=18,
        maximum=65,
    )

    test_cases = generate_test_cases([rule])

    boundary_cases = [
        case
        for case in test_cases
        if case["case_type"] == "boundary"
    ]

    reasons = [case["test_reason"] for case in boundary_cases]

    assert "At minimum boundary" in reasons
    assert "Below minimum boundary" in reasons
    assert "At maximum boundary" in reasons
    assert "Above maximum boundary" in reasons


def test_invalid_format_reason():
    rule = FieldRule(
        field_name="email",
        data_type="string",
        required=True,
        format_rule="email",
    )

    test_cases = generate_test_cases([rule])

    invalid_case = next(
        case
        for case in test_cases
        if case["case_type"] == "invalid"
    )

    assert invalid_case["test_reason"] == "Invalid email format"
    assert invalid_case["expected_valid"] is False


def test_invalid_allowed_value_reason():
    rule = FieldRule(
        field_name="status",
        data_type="string",
        required=True,
        allowed_values=["active", "inactive"],
    )

    test_cases = generate_test_cases([rule])

    invalid_case = next(
        case
        for case in test_cases
        if case["case_type"] == "invalid"
    )

    assert invalid_case["test_reason"] == "Invalid allowed value"
    assert invalid_case["expected_valid"] is False


def test_missing_required_reason():
    rule = FieldRule(
        field_name="username",
        data_type="string",
        required=True,
    )

    test_cases = generate_test_cases([rule])

    missing_case = next(
        case
        for case in test_cases
        if case["case_type"] == "missing_required"
    )

    assert missing_case["test_reason"] == "Missing required field"
    assert missing_case["data"]["username"] is None
    assert missing_case["expected_valid"] is False


def test_wrong_type_reason():
    rule = FieldRule(
        field_name="age",
        data_type="integer",
        required=True,
    )

    test_cases = generate_test_cases([rule])

    wrong_type_case = next(
        case
        for case in test_cases
        if case["case_type"] == "wrong_type"
    )

    assert wrong_type_case["test_reason"] == "Wrong data type"
    assert wrong_type_case["expected_valid"] is False