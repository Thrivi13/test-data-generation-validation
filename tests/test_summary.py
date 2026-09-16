from src.summary import get_failed_fields, summarize_results


def test_summarize_results():
    results = [
        {
            "case_type": "valid",
            "valid": True,
            "matches_expectation": True,
        },
        {
            "case_type": "boundary",
            "valid": True,
            "matches_expectation": True,
        },
        {
            "case_type": "boundary",
            "valid": False,
            "matches_expectation": True,
        },
        {
            "case_type": "invalid",
            "valid": False,
            "matches_expectation": True,
        },
    ]

    summary = summarize_results(results)

    assert summary["total_cases"] == 4
    assert summary["valid_cases"] == 2
    assert summary["invalid_cases"] == 2
    assert summary["boundary_cases"] == 2
    assert summary["expectation_matches"] == 4
    assert summary["expectation_mismatches"] == 0


def test_summarize_expectation_mismatch():
    results = [
        {
            "case_type": "valid",
            "valid": False,
            "matches_expectation": False,
        },
        {
            "case_type": "invalid",
            "valid": False,
            "matches_expectation": True,
        },
    ]

    summary = summarize_results(results)

    assert summary["expectation_matches"] == 1
    assert summary["expectation_mismatches"] == 1


def test_get_failed_fields():
    results = [
        {
            "case_type": "invalid",
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
    assert failures[0]["case_type"] == "invalid"