from src.models import RawFieldRule, FieldRule
from src.rule_normalizer import normalize_rule


def test_normalize_rule():
    raw_rule = RawFieldRule(
        field_name="country_code",
        data_type="string",
        required=True,
        minimum=None,
        maximum=None,
        allowed_values="US|IN|UK|CA|AU",
        format_rule=None,
        description="Supported country code",
    )

    rule = normalize_rule(raw_rule)

    assert isinstance(rule, FieldRule)
    assert rule.field_name == "country_code"
    assert rule.data_type == "string"
    assert rule.required is True
    assert rule.minimum is None
    assert rule.maximum is None
    assert rule.allowed_values == ["US", "IN", "UK", "CA", "AU"]
    assert rule.format_rule is None
    assert rule.description == "Supported country code"
def test_normalize_allowed_values():
    raw_rule = RawFieldRule(
        field_name="country_code",
        data_type="string",
        required=True,
        allowed_values="US|IN|UK|CA|AU"
    )

    rule = normalize_rule(raw_rule)

    assert rule.field_name == "country_code"
    assert rule.data_type == "string"
    assert rule.required is True
    assert rule.allowed_values == ["US", "IN", "UK", "CA", "AU"]
def test_normalize_boolean_rule():
    raw_rule = RawFieldRule(
        field_name="is_active",
        data_type="boolean",
        required="True"
    )

    rule = normalize_rule(raw_rule)

    assert rule.field_name == "is_active"
    assert rule.data_type == "boolean"
    assert rule.required is True
    assert rule.minimum is None
    assert rule.maximum is None
    assert rule.allowed_values is None
def test_normalize_false_boolean_rule():
    raw_rule = RawFieldRule(
        field_name="is_active",
        data_type="boolean",
        required="False"
    )

    rule = normalize_rule(raw_rule)

    assert rule.field_name == "is_active"
    assert rule.data_type == "boolean"
    assert rule.required is False
def test_normalize_float_rule():
    raw_rule = RawFieldRule(
        field_name="discount_pct",
        data_type="float",
        required=False,
        minimum=0,
        maximum=100
    )

    rule = normalize_rule(raw_rule)

    assert rule.field_name == "discount_pct"
    assert rule.data_type == "float"
    assert rule.required is False
    assert rule.minimum == 0.0
    assert rule.maximum == 100.0
def test_normalize_string_rule():
    raw_rule = RawFieldRule(
        field_name="username",
        data_type="string",
        required=True,
        minimum=3.0,
        maximum=20.0,
        description="Alphanumeric username"
    )

    rule = normalize_rule(raw_rule)

    assert rule.field_name == "username"
    assert rule.data_type == "string"
    assert rule.required is True
    assert rule.minimum == 3
    assert rule.maximum == 20
    assert rule.description == "Alphanumeric username"
def test_normalize_format_rule():
    raw_rule = RawFieldRule(
        field_name="email",
        data_type="string",
        required=True,
        format_rule=" email "
    )

    rule = normalize_rule(raw_rule)

    assert rule.field_name == "email"
    assert rule.format_rule == "email"
def test_normalize_regex_format_rule():
    regex = r"regex:^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&]).+$"

    raw_rule = RawFieldRule(
        field_name="password",
        data_type="string",
        required=True,
        minimum=8,
        maximum=64,
        format_rule=regex
    )

    rule = normalize_rule(raw_rule)

    assert rule.field_name == "password"
    assert rule.data_type == "string"
    assert rule.minimum == 8
    assert rule.maximum == 64
    assert rule.format_rule == regex
def test_unsupported_data_type():
    raw_rule = RawFieldRule(
        field_name="profile",
        data_type="object",
        required=True
    )

    try:
        normalize_rule(raw_rule)
        assert False, "Expected ValueError for unsupported data type"
    except ValueError as exc:
        assert "unsupported data type" in str(exc).lower()