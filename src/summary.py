from collections import Counter


def summarize_results(results: list[dict]) -> dict:
    """Create summary statistics from validation results."""

    total_cases = len(results)

    valid_cases = sum(
        1 for result in results
        if result.get("valid") is True
    )

    invalid_cases = sum(
        1 for result in results
        if result.get("valid") is False
    )

    boundary_cases = sum(
        1 for result in results
        if result.get("case_type") == "boundary"
    )

    case_types = Counter(
        result.get("case_type")
        for result in results
    )

    return {
        "total_cases": total_cases,
        "valid_cases": valid_cases,
        "invalid_cases": invalid_cases,
        "boundary_cases": boundary_cases,
        "case_type_counts": dict(case_types),
    }


def get_failed_fields(results: list[dict]) -> list[dict]:
    """Return field-level validation failures."""

    failures = []

    for result in results:
        for field_name, field_result in result.get(
            "field_results", {}
        ).items():
            if not field_result.get("valid"):
                failures.append(
                    {
                        "case_type": result.get("case_type"),
                        "field_name": field_name,
                        "value": field_result.get("value"),
                        "message": field_result.get("message"),
                    }
                )

    return failures
