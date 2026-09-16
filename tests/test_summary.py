from src.summary import summarize_results, get_failed_fields


def test_summarize_results():
    results = [
        {
            "case_type": "valid",
            "valid": True,
            "field_results": {},
        },
        {
            "case_type": "boundary",
            "valid": True,
            "field_results": {},
        },
        {
            "case_type": "invalid",
            "valid": False,
            "field_results": {},
        },
    ]

    summary = summarize_results(results)

    assert summary["total_cases"] == 3
    assert summary["valid_cases"] == 2
    assert summary["invalid_cases"] == 1
    assert summary["boundary_cases"] == 1


def test_empty_results():
    summary = summarize_results([])

    assert summary["total_cases"] == 0
    assert summary["valid_cases"] == 0
    assert summary["invalid_cases"] == 0
    assert summary["boundary_cases"] == 0


def test_get_failed_fields():
    results = [
        {
            "case_type": "invalid",
            "valid": False,
            "field_results": {
                "age": {
                    "value": 17,
                    "valid": False,
                    "message": "Value is below the minimum.",
                },
                "status": {
                    "value": "active",
                    "valid": True,
                    "message": "Value satisfies the field rules.",
                },
            },
        }
    ]

    failures = get_failed_fields(results)

    assert len(failures) == 1
    assert failures[0]["field_name"] == "age"
    assert failures[0]["value"] == 17
