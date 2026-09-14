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
    assert rules[0].required == "True"
    assert rules[0].minimum == 18
    assert rules[0].maximum == 65

    assert rules[1].field_name == "status"
    assert rules[1].allowed_values == "active|inactive|pending"
