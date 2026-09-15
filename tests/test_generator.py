from src.models import FieldRule
from src.generator import generate_test_cases


def test_generate_valid_case():
    rules = [
        FieldRule(
            field_name="age",
            data_type="integer",
            required=True,
            minimum=18,
            maximum=65,
        )
    ]

    cases = generate_test_cases(rules)

    assert cases[0]["case_type"] == "valid"
    assert cases[0]["data"]["age"] == 18


def test_generate_boundary_cases():
    rules = [
        FieldRule(
            field_name="age",
            data_type="integer",
            required=True,
            minimum=18,
            maximum=65,
        )
    ]

    cases = generate_test_cases(rules)

    boundary_cases = [
        case for case in cases if case["case_type"] == "boundary"
    ]

    values = [case["data"]["age"] for case in boundary_cases]

    assert 18 in values
    assert 65 in values
    assert 17 in values
    assert 66 in values


def test_generate_invalid_case_for_allowed_values():
    rules = [
        FieldRule(
            field_name="status",
            data_type="string",
            required=True,
            allowed_values=["active", "inactive"],
        )
    ]

    cases = generate_test_cases(rules)

    invalid_cases = [
        case for case in cases if case["case_type"] == "invalid"
    ]

    assert len(invalid_cases) == 1
    assert invalid_cases[0]["data"]["status"] == "__invalid_value__"


def test_generate_multiple_fields():
    rules = [
        FieldRule(
            field_name="username",
            data_type="string",
            required=True,
            minimum=3,
            maximum=20,
        ),
        FieldRule(
            field_name="age",
            data_type="integer",
            required=True,
            minimum=18,
            maximum=65,
        ),
    ]

    cases = generate_test_cases(rules)

    valid_case = cases[0]

    assert "username" in valid_case["data"]
    assert "age" in valid_case["data"]
