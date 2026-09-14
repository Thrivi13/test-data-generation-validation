import io

from src.rule_parser import parse_rule_table
from src.models import RawFieldRule


def test_parse_valid_rule_table():
    csv_data = """field_name,type,required,min,max,allowed_values,format_rule,description
age,integer,True,18,65,,,User age
status,string,True,,,active|inactive|pending,,Account status
"""

    rules = parse_rule_table(io.StringIO(csv_data))

    assert len(rules) == 2

    assert isinstance(rules[0], RawFieldRule)

    assert rules[0].field_name == "age"
    assert rules[0].data_type == "integer"
    assert rules[0].required is True
    assert rules[0].minimum == 18
    assert rules[0].maximum == 65

    assert rules[1].field_name == "status"
    assert rules[1].allowed_values == "active|inactive|pending"
def test_missing_required_columns():
    csv_data = """field_name,type,min,max
age,integer,18,65
"""

    try:
        parse_rule_table(io.StringIO(csv_data))
        assert False, "Expected ValueError for missing required columns"
    except ValueError as exc:
        assert "required" in str(exc).lower()
def test_empty_rule_table():
    csv_data = """field_name,type,required,min,max,allowed_values,format_rule,description
"""

    try:
        parse_rule_table(io.StringIO(csv_data))
        assert False, "Expected ValueError for empty rule table"
    except ValueError as exc:
        assert "empty" in str(exc).lower()
def test_duplicate_field_names():
    csv_data = """field_name,type,required,min,max,allowed_values,format_rule,description
age,integer,True,18,65,,,User age
age,integer,True,18,65,,,Duplicate age field
"""

    try:
        parse_rule_table(io.StringIO(csv_data))
        assert False, "Expected ValueError for duplicate field names"
    except ValueError as exc:
        assert "duplicate" in str(exc).lower()
def test_empty_field_name():
    csv_data = """field_name,type,required,min,max,allowed_values,format_rule,description
,integer,True,18,65,,,Missing field name
"""

    try:
        parse_rule_table(io.StringIO(csv_data))
        assert False, "Expected ValueError for empty field name"
    except ValueError as exc:
        assert "field name" in str(exc).lower()
def test_unnamed_index_column_is_ignored():
    csv_data = """Unnamed: 0,field_name,type,required,min,max,allowed_values,format_rule,description
0,age,integer,True,18,65,,,User age
1,status,string,True,,,active|inactive|pending,,Account status
"""

    rules = parse_rule_table(io.StringIO(csv_data))

    assert len(rules) == 2
    assert rules[0].field_name == "age"
    assert rules[1].field_name == "status"
