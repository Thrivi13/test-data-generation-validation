import pytest

from src.models import RawFieldRule
from src.rule_normalizer import normalize_rule


def test_invalid_required_value():
    rule = RawFieldRule(
        field_name="username",
        data_type="string",
        required="sometimes",
    )

    with pytest.raises(ValueError, match="Required must be True or False"):
        normalize_rule(rule)


def test_unsupported_data_type():
    rule = RawFieldRule(
        field_name="age",
        data_type="decimal128",
        required=True,
    )

    with pytest.raises(
        ValueError,
        match="Unsupported data type: decimal128",
    ):
        normalize_rule(rule)


def test_invalid_numeric_boundary():
    rule = RawFieldRule(
        field_name="age",
        data_type="integer",
        required=True,
        minimum="abc",
    )

    with pytest.raises(ValueError, match="Invalid numeric boundary"):
        normalize_rule(rule)


def test_invalid_allowed_values():
    rule = RawFieldRule(
        field_name="status",
        data_type="string",
        required=True,
        allowed_values=12345,
    )

    with pytest.raises(
        ValueError,
        match="Allowed values must be pipe-separated text",
    ):
        normalize_rule(rule)